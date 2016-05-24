#!/usr/bin/env bash
set -x
set -o errexit


if [ $# != 2 ]; then
    echo "Usage: $0 URL database"
    exit 1
fi
  
URL=$1
DB=$2

mongo ${URL}/${DB} --eval "var database='${DB}'" RemoveAttachment.js