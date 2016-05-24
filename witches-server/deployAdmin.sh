#!/usr/bin/env bash
set -o errexit

REPO_URL=172.16.100.204
ADMIN_SERVER=172.16.110.35
HOST_DIR=/var/www/voltage-ent.com/
DEPLOY_DIR=/var/www/voltage-ent.com/witches-server


echo "Deploying Admin Tool..."
if ( ssh sysdev@${ADMIN_SERVER} "cd ${HOST_DIR}; [ ! -d witches-server ]" ); then
	ssh sysdev@${ADMIN_SERVER} "cd ${HOST_DIR}; sg apache 'git clone git@${REPO_URL}:witches-server'"
fi
ssh sysdev@${ADMIN_SERVER}  "cd ${DEPLOY_DIR}; sg apache 'git pull origin dev' && ./deploy.sh admin"      # git checkout dev
