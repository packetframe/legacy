#!/bin/bash

SSH_KEY="/home/nate/ssh-key"

echo -n Jumping to node $1
node_ip=$(mongo --quiet --eval "db.nodes.findOne({name: \"${1}\"})[\"management_ip\"]" cdn)
echo " - $node_ip" $(mongo --quiet --eval "db.nodes.findOne({name: \"${1}\"})[\"provider\"]" cdn)

ssh -i $SSH_KEY -p 34553 root@$node_ip
