from django import forms
from django.contrib.gis import admin

from geotagging.models import Point
from geotagging.admin import PointAdmin


# Getting an instance so we can generate the map widget; also
# getting the geometry field for the model.
admin_instance = PointAdmin(Point, admin.site)
point_field = Point._meta.get_field('point')

# Generating the widget.
PointWidget = admin_instance.get_map_widget(point_field)

class PointForm(forms.ModelForm):
    point = forms.CharField(widget=PointWidget())
    class Meta:
        model = Point
        exclude = ("content_type","object_id")
    class Media:
        js = ("http://openlayers.org/api/2.6/OpenLayers.js",)
