#!/usr/bin/env bash
set -x
set -o errexit

PROD_DB=10.114.239.105

if [ -z "${from}" ] || [ -z "${to}" ] || [ -z "${future}" ]; then
    echo "Missing version migration parameters"
    exit 1
fi

# Open VPN connection
pgrep pppd || VPN_CLOSED=$?

if [ -n ${VPN_CLOSED} ]; then
    sudo pppd call softlayer
    sleep 15
fi


./updateAmazonEnvironment.sh ${PROD_DB}/witches ${from} ${to} ${future}