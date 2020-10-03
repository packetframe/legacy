import json
import re
from os import urandom
from time import strftime

from pystalk import BeanstalkClient
from flask import Flask, request, jsonify
from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError

from config import configuration

app = Flask(__name__)
if configuration["development"]:
    app.secret_key = b'0'
else:
    app.secret_key = urandom(12)

client = MongoClient("mongodb://localhost:27017")
db = client["cdn"]

# Collections
zones = db["zones"]
nodes = db["nodes"]
zones.create_index([("zone", ASCENDING)], unique=True)

queue = BeanstalkClient("localhost", 11300)


# Validators

def valid_zone(zone) -> bool:
    return re.match(r"^(((?!-))(xn--|_)?[a-z0-9-]{0,61}[a-z0-9]\.)*(xn--)?([a-z0-9][a-z0-9\-]{0,60}|[a-z0-9-]{1,30}\.[a-z]{2,})$", zone) is not None


def valid_label(label) -> bool:
    return re.match(r"^(?![0-9]+$)(?!-)[a-zA-Z0-9-]{,63}(?<!-)$", label) is None


def valid_ipv4(ipv4) -> bool:
    return re.match(r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ipv4) is not None


def valid_ipv6(ipv6) -> bool:
    return re.match(r"(([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]+|::(ffff(:0{1,4})?:)?((25[0-5]|(2[0-4]|1?[0-9])?[0-9])\.){3}(25[0-5]|(2[0-4]|1?[0-9])?[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1?[0-9])?[0-9])\.){3}(25[0-5]|(2[0-4]|1?[0-9])?[0-9]))", ipv6) is not None


# Helpers

def get_current_serial():
    return strftime("%Y%m%d%S")


def add_queue_message(operation, args):
    queue.put_job(json.dumps({"operation": operation, "args": args}))


def get_args(*args):
    if request.json is None:
        raise ValueError("request body isn't valid JSON")

    payload = []

    for arg in args:
        try:
            arg_val = request.json[arg]
        except KeyError:
            raise ValueError("required argument \"" + str(arg) + "\" not supplied.")
        else:
            payload.append(arg_val)

    if len(payload) == 1:
        return payload[0]
    else:
        return tuple(payload)


@app.route("/zone/add", methods=["POST"])
def zones_add():
    try:
        zone = get_args("zone")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)})

    if not valid_zone(zone):
        return jsonify({"success": False, "message": "Invalid zone"})

    try:
        zones.insert_one({
            "zone": zone,
            "records": [],
            "serial": get_current_serial()
        })
    except DuplicateKeyError:
        return jsonify({"success": False, "message": "Zone already exists"})
    else:
        add_queue_message("refresh_zones", args=None)
        add_queue_message("refresh_single_zone", {"zone": zone})

        return jsonify({"success": True, "message": "Added " + zone})


@app.route("/zones/list", methods=["GET"])
def zones_list():
    _zones = list(zones.find())

    for zone in _zones:
        del zone["_id"]

    return jsonify({"success": True, "message": _zones})


@app.route("/zone/<zone>/delete", methods=["POST"])
def zones_delete(zone):
    if not valid_zone(zone):
        return jsonify({"success": False, "message": "Invalid zone"})

    delete_op = zones.delete_one({"zone": zone})

    if delete_op.deleted_count > 0:
        add_queue_message("delete_zone", args={"zone": zone})
        add_queue_message("refresh_zones", args=None)
        return jsonify({"success": True, "message": "Deleted " + zone})
    else:
        return jsonify({"success": True, "message": "Zone " + zone + " doesn't exist"})


# Record management

@app.route("/zone/<zone>/add", methods=["POST"])
def records_add(zone):
    if not valid_zone(zone):
        return jsonify({"success": False, "message": "Invalid zone"})

    try:
        label, rec_type, ttl = get_args("label", "type", "ttl")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)})

    if type(ttl) != int or ttl < 1 or ttl > 2147483647:
        return jsonify({"success": False, "message": "Invalid TTL !(0 > ttl > 2147483647)"})

    if not valid_label(label):
        return jsonify({"success": False, "message": "Invalid label"})

    if rec_type == "A":
        try:
            value = get_args("value")
        except ValueError as e:
            return jsonify({"success": False, "message": str(e)})

        if not valid_ipv4(value):
            return jsonify({"success": False, "message": "Invalid IPv4 address"})

    elif rec_type == "AAAA":
        try:
            value = get_args("value")
        except ValueError as e:
            return jsonify({"success": False, "message": str(e)})

        if not valid_ipv6(value):
            return jsonify({"success": False, "message": "Invalid IPv6 address"})

    elif rec_type == "MX":
        try:
            value = get_args("value")
        except ValueError as e:
            return jsonify({"success": False, "message": str(e)})

        if not valid_label(value):
            return jsonify({"success": False, "message": "Invalid MX server"})

    elif rec_type == "CNAME":
        try:
            value = get_args("value")
        except ValueError as e:
            return jsonify({"success": False, "message": str(e)})

        if not valid_label(value):
            return jsonify({"success": False, "message": "Invalid CNAME label"})

    elif rec_type == "TXT":
        try:
            value = get_args("value")
        except ValueError as e:
            return jsonify({"success": False, "message": str(e)})

        # TODO: Check for TXT validity
        # if not valid_label(value):
        #     return jsonify({"success": False, "message": "Invalid MX server"})

    else:
        return jsonify({"success": False, "message": "Invalid record type (Allowed values are A/AAAA"})

    zones.update_one({"zone": zone}, {
        "$push": {
            "records": {
                "label": label,
                "ttl": int(ttl),
                "type": rec_type,
                "value": value
            }
        },
        "$set": {
            "serial": get_current_serial()
        }
    })

    add_queue_message("refresh_single_zone", {"zone": zone})

    return jsonify({"success": True, "message": "Record added to " + zone})


@app.route("/zone/<zone>/records", methods=["GET"])
def records_list(zone):
    if not valid_zone(zone):
        return jsonify({"success": False, "message": "Invalid zone"})

    current_records = zones.find_one({"zone": zone}).get("records")

    return jsonify({"success": True, "message": current_records})


@app.route("/zone/<zone>/delete_record/<index>", methods=["POST"])
def record_delete(zone, index):
    if not valid_zone(zone):
        return jsonify({"success": False, "message": "Invalid zone"})

    try:
        index = int(index)
    except ValueError:
        return jsonify({"success": False, "message": "Index must be a positive, nonzero integer"})

    if index < 0:
        return jsonify({"success": False, "message": "Index must be a positive, nonzero integer"})

    current_records = zones.find_one({"zone": zone}).get("records")

    # Remove the record
    try:
        current_records.pop(int(index))
    except IndexError:
        return jsonify({"success": True, "message": "Record at index " + str(index) + " doesn't exist in " + zone})

    # Set the modified records
    zones.update_one({"zone": zone}, {"$set": {
        "records": current_records,
        "serial": get_current_serial()
    }})

    add_queue_message("refresh_single_zone", {"zone": zone})

    return jsonify({"success": True, "message": "Record deleted at index " + str(index) + " from " + zone})


# Node

@app.route("/nodes/add", methods=["POST"])
def nodes_add():
    try:
        name, provider, geoloc, location, management_ip = get_args("name", "provider", "geoloc", "location", "management_ip")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)})

    add_op = nodes.insert_one({
        "name": name,
        "provider": provider,
        "geoloc": geoloc,
        "location": location,
        "management_ip": management_ip,
    })

    if add_op.acknowledged:
        return jsonify({"success": True, "message": "Added " + name})
    else:
        return jsonify({"success": False, "message": "Unable to add node" + name})


@app.route("/nodes/list", methods=["GET"])
def nodes_list():
    _nodes = list(nodes.find())

    for node in _nodes:
        del node["_id"]

    return jsonify({"success": True, "message": _nodes})


# Debug

if configuration["development"]:
    @app.route("/debug/refresh_zones")
    def refresh_zones():
        add_queue_message("refresh_zones", args=None)
        return "Done"


    @app.route("/debug/refresh_single_zone/<zone>")
    def refresh_single_zone(zone):
        add_queue_message("refresh_single_zone", {"zone": zone})
        return "Done"


    @app.route("/debug/refresh_all_zones")
    def refresh_all_zones():
        for zone in zones.find():
            add_queue_message("refresh_single_zone", {"zone": zone["zone"]})

        add_queue_message("refresh_zones", args=None)
        return "Done"

app.run(debug=configuration["development"])
