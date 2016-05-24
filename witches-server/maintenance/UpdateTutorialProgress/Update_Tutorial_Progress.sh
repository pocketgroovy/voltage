#!/usr/bin/env bash

SERVER=$1

if [ $# -ne 1 ]; then
	echo "usage: $0 host:27017/database"
	exit 1
fi

echo "finding users who has finished scene 'mending luna' and update its tutorial flag"

mongo $SERVER --eval "" UpdateTutorialProgress.js