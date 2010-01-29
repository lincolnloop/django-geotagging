import re

from django import forms
from django.contrib.gis.forms import GeometryField
from django.contrib.gis.gdal import OGRException

from geotagging.fixes.gis.admin.options import GeoGenericStackedInline
from geotagging.models import Geotag


class GeotagsAdminForm(forms.ModelForm):
    """Custom form to use for inline admin widget"""
    catchall = forms.CharField(widget=forms.Textarea, required=False)
    line = GeometryField(widget=forms.HiddenInput, null=True, required=False, 
                         geom_type='LINESTRING', srid=4326)
    polygon = GeometryField(widget=forms.HiddenInput, null=True, required=False,
                            geom_type='POLYGON', srid=4326)
    
    
    def full_clean(self):
        """
        Sets geom based on catchall value and erases any other geoms
        """
        if '%s-catchall' % self.prefix in self.data:
            value = self.data['%s-catchall' % self.prefix]
            self.data['%s-point' % self.prefix] = ''
            self.data['%s-line' % self.prefix] = ''
            self.data['%s-polygon' % self.prefix] = ''
            if re.search('POINT\((.*)\)', value):
                self.data['%s-point' % self.prefix] = value
            elif re.search('LINESTRING\((.*)\)', value):
                self.data['%s-line' % self.prefix] = value
            elif re.search('POLYGON\((.*)\)', value):
                self.data['%s-polygon' % self.prefix] = value
        super(GeotagsAdminForm, self).full_clean()
    
    def __init__(self, *args, **kwargs):
        super(GeotagsAdminForm, self).__init__(*args, **kwargs)
        
        # Prefill catchall field if geotag already exists
        if self.instance:
            found = False
            # get SRID of map widget
            srid = self.fields['point'].widget.params['srid']
            # get srid of geom in model
            for geom_type in ('point', 'line', 'polygon'):
                geom = getattr(self.instance, geom_type)
                if geom:
                    db_field = geom
                    found = True
                    break
            if not found:
                return
                
            # Transforming the geometry to the projection used on the
            # OpenLayers map.
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



class GeotagsInline(GeoGenericStackedInline):
    """
    A single inline form for use in the admin
    """
    map_template = 'geotagging/admin/openlayer_multiwidget.html'
    # inject Open Street map if GDAL works
    from django.contrib.gis import gdal
    if gdal.HAS_GDAL:
        map_template = 'geotagging/admin/osm_multiwidget.html'
    template = 'geotagging/admin/edit_inline/geotagging_inline.html'
    model = Geotag
    max_num = 1
    form = GeotagsAdminForm

    
    def get_formset(self, request, obj=None, **kwargs):
        """
        Hacks up the form so we can remove some geometries that OpenLayers
        can't handle.
        """
        fset = super(GeotagsInline, self).get_formset(request, 
                                                      obj=None, **kwargs)
        # put catchall on top so the javascript can access it
        fset.form.base_fields.keyOrder.reverse()
        fset.form.base_fields['point'].label = "Geotag"
        # these fields aren't easily editable via openlayers
        for field in ('geometry_collection', 'multilinestring'):
            fset.form.Meta.exclude.append(field)
            del(fset.form.base_fields[field])
        return fset
