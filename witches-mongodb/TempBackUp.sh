#!/usr/bin/env bash
set -o errexit # immediately exit on any error


if [ $# -ne 2 ]; then
    echo "usage: $0 <host ip> <backup storage dir>"
    exit 1
fi

MONGO_HOST=$1
BACKUPS_DIR=$2


mongodump --host $MONGO_HOST --out $BACKUPS_DIR 