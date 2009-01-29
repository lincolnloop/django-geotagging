from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist


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
