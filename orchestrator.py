import json
import os
import sys

import pika
from jinja2 import Template
from pymongo import MongoClient

from config import configuration

db_client = MongoClient("mongodb://localhost:27017")
db = db_client["cdn"]

with open("templates/local.j2", "r") as local_template_file:
    # noinspection JinjaAutoinspect
    local_template = Template(local_template_file.read())

with open("templates/zone.j2") as zone_template_file:
    # noinspection JinjaAutoinspect
    zone_template = Template(zone_template_file.read())


def callback(ch, method, properties, body):
    content = json.loads(body)

    operation = content["operation"]
    args = content["args"]

    if operation == "refresh_single_zone":
        print("refreshing " + args["zone"])

        zone = db["zones"].find_one({"zone": args["zone"]})

        print(zone_template.render(
            nameservers=configuration["nameservers"],
            soa_root=configuration["soa_root"],
            records=zone["records"],
            serial=zone["serial"]
        ))

        # Pull data out of the database and assemble the zone file into an object
        # POST the object to each node
    elif operation == "refresh_zones":
        print("refreshing local zones file")

        zones_file = ""

        # Assemble named.local.conf based on zones
        for zone in db["zones"].find():
            zones_file += local_template.render(zone=zone["zone"])

        for node in db["nodes"].find():
            print("Sending updated zone file to " + node["name"])
            # TODO: Convert this to an SSH call
            print(zones_file)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="cdn_updates")
    channel.basic_consume(queue="cdn_updates", on_message_callback=callback, auto_ack=True)  # TODO: what is auto ack?

    print("Waiting for messages.")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
