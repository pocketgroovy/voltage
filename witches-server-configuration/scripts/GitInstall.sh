#!/usr/bin/env bash

###################################################################################################
###### This script is responsible for installing git 					 					 ######
###################################################################################################

GITNSTALLED=$(type git) > /dev/null
if [ -n "${GITNSTALLED}" ]; then
 echo "-LOG- git is installed"
else
 echo "-LOG- git is not installed, installing now"
 	yum -y install git || NOGIT=$?
	if [ ${NOGIT} ]; then
	        echo "-LOG- ERROR on git installation"
	        exit 1
	fi
fi

