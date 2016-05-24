#!/usr/bin/env bash
set -o errexit # immediately exit on any error

cd /etc/firewalld/services/

if [ ! -e witchesKPI.xml ]; then
	touch witchesKPI.xml
	KPI_SERVICE=witchesKPI.xml
	echo "<?xml version=\"1.0\" encoding=\"utf-8\"?>" >> $KPI_SERVICE
	echo "<service>" >> $KPI_SERVICE
	echo "<short>WITCHES_KPI</short>" >> $KPI_SERVICE
	echo "<description>" >> $KPI_SERVICE
	echo "Witches KPI" >> $KPI_SERVICE
	echo "</description>" >> $KPI_SERVICE 
	echo "<port protocol=\"tcp\" port=\"8100\"/>" >> $KPI_SERVICE
	echo "</service>" >> $KPI_SERVICE
	echo "-LOG- witchesKPI service xml created"
else
	echo "-LOG- witchesKPI.xml already exists"

fi