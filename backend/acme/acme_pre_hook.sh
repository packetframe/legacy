#!/bin/bash

nodes=$(mongo --quiet --eval 'db.nodes.find().forEach(function(node) {print(node.management_ip);});' cdn)

echo $CERTBOT_VALIDATION > /tmp/acme-challenge.txt

for line in $nodes ; do
	echo "Sending validation to $line"
	scp -P 34553 -i /home/nate/delivr-backend/ssh-key /tmp/acme-challenge.txt root@$line:/usr/share/caddy/$CERTBOT_TOKEN
done

rm -rf /tmp/acme-challenge.txt
