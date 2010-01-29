Django Geotagging
=================

This application is designed to store and query geographic information on any
model in your Django project. It is still under development, use at your own
risk.

Installation
------------

Via ``pip``::
    ``pip install -e git+git://github.com:lincolnloop/django-geotagging.git@inline-widget#egg=django-geotagging``

The old fashioned way::
    1. Download repo http://github.com/lincolnloop/django-geotagging/tarball/inline-widget
    2. Unpack and ``cd django_geotagging``
    3. ``python setup.py install``


Configuration
-------------

Add ``'geotagging'`` to your ``INSTALLED_APPS``.

Optional
^^^^^^^^

Register your models with geotagging to add a ``geotag`` attribute to the model
instances::

    import geotagging

    class MyModel(models.Model):
        ...
    geotagging.register(MyModel)

Add the geotag widget to your admin::

    from geotagging.admin.options import GeotagsInline

    class MyModelAdmin(admin.ModelAdmin):
        ...
        inlines = [GeotagsInline]

Usage
-----

See how it is used in the ``tests`` directory for now.


To Do
-----

* Lots of clean-up and further testing
* Plug in some views
