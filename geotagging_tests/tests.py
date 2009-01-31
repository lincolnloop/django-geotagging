"""
This file test the application geotags. This application can be used
to localised any object of django apps
"""

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

from geotags.models import Point,Line,Polygon
from geotagging_tests.models import DummyModel

class PointTest(TestCase):
    def setUp(self):
        self.dummy_obj = DummyModel(name="foo")
        self.dummy_obj.save()
    def test_create_point(self):
        """
        Tests that a point can be created.
        """
        point = Point(object=self.dummy_obj,
                    point='SRID=4326;POINT (17.6662892078603520 10.1420346563534256)' )
        point.save()
        self.assertEqual(point.object.name, "foo")
        self.assertEqual(point.content_type.name,"dummy model")

class LineTest(TestCase):
    def setUp(self):
        self.dummy_obj = DummyModel(name="foo")
        self.dummy_obj.save()
    def test_create_point(self):
        """
        Tests that a line can be created.
        """
        line = Line(object=self.dummy_obj,
                    line='SRID=4326;LINESTRING (6.4160156241068833 9.5357489968184606, 13.7988281230791880 9.2756221755122059)' )
        line.save()
        self.assertEqual(line.object.name, "foo")
        self.assertEqual(line.content_type.name,"dummy model")

class PolygonTest(TestCase):
    def setUp(self):
        self.dummy_obj = DummyModel(name="foo")
        self.dummy_obj.save()
    def test_create_point(self):
        """
        Tests that a polygon can be created.
        """
        polygon = Polygon(object=self.dummy_obj,
                    polygon='SRID=4326;POLYGON ((10.1074218735930348 10.7469693169815503, 15.9082031227855616 8.9284870614327119, 8.7011718737887858 3.6011423196581052, -0.5273437499265932 8.5810212144563014, 4.5703124993638067 12.1252642166689419, 10.1074218735930348 10.7469693169815503))')
        polygon.save()
        self.assertEqual(polygon.object.name, "foo")
        self.assertEqual(polygon.content_type.name,"dummy model")

class TestUrls(TestCase):
    def setUp(self):
        self.dummy_obj = DummyModel(name="foo")
        self.dummy_obj.save()
        self.dummy_model_contenttype = ContentType.objects.get(name="dummy model")
    def test_geotags_add_view(self):
        response = self.client.get(reverse("geotags-add_edit_point",
                                           kwargs={
                                            "content_type_id" : self.dummy_model_contenttype.id,
                                            "object_id" : self.dummy_obj.id
                                            })
                                   )
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context[0]["object"].name,
                         "foo")


__test__ = {"doctest": """
# Check that GeoIP is properly installed and configured
>>> from django.contrib.gis.utils import GeoIP
>>> g = GeoIP()
>>> g.country('google.com')
{'country_name': 'United States', 'country_code': 'US'}
>>> g.city('google.com')
{'city': 'Mountain View', 'region': 'CA', 'area_code': 650, 'longitude': -122.05740356445312, 'country_code3': 'USA', 'latitude': 37.419200897216797, 'postal_code': '94043', 'dma_code': 807, 'country_code': 'US', 'country_name': 'United States'}

"""}
