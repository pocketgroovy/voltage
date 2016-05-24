#!/usr/bin/env bash
set -o errexit # immediately exit on any error

cd /etc/firewalld/services/

if [ ! -e mongo.xml ]; then
	touch mongo.xml
	MONGO_SERVICE=mongo.xml
	echo "<?xml version=\"1.0\" encoding=\"utf-8\"?>" >> $MONGO_SERVICE
	echo "<service>" >> $MONGO_SERVICE
	echo "<short>MONGO</short>" >> $MONGO_SERVICE
	echo "<description>" >> $MONGO_SERVICE
	echo "Mongo Database" >> $MONGO_SERVICE
	echo "</description>" >> $MONGO_SERVICE 
	echo "<port protocol=\"tcp\" port=\"27017\"/>" >> $MONGO_SERVICE
	echo "</service>" >> $MONGO_SERVICE
	echo "-LOG- mongo service xml created"
else
	echo "-LOG- mongo.xml already exists"

fi

if [ ! -e redis.xml ]; then
	touch redis.xml
	REDIS_SERVICE=redis.xml
	echo "<?xml version=\"1.0\" encoding=\"utf-8\"?>" >> $REDIS_SERVICE
	echo "<service>" >> $REDIS_SERVICE
	echo "<short>REDIS</short>" >> $REDIS_SERVICE
	echo "<description>" >> $REDIS_SERVICE
	echo "Redis Cache" >> $REDIS_SERVICE
	echo "</description>" >> $REDIS_SERVICE 
	echo "<port protocol=\"tcp\" port=\"6379\"/>" >> $REDIS_SERVICE
	echo "</service>" >> $REDIS_SERVICE
	echo "-LOG- redis service xml created"
else
	echo "-LOG- redis.xml already exists"
fi