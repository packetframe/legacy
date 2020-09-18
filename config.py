import os

import yaml

if not os.path.exists("config.yml"):
    print("No config.yml file found.")
    exit(1)

with open("config.yml", "r") as config_file:
    configuration = yaml.safe_load(config_file.read())
