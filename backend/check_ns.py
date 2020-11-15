#!/usr/bin/python3
import sys

from jinja2 import Template
from pymongo import MongoClient
import dns.resolver
import time
from config import configuration
from api import add_queue_message

try:
    send_emails = (sys.argv[1] == "send-emails")
except IndexError:
    send_emails = False

print("Send emails:", send_emails)

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


for zone in db["zones"].find():
    error_message = None
    print(f"Checking {zone['zone']}...", end="", flush=True)
    err, answers = ns_query(zone["zone"])
    if not err:
        nameservers = [str(ns) for ns in answers.rrset]

        if valid_nameservers(nameservers):
            print("\033[92mOK\033[0m")
        else:
            error_message = ("Incorrect nameservers: " + ", ".join(nameservers))
    else:
        error_message = str(err)

    if error_message:
        print("\033[91m" + error_message + "\033[0m")

        if send_emails:
            template = nameserver_issue_template.render(
                nameservers=configuration["dns"]["nameservers"],
                domain=zone["zone"],
                error=error_message
            )

            print("Sending email to", zone["users"])
            add_queue_message("send_email", args={"recipients": zone["users"], "subject": "[delivr.dev] Attention Needed: nameserver update", "body": template})

    time.sleep(0.1)
