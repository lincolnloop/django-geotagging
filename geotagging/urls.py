from django.conf.urls.defaults import *

from geotagging.views import kml_feed, kml_feed_map, kml_feeds_map
from geotagging.views import neighborhood_monitoring, kml_neighborhood_feed


urlpatterns = patterns('',

    # KML feeds
    url(r'^kml_feed/(?P<geotag_field_name>point|line|polygon)/$',kml_feed,
        name="geotagging-kml_feed"),
    url(r'^kml_feed/(?P<geotag_field_name>point|line|polygon)/(?P<content_type_name>[a-z ]+)/$',
        kml_feed,
        name="geotagging-kml_feed_per_contenttype"),

    # KML Feeds visualiser
    url(r'^kml_feeds_map/all/$', kml_feeds_map,
        name="geotagging-kml_feeds_map"),
    url(r'^kml_feeds_map/all/(?P<content_type_name>[a-z]+)/$', kml_feeds_map,
        name="geotagging-kml_feeds_map_per_contenttype"),

    url(r'^kml_feed_map/(?P<geotag_field_name>[a-z]+)/$', kml_feed_map,
        name="geotagging-kml_feed_map"),
    url(r'^kml_feed_map/(?P<geotag_field_name>[a-z]+)/(?P<content_type_name>[a-z ]+)/$', kml_feed_map,
        name="geotagging-kml_feed_map_per_contenttype"),

    # neighborhood monitoring
    url(r'^neighborhood_monitoring/(?P<distance_lt_km>\d*)/$',
        neighborhood_monitoring,
        name="geotagging-neighborhood_monitoring"),
    url(r'^kml_neighborhood_feed/(?P<distance_lt_km>\d*)/$',
        kml_neighborhood_feed,
        name="geotagging-kml_neighborhood_feed"),
)
