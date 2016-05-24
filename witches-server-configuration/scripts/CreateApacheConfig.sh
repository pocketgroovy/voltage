#!/usr/bin/env bash
set -o errexit
######################################################################################################
###### This script is responsible for creating apache config file for app "Kisses and Curses"   ###### 
######################################################################################################


APACHECONFIG=/etc/httpd/conf.d/witches.conf

if [ ! -e $APACHECONFIG ]; then
	echo "WSGIScriptAlias / /var/www/voltage-ent.com/witches-server/Voltage/Voltage/wsgi.py" >  $APACHECONFIG
	echo "WSGIPythonPath /var/www/voltage-ent.com/witches-server/Voltage/" >> $APACHECONFIG
	echo "<Directory /var/www/voltage-ent.com/witches-server/Voltage/Voltage>" >> $APACHECONFIG
	echo "</Directory>" >> $APACHECONFIG
	echo "<Files wsgi.py>" >> $APACHECONFIG
	echo "Order deny,allow" >> $APACHECONFIG
	echo "Require all granted" >> $APACHECONFIG
	echo "</Files>" >> $APACHECONFIG
	echo "Alias /media/ /var/www/voltage-ent.com/witches-server/Voltage/media/" >> $APACHECONFIG
	echo "Alias /static/ /var/www/voltage-ent.com/witches-server/Voltage/static/" >> $APACHECONFIG
	echo "<Directory /var/www/voltage-ent.com/witches-server/Voltage/static>" >> $APACHECONFIG
	echo "Require all granted" >> $APACHECONFIG
	echo "</Directory>" >> $APACHECONFIG
	echo "<Directory /var/www/voltage-ent.com/witches-server/Voltage/media>" >> $APACHECONFIG
	echo "Require all granted" >> $APACHECONFIG
	echo "</Directory>" >> $APACHECONFIG

	echo "-LOG- Apache config created for Kisses & Curses"

else
	echo "-LOG- found Apache config for Kisses & Curses"

fi
