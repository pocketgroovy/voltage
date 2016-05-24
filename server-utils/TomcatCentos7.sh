#!/usr/bin/env bash
set -x
set -o errexit

if [ $# -ne 2 ]; then
    echo "usage: $0 <username> <password>"
    exit 1
fi

USERNAME=$1
PASSWORD=$2

yum install -y tomcat
 
TOMCAT_CONF=/usr/share/tomcat/conf/tomcat.conf

TOMCAT_USER=/usr/share/tomcat/conf/tomcat-users.xml


if [ -e $TOMCAT_CONF ]; then
	echo "JAVA_OPTS=\"-Djava.security.egd=file:/dev/./urandom -Djava.awt.headless=true -Xmx512m -XX:MaxPermSize=256m -XX:+UseConcMarkSweepGC\"" >> $TOMCAT_CONF
fi

yum install -y tomcat-webapps tomcat-admin-webapps

if [ -e $TOMCAT_USER ]; then
	sed -i.bpk '/<tomcat-users>/a <user username=\"${USERNAME}\" password=\"${PASSWORD}\" roles=\"manager-gui,admin-gui\"/>' $TOMCAT_USER
fi

systemctl start tomcat
