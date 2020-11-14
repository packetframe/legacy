#!/usr/bin/python3

from pymongo import MongoClient
import dns.resolver
import time

correct_nameservers = ["ns1.delivr.dev.", "ns2.delivr.dev."]


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


for zone in db["zones"].find():
    print(f"Checking {zone['zone']}...", end="", flush=True)
    err, answers = ns_query(zone["zone"])
    if not err:
        nameservers = [str(ns) for ns in answers.rrset]

        if valid_nameservers(nameservers):
            print("\033[92mOK\033[0m")
        else:
            print("\033[91m" + ", ".join(nameservers) + "\033[0m")
    else:
        print("\033[91m" + str(err) + "\033[0m")

    time.sleep(0.1)
