--------------------------
GeoTagging app for Django
--------------------------

.. contents::

This reusable app enable you to geotag your objects. Let me developp a bit
what do I mean by geotag. You can associate a point, a line and a Polygon
to any objects defined by your other django application used by your project.
This reusable app comes with a convenient user interface that integrate this
feature in django admin interface.

Requirements
============

* GeoDjango_
* GeoIP_

.. _GeoDjango: http://geodjango.org/docs/install.html#requirements
.. _GeoIP: http://www.maxmind.com/app/c

Installation
============

If you want to use this application  you can use the standalone project embded
in the repository. I would recommend to follow these steps :

* Create a virtual env ::

    virtualenv geotagging_env

* Move into that env ::

    cd geotagging_env

* Activate the env ::

    . bin/activate

* Install pip ::

    easy_install pip

* Use pip to grab django-geotagging ::

    pip install -e bzr+http://bazaar.launchpad.net/~yml/django-geotagging/geotags/#egg=django-geotags

* Create a postgis enabled db ::

    createdb -T template_postgis -U django_login geotagging_demo_db

* Download the following geoip datasets (City_, Country_) and copy them in `geotagging_demo_project/geoip_datasets/`. This can be done using this script::

    ./get_geoip_datasets.sh

* Install libgeoip ::

    sudo aptitude install geoip-bin

* Add google projection to your database, you can find the details about this procedure_ in geodjango documentation::

    $ ./manage shell
    >>> from django.contrib.gis.utils import add_postgis_srs
    >>> add_postgis_srs(900913)
* Overwrite the default GOOGLE_MAPS_API_KEY by setting it in a file called local_settings.py


.. _City: http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
.. _Country: http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz
.. _procedure: http://geodjango.org/docs/install.html#add-google-projection-to-spatial-ref-sys-table

Tests
=====

`geotags` reusable application can be tested by using the `geotagging_demo_project`.
In order to do so you need go inside the project directory ::

    $ cd geotagging_demo_project
    $ ./manage.py geotagging_tests

To Do
=====

* Increase the test coverage
* Template tags to make the usage of the maps easier.

.. _`geometry fields`: http://geodjango.org/docs/model-api.html#geometry-field-types
