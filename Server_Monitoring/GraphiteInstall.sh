#!/usr/bin/env bash
set -o errexit
#######################################################################
###### Install Graphite						 					 ######
#######################################################################


yum -y install httpd gcc gcc-c++ git pycairo mod_wsgi epel-release
yum -y install python-pip python-devel blas-devel lapack-devel libffi-devel

# Download and install Graphite
cd /usr/local/src
git clone https://github.com/graphite-project/graphite-web.git
git clone https://github.com/graphite-project/carbon.git
 
pip install -r /usr/local/src/graphite-web/requirements.txt  # might need to update cffi to 1.1.0
 
cd /usr/local/src/carbon/
python setup.py install
 
cd /usr/local/src/graphite-web/
python setup.py install
 echo ">>>>>> coping carbon.conf, storage-schemas.conf, storage-aggregation.conf, relay-rules.conf,  local_settings.py, graphite.wsgi, graphite.conf, copy carbon-* to /etc/init.d/"
cp /opt/graphite/conf/carbon.conf.example /opt/graphite/conf/carbon.conf
cp /opt/graphite/conf/storage-schemas.conf.example /opt/graphite/conf/storage-schemas.conf
cp /opt/graphite/conf/storage-aggregation.conf.example /opt/graphite/conf/storage-aggregation.conf
cp /opt/graphite/conf/relay-rules.conf.example /opt/graphite/conf/relay-rules.conf
cp /opt/graphite/webapp/graphite/local_settings.py.example /opt/graphite/webapp/graphite/local_settings.py
cp /opt/graphite/conf/graphite.wsgi.example /opt/graphite/conf/graphite.wsgi
cp /opt/graphite/examples/example-graphite-vhost.conf /etc/httpd/conf.d/graphite.conf
cp /usr/local/src/carbon/distro/redhat/init.d/carbon-* /etc/init.d/

echo ">>>>>> change mode carbon-*"
chmod +x /etc/init.d/carbon-*


sudo PYTHONPATH=/opt/graphite/webapp/ django-admin.py syncdb --settings=graphite.settings
#reply: "Yes" and enter
#user: admin
#passwd: voltage123
 
#import static files
sudo PYTHONPATH=/opt/graphite/webapp/ django-admin.py collectstatic --settings=graphite.settings
# reply "yes"
 
#set permission
sudo chown -R apache:apache /opt/graphite/storage/
sudo chown -R apache:apache /opt/graphite/static/
sudo chown -R apache:apache /opt/graphite/webapp/


mv graphite.conf /etc/httpd/conf.d



/opt/graphite/bin/carbon-cache.py start
