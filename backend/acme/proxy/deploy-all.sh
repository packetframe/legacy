#!/bin/bash

nodes=$(mongo --quiet --eval 'db.nodes.find({"http": true}).forEach(function(node) {print(node.management_ip);});' cdn)

tar -czvf certs.tar.gz /etc/letsencrypt/live/*

for node in $nodes ; do
	echo Copying to $node
	scp -P 34553 -i /home/nate/ssh-key certs.tar.gz root@$node:/etc/caddy/certs.tar.gz
	ssh -p 34553 -i /home/nate/ssh-key root@$node "tar -xvzf /etc/caddy/certs.tar.gz -C /etc/caddy ; chown -R caddy:caddy /etc/caddy/*.pem ; caddy reload -config /etc/caddy/Caddyfile"
#	TODO: This doesnt extract in the right place
done
