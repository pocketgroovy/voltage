#!/usr/bin/env bash
set -o errexit

POTION_COUNT=$1
MESSAGE=$2
SERVER=$3

if [ $# -ne 3 ]; then
	echo "usage:$0 potion_count, 'message here', host:27017/database"
	exit 1
fi

mongo $SERVER --eval "var potionCount='${POTION_COUNT}'; var message='${MESSAGE}'" SendStaminaPotionGift.js