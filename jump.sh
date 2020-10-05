#!/bin/bash

if [[ "$1" == "list" ]]; then
  echo -n "Nodes: "
  mongo --quiet --eval 'db.nodes.count({});' cdn
  mongo --quiet --eval 'db.nodes.find().forEach(function(node) {print(node.name, node.location);});' cdn
  exit
fi

node="$1"

echo -n Jumping to $node
node_ip=$(mongo --quiet --eval "db.nodes.findOne({name: \"${node}\"})[\"management_ip\"]" cdn)
echo " - $node_ip"

ssh -i ssh-key2 -p 34553 root@$node_ip
