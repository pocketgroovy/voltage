#!/usr/bin/env bash

set -o errexit # immediately exit on any error
APP_NAME="K&C"
BACKUPS_DIR="/home/sysdev/curses_mongodb_BU/$APP_NAME"
FILE_COUNT=100
TEMP_DIR="/home/sysdev/tempdbstorage"

if [ "$(ls -A $TEMP_DIR)" ]; then
	rm $TEMP_DIR/*
fi

pushd $BACKUPS_DIR

latest_file=`find -type f -printf '%p\n' | sort | tail -n 1`
echo $latest_file
cp $latest_file ~/tempdbstorage

popd

