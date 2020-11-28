#!/usr/bin/python3
import glob
import os
import time

import requests


def log_error(err):
    print("Unable to connect to ECA control plane. Please contact info@packetframe.com for more information. Error: " + str(err))
    exit(1)


def query(route):
    return requests.get("https://packetframe.com/api/eca/" + route, headers={"X-Auth-Key": auth_key})


def check_response(response):
    if response.status_code != 200:
        log_error("HTTP status code == " + str(response.status_code))

    if not response.json()["success"]:
        log_error("(PacketFrame) " + str(response.json()["message"]))


print("Clearing zone files")
files = glob.glob("/etc/bind/db.*")
for file in files:
    os.remove(file)

print("Checking credentials")
auth_key = ""
try:
    with open("/etc/packetframe-eca/auth") as auth_key_file:
        auth_key = auth_key_file.read().strip()
except Exception as e:
    print("Unable to read auth file: " + str(e))
else:
    print("Loaded authentication file")

print("Verifying connectivity to ECA control plane")
r = query("check")
check_response(r)
print("Connected to ECA control plane successfully")

with open("/var/packetframe-eca/info", "w") as info_file:
    info_file.write(str(r.json()["message"]))

disabled = False
local_manifest = {}
server_manifest = {}
while not disabled:
    print("Pulling manifest")
    r = query("manifest")
    check_response(r)
    server_manifest = r.json()["message"]["zones"]

    should_pull_registry = False

    for zone in server_manifest:
        server_serial = server_manifest[zone]
        local_serial = local_manifest.get(zone)

        if (not local_serial) or (server_serial > local_serial):
            print("Pulling " + zone)
            r = query("pull/" + zone)
            check_response(r)

            with open("/etc/bind/db." + zone, "w") as zone_file:
                zone_file.write(r.json()["message"]["file"])

            local_manifest[zone] = r.json()["message"]["serial"]

            should_pull_registry = True

    if should_pull_registry:
        print("Pulling zone registry")
        r = query("registry")

        with open("/etc/bind/named.conf.local", "w") as local_file:
            local_file.write(r.json()["message"])

    os.system("rndc reload")

    print("Waiting for next pull")
    time.sleep(60)
