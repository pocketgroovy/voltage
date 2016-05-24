#!/usr/bin/env bash

JENKINS_USER=jenkins

JENKINS_URL=172.16.100.201:8080
REPO_URL=172.16.100.204

curl http://${JENKINS_URL}/git/notifyCommit -d url=${REPO_URL}:witches-KPI

