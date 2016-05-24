#!/usr/bin/env bash
set -o errexit
######################################################################################################
###### This script is responsible for creating apache config file for app "Kisses and Curses"   ###### 
######################################################################################################


APACHECONFIG=/etc/httpd/conf.d/witches-kpi.conf

if [ ! -e $APACHECONFIG ]; then
	echo "WSGIScriptAlias / /var/www/voltage-ent.com/witches-KPI/witches/wsgi.py" >  $APACHECONFIG
	echo "WSGIPythonPath /var/www/voltage-ent.com/witches-KPI/" >> $APACHECONFIG
	echo "<Directory /var/www/voltage-ent.com/witches-KPI/witches>" >> $APACHECONFIG
	echo "<Files wsgi.py>" >> $APACHECONFIG
	echo "Order deny,allow" >> $APACHECONFIG
	echo "Require all granted" >> $APACHECONFIG
	echo "</Files>" >> $APACHECONFIG
	echo "</Directory>" >> $APACHECONFIG
	echo "" >> $APACHECONFIG
	echo "<Location /witcheskpi>" >> $APACHECONFIG
	echo "AuthType Basic" >> $APACHECONFIG
	echo "AuthName \"Restricted Files\"" >> $APACHECONFIG
	echo "AuthUserFile /var/www/voltage-ent.com/passwd/passwords" >> $APACHECONFIG
	echo "Require valid-user" >> $APACHECONFIG
	echo "</Location>" >> $APACHECONFIG
	echo "Alias /static/ /var/www/voltage-ent.com/witches-KPI/static/" >> $APACHECONFIG
	echo "<Directory /var/www/voltage-ent.com/witches-KPI/static>" >> $APACHECONFIG
	echo "Require all granted" >> $APACHECONFIG
	echo "</Directory>" >> $APACHECONFIG

	echo "-LOG- Apache config created for Kisses & Curses"

else
	echo "-LOG- found Apache config for Kisses & Curses"

fi
