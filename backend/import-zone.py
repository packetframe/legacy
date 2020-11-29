#!/usr/bin/python3
import requests
from dns.rdatatype import RdataType
import dns.zone
import sys

domain = sys.argv[1]
dryrun = 0

apikey = "ADMIN_API_KEY"


def _post_record(domain, data):
    data["proxied"] = False
    if dryrun:
        print(data)
    else:
        r = requests.post("https://packetframe.com/api/zone/" + domain + "/add", json=data, headers={"X-API-Key": apikey})
        if not r.json()["success"]:
            print(data, r.json())


zone = dns.zone.from_file(domain)

for name, node in zone.items():
    if str(name) == "@":
        name = domain + "."
    else:
        name = str(name) + "." + domain + "."

    for rdataset in node.rdatasets:
        for rdata in rdataset:
            if rdataset.rdtype == RdataType.A:
                _post_record(domain, {
                    "label": name,
                    "ttl": 3600,
                    "type": "A",
                    "value": str(rdata.address)
                })
            elif rdataset.rdtype == RdataType.AAAA:
                _post_record(domain, {
                    "label": name,
                    "ttl": 3600,
                    "type": "AAAA",
                    "value": str(rdata.address)
                })
            elif rdataset.rdtype == RdataType.MX:
                _post_record(domain, {
                    "label": name,
                    "ttl": 3600,
                    "type": "MX",
                    "value": str(rdata.exchange),
                    "priority": int(rdata.preference)
                })
            elif rdataset.rdtype == RdataType.CNAME:
                _post_record(domain, {
                    "label": name,
                    "ttl": 3600,
                    "type": "CNAME",
                    "value": str(rdata.target)
                })
            elif rdataset.rdtype == RdataType.SRV:
                _post_record(domain, {
                    "label": name,
                    "ttl": 3600,
                    "type": "SRV",
                    "priority": str(rdata.priority),
                    "weight": str(rdata.weight),
                    "port": str(rdata.port),
                    "value": str(rdata.target)
                })
            elif rdataset.rdtype == RdataType.TXT:
                _post_record(domain, {
                    "label": name,
                    "ttl": 3600,
                    "type": "TXT",
                    "value": str(rdata)
                })
            else:
                print("Skipped", rdataset.rdtype)
