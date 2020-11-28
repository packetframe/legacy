import os

import yaml

CONFIG_FILE = "/home/nate/backend/config.yml"

if not os.path.exists(CONFIG_FILE):
    print("No config.yml file found.")
    exit(1)

with open(CONFIG_FILE, "r") as config_file:
    configuration = yaml.safe_load(config_file.read())
