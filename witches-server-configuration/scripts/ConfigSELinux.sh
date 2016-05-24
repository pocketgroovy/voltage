#!/usr/bin/env bash

###################################################################################################
###### This script is responsible for setting SELinux to open port for mongodb" ######
###################################################################################################

ENFORCESTATUS="Enforcing"
ALREADYDEFINED="ValueError"
MONGOPORT=27017

ENFORCE=$(getenforce)
if [ $ENFORCE == $ENFORCESTATUS ]; then
	semanage port -a -t mongod_port_t -p tcp $MONGOPORT || NOSEMANAGE=$? > /dev/null
	if [ ${NOSEMANAGE} ]; then
	        echo "-LOG- Port is already defined in linux"
	fi
fi