#!/usr/bin/env bash
set -x
set -o errexit

# Open VPN connection
pgrep pppd || VPN_CLOSED=$?

if [ -n "$VPN_CLOSED" ]; then
    sudo pppd call softlayer
fi



