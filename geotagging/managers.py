"""
Custom managers for Django models registered with the geotagging
application.
"""
from django.db import models

from geotagging.models import Geotag

class ModelGeotagManager(models.Manager):
    """
    A manager for retrieving tags for a particular model.
    """
    # TODO: when does this actually get called and what should be here?
    pass


class GeotagDescriptor(object):
    """
    A descriptor which provides access to a ``ModelGeotagManager`` for
    model classes and simple retrieval, updating and deletion of tags
    for model instances.
    """
    def __get__(self, instance, owner):
        if not instance:
            tag_manager = ModelGeotagManager()
            tag_manager.model = owner
            return tag_manager
        else:
            return Geotag.objects.get_for_object(instance)

    def __set__(self, instance, value):
        Geotag.objects.update_geotag(instance, value)

    def __delete__(self, instance):
        Geotag.objects.update_geotag(instance, None)
