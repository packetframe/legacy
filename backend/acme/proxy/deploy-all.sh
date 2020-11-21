#!/bin/bash

nodes=$(mongo --quiet --eval 'db.nodes.find({"http": true}).forEach(function(node) {print(node.management_ip);});' cdn)

for cert in $(ls /etc/letsencrypt/live/); do
	for node in $nodes ; do
		echo Copying to $node
		scp -P 34553 -i /home/nate/ssh-key /etc/letsencrypt/live/$cert/fullchain.pem root@$node:/etc/caddy/$cert-chain.pem
		scp -P 34553 -i /home/nate/ssh-key /etc/letsencrypt/live/$cert/privkey.pem root@$node:/etc/caddy/$cert-key.pem
		ssh -p 34553 -i /home/nate/ssh-key root@$node "chown -R caddy:caddy /etc/caddy/*.pem ; caddy reload -config /etc/caddy/Caddyfile"
	done
done
