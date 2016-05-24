#!/usr/bin/env bash
set -x
set -o errexit


if [ $# != 2 ]; then
    echo "Usage: $0 IP_address database"
    exit 1
fi
  
IP=$1
DB=$2

mongo ${IP}/${DB} --eval "var database='${DB}'" SendSystemMail.js