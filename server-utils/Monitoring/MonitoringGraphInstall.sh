#!/usr/bin/env bash
set -o errexit
#######################################################################
###### Install Graphite						 					 ######
#######################################################################

yum -y update

yum -y install httpd gcc gcc-c++ git pycairo mod_wsgi epel-release
yum -y install python-pip python-devel blas-devel lapack-devel libffi-devel

# Download and install Graphite

GRAPHITE_WEB=/usr/local/src/graphite-web
CARBON=/usr/local/src/carbon

pushd /usr/local/src
if [ ! -e $GRAPHITE_WEB ]; then
	git clone https://github.com/graphite-project/graphite-web.git
fi
if [ ! -e $CARBON ]; then
	git clone https://github.com/graphite-project/carbon.git
fi
popd

pip install -r requirements.txt  # might need to update cffi to 1.1.0
 
pushd $CARBON
python setup.py install
popd


pushd $GRAPHITE_WEB
python setup.py install
popd 

 echo ">>>>>> copying carbon.conf, storage-schemas.conf, storage-aggregation.conf, relay-rules.conf, local_settings.py, graphite.wsgi, graphite.conf, carbon-* to /etc/init.d/"
cp /opt/graphite/conf/carbon.conf.example /opt/graphite/conf/carbon.conf
cp /opt/graphite/conf/storage-schemas.conf.example /opt/graphite/conf/storage-schemas.conf
cp /opt/graphite/conf/storage-aggregation.conf.example /opt/graphite/conf/storage-aggregation.conf
cp /opt/graphite/conf/relay-rules.conf.example /opt/graphite/conf/relay-rules.conf
cp /opt/graphite/webapp/graphite/local_settings.py.example /opt/graphite/webapp/graphite/local_settings.py
cp /opt/graphite/conf/graphite.wsgi.example /opt/graphite/conf/graphite.wsgi
cp /opt/graphite/examples/example-graphite-vhost.conf /etc/httpd/conf.d/graphite.conf
cp /usr/local/src/carbon/distro/redhat/init.d/carbon-* /etc/init.d/
echo ">>>>>> change ownership for carbon-*"
chmod +x /etc/init.d/carbon-*

chown -R apache:apache /opt/graphite/storage/


echo ">>>>>> Graphite Succesfully installed"

pushd /etc/init.d/
./carbon-cache start
popd


yum -y install https://grafanarel.s3.amazonaws.com/builds/grafana-2.6.0-1.x86_64.rpm

systemctl start grafana-server