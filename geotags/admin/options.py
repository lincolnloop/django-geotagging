from django import forms
from django.contrib import admin
from geotags.fixes.gis.admin.options import GeoGenericStackedInline
from geotags.models import Point


class GeotagsAdminForm(forms.ModelForm):
    def clean(self):
        # data is accessible via:
        # self.data['geotags-point-content_type-object_id-0-point']
        # having troubles accessing clean_point directly
        return super(GeotagsAdminForm, self).clean()
"""
from django.contrib.contenttypes.generic import BaseGenericInlineFormSet
class GeotagsAdminFormSet(BaseGenericInlineFormSet):
    def clean_point(self):
        import ipdb; ipdb.set_trace()
    form = GeotagsAdminForm
"""

class GeotagsInline(GeoGenericStackedInline):
    map_template = 'geotags/admin/osm_multiwidget.html'
    template = 'geotags/admin/edit_inline/geotags_inline.html'
    model = Point
    max_num = 1
    form = GeotagsAdminForm
    #formset = GeotagsAdminFormSet
    