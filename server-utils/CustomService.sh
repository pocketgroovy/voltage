#!/usr/bin/env bash
set -o errexit # immediately exit on any error

if [ $# -ne 4 ]; then
    echo "usage: $0 <name> <port> <short name> <description>"
    exit 1
fi

XML_NAME=$1
PORT=$2
SHORT=$3
DESCRIPTION=$4

cd /etc/firewalld/services/

if [ ! -e $XML_NAME.xml ]; then
	touch $XML_NAME.xml
	CUSTOME_SERVICE=$XML_NAME.xml
	echo "<?xml version=\"1.0\" encoding=\"utf-8\"?>" >> $CUSTOME_SERVICE
	echo "<service>" >> $CUSTOME_SERVICE
	echo "<short>${SHORT}</short>" >> $CUSTOME_SERVICE
	echo "<description>" >> $CUSTOME_SERVICE
	echo "${DESCRIPTION}" >> $CUSTOME_SERVICE
	echo "</description>" >> $CUSTOME_SERVICE 
	echo "<port protocol=\"tcp\" port=\"${PORT}\"/>" >> $CUSTOME_SERVICE
	echo "</service>" >> $CUSTOME_SERVICE
	echo "-LOG- ${XML_NAME} xml created"
else
	echo "-LOG- ${XML_NAME}.xml already exists"

fi