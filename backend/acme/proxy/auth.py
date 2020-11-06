#!/usr/bin/python3

import os
import requests
import pymongo
import time

API_KEY = "ADMIN_API_KEY"
zone = os.environ["CERTBOT_DOMAIN"]
cdn_zone = ""
true_zone = ".".join(zone.split(".")[1:])

zones = pymongo.MongoClient("mongodb://localhost:27017")["cdn"]["zones"]
for _zone in zones.find():
    if _zone["zone"].endswith(true_zone) or _zone["zone"] == zone:
        cdn_zone = _zone["zone"]
        break

r = requests.post("https://dash.delivr.dev/api/zone/" + cdn_zone + "/add", headers={"X-API-Key": API_KEY}, json={
    "type": "TXT",
    "ttl": 300,
    "label": "_acme-challenge." + zone + ".",
    "value": os.environ["CERTBOT_VALIDATION"]
})

print(r.text)
print(r.json())

time.sleep(60)
