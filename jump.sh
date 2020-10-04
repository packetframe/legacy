#!/bin/bash

node="$1"

echo -n Jumping to $node
node_ip=$(mongo --quiet --eval "db.nodes.findOne({name: \"${node}\"})[\"management_ip\"]" cdn)
echo " - $node_ip"

ssh -i ssh-key2 -p 34553 root@$node_ip
