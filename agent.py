from flask import Flask, request

app = Flask(__name__)

content_directory = "/tmp/bind/"


@app.route("/refresh_zones", methods=["POST"])
def refresh_zones():
    with open(content_directory + "named.conf.local", "w") as named_local_file:
        named_local_file.write(request.json["payload"])


@app.route("/refresh_single_zone", methods=["POST"])
def refresh_single_zone():
    with open(content_directory + "db." + request.json["zone"], "w") as zone_file:
        zone_file.write(request.json["zone_file"])
