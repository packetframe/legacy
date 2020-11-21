import base64
import ipaddress
import json
import re
from functools import wraps
from os import urandom
from time import strftime

import utils
# noinspection PyPackageRequirements
from argon2 import PasswordHasher
# noinspection PyPackageRequirements
from argon2.exceptions import VerifyMismatchError
from config import configuration
from flask import Flask, request, jsonify, make_response
from jinja2 import Template
from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError
from pystalk import BeanstalkClient

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
ecas = db["ecas"]
zones.create_index([("zone", ASCENDING)], unique=True)

argon = PasswordHasher()

queue = BeanstalkClient("localhost", 11300)

with open("templates/zone.j2") as zone_template_file:
    # noinspection JinjaAutoinspect
    zone_template = Template(zone_template_file.read())

with open("templates/new_domain.j2", "r") as new_domain_template_file:
    # noinspection JinjaAutoinspect
    new_domain_template = Template(new_domain_template_file.read())

with open("templates/proxied_record.j2", "r") as proxied_record_template_file:
    # noinspection JinjaAutoinspect
    proxied_record_template = Template(proxied_record_template_file.read())

with open("templates/welcome.j2", "r") as welcome_template_file:
    # noinspection JinjaAutoinspect
    welcome_template = Template(welcome_template_file.read())

with open("templates/collector_bird.j2", "r") as collector_bird_template_file:
    # noinspection JinjaAutoinspect
    collector_bird_template = Template(collector_bird_template_file.read())


# Regex Validators

def valid_zone(zone) -> bool:
    # Validates a DNS zone (example.com)
    return zone and (re.match(r"^(((?!-))(xn--|_)?[a-z0-9-]{0,61}[a-z0-9]\.)*(xn--)?([a-z0-9][a-z0-9\-]{0,60}|[a-z0-9-]{1,30}\.[a-z]{2,})$", zone) is not None) and (zone != ".") and (" " not in zone)


def valid_label(label) -> bool:
    # Validates a DNS zone label (www, @, example.com.)
    return label and (re.match(r"^(?![0-9]+$)(?!-)[a-zA-Z0-9-]{,63}(?<!-)$", label) is None) and (not label.startswith(".")) and (not label.strip().startswith(" ")) and (" " not in label)


def valid_ipv4(ipv4) -> bool:
    # Validates an IPv4 address (192.0.2.1)
    return ipv4 and (re.match(r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ipv4) is not None)


def valid_ipv6(ipv6) -> bool:
    # Validates an IPv4 address (2001:db8::1)
    return ipv6 and (re.match(r"(([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]+|::(ffff(:0{1,4})?:)?((25[0-5]|(2[0-4]|1?[0-9])?[0-9])\.){3}(25[0-5]|(2[0-4]|1?[0-9])?[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1?[0-9])?[0-9])\.){3}(25[0-5]|(2[0-4]|1?[0-9])?[0-9]))", ipv6) is not None)


def valid_email(email) -> bool:
    # Validates an email address (example@example.com)
    return email and (re.match(r"^[a-z0-9]+[._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", email) is not None)


# Helpers

def _get_current_serial():
    return strftime("%Y%m%d%S")


def get_random_key():
    return base64.b64encode(urandom(48)).decode().replace("=", "")


def add_queue_message(operation, args):
    # Add a message to the queue
    queue.put_job(json.dumps({"operation": operation, "args": args}))


def get_args(*args):
    # Parse the request's JSON payload and return as a tuple of arguments.

    if request.json is None:
        # TODO: Replace this function with a decorator that handles this ValueError and returns a correct JSON error response
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


def get_api_key():
    x_api_key = request.headers.get("X-API-Key")
    if not (x_api_key or request.headers.get("Cookie")):
        raise ValueError("X-API-Key or Cookie must not be blank")

    if x_api_key:
        api_key = x_api_key
    else:
        api_key = request.headers.get("Cookie").split("apikey=")[1]

    return api_key


def zone_authentication_required(f):
    # Check if a user is authenticated and permitted to perform operations on a zone

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            api_key = get_api_key()
        except ValueError:
            return jsonify({"success": False, "message": "X-API-Key or Cookie must not be blank"})

        zone = kwargs.get("zone")
        if not zone:
            return jsonify({"success": False, "message": "zone must not be blank"})

        zone_doc = zones.find_one({"zone": zone})
        if not zone_doc:
            return jsonify({"success": False, "message": "zone doesn't exist"})

        user_doc = users.find_one({"key": api_key})
        if not user_doc:
            return jsonify({"success": False, "message": "Access Denied"})

        if user_doc["username"] not in zone_doc["users"] and (not user_doc.get("admin")):
            return jsonify({"success": False, "message": "Access Denied"})

        return f(*args, **kwargs, user_doc=user_doc)

    return decorated_function


def authentication_required(f):
    # Check if a user is authenticated at all

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            api_key = get_api_key()
        except ValueError:
            return jsonify({"success": False, "message": "X-API-Key or Cookie must not be blank"})

        user_doc = users.find_one({"key": api_key})
        if not user_doc:
            return jsonify({"success": False, "message": "Not authenticated"})

        return f(*args, **kwargs, username=user_doc["username"], is_admin=bool(user_doc.get("admin")))

    return decorated_function


def _update_collector():
    _nodes = {}
    for node in nodes.find():
        _nodes[node["name"]] = node["management_ip"]

    with open("/tmp/collector_bird.conf", "w") as bird_config_file:
        bird_config_file.write(collector_bird_template.render(nodes=_nodes, asn=configuration["collector"]["asn"]))

    add_queue_message("update_collector", None)


# Routes

@app.route("/auth/signup", methods=["POST"])
def auth_signup():
    # Create a new user account

    try:
        username, password = get_args("username", "password")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)})

    if not valid_email(username) or len(username) > 100:
        return jsonify({"success": False, "message": "Invalid username"})

    if len(password) > 200:
        return jsonify({"success": False, "message": "Password must not be longer than 200 characters"})

    if len(password) < 16:
        return jsonify({"success": False, "message": "Password must be longer than 16 characters"})

    user_doc = users.find_one({"username": username})
    if user_doc:
        return jsonify({"success": False, "message": "User already exists"})

    add_queue_message("send_email", args={"recipients": [username], "subject": "[delivr.dev] Welcome to delivr.dev!", "body": welcome_template.render(email=username)})

    users.insert_one({
        "username": username,
        "password": argon.hash(password),
        "key": get_random_key(),
        "enabled": False
    })

    return jsonify({"success": True, "message": "Signup success"})


@app.route("/auth/login", methods=["POST"])
def auth_login():
    # Validate credentials and get the API key

    try:
        username, password = get_args("username", "password")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)})

    user_doc = users.find_one({"username": username})
    if not user_doc:
        return jsonify({"success": False, "message": "Invalid username or password"})

    try:
        valid = argon.verify(user_doc["password"], password)
    except VerifyMismatchError:
        return jsonify({"success": False, "message": "Invalid username or password"})
    else:
        if valid:
            if user_doc.get("enabled"):
                resp = make_response(jsonify({"success": True, "message": user_doc["key"]}))
                resp.set_cookie("apikey", user_doc["key"])
                return resp
            else:
                return jsonify({"success": False, "message": "This account is inactive. Please contact info@delivr.dev for more information."})

    return jsonify({"success": False, "message": "Invalid username or password"})


@app.route("/user/acl", methods=["GET", "PUT"])
@authentication_required
def user_acl(username, is_admin):
    if request.method == "GET":
        user_doc = users.find_one({"username": username})
        return jsonify({"success": True, "message": user_doc.get("acl")})
    elif request.method == "PUT":
        addr = get_args("address")
        try:
            _valid = ipaddress.ip_network(addr)
        except ValueError:
            return jsonify({"success": False, "message": "Invalid CIDR notation"})

        users.update_one({"username": username}, {"$push": {"acl": addr}})
        return jsonify({"success": True, "message": "ACL updated"})


@app.route("/user/change_password", methods=["POST"])
@authentication_required
def change_password(username, is_admin):
    password = get_args("password")

    if len(password) > 16:
        users.update_one({"username": username}, {"$set": {
            "password": argon.hash(password),
        }})
        return jsonify({"success": True, "message": "Password updated successfully"})
    else:
        return jsonify({"success": False, "message": "Password must be longer than 16 characters"})


@app.route("/zones/add", methods=["POST"])
@authentication_required
def zones_add(username, is_admin):
    # Add a new zone to the system

    try:
        zone = get_args("zone")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)})

    if not valid_zone(zone):
        return jsonify({"success": False, "message": "Invalid zone"})

    if "arpa" in zone:
        zone_type = "reverse"
    else:
        zone_type = "forward"

    try:
        zones.insert_one({
            "zone": zone,
            "records": [],
            "serial": _get_current_serial(),
            "users": [username],
            "type": zone_type
        })
    except DuplicateKeyError:
        return jsonify({"success": False, "message": "Zone already exists"})
    else:
        mail_template = new_domain_template.render(domain=zone, nameservers=configuration["dns"]["nameservers"])
        add_queue_message("send_email", args={"recipients": [username], "subject": "[delivr.dev] Domain added to delivr.dev", "body": mail_template})
        add_queue_message("refresh_all_zones", args=None)

        return jsonify({"success": True, "message": "Added " + zone})


@app.route("/zones/list", methods=["GET"])
@authentication_required
def zones_list(username, is_admin):
    # Find all zones that have username in their users list

    if is_admin:
        _zones = list(zones.find({}))
    else:
        _zones = list(zones.find({
            "users": {
                "$in": [username]
            }
        }))

    for zone in _zones:
        del zone["_id"]

    return jsonify({"success": True, "message": _zones})


@app.route("/zone/<zone>/delete", methods=["POST"])
@zone_authentication_required
def zones_delete(zone, user_doc):
    # Delete a zone

    if not valid_zone(zone):
        return jsonify({"success": False, "message": "Invalid zone"})

    delete_op = zones.delete_one({"zone": zone})

    if delete_op.deleted_count > 0:
        add_queue_message("delete_zone", args={"zone": zone})
        add_queue_message("refresh_all_zones", args=None)
        return jsonify({"success": True, "message": "Deleted " + zone})
    else:
        return jsonify({"success": False, "message": "Zone " + zone + " doesn't exist"})


@app.route("/zone/<zone>/users", methods=["GET"])
@zone_authentication_required
def zones_users(zone, user_doc):
    # Get a zone's users

    if not valid_zone(zone):
        return jsonify({"success": False, "message": "Invalid zone"})

    zone_doc = zones.find_one({"zone": zone})
    if zone_doc:
        return jsonify({"success": True, "message": zone_doc["users"]})
    else:
        return jsonify({"success": False, "message": "Zone " + zone + " doesn't exist"})


# Record management

@app.route("/zone/<zone>/add", methods=["POST"])
@zone_authentication_required
def records_add(zone, user_doc):
    # Add a record to a zone

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

    zone_doc = zones.find_one({"zone": zone})
    if not zone_doc:
        return jsonify({"success": False, "message": "Zone doesn't exist"})

    if zone_doc["type"] == "forward":
        if rec_type == "A":
            try:
                value, proxied = get_args("value", "proxied")
            except ValueError as e:
                return jsonify({"success": False, "message": str(e)})

            if not valid_ipv4(value):
                return jsonify({"success": False, "message": "Invalid IPv4 address"})

        elif rec_type == "AAAA":
            try:
                value, proxied = get_args("value", "proxied")
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

            # TODO: Check for TXT validity and maybe put quotes around the TXT record?
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
                if int(priority) < 0:
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
            return jsonify({"success": False, "message": "Invalid record type (Allowed values are A/AAAA/CNAME/TXT/MX/SRV"})

    else:  # Reverse zone
        if rec_type == "PTR":
            try:
                value = get_args("value")
            except ValueError as e:
                return jsonify({"success": False, "message": str(e)})

            if not valid_label(value):
                return jsonify({"success": False, "message": "Invalid PTR value"})

        else:
            return jsonify({"success": False, "message": "Invalid record type (Allowed values are PTR"})

    # The new record's universal options
    new_record = {
        "label": label,
        "ttl": int(ttl),
        "type": rec_type,
        "value": value
    }

    pinned_nodes = request.json.get("pinned_nodes")
    if pinned_nodes:
        pinned_nodes_list = []

        # Find all node names
        node_names = []
        for node in nodes.find():
            node_names.append(node["name"])

        # Iterate over a comma-separated list of pinned nodes
        for pinned_node in pinned_nodes.split(", "):
            # Check for invalid nodes
            if pinned_node not in node_names:
                return jsonify({"success": False, "message": "Node " + pinned_nodes + " is not a valid node"})
            else:
                pinned_nodes_list.append(pinned_node)

        if len(pinned_nodes_list) < 1:
            return jsonify({"success": False, "message": "You must pin at least one node"})

        new_record["pinned_nodes"] = pinned_nodes_list

    is_proxied = False
    try:
        # noinspection PyUnboundLocalVariable
        _proxied = proxied
    except NameError:  # If not an A/AAAA record
        pass
    else:
        if proxied:
            is_proxied = True
            new_record["proxied"] = True
            add_queue_message("send_email", args={"recipients": [user_doc["username"]], "subject": "[delivr.dev] Proxied record added", "body": proxied_record_template.render(domain=zone)})

    # BEGIN HACK

    if is_proxied:
        if not user_doc.get("admin"):
            return jsonify({"success": False, "message": "Proxied records is not available on your account. Please contact info@delivr.dev for more information."})

        if not user_doc.get("acl") and len(user_doc.get("acl")) > 0:
            return jsonify({"success": False, "message": "You must configure an ACL before adding a proxied record. See https://delivr.dev/docs/caching-proxy for more information."})

    # END HACK

    zones.update_one({"zone": zone}, {
        "$push": {"records": new_record},
        "$set": {"serial": _get_current_serial()}
    })

    if is_proxied:
        add_queue_message("refresh_cache", None)

    add_queue_message("refresh_all_zones", args=None)

    return jsonify({"success": True, "message": "Record added to " + zone})


@app.route("/zone/<zone>/records", methods=["GET"])
@zone_authentication_required
def records_list(zone, user_doc):
    # Get a list of all the records of a zone

    if not valid_zone(zone):
        return jsonify({"success": False, "message": "Invalid zone"})

    zone_doc = zones.find_one({"zone": zone})
    if zone_doc:
        return jsonify({"success": True, "message": zone_doc.get("records")})
    else:
        return jsonify({"success": False, "message": "zone " + zone + " doesn't exit"}), 400


@app.route("/zone/<zone>/delete_record/<index>", methods=["POST"])
@zone_authentication_required
def record_delete(zone, index, user_doc):
    # Delete a zone's record by index

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
        "serial": _get_current_serial()
    }})

    add_queue_message("refresh_all_zones", args=None)

    return jsonify({"success": True, "message": "Record deleted at index " + str(index) + " from " + zone})


@app.route("/zones/<zone>/export", methods=["GET"])
def zones_export(zone):
    # Export zone's RFC 1035 (BIND-format) zone file

    if not valid_zone(zone):
        return jsonify({"success": False, "message": "Invalid zone"})

    zone = zones.find_one({"zone": zone})
    current_time = strftime("%b %d %Y %H:%M")

    if not zone:
        return jsonify({"success": False, "message": "Zone doesn't exist"})

    zone_file = utils.render_zone(zone, {"name": "no-node-selected"})

    return jsonify({"success": True, "message": "; " + zone["zone"] + " exported from delivr.dev at " + current_time + "\n\n" + zone_file})


# Node

@app.route("/nodes/add", methods=["POST"])
@authentication_required
def nodes_add(username, is_admin):
    # Add a node

    if not is_admin:
        return 404

    try:
        name, provider, connectivity, datacenter, geoloc, location, management_ip = get_args("name", "provider", "connectivity", "datacenter", "geoloc", "location", "management_ip")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)})

    add_op = nodes.insert_one({
        "name": name,
        "provider": provider,
        "connectivity": connectivity,
        "datacenter": datacenter,
        "geoloc": geoloc,
        "location": location,
        "management_ip": management_ip,
    })

    _update_collector()

    if add_op.acknowledged:
        return jsonify({"success": True, "message": "Added " + name})
    else:
        return jsonify({"success": False, "message": "Unable to add node" + name})


@app.route("/nodes/list", methods=["GET"])
@authentication_required
def nodes_list(username, is_admin):
    # Get a list of all nodes

    _nodes = list(nodes.find())

    for node in _nodes:
        del node["_id"]

        if not is_admin:  # If user isn't admin, remove sensitive info
            del node["management_ip"]

    return jsonify({"success": True, "message": _nodes})


@app.route("/counters", methods=["GET"])
def counters():
    # Get node and location counters

    _nodes = list(nodes.find())
    node_count = 0

    unique_locations = set()
    for node in nodes.find():
        node_count += 1
        unique_locations.add(node["location"])

    return jsonify({"success": True, "message": {
        "nodes": node_count,
        "locations": len(unique_locations)
    }})


@app.route("/nodes/power", methods=["POST"])
@authentication_required
def nodes_power(username, is_admin):
    # Start or stop a node's BGP daemon

    if not is_admin:
        return jsonify({"success": False, "message": "Unauthorized"})

    try:
        name, state = get_args("name", "state")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)})

    if not (state == "on" or state == "off"):
        return jsonify({"success": False, "message": "state must be either \"on\" or \"off\""})

    node = nodes.find_one({"name": name})
    if not node:
        return jsonify({"success": False, "message": "node \"" + name + "\" doesn't exist"})

    add_queue_message("node_power", {"ip": node["management_ip"], "state": state})

    return jsonify({"success": True, "message": "Set BGP status to " + state})


@app.route("/stats", methods=["GET"])
@authentication_required
def stats(username, is_admin):
    # Get general system stats

    if not is_admin:
        return jsonify({"success": False, "message": "Unauthorized"})

    unique_locations = set()
    for node in nodes.find():
        unique_locations.add(node["location"])

    return jsonify({"success": True, "message": {
        "nodes": nodes.count_documents({}),
        "zones": zones.count_documents({}),
        "users": users.count_documents({}),
        "locations": len(unique_locations)
    }})


@app.route("/admin")
@authentication_required
def admin(username, is_admin):
    # Return if you are an admin or not

    return jsonify({"success": is_admin, "message": "200"})


@app.route("/users", methods=["GET"])
@authentication_required
def get_users(username, is_admin):
    # Get a list of users

    if not is_admin:
        return jsonify({"success": False, "message": "Unauthorized"})

    _users = list(users.find())

    for user in _users:
        del user["_id"]
        del user["key"]
        del user["password"]

    return jsonify({"success": True, "message": _users})


@app.route("/user/<user>/toggle", methods=["POST"])
@authentication_required
def user_toggle(username, is_admin, user):
    # Toggle the enabled state of a user

    if not is_admin:
        return jsonify({"success": False, "message": "Unauthorized"})

    _user = users.find_one({"username": user})
    if not _user:
        return jsonify({"success": False, "message": "User doesn't exist"})

    users.update_one({"username": user}, {"$set": {
        "enabled": not _user["enabled"]
    }})

    return jsonify({"success": True, "message": "User enabled state is now " + str(not _user["enabled"])})


@app.route("/authenticated")
def authenticated():
    # Return if you are authenticated or not
    return jsonify({"success": True, "message": (request.headers.get("X-API-Key") or request.headers.get("Cookie"))})


# ECA helpers


def eca_auth_required(f):
    # Check if an ECA node is authenticated and enabled

    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_key = request.headers.get("X-Auth-Key")
        if not auth_key:
            return jsonify({"success": False, "message": "X-Auth-Key header must be supplied"})

        eca = ecas.find_one({"key": auth_key})
        if not eca:
            return jsonify({"success": False, "message": "Cannot find ECA node"})

        if not eca["enabled"]:
            return jsonify({"success": False, "message": "This ECA node is disabled. Please contact info@delivr.dev for more information"})

        return f(*args, **kwargs, eca=eca)

    return decorated_function


# ECA routes
@app.route("/eca/add", methods=["POST"])
@authentication_required
def eca_add(username, is_admin):
    # add an ECA node

    if not is_admin:
        return jsonify({"success": False, "message": "Unauthorized"})

    try:
        contact_name, contact_email, location = get_args("contact_name", "contact_email", "location")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)})

    key = get_random_key()

    ecas.insert_one({
        "contact_name": contact_name,
        "contact_email": contact_email,
        "location": location,
        "enabled": False,
        "key": key
    })

    return jsonify({"success": True, "message": key})


@app.route("/eca/manifest")
@eca_auth_required
def eca_manifest(eca):
    # Get an ECA zone manifest

    manifest = {
        "zones": {}
    }

    for zone in zones.find():
        manifest["zones"][zone["zone"]] = zone["serial"]

    return jsonify({"success": True, "message": manifest})


@app.route("/eca/pull/<zone>")
@eca_auth_required
def eca_pull(eca, zone):
    # Pull a single zone

    zone = zones.find_one({"zone": zone})
    if not zone:
        return jsonify({"success": False, "message": "Zone doesn't exist"})

    zone = dict(zone)
    del zone["_id"]

    return jsonify({"success": True, "message": {
        "file": utils.render_zone(zone, {"name": None}),
        "serial": zone["serial"]
    }})


@app.route("/eca/registry")
@eca_auth_required
def eca_registry(eca):
    # Get the zone registry file

    zones_file = ""

    for zone in db["zones"].find():
        zones_file += utils.render_local(zone["zone"])

    return jsonify({"success": True, "message": zones_file})


@app.route("/eca/check")
@eca_auth_required
def eca_check(eca):
    # Check if this ECA is authorized

    eca = dict(eca)
    eca["id"] = str(eca["_id"])
    del eca["_id"]
    del eca["enabled"]
    del eca["key"]

    return jsonify({"success": True, "message": eca})


# Admin control

@app.route("/debug/refresh_all_zones")
@authentication_required
def refresh_zones(username, is_admin):
    # Refresh the named.conf.local file

    if not is_admin:
        return jsonify({"success": False, "message": "Unauthorized"})

    add_queue_message("refresh_all_zones", args=None)
    return jsonify({"success": True, "message": "Refreshing zones"})


@app.route("/debug/clear_queue")
@authentication_required
def clear_queue(username, is_admin):
    # Clear the beanstalk queue

    if not is_admin:
        return jsonify({"success": False, "message": "Unauthorized"})

    for job in queue.reserve_iter():
        queue.delete_job(job.job_id)

    return jsonify({"success": True, "message": "Cleared queue"})


@app.route("/debug/queue_stats")
@authentication_required
def queue_stats(username, is_admin):
    # Clear the beanstalk queue

    if not is_admin:
        return jsonify({"success": False, "message": "Unauthorized"})

    stats = queue.stats()

    return jsonify({"success": True, "message": {
        "current_ready": stats["current-jobs-ready"],
        "current_reserved": stats["current-jobs-reserved"]
    }})


@app.route("/debug/refresh_cache")
@authentication_required
def refresh_cache(username, is_admin):
    # Refresh the default.vcl cache file

    if not is_admin:
        return jsonify({"success": False, "message": "Unauthorized"})

    add_queue_message("refresh_cache", None)
    return jsonify({"success": True, "message": "Refreshing cache config"})


@app.route("/debug/update_collector")
@authentication_required
def update_collector(username, is_admin):
    # Update the BGP config on the route collector

    if not is_admin:
        return jsonify({"success": False, "message": "Unauthorized"})

    _update_collector()
    return jsonify({"success": True, "message": "Refreshing cache config"})


if __name__ == "__main__":
    app.run(debug=configuration["development"])
