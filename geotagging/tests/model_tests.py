from django import template
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point, Polygon

from geotagging.models import Geotag
from geotagging import register, AlreadyRegistered

class ModelTest(TestCase):
    
    def setUp(self):
        try:
            register(User)
        except AlreadyRegistered:
            pass
        self.obj = User.objects.create(username='user')
        self.point = Point(5,5)
        self.poly = Polygon(((0, 0), (0, 10), (10, 10), (0, 10), (0, 0)),
                               ((4, 4), (4, 6), (6, 6), (6, 4), (4, 4)))
        
    def testEmptyGeotag(self):
        "Empty geotag returns none"
        self.assertEqual(self.obj.geotag, None)
    
    def testSetGeotag(self):
        "Geotag can be set on the object"
        self.obj.geotag = self.point
        self.assertEqual(self.obj.geotag.point, self.point)
        geotag = Geotag.objects.get_for_object(self.obj)
        self.assertEqual(geotag.point, self.point)
    
    def testChangeGeotag(self):
        "Geotag can be changed on the object"
        self.obj.geotag = self.point
        self.obj.geotag = self.poly
        self.assertEqual(self.obj.geotag.polygon, self.poly)
        geotag = Geotag.objects.get_for_object(self.obj)
        self.assertEqual(geotag.point, None)
        self.assertEqual(geotag.polygon, self.poly)
    
    def testGetGeomGeotag(self):
        "Geotag can find the right geom"
        self.obj.geotag = self.poly
        self.assertEqual(self.obj.geotag.get_geom(), self.poly)
        
    def testDeleteGeotag(self):
        "Geotag can be removed from the object"
        self.obj.geotag = None
        self.assertEqual(self.obj.geotag, None)
        geotag = Geotag.objects.get_for_object(self.obj)
        self.assertEqual(geotag, None)
        