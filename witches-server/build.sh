#!/usr/bin/env bash
set -o errexit

DEPLOY_DIR=/var/www/voltage-ent.com/witches-server

echo "Deploying Dev Server..."
REZAKATANA=172.16.100.205
ssh deployment@${REZAKATANA} "cd ${DEPLOY_DIR}; sg www-data 'git pull' && ./deploy.sh dev"


# update admin tool, for modifying database
echo "Deploying Admin Tool..."
ADMIN_SERVER=172.16.110.35
ssh sysdev@${ADMIN_SERVER}  "cd ${DEPLOY_DIR}; sg www-data 'git pull' && ./deploy.sh admin"


