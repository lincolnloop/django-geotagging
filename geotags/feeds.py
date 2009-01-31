from django.contrib.gis import feeds

from geotags.models import Point, Line, Polygon

class GeorssPoint(feeds.Feed):
    link="/points/"
    title="GeoRSS feeds for the points"

    def items(self):
        return Point.objects.all()

    def item_link(self,item):
        return item.object.get_absolute_url()

    def geometry(self,obj):
        return Point.objects.extent()

    def item_geometry(self,item):
        return item.point.x, item.point.y

class GeorssLine(feeds.Feed):
    """
    The line is approximated by its first point this
    will make representing it easier with openlayers.
    """
    link="/points/"
    title="GeoRSS feeds for the line"

    def items(self):
        return Line.objects.all()

    def item_link(self,item):
        return item.object.get_absolute_url()

    def geometry(self,obj):
        return Line.objects.extent()

    def item_geometry(self,item):
        return item.line.x[0], item.line.y[0]


feed_dict = {
    "georss_point" : GeorssPoint,
    "georss_line" : GeorssLine,
}
