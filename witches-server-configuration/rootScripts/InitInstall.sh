RSYNCINSTALLED=$(type rsync) > /dev/null
if [ -n "${RSYNCINSTALLED}" ]; then
 echo "-LOG- rsync is installed"
else
 echo "-LOG- rsync is not installed, installing now"
 	yum -y install rsync || NORSYNC=$?
	if [ ${NORSYNC} ]; then
	        echo "-LOG- ERROR on rsync installation"
	        exit 1
	fi
fi
