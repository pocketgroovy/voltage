#!/usr/bin/env bash

set -o errexit # immediately exit on any error

APP_NAME="K&C"
MONGO_HOST="localhost"
MONGO_PORT="27017"
MONGO_DATABASE="witches"
TIMESTAMP=`date +%F-%H%M`
BACKUPS_HOME="/home/sysdev/curses_mongodb_BU"
BACKUPS_DIR="$BACKUPS_HOME/$APP_NAME"
BACKUP_NAME="$APP_NAME-$TIMESTAMP"

mongodump --host $MONGO_HOST --out $BACKUPS_DIR 

pushd $BACKUPS_DIR
mv $MONGO_DATABASE $BACKUP_NAME
tar -zcvf $BACKUPS_DIR/$BACKUP_NAME.tgz $BACKUP_NAME
rm -rf $BACKUP_NAME
popd

$BACKUPS_HOME/Keep100RecentBackUps.sh