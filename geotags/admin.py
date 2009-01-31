from django.contrib.gis import admin
from django.contrib.gis.maps.google import GoogleMap
from django.conf import settings

from geotags.models import Point, Line, Polygon
from geotags.models import Line,MultiLine
from geotags.models import Polygon
from geotags.models import GeometryCollection

GMAP = GoogleMap(key=settings.GOOGLE_MAPS_API_KEY)

class PointAdmin(admin.OSMGeoAdmin):
    extra_js = [GMAP.api_url + GMAP.key]
    map_template = 'gis/admin/google.html'
    list_filter = ('content_type','point' )
    list_display = ('object', 'point', 'content_type', 'object_id')

class LineAdmin(admin.OSMGeoAdmin):
    extra_js = [GMAP.api_url + GMAP.key]
    map_template = 'gis/admin/google.html'
    list_filter = ('content_type','line' )
    list_display = ('object', 'line', 'content_type', 'object_id')

class PolygonAdmin(admin.OSMGeoAdmin):
    extra_js = [GMAP.api_url + GMAP.key]
    map_template = 'gis/admin/google.html'
    list_filter = ('content_type','polygon' )
    list_display = ('object', 'polygon', 'content_type', 'object_id')

admin.site.register(Point, PointAdmin)
admin.site.register(Line, LineAdmin)
admin.site.register(Polygon, PolygonAdmin)
admin.site.register(MultiLine, admin.GeoModelAdmin)
admin.site.register(GeometryCollection, admin.GeoModelAdmin)
