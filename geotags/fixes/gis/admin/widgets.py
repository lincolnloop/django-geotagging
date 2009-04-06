from django.conf import settings
from django.contrib.gis.admin.widgets import OpenLayersWidget
from django.contrib.gis.geos import GEOSGeometry, GEOSException
from django.template import loader, Context
from django.utils import translation

# Creating a template context that contains Django settings
# values needed by admin map templates.
geo_context = Context({'ADMIN_MEDIA_PREFIX' : settings.ADMIN_MEDIA_PREFIX,
                       'LANGUAGE_BIDI' : translation.get_language_bidi(),
                       })

class OpenLayersWidgetFixed(OpenLayersWidget):
    """
    Renders an OpenLayers map using the WKT of the geometry.
    """
    def render(self, name, value, attrs=None):
        attrs['field_name'] = name
        # Update the template parameters with any attributes passed in.
        if attrs: self.params.update(attrs)
        # Defaulting the WKT value to a blank string -- this
        # will be tested in the JavaScript and the appropriate
        # interfaace will be constructed.
        self.params['wkt'] = ''

        # If a string reaches here (via a validation error on another
        # field) then just reconstruct the Geometry.
        if isinstance(value, basestring):
            try:
                value = GEOSGeometry(value)
            except (GEOSException, ValueError):
                value = None

        if value and value.geom_type.upper() != self.geom_type:
            value = None

        # Constructing the dictionary of the map options.
        self.params['map_options'] = self.map_options()

        # Constructing the JavaScript module name using the ID of
        # the GeometryField (passed in via the `attrs` keyword).
        js_safe_field_name = self.params['field_name'].replace('-', '__')
        self.params['module'] = 'geodjango_%s' % js_safe_field_name

        if value:
            # Transforming the geometry to the projection used on the
            # OpenLayers map.
            srid = self.params['srid']
            if value.srid != srid: 
                try:
                    ogr = value.ogr
                    ogr.transform(srid)
                    wkt = ogr.wkt
                except OGRException:
                    wkt = ''
            else:
                wkt = value.wkt
               
            # Setting the parameter WKT with that of the transformed
            # geometry.
            self.params['wkt'] = wkt
        return loader.render_to_string(self.template, self.params,
                                       context_instance=geo_context)