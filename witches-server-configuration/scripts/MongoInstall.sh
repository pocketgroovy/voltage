#!/usr/bin/env bash
 

###################################################################################################
###### This script is responsible for installing mongo 										 ######
###################################################################################################

 MONGOREPO=/etc/yum.repos.d/mongodb-org-3.0.repo

# create mongo repo in yum directory so that we can use "yum install"
 if [ ! -e $MONGOREPO ]; then

	echo "[mongodb-org-3.0]" > $MONGOREPO
	echo "name=MongoDB Repository" >> $MONGOREPO
	echo "baseurl=https://repo.mongodb.org/yum/redhat/\$releasever/mongodb-org/3.0/x86_64/" >> $MONGOREPO
	echo "gpgcheck=0" >> $MONGOREPO
	echo "enabled=1" >> $MONGOREPO

	chmod 644 $MONGOREPO
	echo "-LOG- mongo repo file created"
fi

MONGOINSTALLED=$(type mongo) > /dev/null
if [ -n "$MONGOINSTALLED" ]; then
 	echo "-LOG- mongo is installed"
else
	echo "-LOG- mongo is not installed, installing now"
	yum install -y mongodb-org-3.0.7 mongodb-org-server-3.0.7 mongodb-org-shell-3.0.7 mongodb-org-mongos-3.0.7 mongodb-org-tools-3.0.7 || NOMONGO=$?
	if [ ${NOMONGO} ]; then
	        echo "-LOG- ERROR on mongodb installation"
	        exit 1
	fi
fi

chown -R mongod:mongod /var/lib/mongo || CHOWN_MONGOD=$?
	if [ ${CHOWN_MONGOD} ]; then
	        echo "-LOG- ERROR on changing ownership for mongo db"
	        exit 1
	fi



