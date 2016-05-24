#!/usr/bin/env bash

###################################################################################################
###### This script is responsible for installing Apache, vim, and selinux management tool"   ######
###################################################################################################

APACHE_INSTALLED=$(yum list installed | grep httpd)
if [ -n "${APACHE_INSTALLED}" ]; then
 echo "-LOG- apache is installed"
else
 echo "-LOG- apache is not installed, installing now"
 	yum -y install httpd || NOAPACHE=$?
	if [ ${NOAPACHE} ]; then
	        echo "-LOG- ERROR on apache installation"
	        echo " Are you on sudo? be root and visudo to add you"
	        exit 1
	fi
fi

VIM_INSTALLED=$(type vim) > /dev/null
if [ -n "${VIM_INSTALLED}" ]; then
 echo "-LOG- vim is installed"
else
 echo "-LOG- vim is not installed, installing now"
 	yum -y install vim || NOVIM=$?
	if [ ${NOVIM} ]; then
	        echo "-LOG- ERROR on vim installation"
	        exit 1
	fi
fi

SE_INSTALLED=$(type semanage) > /dev/null
if [ -n "${SE_INSTALLED}" ]; then
 echo "-LOG- semanage is installed"
else
 echo "-LOG- semanage is not installed, installing now"
 	yum -y install policycoreutils-python || NOSEMANAGE=$?
	if [ ${NOSEMANAGE} ]; then
	        echo "-LOG- ERROR on semanage installation"
	        exit 1
	fi
fi

WSGI_INSTALLED=$(yum list installed | grep mod_wsgi)
if [ -n "${WSGI_INSTALLED}" ]; then
 echo "-LOG- mod_wsgi is installed"
else
 echo "-LOG- mod_wsgi is not installed, installing now"
 	yum -y install mod_wsgi || NOWSGI=$?
	if [ ${NOWSGI} ]; then
	        echo "-LOG- ERROR on mod_wsgi installation"
	        exit 1
	fi
fi

SSL_INSTALLED=$(yum list installed | grep mod_ssl)
if [ -n "${SSL_INSTALLED}" ]; then
 echo "-LOG- mod_ssl is installed"
else
 echo "-LOG- mod_ssl is not installed, installing now"
 	yum -y install mod_ssl || NO_SSL=$?
	if [ ${NO_SSL} ]; then
	        echo "-LOG- ERROR on mod_ssl installation"
	        exit 1
	fi
fi