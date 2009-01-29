from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings

from geotagging.views import add_edit_point
from geotagging.forms import PointForm
from geotagging.forms import LineForm
from geotagging.forms import PolygonForm
from geotagging.feeds import feed_dict

urlpatterns = patterns('',
    url(r'^geo_point/(?P<content_type_id>\d*)/(?P<object_id>\d*)/$',add_edit_point,
        {"form_class":PointForm,
         "template":"geotagging/add_edit_point.html"}
        , name="geotagging-add_edit_point"),
    url(r'^geo_line/(?P<content_type_id>\d*)/(?P<object_id>\d*)/$',add_edit_point,
        {"form_class":LineForm,
         "template":"geotagging/add_edit_point.html"}
        , name="geotagging-add_edit_line"),
    url(r'^geo_polygon/(?P<content_type_id>\d*)/(?P<object_id>\d*)/$',add_edit_point,
        {"form_class":PolygonForm,
         "template":"geotagging/add_edit_point.html"}
        , name="geotagging-add_edit_polygon"),

    # GeoRSS Feeds
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
     {'feed_dict': feed_dict}),
    # Feeds visualiser
    url(r'^point_feed_map/$', direct_to_template,
        {
            "template" : "geotagging/view_georss_feed.html",
            "extra_context" :
                {
                    "google_key" : settings.GOOGLE_MAPS_API_KEY,
                    "georss_feed" : "http://127.0.0.1:8000/geotagging/feeds/georss_point/",
                    #"georss_feed" : "http://api.flickr.com/services/feeds/geo/?g=322338@N20&lang=en-us&format=feed-georss",
                }
        })
)
