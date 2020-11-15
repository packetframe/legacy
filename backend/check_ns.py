#!/usr/bin/python3
import sys

from jinja2 import Template
from pymongo import MongoClient
import dns.resolver
import time
from config import configuration

correct_nameservers = [(ns + ".") for ns in configuration["dns"]["nameservers"]]

with open("templates/nameserver_issue.j2", "r") as nameserver_issue_template_file:
    # noinspection JinjaAutoinspect
    nameserver_issue_template = Template(nameserver_issue_template_file.read())


def valid_nameservers(arr1):
    if len(arr1) != len(correct_nameservers):
        return False

    arr1.sort()
    correct_nameservers.sort()

    for i in range(0, len(arr1) - 1):
        if arr1[i] != correct_nameservers[i]:
            return False

    return True


db = MongoClient("mongodb://localhost:27017")["cdn"]


def ns_query(label):
    try:
        return None, dns.resolver.resolve(label, "NS")
    except Exception as e:
        return str(e), None


bad_zones = {}
for zone in db["zones"].find():
    print(f"Checking {zone['zone']}...", end="", flush=True)
    err, answers = ns_query(zone["zone"])
    if not err:
        nameservers = [str(ns) for ns in answers.rrset]

        if valid_nameservers(nameservers):
            print("\033[92mOK\033[0m")
        else:
            bad_zones[zone["zone"]] = ("Incorrect nameservers: " + ", ".join(nameservers))
            print("\033[91m Incorrect nameservers: " + ", ".join(nameservers) + "\033[0m")
    else:
        bad_zones[zone["zone"]] = str(err)
        print("\033[91m" + str(err) + "\033[0m")

    time.sleep(0.1)

try:
    arg1 = sys.argv[1]
except IndexError:
    pass
else:
    if arg1 == "send-emails":
        for zone in bad_zones:
            print(nameserver_issue_template.render(nameservers=configuration["dns"]["nameservers"], domain=zone, error=bad_zones[zone]))
