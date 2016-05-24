#!/usr/bin/env bash

set -o errexit # immediately exit on any error

JENKINS_URL=172.16.100.201:8080
REPO_URL=172.16.100.204
WITCHES_CLIENT=WitchesClient
WITCHES_SERVER=WitchesServer
SERVER_PATH=/var/www/voltage-ent.com/witches-server
SCRIPT_ARCHIVE_NAME=scripts.zip
export BUILD_ENV=staging


BUILDER_ID=builder2
BUILD_SERVER=172.16.100.203

# Get Latest Client build #
CLIENT_BUILD_NUM=`curl -s "http://${JENKINS_URL}/job/${WITCHES_CLIENT}/lastSuccessfulBuild/buildNumber"`

# Get Latest Client build
CLIENT_HASH=`curl -s "http://${JENKINS_URL}/job/${WITCHES_CLIENT}/lastSuccessfulBuild/api/xml?xpath=/*/action/lastBuiltRevision/SHA1/text()"`

if [ ! -d witches-client ]; then
    git clone git@${REPO_URL}:witches-client
fi

# execute client build for localtest
pushd witches-client

# remove local changes
git clean -d -f -q
git reset --hard
# retrieve the latest code
git checkout master
git pull origin master
# ...but use the version that was in the last successful dev build
git reset --hard ${CLIENT_HASH}

# Prepare build
HASH=${CLIENT_HASH} make -f remoteMakefile prep

# Always try to fetch the latest scripts -- this isn't based on any successful version
make -f remoteMakefile scripts

# Kick off the actual client build
BUILD_NUMBER=${CLIENT_BUILD_NUM} make -f remoteMakefile
# Archive scripts
make -f remoteMakefile archiveScripts
popd

scp ${BUILDER_ID}@${BUILD_SERVER}:Repos/witches-client-staging/Build/scripts.zip scripts.zip

# Get Latest Server build
SERVER_HASH=`curl -s "http://${JENKINS_URL}/job/${WITCHES_SERVER}/lastSuccessfulBuild/api/xml?xpath=/*/action/lastBuiltRevision/SHA1/text()"`

# execute server build for localtest
if [ ! -d witches-server ]; then
	git clone git@${REPO_URL}:witches-server
fi
pushd witches-server

# remove local changes
git clean -d -f -q
git reset --hard
# retrieve the latest code
git checkout master
git pull origin master
# ...but use the version that was in the last successful dev build
git reset --hard ${SERVER_HASH}

# Copy
rsync -a -c --delete --progress --exclude-from '../syncExclusions' . sysdev@localtest:${SERVER_PATH}/

# Set the appropriate group on all the server files
ssh sysdev@localtest "find '${SERVER_PATH}' -user sysdev -exec chown :www-data {} \;"
popd

# deploy client to hockey kit
pushd witches-client
make -f remoteMakefile deploy
popd

# Finally, Compile server & Reboot
ssh sysdev@localtest "${SERVER_PATH}/deploy.sh"

echo ${CLIENT_HASH} > clientSHA
echo ${SERVER_HASH} > serverSHA

# save the build number
echo ${CLIENT_BUILD_NUM} > clientBuildNumber
