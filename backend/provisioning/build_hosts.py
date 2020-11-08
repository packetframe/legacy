from pymongo import MongoClient
import yaml
import os

db_client = MongoClient("mongodb://localhost:27017")

with open("/home/nate/delivr/config.yml", "r") as config_file:
    config = yaml.safe_load(config_file.read())

_config = {
    "nodes": {
        "hosts": {},
        "vars": {
            "ansible_user": "root",
            "ansible_port": 34553,
            "ansible_ssh_private_key_file": config["ssh-key"]
        }
    },
    "cache": {
        "hosts": {},
        "vars": {
            "ansible_user": "root",
            "ansible_port": 34553,
            "ansible_ssh_private_key_file": config["ssh-key"]
        }
    }
}

prometheus_config = """global:
  scrape_interval:     60s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 60s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

  # Attach these labels to any time series or alerts when communicating with
  # external systems (federation, remote storage, Alertmanager).
  external_labels:
      monitor: 'example'

# Alertmanager configuration
alerting:
  alertmanagers:
  - static_configs:
    - targets: ['localhost:9093']

scrape_configs:
  - job_name: dns_nodes
    static_configs:"""

for node in db_client["cdn"]["nodes"].find():
    _config["nodes"]["hosts"][node["name"]] = {
        "ansible_host": node["management_ip"]
    }

    prometheus_config += """
      - targets: ['""" + node["management_ip"] + """:9119']
        labels:
          service: '""" + node["name"] + """'"""

    print("+ " + node["name"])


prometheus_config += """

  - job_name: cache_nodes_caddy
    static_configs:"""

for node in db_client["cdn"]["cache_nodes"].find():
    _config["cache"]["hosts"]["cache-" + node["name"]] = {
        "ansible_host": node["management_ip"]
    }

    prometheus_config += """
      - targets: ['""" + node["management_ip"] + """:2019']
        labels:
          service: '""" + node["name"] + """'"""

    print("- cache + " + node["name"])

prometheus_config += """

  - job_name: cache_nodes_varnish
    static_configs:"""

for node in db_client["cdn"]["cache_nodes"].find():
    prometheus_config += """
      - targets: ['""" + node["management_ip"] + """:9131']
        labels:
          service: '""" + node["name"] + """'"""

with open("hosts.yml", "w") as hosts_file:
    hosts_file.write(yaml.dump(_config, default_flow_style=False))

with open("/home/nate/delivr/intra/prometheus.yml", "w") as prometheus_file:
    prometheus_file.write(prometheus_config + "\n")

print("Deploying monitoring config...")
os.system("ssh " + config["monitoring_host"] + " -i /home/nate/ssh-key \"pct exe 101 ./update-prometheus.sh\"")
