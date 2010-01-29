from django.contrib.gis.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class GeotagManager(models.GeoManager):
    def get_for_object(self, obj):
        """
        Returns the Geotag associated with the given object or None.
        """
        ctype = ContentType.objects.get_for_model(obj)
        try:
            return self.get(content_type=ctype, object_id=obj.pk)
        except ObjectDoesNotExist:
            pass
        return None
        
    def update_geotag(self, obj, geotag):
        """
        Updates the geotag associated with an object
        """
        geotag_obj = self.get_for_object(obj)
        if not geotag_obj and not geotag:
            return
        if not geotag_obj:
            ctype = ContentType.objects.get_for_model(obj)
            geotag_obj = self.create(content_type=ctype, object_id=obj.pk)
        if not geotag:
                geotag_obj.delete()
        else:
            old_geotag_geom = geotag_obj.get_geom()
            if old_geotag_geom:
                old_field_name = old_geotag_geom.geom_type.lower()
                setattr(geotag_obj, old_field_name, None)
            field_name = geotag.geom_type.lower()
            setattr(geotag_obj, field_name, geotag)
            geotag_obj.save()
        
        

class Geotag(models.Model):
    """
    A simple wrapper around the GeoDjango field types
    """

    # Content-object field
    content_type   = models.ForeignKey(ContentType,
            related_name="content_type_set_for_%(class)s")
    object_id      = models.PositiveIntegerField(_('object ID'),max_length=50)
    object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_id")
    
    point = models.PointField(verbose_name=_("point"), blank=True, null=True)
    multilinestring = models.MultiLineStringField(blank=True, null=True)
    line = models.LineStringField(blank=True, null=True)
    polygon = models.PolygonField(blank=True, null=True)
    geometry_collection = models.GeometryCollectionField(verbose_name=_("geometry collection"), blank=True, null=True)
    
    objects = GeotagManager()
    
    def get_geom(self):
        for geom_type in ('point', 'line', 'multilinestring', 
                          'polygon', 'geometry_collection'):
            geom = getattr(self, geom_type)
            if geom:
                return geom
        return None

