{% extends "geotagging/admin/openlayer_multiwidget.js" %}
{% block base_layer %}new OpenLayers.Layer.OSM.Mapnik("OpenStreetMap (Mapnik)");{% endblock %}
