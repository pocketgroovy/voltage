#!/usr/bin/env bash

######################################################################################################
###### This script is responsible for creating directory in which witches-server reside for app ###### 
###### "Kisses and Curses" 																		######
######################################################################################################


if [ ! -d /var/www/voltage-ent.com ]; then
	mkdir /var/www/voltage-ent.com/ 
	echo "Directory, \"voltage-ent.com\" is created"
	chown sysdev:sysdev /var/www/voltage-ent.com
fi