from jinja2 import Template
from config import configuration

with open("templates/local.j2", "r") as local_template_file:
    local_template = Template(local_template_file.read())

with open("templates/zone.j2") as zone_template_file:
    zone_template = Template(zone_template_file.read())

with open("templates/default.vcl.j2", "r") as vcl_template_file:
    vcl_template = Template(vcl_template_file.read())

with open("templates/Caddyfile.j2", "r") as caddy_template_file:
    caddy_template = Template(caddy_template_file.read())


def render_local(zone):
    return local_template.render(zone=zone)


def render_zone(zone, node):
    return zone_template.render(
        nameservers=configuration["dns"]["nameservers"],
        rname=configuration["dns"]["rname"],
        records=zone.get("records"),
        serial=zone["serial"],
        proxy4=configuration["proxy"]["server4"],
        proxy6=configuration["proxy"]["server6"],
        node=node["name"]
    )


def render_vcl(backends, domains, acls):
    return vcl_template.render(backends=backends, domains=domains, acls=acls)


def render_caddy(domains, node):
    return caddy_template.render(domains=domains, host=node["management_ip"], hostname=node["name"])
