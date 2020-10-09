#!/bin/bash

nodes=$(mongo --quiet --eval 'db.nodes.find().forEach(function(node) {print(node.management_ip);});' cdn)

for line in $nodes ; do
	echo "Copying certificates to $line"
	scp -P 34553 -i /home/nate/delivr-backend/ssh-key /etc/letsencrypt/live/local.delivr.dev/fullchain.pem root@$line:/caddy/fullchain.pem
	scp -P 34553 -i /home/nate/delivr-backend/ssh-key /etc/letsencrypt/live/local.delivr.dev/privkey.pem root@$line:/caddy/privkey.pem
	ssh -p 34553 -i /home/nate/delivr-backend/ssh-key root@$line "chown -R caddy:caddy /caddy/*"
done
