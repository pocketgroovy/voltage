#!/usr/bin/env bash

Phone_Id=$1

if [ $# -ne 1 ]; then
    echo "usage: $0 <phone id>"
    exit 1
fi


LOG_DIR=~/server-utils/WitchUserLogs/server_logs
REMOTE_LOG_DIR=/var/www/voltage-ent.com/witches-server/log/witches.log
REMOTE_TEMP_FILE=/home/sysdev/UserLogs/user${Phone_Id}

WEB_SERVER_ONE=sysdev@10.114.239.77
WEB_SERVER_TWO=sysdev@10.114.239.121

if [ ! -d ${LOG_DIR} ]; then
    mkdir ${LOG_DIR}
fi

echo "getting log info from witch prod1"
ssh ${WEB_SERVER_ONE} "cat ${REMOTE_LOG_DIR} | grep '$Phone_Id' > ${REMOTE_TEMP_FILE}.txt"
scp ${WEB_SERVER_ONE}:${REMOTE_TEMP_FILE}.txt ${LOG_DIR}/
ssh ${WEB_SERVER_ONE} "rm ${REMOTE_TEMP_FILE}.txt"


echo "getting log info from witch prod2"
ssh ${WEB_SERVER_TWO} "cat ${REMOTE_LOG_DIR} | grep '$Phone_Id' > ${REMOTE_TEMP_FILE}-2.txt"
scp ${WEB_SERVER_TWO}:${REMOTE_TEMP_FILE}-2.txt ${LOG_DIR}/
ssh ${WEB_SERVER_TWO} "rm ${REMOTE_TEMP_FILE}-2.txt"
