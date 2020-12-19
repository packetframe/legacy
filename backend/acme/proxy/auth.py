#!/usr/bin/python3

import os
import requests
import time

API_KEY = "ADMIN_API_KEY"

zone = ""
cdn_zone = ""

r = requests.post("https://packetframe.com/api/zone/" + cdn_zone + "/add", headers={"X-API-Key": API_KEY}, json={
    "type": "TXT",
    "ttl": 300,
    "label": "_acme-challenge." + zone + ".",
    "value": os.environ["CERTBOT_VALIDATION"]
})

print(r.text)
print(r.json())

time.sleep(60)
