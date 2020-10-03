import json
import time

from jinja2 import Template
from paramiko import SSHClient, AutoAddPolicy
from pymongo import MongoClient
from pystalk import BeanstalkClient
from scp import SCPClient

from config import configuration

db_client = MongoClient("mongodb://localhost:27017")
db = db_client["cdn"]

queue = BeanstalkClient("localhost", 11300)

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(AutoAddPolicy())

with open("templates/local.j2", "r") as local_template_file:
    local_template = Template(local_template_file.read())

with open("templates/zone.j2") as zone_template_file:
    zone_template = Template(zone_template_file.read())


def reload_dns():
    print("    - reloading DNS config", end="", flush=True)
    stdin, stdout, stderr = ssh.exec_command("rndc reload")
    for line in stdout:
        print(" - " + line.strip('\n'))
    for line in stderr:
        print(" - ERR " + line.strip('\n'))


print("Starting main loop")

while True:
    for job in queue.reserve_iter():
        content = json.loads(job.job_data)

        operation = content["operation"]
        args = content["args"]

        if operation == "refresh_single_zone":
            print("refreshing " + args["zone"])

            zone = db["zones"].find_one({"zone": args["zone"]})

            zone_file = zone_template.render(
                nameservers=configuration["nameservers"],
                soa_root=configuration["soa_root"],
                records=zone["records"],
                serial=zone["serial"]
            )

            with open("/tmp/db." + zone["zone"], "w") as zone_file_writer:
                zone_file_writer.write(zone_file)

            # Loop over the nodes and send the updated zone file to each one, then reload the configuration
            for node in db["nodes"].find():
                print("... now updating " + node["name"] + " " + node["management_ip"] + " " + node["location"])

                print("    - sending updated zone file")
                ssh.connect(node["management_ip"], username="root", port=34553, key_filename="./ssh-key2")
                with SCPClient(ssh.get_transport()) as scp:
                    scp.put("/tmp/db." + zone["zone"], "/etc/bind/db." + zone["zone"])

                reload_dns()
                ssh.close()
            print("finished sending updates")

        elif operation == "refresh_zones":
            print("refreshing local zones file")

            zones_file = ""

            # Assemble named.local.conf based on zones
            for zone in db["zones"].find():
                zones_file += local_template.render(zone=zone["zone"])

            # Write the named.conf.local tmp file
            with open("/tmp/named.conf.local", "w") as named_file:
                named_file.write(zones_file)

            # Loop over the nodes and send the updated zone file to each one, then reload the configuration
            for node in db["nodes"].find():
                print("... now updating " + node["name"] + " " + node["management_ip"] + " " + node["location"])

                print("    - sending updated zone file")
                ssh.connect(node["management_ip"], username="root", port=34553, key_filename="./ssh-key2")
                with SCPClient(ssh.get_transport()) as scp:
                    scp.put("/tmp/named.conf.local", "/etc/bind/named.conf.local")

                reload_dns()
                ssh.close()
            print("finished sending updates")

        queue.delete_job(job.job_id)

    time.sleep(0.5)
