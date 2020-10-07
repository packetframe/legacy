#!/bin/bash

nodes=$(mongo --quiet --eval 'db.nodes.find().forEach(function(node) {print(node.management_ip);});' cdn)

for line in $nodes ; do
	echo "Removing file from $line"
	ssh -p 34553 -i delivr-backend/ssh-key root@$line "rm -rf /usr/share/caddy/*"
done
