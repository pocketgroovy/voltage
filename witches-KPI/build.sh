#!/usr/bin/env bash
set -o errexit


REPO_SERVER=172.16.100.204
DEPLOY_DIR=/var/www/voltage-ent.com/witches-KPI
SLAVE_DB=10.114.239.117
MASTER_DB=10.114.239.105
# execute server build for dev
if [ ! -d witches-KPI ]; then
        git clone git@${REPO_SERVER}:witches-KPI
fi
pushd witches-KPI

# remove local changes
git clean -d -f -q
git reset --hard
# retrieve the latest code
git checkout master
git pull origin master


# Open VPN connection
pgrep pppd || VPN_CLOSED=$?

if [ -n ${VPN_CLOSED} ]; then
    sudo pppd call softlayer
    sleep 15
fi

# Copy
rsync -a -c --delete --progress . sysdev@${MASTER_DB}:${DEPLOY_DIR}/

ssh sysdev@${MASTER_DB} "find '${DEPLOY_DIR}' -user sysdev -exec chown :apache {} \;"

popd


# Finally, Compile server & Reboot
ssh sysdev@${MASTER_DB} "${DEPLOY_DIR}/deploy.sh kpi"


