from django.contrib.gis import admin
from django.contrib.gis.maps.google import GoogleMap
from django.conf import settings

from geotags.models import Point, Line, Polygon
from geotags.models import Line,MultiLine
from geotags.models import Polygon
from geotags.models import GeometryCollection

GMAP = GoogleMap(key=settings.GOOGLE_MAPS_API_KEY)

class LinkToObjectMixin(object):
    """
    This Mixin add a column with a link to the object associated with the geom
    (point, line, polygon)
    """
    def link_to_object(self,obj):
        """
        Add a link to the related object
        """
        item = obj.object
        return u'<a href="../../%s/%s/%s/" title="Access in admin">%s</a>' % (\
                                   item.__class__._meta.app_label,
                                   item.__class__._meta.module_name,
                                   item.id,
                                   item)
    link_to_object.short_description = u'Object'
    link_to_object.allow_tags = True


class PointAdmin(admin.OSMGeoAdmin,LinkToObjectMixin):
    extra_js = [GMAP.api_url + GMAP.key]
    map_template = 'gis/admin/google.html'
    list_filter = ('content_type','point' )
    list_display = ('point', 'content_type', 'object_id','link_to_object')


class LineAdmin(admin.OSMGeoAdmin,LinkToObjectMixin):
    extra_js = [GMAP.api_url + GMAP.key]
    map_template = 'gis/admin/google.html'
    list_filter = ('content_type','line' )
    list_display = ('line', 'content_type', 'object_id','link_to_object')

class PolygonAdmin(admin.OSMGeoAdmin,LinkToObjectMixin):
    extra_js = [GMAP.api_url + GMAP.key]
    map_template = 'gis/admin/google.html'
    list_filter = ('content_type','polygon' )
    list_display = ('polygon', 'content_type', 'object_id','link_to_object')

admin.site.register(Point, PointAdmin)
admin.site.register(Line, LineAdmin)
admin.site.register(Polygon, PolygonAdmin)
admin.site.register(MultiLine, admin.GeoModelAdmin)
admin.site.register(GeometryCollection, admin.GeoModelAdmin)
