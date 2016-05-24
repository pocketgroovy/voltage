#!/usr/bin/env bash

###################################################################################################
###### This script is responsible for setting up django for "Kisses and Curses" 			 ######
###################################################################################################

pip install -r django_requirements.txt || DJANGOINSTALLED=$?

if [ ${DJANGOINSTALLED} ]; then
        echo "-LOG- ERROR on django requirements installation"
        exit 1
fi

