from django.conf.urls.defaults import *
from geotagging.views import add_edit_point
from geotagging.forms import PointForm
from geotagging.forms import LineForm
from geotagging.forms import PolygonForm

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
)
