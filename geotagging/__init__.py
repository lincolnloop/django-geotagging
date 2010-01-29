"""Handles registration of models in the geotagging registry"""


class AlreadyRegistered(Exception):
    """
    An attempt was made to register a model more than once.
    """
    pass


registry = []


def register(model, geotag_descriptor_attr='geotag'):
    """
    Sets the given model class up for working with geotagging.
    """

    from geotagging.managers import GeotagDescriptor

    if model in registry:
        raise AlreadyRegistered("The model '%s' has already been "
            "registered." % model._meta.object_name)
    if hasattr(model, geotag_descriptor_attr):
        raise AttributeError("'%s' already has an attribute '%s'. You must "
            "provide a custom geotag_descriptor_attr to register." % (
                model._meta.object_name,
                geotag_descriptor_attr,
            )
        )

    # Add tag descriptor
    setattr(model, geotag_descriptor_attr, GeotagDescriptor())

    # Finally register in registry
    registry.append(model)

from django.contrib.auth.models import User
register(User)