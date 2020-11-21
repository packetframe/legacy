#!/bin/bash

nodes=$(mongo --quiet --eval 'db.nodes.find({"http": true).forEach(function(node) {print(node.management_ip);});' cdn)

for node in $nodes ; do
	echo Copying to $node
	scp -P 34553 -i /home/nate/ssh-key /etc/letsencrypt/live/$CERTBOT_DOMAIN/fullchain.pem root@$node:/etc/caddy/$CERTBOT_DOMAIN-chain.pem
	scp -P 34553 -i /home/nate/ssh-key /etc/letsencrypt/live/$CERTBOT_DOMAIN/privkey.pem root@$node:/etc/caddy/$CERTBOT_DOMAIN-key.pem
	ssh -p 34553 -i /home/nate/ssh-key root@$node "chown -R caddy:caddy /etc/caddy/*.pem ; caddy reload -config /etc/caddy/Caddyfile"
done
