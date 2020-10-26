#!/bin/bash

SSH_KEY="/home/nate/ssh-key"

if [[ "$1" == "node" ]]; then
  target="$2"
  echo -n Jumping to node $target
  node_ip=$(mongo --quiet --eval "db.nodes.findOne({name: \"${target}\"})[\"management_ip\"]" cdn)
  echo " - $node_ip"
elif [[ "$1" == "cache" ]]; then
  target="$2"
  echo -n Jumping to cache $target
  node_ip=$(mongo --quiet --eval "db.cache_nodes.findOne({name: \"${target}\"})[\"management_ip\"]" cdn)
  echo " - $node_ip"
else
  echo "Usage: ./cdnctl.sh [cache|node] NODE_IP"
  exit 1
fi


ssh -i $SSH_KEY -p 34553 root@$node_ip
