#!/usr/bin/env bash
set -x
set -o errexit

if [ $# != 2 ]; then
    echo "Usage: $0 IPaddress database"
    exit 1
fi
  
IP=$1
DB=$2

mongo ${IP}/${DB} --eval "var database='${DB}'" UpdateLoginsWuser.js