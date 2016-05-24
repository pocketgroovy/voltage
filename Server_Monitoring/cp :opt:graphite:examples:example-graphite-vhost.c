cp /opt/graphite/examples/example-graphite-vhost.conf /etc/httpd/conf.d/graphite.conf 
cp /opt/graphite/conf/storage-schemas.conf.example /opt/graphite/conf/storage-schemas.conf 
cp /opt/graphite/conf/storage-aggregation.conf.example /opt/graphite/conf/storage-aggregation.conf cp /opt/graphite/conf/graphite.wsgi.example /opt/graphite/conf/graphite.wsgi 
cp /opt/graphite/conf/graphTemplates.conf.example /opt/graphite/conf/graphTemplates.conf 
cp /opt/graphite/conf/carbon.conf.example /opt/graphite/conf/carbon.conf



pip install "django-tagging<0.4"


PYTHONPATH=/opt/graphite/webapp/ /usr/lib/python2.7/site-packages/django/bin/django-admin.py syncdb --settings=graphite.settings