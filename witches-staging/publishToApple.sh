#!/usr/bin/env bash
set -o errexit

# use: ./publishToApple.sh username@itunesconnect.com password 1234567890 /some/path/to/app.ipa
# https://developer.apple.com/library/ios/documentation/LanguagesUtilities/Conceptual/iTunesConnect_Guide/Chapters/SubmittingTheApp.html
# https://help.apple.com/itc/transporteruserguide/?lang=en


# bare minimum guard clause
if [ $# -ne 4 ]; then
    echo "error! please provide correct arguments; arg count was $#"
    echo "Args are: $@"
    exit 1
fi

TRANSPORTER_DIR=/Applications/Xcode.app/Contents/Applications/Application\ Loader.app/Contents/itms/bin   
TRANSPORT_TYPE=DAV      # options are: DAV, Aspera, Signiant
TRANSPORT_LOG_TYPE=eXtreme    # off | informational | critical | detailed | eXtreme

USERNAME=$1
PASSWORD=$2

# the iTunes Connect App ID, NOT the bundle ID. should be ten digits (e.g., 1234567890)
# see iTunes Connect > Your App > 'App Store' > 'App Information' > 'Apple ID'
APP_ID=$3

IPA_FULLPATH=$4
IPA_DIR=$(dirname "${IPA_FULLPATH}")
IPA_FILE=$(basename "${IPA_FULLPATH}")
IPA_MD5=$(md5 -q "${IPA_FULLPATH}")
IPA_BYTE_SIZE=$(wc -c "${IPA_FULLPATH}" | awk '{print $1}')


# temporary directory for iTMS package
DEPLOY_DIR="${IPA_DIR}/itsmp"
ITMS_PACKAGE=$(basename ${IPA_FILE} .ipa).itmsp

# remove any prior deploy directories and create new
test -d "${DEPLOY_DIR}" && rm -rf "${DEPLOY_DIR}"
mkdir "${DEPLOY_DIR}"
mkdir "${DEPLOY_DIR}/${ITMS_PACKAGE}"

# create metadata.xml for iTMS (iTunes Music Store) package
# XPath /package/software_assets/asset/data_file/file_name", match regular expression "[^/: ]*"
cat <<EOM > ${DEPLOY_DIR}/${ITMS_PACKAGE}/metadata.xml
<?xml version="1.0" encoding="UTF-8"?>
<package version="software4.7" xmlns="http://apple.com/itunes/importer">
    <software_assets apple_id="${APP_ID}">
        <asset type="bundle">
            <data_file>
                <file_name>${IPA_FILE}</file_name>
                <checksum type="md5">${IPA_MD5}</checksum>
                <size>${IPA_BYTE_SIZE}</size>
            </data_file>
        </asset>
    </software_assets>
</package>
EOM
# change metadata.xml file access and modification times to that of the ipa
touch -r "${IPA_FULLPATH}" "${DEPLOY_DIR}/${ITMS_PACKAGE}/metadata.xml"

# copy ipa into the iTMS package 
cp -p "${IPA_FULLPATH}" "${DEPLOY_DIR}/${ITMS_PACKAGE}/"


echo "Deploying ${IPA_FILE} to Apple..."
# cat ${DEPLOY_DIR}/${ITMS_PACKAGE}/metadata.xml

# upload to App Store (must be from a mac, error ITMS-6000: "Uploads of Mac and iOS apps are only supported on OS X.")
"${TRANSPORTER_DIR}"/iTMSTransporter -m upload -f "${DEPLOY_DIR}" -u "${USERNAME}" -p "${PASSWORD}" -v ${TRANSPORT_LOG_TYPE} -t ${TRANSPORT_TYPE}



