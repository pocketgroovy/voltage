#!/usr/bin/env bash

set -o errexit # immediately exit on any error

APP_NAME="K&C"
BACKUPS_DIR="/home/sysdev/curses_mongodb_BU/$APP_NAME"
DB_SLAVE=10.114.239.117
SCRIPT_BUCOPY="/home/sysdev/CreateLatestBackupCopy.sh"
BACKUPS_HOME="/home/sysdev/curses_mongodb_BU"

# Open VPN connection
pgrep pppd || VPN_CLOSED=$?

if [ -n ${VPN_CLOSED} ]; then
    pppd call softlayer
    sleep 15
fi

if ( ssh sysdev@$DB_SLAVE '[ ! -d ~/tempdbstorage ]' ); then
	echo "create tempdbstorage dir in remote system"
	ssh sysdev@$DB_SLAVE mkdir -p tempdbstorage
fi


ssh sysdev@$DB_SLAVE $SCRIPT_BUCOPY || NOT_COPIED=$?
if [ ${NOT_COPIED} ]; then
        echo "-LOG- Failed creating back up copy"
        exit 1
fi

scp sysdev@$DB_SLAVE:~/tempdbstorage/* $BACKUPS_DIR || NOT_RECEIVED=$?

if [ ${NOT_RECEIVED} ]; then
        echo "-LOG- Failed receiving back up copy"
        exit 1
fi

$BACKUPS_HOME/Keep100RecentBackUps.sh