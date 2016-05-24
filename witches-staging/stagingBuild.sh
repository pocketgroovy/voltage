#!/usr/bin/env bash

set -o errexit # immediately exit on any error

DEV_BRANCH=dev
STAGING_BRANCH=master
REMOTE_NAME=origin

# temporary till SSH access is enabled
if [ "${GIT_PASSWORD}" != "" ]; then
    ROOT_REPO_PATH=https://${GIT_USER}:${GIT_PASSWORD}@github.com/VoltageEntertainment
else
    ROOT_REPO_PATH=https://${GIT_USER}@github.com/VoltageEntertainment
fi

CLIENT_REPO=WitchesClient
SERVER_REPO=witches-server
STORY_SCRIPTS_REPO=witches-scripts

# Database stuff
DEV_DB=10.122.146.120 # witchdev softlayer
STAGING_DB=10.91.91.254 # witchstage softlayer

mergeChanges()
{
    HASH=$1
    
    # Remove any local changes leftover from previous builds
    git clean -d -f -q
    git reset --hard

    # Start working on the actual staging branch in the event a merge is needed
    git checkout ${STAGING_BRANCH}
    # pull down all changes affecting either dev or staging
    git fetch ${REMOTE_NAME} ${DEV_BRANCH} ${STAGING_BRANCH}
    # apply the latest staging changes
    git pull ${REMOTE_NAME} ${STAGING_BRANCH}

    git merge -m "Promoted to Staging" ${HASH}
    git push ${REMOTE_NAME}
}

tagReleases()
{
    pushd ${CLIENT_REPO}
    VERSION=`cat Assets/Resources/buildNumber.txt | cut -d _ -f 1`
    
    newTag="v${VERSION}_${BUILD_NUMBER}"

    # Tag client
    git tag "${newTag}"
    git push origin "${newTag}"
    popd

    pushd ${SERVER_REPO}
    git tag "${newTag}"
    git push origin "${newTag}"
    popd

    pushd ${STORY_SCRIPTS_REPO}
    git tag "${newTag}"
    git push origin "${newTag}"
    popd
}

initRepos()
{
    if [ ! -d ${CLIENT_REPO} ]; then
    	git clone ${ROOT_REPO_PATH}/${CLIENT_REPO}.git
    fi

    if [ ! -d ${SERVER_REPO} ]; then
	   git clone ${ROOT_REPO_PATH}/${SERVER_REPO}.git
    fi

    if [ ! -d ${STORY_SCRIPTS_REPO} ]; then
	   git clone ${ROOT_REPO_PATH}/${STORY_SCRIPTS_REPO}.git
    fi
}

promoteToStaging()
{
    # Pull the latest Dev SHA for every repo we're going to promote.
    # We want to do this immediately to reduce the chance of one of these repos
    # receiving a commit in the middle of processing another
    CLIENT_HASH=`git ls-remote ${ROOT_REPO_PATH}/${CLIENT_REPO}.git refs/heads/${DEV_BRANCH} | cut -f 1`
    SERVER_HASH=`git ls-remote ${ROOT_REPO_PATH}/${SERVER_REPO}.git refs/heads/${DEV_BRANCH} | cut -f 1`
    STORY_HASH=`git ls-remote ${ROOT_REPO_PATH}/${STORY_SCRIPTS_REPO}.git refs/heads/${DEV_BRANCH} | cut -f 1`
    
    # # Handle Client first
    pushd ${CLIENT_REPO}
    mergeChanges ${CLIENT_HASH}
    popd

    # Handle Server
    pushd ${SERVER_REPO}
    mergeChanges ${SERVER_HASH}
    popd

    # Handle Scripts
    pushd ${STORY_SCRIPTS_REPO}
    mergeChanges ${STORY_HASH}
    popd
}



buildClient()
{
    pushd ${CLIENT_REPO}
    git checkout ${STAGING_BRANCH}
    make -f remoteMakefile prep
    make -f remoteMakefile scripts
    make -f remoteMakefile
    popd
}

deployClient()
{
    pushd ${CLIENT_REPO}
    make -f remoteMakefile deploy
    popd
}

STAGING_URL=sysdev@witchstage
SERVER_PATH=/var/www/voltage-ent.com/witches-server

deployServer()
{
    # Handle Server deployment
    pushd ${SERVER_REPO}
    git checkout ${STAGING_BRANCH}

    # Remove admin tool URLs
    ./remove_admintools_url.sh Voltage/witches/urls_current.py Voltage/witches/urls_historical.py

    # Open VPN connection
    pgrep pppd || VPN_CLOSED=$?

    if [ -n ${VPN_CLOSED} ]; then
	sudo pppd call softlayer
	# Hack...assumes any VPN connection will be safely opened in 15 seconds.
	# There is a way to turn this into a callback approach, but it involves extra configuration
	sleep 15
    fi

    # Copy
    rsync -a -c --delete --progress --exclude-from '../stagingExclusions' . ${STAGING_URL}:${SERVER_PATH}/

    # Set the appropriate group on all server files
    ssh ${STAGING_URL} "find '${SERVER_PATH}' -user sysdev -exec chown :apache {} \;"
    popd

    # Finally, Compile server & Reboot
    ssh sysdev@witchstage "${SERVER_PATH}/deploy.sh staging"
}

updateDatabase()
{
    ./updateReferenceData.sh ${DEV_DB} ${STAGING_DB}

    # update obb path in db to reference internal CDN [Android specific]
    mongo ${STAGING_DB}/witches --eval 'db.Environment.update({description:"s"},{$set:{obb_path:""}},{multi:true});'
}


initRepos

if [ "${IS_HOTFIX}" == false ]; then
    promoteToStaging
fi

tagReleases
buildClient
deployServer
updateDatabase
deployClient
