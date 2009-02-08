--------
Tutorial
--------

.. contents::

After reading this page you should be able to use `geotags` in the context of
your project. For practical reason I will use `geotagging_demo_project`  as
example. The installation of this project is explained in the documentation
`INSTALL.rst`.

Geotag contents
---------------

`geotags` come with and handy customization of admin site, it allows you to
add edit your geotags directly with in the admin interface.

When you edit any object with in the django database you will see 3 buttons in
the top right corner. They allow you to associate a Point, a Line, a Polygon to
this object:

.. image:: _images/geotags_buttons.png

.. Note:: The geocoder will work only if you use django-grappelli_. It requires jQuery.

.. _django-grappelli: http://code.google.com/p/django-grappelli/

Point
=====

You will find below a screen shot of the interface to add or edit a point :

.. image:: _images/add_point.png


KML feeds and maps
------------------

`geotags` comes with 2 ways to consume the geometries you have associated to your
django objects::

* maps
* kml feeds

You have 2 types of URL patterns to select what you want to see :

points, lines and polygons
  URL : http://127.0.0.1:8000/geotagging/kml_feeds_map/all/

.. image:: _images/kml_feeds_map_all.png

points or lines or polygons
  URL : http://127.0.0.1:8000/geotagging/kml_feed_map/point/

.. image:: _images/kml_feed_map_point.png
.. Note:: You can replace point by line or polygon

points or lines or polygons for a particular content type
  URL : "http://127.0.0.1:8000/geotagging/kml_feed_map/point/dummy model/"
  You can add the name of the content type you want to work on.


Neighborhood monitoring
-----------------------
`geotags` come also with the capability to presents to your user the objects
that have been geotags in their neighborhood.

* URL : http://127.0.0.1:8000/geotagging/neighborhood_monitoring/10/

The last bit in the url, the integer, represents the radius in km around you
you are interested in.

.. image:: _images/neighborhood_monitoring.png
