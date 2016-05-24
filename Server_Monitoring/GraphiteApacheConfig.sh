#!/usr/bin/env bash

######################################################################################################
###### This script is responsible for creating apache config file for app "Kisses and Curses"   ###### 
######################################################################################################


TARGETWORD="/opt/graphite/static/"

NEWWORD="<Directory /opt/graphite/static/>"

TARGETTEXT="/etc/httpd/conf.d/graphite.conf"
BACKUP="backup"
TEMPFILE="/tmp/out.tmp"

[ ! -d $BACKUP ] && mkdir -p $BACKUP || :


if [ -f $TARGETTEXT ]; then

	FOUND=`grep "$NEWWORD" $TARGETTEXT`

	if [ ! -n "$FOUND" ]; then 

		/bin/cp -f $TARGETTEXT $BACKUP

		sed "s/$TARGETWORD/$NEWWORD/" "$TARGETTEXT" > $TEMPFILE 

		echo "sysdev  ALL=(ALL)       ALL # added sysdev" >> $TEMPFILE 
		echo "sysdev  ALL=NOPASSWD: /usr/bin/systemctl, /var/www/voltage-ent.com/witches-server/*" >> $TEMPFILE

		mv $TEMPFILE "$TARGETTEXT"

	else
		echo "Already Modified"

	fi
else
	echo "no sudoers found"
	exit 1

fi
APACHECONFIG=/etc/httpd/conf.d/graphite.conf

echo "<Directory /opt/graphite/static/>" >>  $APACHECONFIG
echo "Require all granted" >> $APACHECONFIG
echo "Order allow,deny" >> $APACHECONFIG
echo "Allow from all" >> $APACHECONFIG
echo "</Directory>" >> $APACHECONFIG

echo "-LOG- Apache config modified for Graphite"
