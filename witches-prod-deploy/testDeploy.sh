#!/usr/bin/env bash
set -x
set -o errexit

PROD_DB=172.16.110.35
# PROD1=10.114.239.77
# PROD2=10.114.239.120
# CACHE_SERVER=10.114.239.105
SERVER_REPO=172.16.100.204

DEPLOY_PATH=/var/www/voltage-ent.com/witches-server

JENKINS_URL=172.16.100.201:8080
STAGING_JOB=Kisses%20and%20Curses%20Staging

# Store the staging build number used for this build
curl -s "http://${JENKINS_URL}/job/${STAGING_JOB}/lastSuccessfulBuild/buildNumber" > stagingBuildNumber.txt

if [ -z "${from}" ] || [ -z "${to}" ] || [ -z "${future}" ]; then
    echo "Missing version migration parameters"
    exit 1
fi

# # Open VPN connection
# pgrep pppd || VPN_CLOSED=$?

# if [ -n ${VPN_CLOSED} ]; then
#     sudo pppd call softlayer
#     sleep 15
# fi

# # Shut down both servers
# ssh sysdev@${PROD1} "sudo /usr/sbin/service apache2 stop"
# ssh sysdev@${PROD2} "sudo /usr/sbin/service apache2 stop"
# echo "Web servers stopped"

# # Clear the cache
# RESULT=`ssh sysdev@${CACHE_SERVER} "redis-cli -h ${CACHE_SERVER} flushall"`
# echo "Cache cleared"

# # Update the database
# ./updateReferenceData.sh ${PREPROD_DB} ${PROD_DB}
# echo "Database Updated"

# Update the database version table
./updateVersions.sh ${PROD_DB}/witches ${from} ${to} ${future}
./updateAndroidEnvironments.sh ${PROD_DB}/witches ${from} ${to} ${future}

# Copy over the new server code
if [ ! -e witches-server ]; then
    git clone git@${SERVER_REPO}:witches-server
fi
pushd witches-server
git clean -d -f -q
git reset --hard

git pull
git reset --hard ${SERVER_COMMIT}
# Remove admin tool URLs
#./remove_admintools_url.sh Voltage/witches/urls_current.py Voltage/witches/urls_historical.py 

# rsync -a -c --delete --progress --exclude-from '../syncExclusions' . sysdev@${PROD1}:${DEPLOY_PATH}
# rsync -a -c --delete --progress --exclude-from '../syncExclusions' . sysdev@${PROD2}:${DEPLOY_PATH}

# ssh sysdev@${PROD1} "find '${DEPLOY_PATH}' -user sysdev -exec chown :www-data {} \;"
# ssh sysdev@${PROD2} "find '${DEPLOY_PATH}' -user sysdev -exec chown :www-data {} \;"
popd

export BUILD_ENV=production
# Start the servers
# ssh sysdev@${PROD1} "cd ${DEPLOY_PATH}; ./deploy.sh ${BUILD_ENV}"
# ssh sysdev@${PROD2} "cd ${DEPLOY_PATH}; ./deploy.sh ${BUILD_ENV}"
echo "Web servers restarted"
