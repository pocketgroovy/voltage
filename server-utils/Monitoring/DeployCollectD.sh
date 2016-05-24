#!/usr/bin/env bash
set -o errexit
#######################################################################
###### Deploy CollectD to server						 					 ######
#######################################################################

SERVER=$1
SERVER_NAME=$2
PORT=$3

if [ $# -ne 3 ]; then
    echo "usage: $0 <server ip> <server_name> <port>"
    exit 1
fi

scp -r CollectD root@$SERVER:

ssh root@$SERVER "~/CollectD/CollectDInstall.sh $SERVER_NAME $PORT"
