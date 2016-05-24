#!/usr/bin/env bash
set -o errexit
#######################################################################
###### Install CollectD						 					 ######
#######################################################################

SERVER_NAME=$1
PORT=$2

if [ $# -ne 2 ]; then
    echo "usage: $0 <server_name> <port>"
    exit 1
fi


SERVERGROUP=`cat /etc/*-release | grep NAME`

if [[ $SERVERGROUP == *"Ubuntu"* ]]; then
    echo "it's ubuntu"
    apt-get update
    apt-get install -y collectd collectd-utils
    ./CollectDSettings.sh

    service collectd start
	service collectd status
elif [[ $SERVERGROUP == *"CentOS"* ]]; then
    echo "it's CentOS"
	# install collectD
	# As we will compile CollectD from source we need a compiler:
	yum install -y bzip2 wget
	yum install -y make automake gcc gcc-c++ kernel-devel perl-devel

	# Next we download CollectD 5.5.0:
	pushd /tmp/
	wget https://www.collectd.org/files/collectd-5.5.0.tar.bz2
	tar -jxf collectd-5.5.0.tar.bz2
	pushd collectd-5.5.0
	

	# Fedora compiler might yield warnings as error who look like this:
	#error: #warning “_BSD_SOURCE and _SVID_SOURCE are deprecated, use _DEFAULT_SOURCE” [-Werror=cpp]
	#So you have to disable warning as error first before you run ./configure

	export CFLAGS="-Wno-error"

	# Compile and install:
	./configure
	# for centos 6
	# ./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var --libdir=/usr/lib --mandir=/usr/share/man --enable-all-plugins
	# make
	make all install
	popd
	popd

	# Start CollectD on startup
	pushd /etc/systemd/system/
	wget https://raw.githubusercontent.com/martin-magakian/collectd-script/master/collectd.service
	chmod +x collectd.service
	popd

	~/CollectD/CollectDSettings.sh $SERVER_NAME $PORT

	systemctl start collectd.service
	systemctl status collectd.service

fi