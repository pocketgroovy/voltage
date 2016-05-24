#!/usr/bin/env bash
set -o errexit


REPO_SERVER=172.16.100.204
DEPLOY_DIR=/var/www/voltage-ent.com/witches-server


# execute server build for dev
if [ ! -d witches-server ]; then
        git clone git@${REPO_URL}:witches-server
fi
pushd witches-server

# remove local changes
git clean -d -f -q
git reset --hard
# retrieve the latest code
git checkout dev
git pull origin dev


# Open VPN connection
pgrep pppd || VPN_CLOSED=$?

if [ -n ${VPN_CLOSED} ]; then
    sudo pppd call softlayer
    sleep 15
fi

# Copy
rsync -a -c --delete --progress --exclude-from '../syncExclusions' . sysdev@witchdev:${DEPLOY_DIR}/

# Set the appropriate group on all the server files
ssh sysdev@witchdev "find '${DEPLOY_DIR}' -user sysdev -exec chown :apache {} \;"
popd


# Finally, Compile server & Reboot
ssh sysdev@witchdev "${DEPLOY_DIR}/deploy.sh dev"


