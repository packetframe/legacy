#!/bin/bash

nodes=$(mongo --quiet --eval 'db.nodes.find({"http": true}).forEach(function(node) {print(node.management_ip);});' cdn)

rm -rf /tmp/certs/ certs.tar.gz
mkdir /tmp/certs/

for zone in $(ls /etc/letsencrypt/live/); do
  cp /etc/letsencrypt/live/$zone/privkey.pem /tmp/certs/$zone-key.pem
  cp /etc/letsencrypt/live/$zone/fullchain.pem /tmp/certs/$zone-chain.pem
done

tar -cvzf certs.tar.gz /tmp/certs/*

for node in $nodes ; do
  echo "Updating $node"
  scp -P 34553 -i /home/nate/ssh-key certs.tar.gz root@$node:/etc/caddy/certs.tar.gz
  ssh -p 34553 -i /home/nate/ssh-key root@$node "bash /root/update-certs.sh"
done
