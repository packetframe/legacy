#!/bin/bash

echo "Backup at $(date)" > backup.txt
mongo --quiet --eval 'db.cache_nodes.find();' cdn >> backup.txt
mongo --quiet --eval 'db.nodes.find();' cdn >> backup.txt
mongo --quiet --eval 'db.zones.find();' cdn >> backup.txt
mongo --quiet --eval 'db.users.find();' cdn >> backup.txt
