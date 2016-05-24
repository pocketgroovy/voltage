#!/usr/bin/env bash

set -o errexit # immediately exit on any error
SERVER=$1

if [ $# -ne 1 ]; then
    echo "usage: $0 <from>"
    exit 1
fi

USER=sysdev
USER_HOST=$USER@$SERVER

if ( ssh $USER_HOST '[ ! -d ~/curses_mongodb_BU ]' ); then
		echo "create curses_mongodb_BU dir in remote system"
		ssh $USER_HOST mkdir -p curses_mongodb_BU
fi

scp Keep100RecentBackUps.sh MongoBackUP.sh CreateLatestBackupCopy.sh $USER_HOST:~/curses_mongodb_BU/
