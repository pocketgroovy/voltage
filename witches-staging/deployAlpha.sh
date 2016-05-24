#!/usr/bin/env bash
#####################################################################################################
# This script is responsible for deploying the staging build to our external alpha testing channels #
#####################################################################################################


set -o errexit # immediately exit on any error
set -x

GAME_NAME=$1
AMAZON_GAME_NAME=AMAZON_${GAME_NAME}
PACKAGE_NAME=com.voltage.curse.en
JENKINS_JOB_PATH=/var/lib/jenkins/jobs
PROJECT=Kisses\ and\ Curses\ Staging
CLIENT=WitchesClient
BUILD_PATH=${JENKINS_JOB_PATH}/${PROJECT}/workspace/${CLIENT}/Build

PROD_DB=10.114.239.105

# unfortunately, apple transporter requires username/password as arguments
APPLE_USER=deploy@voltage-ent.com
APPLE_PASS=${APPLE_PASSWORD} 
APPLE_APP_ID=962414762


AMAZON_USER=VM1DHQJMEFO4LB9
AMAZON_HOST=dar.amazon-digital-ftp.com
AMAZON_CONNECTION_STRING=${AMAZON_USER}@${AMAZON_HOST}
AMAZON_DEPOY_NAME=${AMAZON_VERSION_ID}-${AMAZON_GAME_NAME}

# Uploads of Mac/iOS apps are only supported on OSX, so builder2 must perform the action
BUILDER=172.16.100.203
BUILDER_USER=builder2
BUILDER_DEPLOY_IPA_PATH='${HOME}'/Desktop/deploy_IPA    # working directory on builder2



to_google()
{
    echo "Deploying to Google Play Developer Console..."

    OBB_PATH=`ls "${BUILD_PATH}"/*.obb`       # WARNING: can find multiple OBB files

    if [ -n "${OBB_PATH}" ]; then 
        ./publishToGooglePlay.py ${PACKAGE_NAME} "${BUILD_PATH}/${GAME_NAME}.apk" --main "${OBB_PATH}"
    else 
        echo "No obb file found"
        exit 1
    fi
}

to_iTunes()
{
    echo "Deploying to iTunes Connect..."

    # copy staging ipa to builder2, which technically has a local copy but wanted to follow data flow and avoid any sync issues
    ssh "${BUILDER_USER}@${BUILDER}" mkdir -p "${BUILDER_DEPLOY_IPA_PATH}"
    scp -p "${BUILD_PATH}/${GAME_NAME}.ipa" "${BUILDER_USER}@${BUILDER}:${BUILDER_DEPLOY_IPA_PATH}"

    # have builder2 run publishToApple.sh
    ssh ${BUILDER_USER}@${BUILDER} 'bash -s' < publishToApple.sh ${APPLE_USER} ${APPLE_PASS} ${APPLE_APP_ID} "${BUILDER_DEPLOY_IPA_PATH}/${GAME_NAME}.ipa"  

    # unset APPLE_PASSWORD
}

to_amazon()
{
    # add version code to the file name to comply with Amazon requirement
    cp "${BUILD_PATH}/${AMAZON_GAME_NAME}.apk" "${BUILD_PATH}/${AMAZON_DEPOY_NAME}.apk"
    sshpass -p "RgSYg6L0Mm" scp "${BUILD_PATH}/${AMAZON_DEPOY_NAME}.apk" ${AMAZON_CONNECTION_STRING}:
}



echo "Deploying to Alpha Channels [${PACKAGE_NAME}]..."

if [ ! -d "${BUILD_PATH}" ]; then
    echo "Path:${BUILD_PATH}, not found"
    exit 1
fi  
echo "Path: ${BUILD_PATH}"


if [ "${DEPLOY_GOOGLE}" == false ] && [ "${DEPLOY_IOS}" == false ] && [ "${DEPLOY_AMAZON}" == false ]; then    # set by Jenkins
    echo "No deploy targets given"
    exit 1
fi

if [ "${DEPLOY_AMAZON}" == true ]; then
   to_amazon
fi

if [ "${DEPLOY_IOS}" == true ]; then
   to_iTunes
fi

if [ "${DEPLOY_GOOGLE}" == true ]; then
   to_google

    ### Database
    # Open VPN connection
    pgrep pppd || VPN_CLOSED=$?

    if [ -n ${VPN_CLOSED} ]; then
        sudo pppd call softlayer
        sleep 15
    fi

    # update obb path in db to reference GooglePlay [Android specific!]
    mongo ${PROD_DB}/witches --eval 'db.Environment.update({description:"s"},{$set:{obb_path:"GooglePlay"}},{multi:true});'
fi

