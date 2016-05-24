#!/usr/bin/env bash
set -x
set -o errexit

if [ $# != 1 ] ; then
    echo "Missing version parameter to be removed"
    exit 1
fi

  
DB=10.114.239.105
VERSION=$1

mongo ${DB}/witches --eval "var version='${VERSION}'" removePrevAndroidVersion.js