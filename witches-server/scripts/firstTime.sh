#!/usr/bin/env bash

ENVIRONMENT_HOME=deps

if [ ! -d deps ]; then
    echo "Creating initial configuration..."
    virtualenv ${ENVIRONMENT_HOME}
    cat ${ENVIRONMENT_HOME}/bin/activate | sed 's|PS1="(`basename.*|PS1=(witches)$PS1|' > ${ENVIRONMENT_HOME}/bin/myActivate
    mv ${ENVIRONMENT_HOME}/bin/myActivate ${ENVIRONMENT_HOME}/bin/activate
    source ${ENVIRONMENT_HOME}/bin/activate
    pip install -r requirements.txt
else
    echo "Project already configured"
fi
