#!/usr/bin/env bash
set -o errexit

# if [ $# -ne 1 ]; then
#     echo "Syntax: $0 [archive|restore]"
#     exit 1
# fi

# COMMAND=$1
ARCHIVE_NAME=scripts.zip

SCRIPT_ASSETS="Assets/StreamingAssets/Story/Scenes Assets/Resources/JSON/STORY/masterData.json Assets/Resources/JSON/STORY/sceneManifest.json"

# if [ $COMMAND == "restore" ]; then
#     # remove previous scripts
#     rm -rf witches-client/Assets/StreamingAssets/Story/Scenes
#     # unzip the scripts and config files -- overwrite the existing config files
#     unzip -o -d witches-client ${ARCHIVE_NAME}
# else
pushd witches-client
BUILD_ENV=staging make -f remoteMakefile archiveScripts
scp builder2@172.16.100.203:Repos/witches-client-staging/Build/scripts.zip ${ARCHIVE_NAME}
popd
mv witches-client/${ARCHIVE_NAME} .



