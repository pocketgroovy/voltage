#!/usr/bin/env bash
set -o errexit

SERVERIP=$1

if [ -n "$SERVERIP" ]; then
scp RootInitSetup.sh root@$SERVERIP:
scp -r rootScripts root@$SERVERIP:

else
	echo "enter the server IP address"
	exit 1
fi