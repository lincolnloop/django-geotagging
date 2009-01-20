from django.contrib.gis import admin
from geotagging.models import Point, Line, Polygon
from geotagging.models import Line,MultiLine
from geotagging.models import Polygon
from geotagging.models import GeometryCollection

class PointAdmin(admin.OSMGeoAdmin):
    list_filter = ('content_type','point' )
    list_display = ('object', 'point', 'content_type', 'object_id')

class LineAdmin(admin.OSMGeoAdmin):
    list_filter = ('content_type','line' )
    list_display = ('object', 'line', 'content_type', 'object_id')

class PolygonAdmin(admin.OSMGeoAdmin):
    list_filter = ('content_type','polygon' )
    list_display = ('object', 'polygon', 'content_type', 'object_id')

admin.site.register(Point, PointAdmin)
admin.site.register(Line, LineAdmin)
admin.site.register(Polygon, PolygonAdmin)
admin.site.register(MultiLine, admin.GeoModelAdmin)
admin.site.register(GeometryCollection, admin.GeoModelAdmin)
