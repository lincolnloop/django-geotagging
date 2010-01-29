from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.measure import D
from django.contrib.gis.shortcuts import render_to_kml
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.simple import direct_to_template


from geotagging.models import Geotag

def kml_feed(request, template="geotagging/geotagging.kml",
             geotag_field_name=None, content_type_name=None,
             object_id=None):
    """
    Return a KML feed of a particular geotag type : point, line, polygon
    This feed can be restricted by content_type and object_id.
    """
    if geotag_field_name:
        kw = str('%s__isnull' % geotag_field_name)
        geotagging = Geotag.objects.filter(**{kw:False})
    if content_type_name:
        geotagging = geotagging.objects.filter(content_type__name=content_type_name)
    if object_id:
        geotagging = geotagging.filter(object_id=object_id)
    context = RequestContext(request, {
        'places' : geotagging.kml(),
    })
    return render_to_kml(template,context_instance=context)

def kml_feed_map(request,template="geotagging/view_kml_feed.html",
                 geotag_field_name=None, content_type_name=None):
    """
    Direct the user to a template with all the required parameters to render
    the KML feed on a google map.
    """
    if content_type_name:
        kml_feed = reverse("geotagging-kml_feed_per_contenttype",
                           kwargs={
                            "geotag_field_name" : geotag_class_name,
                            "content_type_name" : content_type_name,
                            })
    else:
        kml_feed = reverse("geotagging-kml_feed",kwargs={"geotag_class_name":geotag_class_name})


    extra_context = {
        "kml_feed" : kml_feed
    }
    return direct_to_template(request,template=template,extra_context=extra_context)

def kml_feeds_map(request,template="geotagging/view_kml_feeds.html",
                 content_type_name=None):
    """
    Direct the user to a template with all the required parameters to render
    the KML feeds (point, line, polygon) on a google map.
    """
    if content_type_name:
        kml_feed_point = reverse("geotagging-kml_feed_per_contenttype",
                           kwargs={
                            "geotag_class_name" : "point",
                            "content_type_name" : content_type_name,
                            })
        kml_feed_line = reverse("geotagging-kml_feed_per_contenttype",
                           kwargs={
                            "geotag_class_name" : "line",
                            "content_type_name" : content_type_name,
                            })
        kml_feed_polygon = reverse("geotagging-kml_feed_per_contenttype",
                           kwargs={
                            "geotag_class_name" : "polygon",
                            "content_type_name" : content_type_name,
                            })
    else:
        kml_feed_point = reverse("geotagging-kml_feed",kwargs={"geotag_class_name": "point"})
        kml_feed_line = reverse("geotagging-kml_feed",kwargs={"geotag_class_name": "line"})
        kml_feed_polygon = reverse("geotagging-kml_feed",kwargs={"geotag_class_name": "polygon"})


    extra_context = {
        "kml_feed_point" : kml_feed_point,
        "kml_feed_line" : kml_feed_line,
        "kml_feed_polygon" : kml_feed_polygon
    }
    return direct_to_template(request,template=template,extra_context=extra_context)



def kml_neighborhood_feed(request, template="geotagging/geotagging.kml",
             distance_lt_km=None ,content_type_name=None,
             object_id=None):
    """
    Return a KML feed of all the geotagging in a around the user. This view takes
    an argument called `distance_lt_km` which is the radius of the permeter your
    are searching in. This feed can be restricted based on the content type of
    the element you want to get.
    """
    from django.contrib.gis.utils import GeoIP
    gip=GeoIP()
    if request.META["REMOTE_ADDR"] != "127.0.0.1":
        user_ip = request.META["REMOTE_ADDR"]
    else:
        user_ip = "populous.com"
    user_location_pnt = gip.geos(user_ip)

    criteria_pnt = {
        "point__distance_lt" : (user_location_pnt,
                                D(km=float(distance_lt_km))
                                )
            }
    if content_type_name:
        criteria_pnt["content_type__name"]==content_type_name

    geotagging = Point.objects.filter(**criteria_pnt)

    context = RequestContext(request, {
        'places' : geotagging.kml(),

    })
    return render_to_kml(template,context_instance=context)

def neighborhood_monitoring(request,
                          template="geotagging/view_neighborhood_monitoring.html",
                          content_type_name=None, distance_lt_km=None):
    """
    Direct the user to a template that is able to render the `kml_neighborhood_feed`
    on a google map. This feed can be restricted based on the content type of
    the element you want to get.
    """
    if distance_lt_km == None:
        distance_lt_km = 10
    gip=GeoIP()
    if request.META["REMOTE_ADDR"] != "127.0.0.1":
        user_ip = request.META["REMOTE_ADDR"]
    else:
        user_ip = "populous.com"
    user_location_pnt = gip.geos(user_ip)

    kml_feed = reverse("geotagging-kml_neighborhood_feed",
                       kwargs={"distance_lt_km":distance_lt_km})
    criteria_pnt = {
        "point__distance_lt" : (user_location_pnt,
                                D(km=float(distance_lt_km))
                                )
            }
    geotag_points = Point.objects.filter(**criteria_pnt).distance(user_location_pnt).order_by("-distance")
    context = RequestContext(request, {
        "user_ip" : user_ip,
        "user_location_pnt" : user_location_pnt,
        "geotag_points" : geotag_points,
        "user_city" : gip.city(user_ip),
        "kml_feed" : kml_feed,
    })
    return render_to_response(template,context_instance=context)
