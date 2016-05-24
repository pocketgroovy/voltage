#!/usr/bin/env bash

if [ $# != 4 ]; then
    echo "Usage: $0 database fromVersion toVersion futureVersion"
    exit 1
fi
  
DB=$1
FROM=$2
TO=$3
FUTURE=$4

mongo ${DB} --eval "var fromVersion='${FROM}'; var toVersion='${TO}'; var futureVersion='${FUTURE}'" updateDBOnIOSRelease.js
