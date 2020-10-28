#!/bin/bash

sudo certbot certonly \
	-d "$1" \
	--manual \
	--preferred-challenges=dns \
	--text \
	--agree-tos \
	--manual-public-ip-logging-ok \
	--keep-until-expiring \
	--email info@delivr.dev \
	--manual-auth-hook $(pwd)/auth.py \
	--manual-cleanup-hook $(pwd)/deploy.sh
