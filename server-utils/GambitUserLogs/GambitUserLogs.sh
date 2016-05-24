#!/usr/bin/env bash

LOG_DIR=~/server-utils/GambitUserLogs/server_logs
REMOTE_LOG_DIR=/var/log/httpd/error_log*
REMOTE_TEMP_FILE=/home/sysdev/UserLogs/user${Phone_Id}

WEB_SERVER_ONE=root@10.114.239.108

if [ ! -d ${LOG_DIR} ]; then
    mkdir ${LOG_DIR}
fi

scp ${WEB_SERVER_ONE}:${REMOTE_LOG_DIR} ${LOG_DIR}/
