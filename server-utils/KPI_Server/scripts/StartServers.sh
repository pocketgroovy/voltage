#!/usr/bin/env bash


systemctl start httpd.service || NOHTTPD=$?
if [ ${NOHTTPD} ]; then
        echo "-LOG- ERROR on starting apache"
        exit 1
else
	echo "-LOG- apache started"
fi
