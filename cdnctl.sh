#!/bin/bash

SSH_KEY="/home/nate/ssh-key"

echo -n Jumping to node $2
node_ip=$(mongo --quiet --eval "db.nodes.findOne({name: \"${2}\"})[\"management_ip\"]" cdn)
echo " - $node_ip"

ssh -i $SSH_KEY -p 34553 root@$node_ip
