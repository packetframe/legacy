from pymongo import MongoClient
import yaml

db_client = MongoClient("mongodb://localhost:27017")

with open("../config.yml", "r") as config_file:
    config = yaml.safe_load(config_file.read())

_config = {
    "all": {
        "hosts": {},
        "vars": {
            "ansible_user": config["nodes"]["username"],
            "ansible_port": config["nodes"]["port"],
            "ansible_ssh_private_key_file": config["nodes"]["key"]
        }
    }
}

for node in db_client["cdn"]["nodes"].find():
    _config["all"]["hosts"][node["name"]] = {
        "ansible_host": node["management_ip"]
    }

    print("+ " + node["name"])

with open("hosts.yml", "w") as hosts_file:
    hosts_file.write(yaml.dump(_config, default_flow_style=False))
