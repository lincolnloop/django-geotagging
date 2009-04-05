{% extends "gis/admin/openlayers.js" %}
{% block controls %}
// Map controls:
// Add geometry specific panel of toolbar controls
{{ module }}.getControls({{ module }}.layers.vector);

//adds extra widgets
var path_ctl = new OpenLayers.Control.DrawFeature(lyr, OpenLayers.Handler.Path, {'displayClass': 'olControlDrawFeaturePath', 'title':'Draw a path'});
var poly_ctl = new OpenLayers.Control.DrawFeature(lyr, OpenLayers.Handler.Polygon, {'displayClass': 'olControlDrawFeaturePolygon', 'title':'Draw a polygon'});
{{ module }}.panel.controls.splice(1, 0, path_ctl, poly_ctl);


{{ module }}.panel.addControls({{ module }}.controls);
{{ module }}.map.addControl({{ module }}.panel);
{{ module }}.addSelectControl();
// Then add optional visual controls
{% if mouse_position %}{{ module }}.map.addControl(new OpenLayers.Control.MousePosition());{% endif %}
{% if scale_text %}{{ module }}.map.addControl(new OpenLayers.Control.Scale());{% endif %}
{% if layerswitcher %}{{ module }}.map.addControl(new OpenLayers.Control.LayerSwitcher());{% endif %}
// Then add optional behavior controls
{% if not scrollable %}{{ module }}.map.getControlsByClass('OpenLayers.Control.Navigation')[0].disableZoomWheel();{% endif %}
{% endblock; %}