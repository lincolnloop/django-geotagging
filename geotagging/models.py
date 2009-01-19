from django.contrib.gis.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class BaseAbstractModel(models.Model):
    """
    An abstract base class that any custom generic geo models probably should
    subclass.
    """

    # Content-object field
    content_type   = models.ForeignKey(ContentType,
            related_name="content_type_set_for_%(class)s")
    object_id      = models.CharField(_('object ID'),max_length=50)
    object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_id")
    objects = models.GeoManager()

    class Meta:
        abstract = True


class MultiLine(BaseAbstractModel):
    """

    """
    multi_line = models.MultiLineStringField()

    def __unicode__(self):
        return 'MultiLine for %s' % self.object

class Line(BaseAbstractModel):
    """

    """
    multi_line = models.LineStringField()

    def __unicode__(self):
        return 'Line for %s' % self.object

class Polygon(BaseAbstractModel):
    """

    """
    polygon = models.PolygonField()

    def __unicode__(self):
        return 'polygon for %s' % self.object


class Point(BaseAbstractModel):
    """
    """
    point = models.PointField(verbose_name=_("point"),srid=4326)

    def __unicode__(self):
        return 'Point for %s' % self.object

class GeometryCollection(BaseAbstractModel):
    """
    """
    geometry_collection = models.GeometryCollectionField(verbose_name=_("gemometry collection"),srid=4326)
    class Meta:
        verbose_name_plural = "Geometry collections"


    def __unicode__(self):
        return 'Geometry collection for %s' % self.object
