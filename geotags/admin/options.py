import re

from django import forms
from django.contrib import admin
from geotags.fixes.gis.admin.options import GeoGenericStackedInline
from geotags.models import Point, GeometryCollection


class GeotagsAdminForm(forms.ModelForm):
    catchall = forms.CharField(widget=forms.Textarea, required=False)
    def __init__(self, *args, **kwargs):
        super(GeotagsAdminForm, self).__init__(*args, **kwargs)
        
        # Prefill catchall field if geotag already exists
        if self.instance:
            
            if self.instance.point:
                db_field = self.instance.point
                form_field = 'point'
            #TODO test for other geom types
            else:
                return
                
            # Transforming the geometry to the projection used on the
            # OpenLayers map.
            srid = self.fields[form_field].widget.params['srid']
            if db_field.srid != srid: 
                try:
                    ogr = db_field.ogr
                    ogr.transform(srid)
                    wkt = ogr.wkt
                except OGRException:
                    wkt = ''
            else:
                wkt = db_field.wkt
            self.fields['catchall'].initial = wkt

               
    def clean(self):
        # splits catchall field out into proper model field
        # TODO properly validate data
        if self.cleaned_data['catchall']:
            value = self.cleaned_data['catchall']
            if re.search('POINT\((.*)\)', value):
                self.cleaned_data['point'] = value
                if 'point' in self.errors:
                    self.errors.pop('point')
            elif re.search('LINESTRING\((.*)\)', value):
                print "LINESTRING"
                #TODO save linestring
                pass
            elif re.search('POLYGON\((.*)\)', value):
                print 'POLYGON'
                #TODO save polygon
                pass
        return super(GeotagsAdminForm, self).clean()


class GeotagsInline(GeoGenericStackedInline):
    map_template = 'geotags/admin/osm_multiwidget.html'
    template = 'geotags/admin/edit_inline/geotags_inline.html'
    model = Point
    max_num = 1
    form = GeotagsAdminForm

    
    def get_formset(self, request, obj=None, **kwargs):
        fs = super(GeotagsInline, self).get_formset(request, obj=None, **kwargs)
        fs.form.base_fields.keyOrder.reverse()
        return fs