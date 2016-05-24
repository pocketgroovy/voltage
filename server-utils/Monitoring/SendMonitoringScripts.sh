#!/usr/bin/env bash
set -o errexit

SERVERIP=$1

if [ -n "$SERVERIP" ]; then
	rsync -a -c --delete --progress --exclude-from './syncExclusions' . sysdev@$SERVERIP:Monitoring

else
	echo "enter the server IP address"
	exit 1

fi