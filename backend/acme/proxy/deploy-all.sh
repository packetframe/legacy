#!/bin/bash

nodes=$(mongo --quiet --eval 'db.nodes.find({"http": true}).forEach(function(node) {print(node.management_ip);});' cdn)

for node in $nodes ; do
  echo "Updating $node"
  for zone in $(ls /etc/letsencrypt/live/); do
    scp -P 34553 -i /home/nate/ssh-key /etc/letsencrypt/live/$zone/privkey.pem root@$node:/etc/caddy/$zone-key.pem
    scp -P 34553 -i /home/nate/ssh-key /etc/letsencrypt/live/$zone/fullchain.pem root@$node:/etc/caddy/$zone-chain.pem
  done

  ssh -p 34553 -i /home/nate/ssh-key root@$node "chown -R caddy:caddy /etc/caddy/*.pem ; caddy reload -config /etc/caddy/Caddyfile"
done
