#!/usr/bin/env bash
set -o errexit

###################################################################################################
###### This script is responsible for setting up a server for an app "Kisses and Curses" 	 ######
###################################################################################################

./scripts/InstallInitialTools.sh
./scripts/CreateApacheConfig.sh
./scripts/AddUserGroup.sh # apache or www-data group is added to sysdev.
./scripts/CreateDir.sh # directory in which witches-server will reside 
./scripts/GitInstall.sh
./scripts/PipInstall.sh
./scripts/ConfigSELinux.sh
./scripts/DjangoRequirementsInstall.sh
./scripts/PyCryptoInstall.sh
./scripts/StartServers.sh
