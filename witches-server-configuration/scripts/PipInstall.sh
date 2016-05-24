#!/usr/bin/env bash

###################################################################################################
###### This script is responsible for installing pip and epel repo in which pip can be found ######
###################################################################################################

EPELINSTALLED=$(yum list installed | grep epel-release)

if [ -n "$EPELINSTALLED" ]; then
 echo "-LOG- epel is installed"
else
 echo "-LOG- epel is not installed, installing now"
 	yum -y install epel-release || NOEPEL=$?
	if [ ${NOEPEL} ]; then
	        echo "-LOG- ERROR on epel installation"
	        exit 1
	fi
fi

PIPINSTALLED=$(type pip) > /dev/null
if [ -n "$PIPINSTALLED" ]; then
 echo "-LOG- pip is installed"
else
 echo "-LOG- pip is not installed, installing now"
	yum -y install python-pip || NOPIP=$?
	if [ ${NOPIP} ]; then
	        echo "-LOG- ERROR on pip installation"
	        exit 1
	fi
fi

