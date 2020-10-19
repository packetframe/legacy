#!/bin/bash

if [[ "$1" == "list" ]]; then
  echo -n "Nodes: "
  mongo --quiet --eval 'db.cache_nodes.count({});' cdn
  mongo --quiet --eval 'db.cache_nodes.find().forEach(function(node) {print(node.name, node.location);});' cdn
  exit
fi

if [[ "$1" == "stop" ]]; then
  echo -n "Stopping "
  mongo --quiet --eval 'db.cache_nodes.find().forEach(function(node) {print(node.name, node.location);});' cdn | grep "$2"
  node_ip=$(mongo --quiet --eval 'db.cache_nodes.find({"name": "'$2'"}).forEach(function(x) {print(x.management_ip);});' cdn)
  ssh -p 34553 -i ssh-key root@"$node_ip" 'systemctl stop bird && echo "$(hostname) Stopped BGP process" || echo "ERROR: Failed to stop BGP process"'
  exit
fi

if [[ "$1" == "start" ]]; then
  echo -n "Starting "
  mongo --quiet --eval 'db.cache_nodes.find().forEach(function(node) {print(node.name, node.location);});' cdn | grep "$2"
  node_ip=$(mongo --quiet --eval 'db.cache_nodes.find({"name": "'$2'"}).forEach(function(x) {print(x.management_ip);});' cdn)
  ssh -p 34553 -i ssh-key root@"$node_ip" 'systemctl start bird && echo "$(hostname) Started BGP process" || echo "ERROR: Failed to start BGP process"'
  exit
fi

node="$1"

echo -n Jumping to $node
node_ip=$(mongo --quiet --eval "db.cache_nodes.findOne({name: \"${node}\"})[\"management_ip\"]" cdn)
echo " - $node_ip"

ssh -i ssh-key -p 34553 root@$node_ip
