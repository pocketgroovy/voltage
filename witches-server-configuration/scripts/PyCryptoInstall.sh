#!/usr/bin/env bash
set -o errexit

######################################################################
######  PyCrypto is resposible for Android Receipt Verification ######
######################################################################

PYTHON_EGG_DIR=/var/www/.python-eggs

SERVERGROUP=`cat /etc/*-release | grep NAME`

if [[ $SERVERGROUP == *"Ubuntu"* ]]; then
    echo "it's ubuntu"
  	apt-get install -y python-dev
  	pip install --upgrade pycrypto
  	mkdir ${PYTHON_EGG_DIR}  # Ubuntu needs this cache directory http://stackoverflow.com/questions/2192323/what-is-the-python-egg-cache-python-egg-cache
	chown www-data:www-data ${PYTHON_EGG_DIR}
	chmod 755 ${PYTHON_EGG_DIR}
elif [[ $SERVERGROUP == *"CentOS"* ]]; then
    echo "it's CentOS"
    yum install -y python-crypto
fi



