Generic GeoTagging app for Django.

Requirements
============

GeoDjango_

.. _GeoDjango: http://geodjango.org/docs/install.html#requirements

Installation
============

If you want to use test this application in its standalone project I would
recommend the following approach :
* Create a virtual env : virtualenv geotagging_env
* Move into that env :  cd geotagging_env
* Activate the env : . bin/activate
* Install pip : easy_install pip
* Use pip to grab django-geotagging : pip install -e bzr+http://bazaar.launchpad.net/~yml/django-geotagging/geotags/#egg=django-geotags
* Create a postgis enabled db : createdb -T template_postgis -U django_login geotagging_demo_db
* Download the following geoip datasets from and copy them in `geotagging_demo_project/geoip_datasets/` :
     - http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
     - http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz
* Install libgeoip : sudo aptitude install geoip-bin
* Add google projection : http://geodjango.org/docs/install.html#add-google-projection-to-spatial-ref-sys-table
     - $ ./manage shell
     - >>> from django.contrib.gis.utils import add_postgis_srs
     - >>> add_postgis_srs(900913)

To Do
=====

* Tests
* Template tags to make the usage of the maps easier.

.. _`geometry fields`: http://geodjango.org/docs/model-api.html#geometry-field-types
