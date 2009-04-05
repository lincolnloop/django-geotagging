from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.utils.datastructures import SortedDict
from django.contrib.gis.forms.fields import GeometryField
from django.contrib.gis.admin import OSMGeoAdmin

from lincolnloop.fixes import fixed_generic
from geotags.models import Point
from geotags.forms import PointWidget

GEOTAG_MODELS = ('Point',)
# Getting an instance so we can generate the map widget; also
# getting the geometry field for the model.
admin_instance = OSMGeoAdmin(Point, admin.site)
admin_instance.map_template = 'geotags/admin/osm_multiwidget.html'
point_field = Point._meta.get_field('point')
# Generating the widget.
PointWidget = admin_instance.get_map_widget(point_field)

class GeotagsAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GeotagsAdminForm, self).__init__(*args, **kwargs)
        
        #create getagging maps
        obj = self.instance
        self.potential_geotags_fields = []
        for model in GEOTAG_MODELS:
            field_name = model
            field = GeometryField(null=True, geom_type="point", label=model, widget=PointWidget)
            ct = ContentType.objects.get_for_model(obj)
            try:
                #todo
                Point.objects.get(object_id=obj.pk, content_type=ct)
            except Point.DoesNotExist:
                self.potential_geotags_fields.append((model, field_name))
            self.fields[field_name] = field

    def save(self, *args, **kwargs):
        output = super(GeotagsAdminForm, self).save(*args, **kwargs)
        for slug, field_name in self.potential_geotags_fields:
            value = self.cleaned_data.get(field_name)
            if value:
                Point.objects.create(content_object=self.instance)
        return output

class GeotagsInline(fixed_generic.GenericStackedInline):
    model = Point
    max_num = 1
    form = GeotagsAdminForm
    #ct_fk_field = "object_pk"

class GeotagsAdmin(OSMGeoAdmin):
    form = GeotagsAdminForm
    map_template = 'geotags/admin/osm_multiwidget.html'
    def __init__(self, model, *args, **kwargs):
        fieldsets = SortedDict(self.fieldsets)
        # Get the currently named fields from the fieldsets.
        fieldsets['Geotags'] = {
            'classes': ('collapse',),
            'fields': GEOTAG_MODELS
        }
        self.fieldsets = fieldsets.items()
        super(GeotagsAdmin, self).__init__(model, *args, **kwargs)
