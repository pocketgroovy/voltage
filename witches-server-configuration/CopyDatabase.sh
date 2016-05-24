#!/usr/bin/env bash
set -o errexit

DBFROM=$1

if [ $# -ne 2 ]; then
    echo "usage: $0 <from>"
    exit 1
fi


DEPLOY_DIR=/var/www/voltage-ent.com/witches-server

cd $DEPLOY_DIR/Voltage

./DBscripts/copyReferenceData.sh $DBFROM localhost