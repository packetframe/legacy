import base64
import json
import re
from functools import wraps
from os import urandom
from time import strftime

import dns.zone
import requests
from argon2 import PasswordHasher
from dns.rdatatype import RdataType
from flask import Flask, request, jsonify
from jinja2 import Template
from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError
from pystalk import BeanstalkClient

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
users = db["users"]
zones.create_index([("zone", ASCENDING)], unique=True)

argon = PasswordHasher()

queue = BeanstalkClient("localhost", 11300)

with open("templates/zone.j2") as zone_template_file:
    zone_template = Template(zone_template_file.read())


def _post_record(domain, data):
    requests.post("http://localhost/api/zone/" + domain + "/add", json=data)


# Validators

def valid_zone(zone) -> bool:
    return re.match(r"^(((?!-))(xn--|_)?[a-z0-9-]{0,61}[a-z0-9]\.)*(xn--)?([a-z0-9][a-z0-9\-]{0,60}|[a-z0-9-]{1,30}\.[a-z]{2,})$", zone) is not None


def valid_label(label) -> bool:
    return re.match(r"^(?![0-9]+$)(?!-)[a-zA-Z0-9-]{,63}(?<!-)$", label) is None


def valid_ipv4(ipv4) -> bool:
    return re.match(r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ipv4) is not None


def valid_ipv6(ipv6) -> bool:
    return re.match(r"(([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]+|::(ffff(:0{1,4})?:)?((25[0-5]|(2[0-4]|1?[0-9])?[0-9])\.){3}(25[0-5]|(2[0-4]|1?[0-9])?[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1?[0-9])?[0-9])\.){3}(25[0-5]|(2[0-4]|1?[0-9])?[0-9]))", ipv6) is not None


def valid_email(email) -> bool:
    return re.match(r"^[a-z0-9]+[._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", email) is not None


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


def zone_authentication_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")
        if not api_key:
            return jsonify({"success": False, "message": "X-API-Key must not be blank"})

        zone = kwargs.get("zone")
        if not api_key:
            return jsonify({"success": False, "message": "zone must not be blank"})

        zone_doc = zones.find_one({"zone": zone})
        if not zone_doc:
            return jsonify({"success": False, "message": "zone doesn't exist"})

        if api_key not in zone_doc["keys"]:
            return jsonify({"success": False, "message": "access denied"})

        return f(*args, **kwargs)

    return decorated_function


def authentication_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")
        if not api_key:
            return jsonify({"success": False, "message": "X-API-Key must not be blank"})

        user_doc = users.find_one({"key": api_key})
        if not user_doc:
            return jsonify({"success": False, "message": "Not authenticated"})

        return f(*args, **kwargs, username=user_doc["username"])

    return decorated_function


# Routes

@app.route("/auth/signup", methods=["POST"])
def auth_signup():
    try:
        username, password = get_args("username", "password")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)})

    if not valid_email(username) or len(username) > 100:
        return jsonify({"success": False, "message": "Invalid username"})

    if len(password) > 200:
        return jsonify({"success": False, "message": "Password must not be longer than 200 characters"})

    user_doc = users.find_one({"username": username})
    if user_doc:
        return jsonify({"success": False, "message": "User already exists"})

    users.insert_one({
        "username": username,
        "password": argon.hash(password),
        "key": base64.b64encode(urandom(32)).decode().replace("=", "")
    })

    return jsonify({"success": True, "message": "Signup success"})


@app.route("/auth/login", methods=["POST"])
def auth_login():
    try:
        username, password = get_args("username", "password")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)})

    user_doc = users.find_one({"username": username})
    if not user_doc:
        return jsonify({"success": False, "message": "Invalid username or password"})

    if argon.verify(user_doc["password"], password):
        return jsonify({"success": True, "message": user_doc["key"]})
    else:
        return jsonify({"success": False, "message": "Invalid username or password"})


@app.route("/zones/add", methods=["POST"])
@authentication_required
def zones_add(username):
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
            "serial": get_current_serial(),
            "users": [username]
        })
    except DuplicateKeyError:
        return jsonify({"success": False, "message": "Zone already exists"})
    else:
        add_queue_message("refresh_zones", args=None)
        add_queue_message("refresh_single_zone", {"zone": zone})

        return jsonify({"success": True, "message": "Added " + zone})


@app.route("/zones/list", methods=["GET"])
@authentication_required
def zones_list(username):
    # Find all zones that have username in their users list
    _zones = list(zones.find({
        "users": {
            "$in": [username]
        }
    }))

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

    elif rec_type == "CNAME":
        try:
            value = get_args("value")
        except ValueError as e:
            return jsonify({"success": False, "message": str(e)})

        if not valid_label(value):
            return jsonify({"success": False, "message": "Invalid CNAME value"})

    elif rec_type == "TXT":
        try:
            value = get_args("value")
        except ValueError as e:
            return jsonify({"success": False, "message": str(e)})

        # TODO: Check for TXT validity
        # if not valid_label(value):
        #     return jsonify({"success": False, "message": "Invalid MX server"})

    elif rec_type == "MX":
        try:
            value, priority = get_args("value", "priority")
        except ValueError as e:
            return jsonify({"success": False, "message": str(e)})

        if not valid_label(value):
            return jsonify({"success": False, "message": "Invalid MX server label"})

        try:
            # TODO: What is in bound here?
            if int(priority) < 1:
                raise TypeError
        except TypeError:
            return jsonify({"success": False, "message": "MX priority must be an integer"})

        value = str(priority) + " " + value

    elif rec_type == "SRV":
        try:
            value, priority, weight, port = get_args("value", "priority", "weight", "port")
        except ValueError as e:
            return jsonify({"success": False, "message": str(e)})

        if not valid_label(value):
            return jsonify({"success": False, "message": "Invalid SRV target"})

        try:
            # TODO: What is in bound here?
            if int(priority) < 0 or int(weight) < 0 or int(port) < 0:
                raise TypeError
        except TypeError:
            return jsonify({"success": False, "message": "SRV priority, weight, and port must be a positive integer"})

        value = str(priority) + " " + str(weight) + " " + str(port) + " " + value

    elif rec_type == "CNAME":
        try:
            value = get_args("value")
        except ValueError as e:
            return jsonify({"success": False, "message": str(e)})

        if not valid_label(value):
            return jsonify({"success": False, "message": "Invalid CNAME value"})

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

    zone_doc = zones.find_one({"zone": zone})
    if zone_doc:
        return jsonify({"success": True, "message": zone_doc.get("records")})
    else:
        return jsonify({"success": False, "message": "zone " + zone + " doesn't exit"}), 400


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


@app.route("/zones/<zone>/export", methods=["GET"])
def zones_export(zone):
    if not valid_zone(zone):
        return jsonify({"success": False, "message": "Invalid zone"})

    zone = zones.find_one({"zone": zone})
    current_time = strftime("%b %d %Y %H:%M")

    if not zone:
        return jsonify({"success": False, "message": "Zone doesn't exist"})

    zone_file = zone_template.render(
        nameservers=configuration["nameservers"],
        soa_root=configuration["soa_root"],
        records=zone["records"],
        serial=zone["serial"]
    )

    return jsonify({"success": True, "message": "; " + zone["zone"] + " exported from delivr.dev at " + current_time + "\n\n" + zone_file})


@app.route("/zones/<zone>/import", methods=["POST"])
def zone_import(domain):
    if not valid_zone(domain):
        return jsonify({"success": False, "message": "Invalid zone"})

    try:
        file = get_args("file")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)})

    zone = dns.zone.from_text(file, domain)

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
                if rdataset.rdtype == RdataType.AAAA:
                    _post_record(domain, {
                        "label": name,
                        "ttl": 3600,
                        "type": "AAAA",
                        "value": str(rdata.address)
                    })
                if rdataset.rdtype == RdataType.MX:
                    _post_record(domain, {
                        "label": name,
                        "ttl": 3600,
                        "type": "MX",
                        "value": f"{rdata.preference} {rdata.exchange}"
                    })
                if rdataset.rdtype == RdataType.CNAME:
                    _post_record(domain, {
                        "label": name,
                        "ttl": 3600,
                        "type": "CNAME",
                        "value": str(rdata.target)
                    })
                if rdataset.rdtype == RdataType.SRV:
                    _post_record(domain, {
                        "label": name,
                        "ttl": 3600,
                        "type": "SRV",
                        "value": f"{rdata.priority} {rdata.weight} {rdata.port} {rdata.target}"
                    })
                if rdataset.rdtype == RdataType.TXT:
                    _post_record(domain, {
                        "label": name,
                        "ttl": 3600,
                        "type": "TXT",
                        "value": str(rdata).replace("\" \"", "").replace("\"", "")
                    })

    return "Done"


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
