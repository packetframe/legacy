#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run the ECA installer as root"
  exit
fi

mkdir -p /etc/delivr-eca/
mkdir -p /var/delivr-eca/

apt update
apt install -y bind9 dnsutils python3 python3-pip
