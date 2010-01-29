"""Handles registration of models in the geotagging registry"""


class AlreadyRegistered(Exception):
    """
    An attempt was made to register a model more than once.
    """
    pass


registry = []


def register(model, geotag_descriptor_attr='geotagging',
             geotagged_item_manager_attr='geotagged'):
    """
    Sets the given model class up for working with geotagging.
    """

    from geotagging.managers import ModelGeotaggedItemManager, GeotagDescriptor

    if model in registry:
        raise AlreadyRegistered("The model '%s' has already been "
            "registered." % model._meta.object_name)
    if hasattr(model, geotag_descriptor_attr):
        raise AttributeError("'%s' already has an attribute '%s'. You must "
            "provide a custom geotag_descriptor_attr to register." % (
                model._meta.object_name,
                tag_descriptor_attr,
            )
        )
    if hasattr(model, geotagged_item_manager_attr):
        raise AttributeError("'%s' already has an attribute '%s'. You must "
            "provide a custom geotagged_item_manager_attr to register." % (
                model._meta.object_name,
                geotagged_item_manager_attr,
            )
        )

    # Add tag descriptor
    setattr(model, tag_descriptor_attr, TagDescriptor())

    # Add custom manager
    ModelTaggedItemManager().contribute_to_class(model, tagged_item_manager_attr)

    # Finally register in registry
    registry.append(model)
