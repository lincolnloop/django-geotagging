--------------------------
GeoTagging app for Django
--------------------------

.. contents::

This reusable app enable you to geotag your objects. Let me develop a bit
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

What is django-geottaging
=========================

django-geotagging is the name of the project which is commposed of 3 building blocks that I am going to details :

geotags
  This is the django reusable app that allows you to geotags any object in
  the django database.

geotagging_demo_project
  This demo project gives you the possibility to use geotags directly after
  the installation.

geotagging_tests
  This is a django app that contains all the tests of geotags and also a
  `DummyModel` that you could use to experiment with geotags.

Installation
=============

In order to use django-geotagging, you will need to have a
functioning installation of Django 1.0 or newer and then follow
the instruction given in the file called `INSTALL.rst`.

Usage
=====

You can use this reusable application in at least 2 ways. You can start with
project embed  in the repository and extend it with other django apps or you
can put geotags inside your PYTHONPATH and add it into the INSTALLED_APP.
`INSTALL.rst`, inside the `docs` directory, explains how to install this app.
`TUTORIAL.rst` shows the capability of this reusable app. django-geotagging allows you to :

* associate in the `admin site`_ a Point, Line, Polygon to any object in your django project
* produce kml feed per geometry and per content type
* view these feeds on a map
* View the objects in your neighborhood

.. _`admin site`: http://docs.djangoproject.com/en/dev/ref/contrib/admin/#ref-contrib-admin

To Do
=====

* Increase the test coverage
* Template tags to make the usage of the maps easier.
* Geocoder requires jQuery. The implementation sould be transformed to pure js


Contribute to this project
==========================

You could contribute to this project in several ways : feedback, documentation,
translation, code and probably many more.

If needed you can contact me by mail : yann.malet@gmail.com
