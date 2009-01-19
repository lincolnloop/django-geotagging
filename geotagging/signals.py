from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping
    
def parse_data_file(instance, sender, **kwargs):
    """
    Populates multi_line field using built in parsers from GeoDjango
    
    """
    if not instance.data_file:
        #nothing to do
        return
        
    from geotagging.models import GeoMultiLine
    
    ds = DataSource(instance.data_file.path)
    
    # this bombs for some reason
    #lm = LayerMapping(GeoMultiLine, ds, {'multi_line': 'MULTILINESTRING'})
    
    #TODO, this is far too fragile
    instance.multi_line = ds['tracks'].get_geoms()[0].wkt
    
    #save metadata
    points = []
    for pt in ds['track_points']:
        points.append({
            'lat': pt.geom.x,
            'lon': pt.geom.y,
            'time': pt['time'].value,
            'ele': pt['ele'].value,
        })
        
    instance.metadata = points