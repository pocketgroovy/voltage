#!/usr/bin/env bash

###################################################################################################
###### This script is responsible for installing redis 										 ######
###################################################################################################

REDISNSTALLED=$(type redis-cli) > /dev/null
if [ -n "${REDISNSTALLED}" ]; then
 echo "-LOG- redis is installed"
else
 echo "-LOG- redis is not installed, installing now"
 	yum -y install redis || NOREDIS=$?
	if [ ${NOREDIS} ]; then
	        echo "-LOG- ERROR on redis installation"
	        exit 1
	else
		systemctl enable redis.service
	fi

fi
