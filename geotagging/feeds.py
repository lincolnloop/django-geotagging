from django.contrib.gis import feeds

from geotagging.models import Point

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


feed_dict = {
    "georss_point" : GeorssPoint,
}
