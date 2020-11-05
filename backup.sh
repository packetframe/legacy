#!/bin/bash

BACKUP_FILE="/var/log/delivr-backup.txt"

echo "Backup at $(date)" > $BACKUP_FILE
mongo --quiet --eval 'db.cache_nodes.find();' cdn >> $BACKUP_FILE
mongo --quiet --eval 'db.nodes.find();' cdn >> $BACKUP_FILE
mongo --quiet --eval 'db.zones.find();' cdn >> $BACKUP_FILE
mongo --quiet --eval 'db.users.find();' cdn >> $BACKUP_FILE
