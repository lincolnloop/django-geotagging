from django.contrib.gis.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from geotagging.utils.serialized_data_field.fields import SerializedDataField
from geotagging.signals import parse_data_file


class BaseGeoAbstractModel(models.Model):
    """
    An abstract base class that any custom generic geo models probably should
    subclass.
    """

    # Content-object field
    content_type   = models.ForeignKey(ContentType,
            related_name="content_type_set_for_%(class)s")
    object_pk      = models.TextField(_('object ID'))
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")
    data_file = models.FileField(upload_to="geo_files")
    metadata = SerializedDataField(blank=True, editable=False)
    objects = models.GeoManager()

    class Meta:
        abstract = True

            
class GeoMultiLine(BaseGeoAbstractModel):
    """
    A multi-line implementation. Use the metadata field to store
    additional additional details about the geo object.
    Helper functions are provided that assume metadata is a list of
    dictionaries with any of the following keys:
    
    * time
    * elevation
    
    """
    multi_line = models.MultiLineStringField()

    def __unicode__(self):
        return 'GeoMultiLine for %s' % self.content_object
            
            
    def miles(self):
        t = GeoMultiLine.objects.length().get(pk=self.pk)
        return t.length.mi

    def intersecting_lines(self):
        return GeoMultiLine.objects.filter(
                    multi_line__intersects=self.multi_line).exclude(pk=self.pk)
        
    @property
    def elevations(self):   
        try:
            return [d['ele'] for d in self.metadata]
        except KeyError:
            return None
            
    def max_elevation(self):
        if self.elevations:
            self.elevations.sort()
            return e[-1]
        else:
            return None
            
    def min_elevation(self):
        if self.elevations:
            self.elevations.sort()
            return e[0]
        else:
            return None
            

models.signals.pre_save.connect(parse_data_file, sender=GeoMultiLine)