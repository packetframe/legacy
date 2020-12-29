#!/usr/bin/python3
"""Usage:
    pfctl account [login|logout]
    pfctl records <zone> [add]
    pfctl records <zone> delete <index>
    pfctl zones list
"""

from os import makedirs
from os.path import exists
from pathlib import Path
from shutil import rmtree

import requests
from PyInquirer import style_from_dict, prompt, Token
from docopt import docopt
from rich import box
from rich.console import Console
from rich.table import Table
from rich.traceback import install

# Register rich traceback hook
install()

args = docopt(__doc__)

console = Console()

PARENT_ENDPOINT = "https://packetframe.com/api/"
config_path = str(Path.home()) + "/.config/packetframe/"

PYINQUIRER_STYLE = style_from_dict({
    Token.Separator: "#6C6C6C",
    Token.QuestionMark: "#FFF",
    Token.Selected: "#dd00ff",
    Token.Pointer: "#FFF",
    Token.Instruction: "",
    Token.Answer: "#dd00ff",
    Token.Question: "",
})

# Set API key if not trying to lotg in
if args and not args["login"]:
    try:
        with open(config_path + "key", "r") as api_key_file:
            API_KEY = api_key_file.read()
    except FileNotFoundError:
        console.print(":x: Account not found: run [dim]pfctl login[/] to log into your account")
        exit(1)
else:
    API_KEY = ""


# Request helper


def _request(message, route, method, body=None):
    with console.status(f"[bold green]{message}..."):
        r = requests.request(method, PARENT_ENDPOINT + route, json=body, headers={"X-API-Key": API_KEY})
        if r.status_code != 200:
            console.log(
                f"[bold red]ERROR (request)[reset] code {r.status_code} body {r.text}")
            exit(1)
        elif not r.json()["success"]:
            console.log(f"[bold red]ERROR (api)[reset] {r.json()['message']}")
            exit(1)
        return r.json()["message"]


def list_zones():
    table = Table(
        title="Zones List",
        show_header=True,
        show_edge=False,
        expand=False,
        row_styles=["none", "dim"],
        box=box.SIMPLE
    )

    table.add_column("Zone", style="cyan")
    table.add_column("Records", style="magenta")
    table.add_column("Users", style="green")

    for zone in _request("Getting zones", "zones/list", "GET"):
        table.add_row(zone["zone"], str(
            len(zone["records"])), str(len(zone["users"])))

    console.print(table)


def list_records(zone: str):
    table = Table(
        title=f"Records for {zone}",
        show_header=True,
        show_edge=False,
        expand=False,
        row_styles=["none", "dim"],
        box=box.SIMPLE
    )

    table.add_column("Label", style="cyan")
    table.add_column("Index", style="magenta")
    table.add_column("TTL", style="magenta")
    table.add_column("Type", style="magenta")
    table.add_column("Value", style="green")

    for index, record in enumerate(_request(f"Getting records for {zone}", f"zone/{zone}/records", "GET")):
        table.add_row(record["label"], str(index), record["type"], str(record["ttl"]), record["value"])

    console.print(table)


def add_record(zone):
    console.print(f"[underline]Add a new record to {zone}")
    record = prompt([
        {
            "type": "input",
            "name": "label",
            "message": "Label",
        },
        {
            "type": "list",
            "name": "type",
            "message": "Type",
            "choices": ["A", "AAAA", "TXT", "MX", "CNAME", "PTR"]
        },
        {
            "type": "input",
            "name": "ttl",
            "message": "TTL",
            "default": "86400"
        },
        {
            "type": "input",
            "name": "value",
            "message": "Value",
        },
        {
            "type": "confirm",
            "name": "proxied",
            "message": "Proxied"
        }
    ], style=PYINQUIRER_STYLE)

    if record:
        # Add domain suffix
        if not record["label"].endswith(zone):
            record["label"] += "." + zone + "."

        # Cast TTL to an int
        record["ttl"] = int(record["ttl"])

        r = _request(f"Adding record {record['label']}", f"zone/{zone}/add", "POST", record)
        print(r)

    else:
        console.print("Exited")


def delete_record(zone, index):
    print(_request("Deleting record", f"zone/{zone}/delete_record/{index}", "POST"))


def login():
    console.print("[underline]PacketFrame Login")
    account = prompt([
        {
            "type": "input",
            "name": "username",
            "message": "Email:",
        },
        {
            "type": "password",
            "message": "Password:",
            "name": "password"
        }
    ], style=PYINQUIRER_STYLE)

    if account:
        r = _request(f"Logging in as {account['username']}", "auth/login", "POST", account)
        console.print("[bold green]Login successful")
        if not exists(config_path):
            makedirs(config_path)
        with open(config_path + "key", "w") as api_key_file:
            api_key_file.write(r)
        with open(config_path + "email", "w") as email_file:
            email_file.write(account["username"])


def account():
    with open(config_path + "email", "r") as email_file:
        console.print(f":lock: Logged in as [underline]{email_file.read()}")


def logout():
    rmtree(config_path)
    console.print("Logout complete")


# Main
if args["login"]:
    login()
elif args["logout"]:
    logout()
elif args["account"] and not args["login"]:
    account()
elif args["zones"] and args["list"]:
    list_zones()
elif args["records"] and not args["add"] and not args["delete"]:
    list_records(args["<zone>"])
elif args["records"] and args["add"]:
    add_record(args["<zone>"])
elif args["records"] and args["delete"]:
    delete_record(args["<zone>"], args["<index>"])
