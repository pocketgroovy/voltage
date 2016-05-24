#!/usr/bin/env bash

set -o errexit # immediately exit on any error
APP_NAME="K&C"
BACKUPS_DIR="/home/sysdev/curses_mongodb_BU/$APP_NAME"
FILE_COUNT=100
FILE_NAME="K\&C*.tgz"

pushd $BACKUPS_DIR

count=`ls -l $FILE_NAME | wc -l`

if [ $count -gt $FILE_COUNT ]; then
	extra_files_count=$((count-FILE_COUNT))
	oldest_file_list=`find -type f -printf '%p\n' | sort | head -n $extra_files_count`
	echo $oldest_file_list
	rm $oldest_file_list
fi

popd
