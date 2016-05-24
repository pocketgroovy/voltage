SERVERGROUP=`cat /etc/*-release | grep NAME`

if [[ $SERVERGROUP == *"Ubuntu"* ]]; then
	echo "it's ubuntu"
	usermod -a -G www-data sysdev
elif [[ $SERVERGROUP == *"CentOS"* ]]; then
	echo "it's CentOS"
	usermod -a -G apache sysdev
fi
