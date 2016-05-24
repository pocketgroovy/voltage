#!/usr/bin/env bash
set -o errexit
#######################################################################
###### Modify  CollectD	Setting					 				 ######
#######################################################################

SERVER_NAME=$1
PORT=$2

if [ $# -ne 2 ]; then
    echo "usage: $0 <server_name> <port>"
    exit 1
fi


SERVERGROUP=`cat /etc/*-release | grep NAME`

if [[ $SERVERGROUP == *"Ubuntu"* ]]; then 
	CONFIG_FILE=/etc/collectd/collectd.conf

elif [[ $SERVERGROUP == *"CentOS"* ]]; then
	CONFIG_FILE=/opt/collectd/etc/collectd.conf
fi


echo "modifying collectd setting"
if [ -e $CONFIG_FILE ]; then
	echo "Interval   1" >> $CONFIG_FILE
	echo "" >> $CONFIG_FILE
	echo "Hostname \"$SERVER_NAME\"" >> $CONFIG_FILE
	echo "LoadPlugin write_graphite" >>  $CONFIG_FILE
	echo "LoadPlugin tcpconns" >> $CONFIG_FILE
	echo "" >> $CONFIG_FILE
	echo "LoadPlugin aggregation" >> $CONFIG_FILE
	echo "" >> $CONFIG_FILE
	echo "<Plugin aggregation>" >> $CONFIG_FILE
	echo "<Aggregation>" >> $CONFIG_FILE
	echo "Plugin \"cpu\"" >> $CONFIG_FILE
	echo "Type \"cpu\"" >> $CONFIG_FILE
	echo "SetPlugin \"cpu\"" >> $CONFIG_FILE
	echo "SetPluginInstance \"%{aggregation}\"" >> $CONFIG_FILE
	echo "GroupBy \"Host\"" >> $CONFIG_FILE
	echo "GroupBy \"TypeInstance\"" >> $CONFIG_FILE
	echo "CalculateNum false" >> $CONFIG_FILE
	echo "CalculateSum false" >> $CONFIG_FILE
	echo "CalculateAverage true" >> $CONFIG_FILE
	echo "CalculateMinimum false" >> $CONFIG_FILE
	echo "CalculateMaximum false" >> $CONFIG_FILE
	echo "CalculateStddev false" >> $CONFIG_FILE
	echo "</Aggregation>" >> $CONFIG_FILE
	echo "</Plugin>" >> $CONFIG_FILE
	echo "" >> $CONFIG_FILE
	echo "" >> $CONFIG_FILE
	echo "<Plugin write_graphite>" >> $CONFIG_FILE
	echo "<Node \"${SERVER_NAME}\">" >> $CONFIG_FILE
	echo "Host \"10.1.3.54\"" >> $CONFIG_FILE
	echo "Port \"${PORT}\"" >> $CONFIG_FILE
	echo "Prefix \"collectd.\"" >> $CONFIG_FILE
	echo "Protocol \"tcp\"" >> $CONFIG_FILE
	echo "StoreRates true" >> $CONFIG_FILE
	echo "AlwaysAppendDS false" >> $CONFIG_FILE
	echo "EscapeCharacter \"_\"" >> $CONFIG_FILE
	echo "</Node>" >> $CONFIG_FILE
	echo "</Plugin>" >> $CONFIG_FILE

	echo "-LOG- CollectD config modified successfully"

else
	echo "-LOG- No config file found: CollecD might have not be installed correctly"

fi