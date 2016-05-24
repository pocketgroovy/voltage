#!/usr/bin/env bash
set -o errexit

DEPLOY_ENV=$1
# APACHE_GRP=${2:-www-data}
DEPLOY_DIR=/var/www/voltage-ent.com/witches-KPI

SERVERGROUP=`cat /etc/*-release | grep NAME`

if [[ $SERVERGROUP == *"Ubuntu"* ]]; then
    echo "it's ubuntu"
    APACHE_GRP="www-data"
elif [[ $SERVERGROUP == *"CentOS"* ]]; then
    echo "it's CentOS"
    APACHE_GRP="apache"
fi

echo "Group: ${APACHE_GRP}"
newgrp ${APACHE_GRP} << END
    set -o errexit # Also make sure to exit on error for this heredoc
    # Compile python scripts for this machine
    python -m compileall -q .

        # Reboot apache
    if [ "${APACHE_GRP}" == "apache" ]; then
        sudo systemctl restart httpd.service
        echo "Server Deploy [${DEPLOY_ENV}] Complete!"
    else
        sudo /usr/sbin/service apache2 restart
        echo "Server Deploy [${DEPLOY_ENV}] Complete!"
    fi

END

    if [ -d $DEPLOY_DIR/log ]; then
        chmod 775 $DEPLOY_DIR/log 
    fi
