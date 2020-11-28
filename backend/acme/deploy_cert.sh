#!/bin/bash

nodes=$(mongo --quiet --eval 'db.nodes.find().forEach(function(node) {print(node.management_ip);});' cdn)

for line in $nodes ; do
	echo "Copying certificates to $line"
	scp -P 34553 -i /home/nate/ssh-key /etc/letsencrypt/live/local.packetframe.com/fullchain.pem root@$line:/caddy/fullchain.pem
	scp -P 34553 -i /home/nate/ssh-key /etc/letsencrypt/live/local.packetframe.com/privkey.pem root@$line:/caddy/privkey.pem
	ssh -p 34553 -i /home/nate/ssh-key root@$line "chown -R caddy:caddy /caddy/* ; caddy reload -config /etc/caddy/Caddyfile"
done
