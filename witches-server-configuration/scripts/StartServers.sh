#!/usr/bin/env bash


###################################################################################################
###### This script is responsible for setting up a server for an app "Kisses and Curses" ######
###################################################################################################

mongod --dbpath /var/lib/mongo/ --fork --syslog || NOMONGOSTART=$?     # systemctl start mongod || NOMONGOSTART=$?   <- this should be 
						               # used but somehow it doesn't find dbpath even though it's set up
						               # in /etc/mongod.conf
if [ ${NOMONGOSTART} ]; then
        echo "-LOG- ERROR on starting mongo"
        exit 1
else
	echo "-LOG- Mongo started"
fi


systemctl start redis.service || NOREDISSTART=$?
if [ ${NOREDISSTART} ]; then
        echo "-LOG- ERROR on starting redis"
        exit 1
else
	echo "-LOG- Redis started"
fi

systemctl start httpd.service || NOHTTPD=$?
if [ ${NOHTTPD} ]; then
        echo "-LOG- ERROR on starting apache"
        exit 1
else
	echo "-LOG- apache started"
fi
