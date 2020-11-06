#!/bin/bash

# Check for sudo

mkdir -p /etc/delivr-eca/
mkdir -p /var/delivr-eca/

apt update
apt install -y bind9 dnsutils python3 python3-pip
