from django.contrib.gis.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class Geotag(models.Model):
    """
    An abstract base class that any custom generic geo models probably should
    subclass.
    """

    # Content-object field
    content_type   = models.ForeignKey(ContentType,
            related_name="content_type_set_for_%(class)s")
    object_id      = models.PositiveIntegerField(_('object ID'),max_length=50)
    object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_id")
    
    point = models.PointField(verbose_name=_("point"), blank=True, null=True)
    multi_line = models.MultiLineStringField(blank=True, null=True)
    line = models.LineStringField(blank=True, null=True)
    polygon = models.PolygonField(blank=True, null=True)
    geometry_collection = models.GeometryCollectionField(verbose_name=_("geometry collection"), blank=True, null=True)
    
    objects = models.GeoManager()

