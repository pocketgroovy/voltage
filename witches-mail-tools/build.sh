#!/usr/bin/env bash
set -o errexit


REPO_SERVER=172.16.100.204

PROD=witches-admin-tools-production
STAGING=witches-admin-tools-staging
DEV=witches-admin-tools-dev

DEPLOY_BASE_DIR=/var/www/voltage-ent.com
DEPLOY_DIR_PROD=${DEPLOY_BASE_DIR}/${PROD}
DEPLOY_DIR_STAGING=${DEPLOY_BASE_DIR}/${STAGING}
DEPLOY_DIR_DEV=${DEPLOY_BASE_DIR}/${DEV}


if [ ! -d witches-mail-tools ]; then
        git clone git@${REPO_URL}:witches-mail-tools
fi
pushd witches-mail-tools

# remove local changes
git clean -d -f -q
git reset --hard
# retrieve the latest code
git checkout master
git pull origin master

 
# Copy
for dest in sysdev@tanuki:${DEPLOY_DIR_PROD} sysdev@tanuki:${DEPLOY_DIR_STAGING} sysdev@tanuki:${DEPLOY_DIR_DEV}; do
	rsync -a -c --delete --progress --exclude-from '../syncExclusions' . $dest/
done

popd


# Set the appropriate group on all the server files
ssh sysdev@tanuki << EOF
	find '${DEPLOY_DIR_PROD}' -user sysdev -exec chown :apache {} \;
	find '${DEPLOY_DIR_STAGING}' -user sysdev -exec chown :apache {} \;
	find '${DEPLOY_DIR_DEV}' -user sysdev -exec chown :apache {} \;
EOF


# Finally, Compile server & Reboot
ssh sysdev@tanuki << EOF
	${DEPLOY_DIR_PROD}/deploy.sh $PROD
	${DEPLOY_DIR_STAGING}/deploy.sh $STAGING
	${DEPLOY_DIR_DEV}/deploy.sh $DEV
EOF



