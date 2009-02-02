from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings

from geotags.views import add_edit_geotag,kml_feed, kml_feed_map, kml_feeds_map
from geotags.views import neighborhood_monitoring, kml_neighborhood_feed
from geotags.models import Line, Point, Polygon
from geotags.forms import PointForm
from geotags.forms import LineForm
from geotags.forms import PolygonForm
from geotags.feeds import feed_dict

urlpatterns = patterns('',
    url(r'^geo_point/(?P<content_type_id>\d*)/(?P<object_id>\d*)/$',add_edit_geotag,
        {"form_class":PointForm, "geotag_class":Point,
         "template":"geotags/add_edit_point.html"}
        , name="geotags-add_edit_point"),
    url(r'^geo_line/(?P<content_type_id>\d*)/(?P<object_id>\d*)/$',add_edit_geotag,
        {"form_class":LineForm,"geotag_class":Line,
         "template":"geotags/add_edit_point.html"}
        , name="geotags-add_edit_line"),
    url(r'^geo_polygon/(?P<content_type_id>\d*)/(?P<object_id>\d*)/$',add_edit_geotag,
        {"form_class":PolygonForm,"geotag_class":Polygon,
         "template":"geotags/add_edit_point.html"}
        , name="geotags-add_edit_polygon"),

    # KML feeds
    url(r'^kml_feed/(?P<geotag_class_name>[a-z]+)/$',kml_feed,
        name="geotags-kml_feed"),
    url(r'^kml_feed/(?P<geotag_class_name>[a-z]+)/(?P<content_type_name>[a-z]+)/$',kml_feed,
        name="geotags-kml_feed_per_contenttype"),

    # KML Feeds visualiser
    url(r'^kml_feeds_map/all/$', kml_feeds_map,
        name="geotags-kml_feeds_map"),
    url(r'^kml_feeds_map/all/(?P<content_type_name>[a-z]+)/$', kml_feeds_map,
        name="geotags-kml_feeds_map_per_contenttype"),

    url(r'^kml_feed_map/(?P<geotag_class_name>[a-z]+)/$', kml_feed_map,
        name="geotags-kml_feed_map"),
    url(r'^kml_feed_map/(?P<geotag_class_name>[a-z]+)/(?P<content_type_name>[a-z]+)/$', kml_feed_map,
        name="geotags-kml_feed_map_per_contenttype"),

    # neighborhood monitoring
    url(r'^neighborhood_monitoring/(?P<distance_lt_km>\d*)/$',
        neighborhood_monitoring,
        name="geotags-neighborhood_monitoring"),
    url(r'^kml_neighborhood_feed/(?P<distance_lt_km>\d*)/$',
        kml_neighborhood_feed,
        name="geotags-kml_neighborhood_feed"),
)
