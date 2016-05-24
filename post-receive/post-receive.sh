#!/usr/bin/env bash

DEV_BRANCH=dev
STAGING_BRANCH=master
JENKINS_USER=jenkins

JENKINS_URL=172.16.100.201:8080
REPO_URL=172.16.100.204

# script arguments are read from from stdin rather than arguments, so need to use 'read'
# additionally, each push can contain multiple branches, so a loop is required
while read oldrev newrev refname
do
    branch=$(git rev-parse --symbolic --abbrev-ref $refname)
    if [ ${branch} == ${DEV_BRANCH} ]; then
        BUILD_DEV=1
    elif [ ${branch} == ${STAGING_BRANCH} ]; then
        BUILD_STAGING=1
    fi
done

if [ -n "${BUILD_DEV}" ]; then
    curl http://${JENKINS_URL}/git/notifyCommit -d url=${REPO_URL}:witches-server -d branches=${DEV_BRANCH}
fi

# The jenkins user can create merge commits when merging dev into master -- if we triggered a build on this commit,
# we'd go into a semi-infinite loop (or at least unnecessary builds)
if [ -n "${BUILD_STAGING}" ] && [ "${GL_USER}" != "${JENKINS_USER}" ]; then
    curl -X POST http://${JENKINS_URL}/job/Kisses%20and%20Curses%20Staging/build
fi
