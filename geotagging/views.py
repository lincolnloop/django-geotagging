from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.gis.shortcuts import render_to_kml
from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.conf import settings



from geotagging.models import Point, Line, Polygon

def add_edit_geotag(request, content_type_id, object_id,
                  template=None, form_class=None,
                  geotag_class=None):
    model_class = ContentType.objects.get(id=content_type_id).model_class()
    object = model_class.objects.get(id=object_id)
    object_content_type = ContentType.objects.get_for_model(object)
    try:
        # TODO : Handle the case of Line and Polygon
        geotag = geotag_class.objects.get(content_type__pk=object_content_type.id,
                               object_id=object.id)
    except ObjectDoesNotExist:
        geotag = None
    if request.method == "POST":
        form = form_class(request.POST, instance=geotag)
        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.object = object
            new_object.save()
            return HttpResponseRedirect("/admin/%s/%s/%s/"
                                        %(object_content_type.app_label,
                                          object_content_type.model,
                                          object.id))
    form = form_class(instance=geotag)

    context = RequestContext(request, {
        'form': form,
        'object' : object,
        'object_content_type' : object_content_type,
        'geotag' : geotag,
    })
    return render_to_response(template, context_instance=context )

def kml_feed(request, template="geotagging/geotags.kml",
             geotag_class_name=None,content_type_name=None,
             object_id=None):
    geotag_class = ContentType.objects.get(name=geotag_class_name).model_class()
    if content_type_name:
        geotags = geotag_class.objects.filter(content_type__name=content_type_name)
    if object_id:
        geotags = geotags.filter(object_id=object_id)
    if object_id == None and content_type_name == None :
        geotags = geotag_class.objects.all()
    context = RequestContext(request, {
        'geotags' : geotags,
    })
    return render_to_kml(template,context_instance=context)

def kml_feed_map(request,template="geotagging/view_kml_feed.html", geotag_class_name=None):
    kml_feed = reverse("geotagging-kml_feed",kwargs={"geotag_class_name":geotag_class_name})
    extra_context = {
        "google_key" : settings.GOOGLE_MAPS_API_KEY,
        "kml_feed" : kml_feed
    }
    return direct_to_template(request,template=template,extra_context=extra_context)
