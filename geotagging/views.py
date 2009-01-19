from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType


from geotagging.models import Point

def add_edit_point(request, content_type_id, object_id,
                  template=None, form_class=None):
    model_class = ContentType.objects.get(id=content_type_id).model_class()
    object = model_class.objects.get(id=object_id)
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.object = object
            new_object.save()
            return HttpResponseRedirect("/admin")
    form = form_class()
    import ipdb; ipdb.set_trace()

    context = RequestContext(request, {
        'form': form,
    })
    return render_to_response(template, context_instance=context )
