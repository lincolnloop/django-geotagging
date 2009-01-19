from django.contrib.gis import admin
from geotagging.models import Point
from geotagging.models import Line,MultiLine
from geotagging.models import Polygon
from geotagging.models import GeometryCollection

class PointAdmin(admin.GeoModelAdmin):
    list_filter = ('content_type','point' )
    list_display = ('object', 'point', 'content_type', 'object_id')


admin.site.register(Point, PointAdmin)
admin.site.register(Line, admin.GeoModelAdmin)
admin.site.register(MultiLine, admin.GeoModelAdmin)
admin.site.register(Polygon, admin.GeoModelAdmin)
admin.site.register(GeometryCollection, admin.GeoModelAdmin)
