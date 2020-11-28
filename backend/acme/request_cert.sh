#!/bin/bash
sudo certbot certonly \
  --manual \
  --preferred-challenges http-01 \
  -m info@packetframe.com \
  --agree-tos \
  --manual-public-ip-logging-ok \
  --manual-auth-hook /home/nate/backend/acme/acme_pre_hook.sh \
  --manual-cleanup-hook /home/nate/backend/acme/acme_post_hook.sh \
  -d local.packetframe.com