"""
This file test the application geotagging. This application can be used
to localised any object of django apps
"""

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.utils import add_postgis_srs

from geotagging.models import Geotag
from geotagging_tests.models import DummyModel

class PointTest(TestCase):
    def setUp(self):
        self.dummy_obj = DummyModel(name="foo")
        self.dummy_obj.save()
    def test_create_point(self):
        """
        Tests that a point can be created.
        """
        point = Geotag(object=self.dummy_obj,
                    point='SRID=4326;POINT (17.6 10.1)' )
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
        line = Geotag(object=self.dummy_obj,
                    line='SRID=4326;LINESTRING (6.41 9.53, 13.79 9.27)' )
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
        polygon = Geotag(object=self.dummy_obj,
                    polygon='SRID=4326;POLYGON ((10.10 10.74, 15.90 8.92, 8.70 3.60, -0.52 8.58, 4.57 12.12, 10.10 10.74))')
        polygon.save()
        self.assertEqual(polygon.object.name, "foo")
        self.assertEqual(polygon.content_type.name,"dummy model")

class TestKmlFeedUrls(TestCase):
    def setUp(self):
        self.dummy_foo = DummyModel(name="foo")
        self.dummy_foo.save()
        self.point_foo = Geotag(object=self.dummy_foo,
                      point='SRID=4326;POINT (17.6 10.1)')
        self.point_foo.save()
        self.dummy_bar = DummyModel(name="bar")
        self.dummy_bar.save()
        self.point_bar = Geotag(object=self.dummy_bar,
                      point='SRID=4326;POINT (17.6 10.1)')
        self.point_bar.save()
        self.dummy_baz = DummyModel(name="baz")
        self.dummy_baz.save()
        self.point_baz = Geotag(object=self.dummy_baz,
                      point='SRID=4326;POINT (17.6 10.1)')
        self.point_baz.save()
    def test_kml_feed_view(self):
        response = self.client.get(reverse("geotagging-kml_feed",
                                           kwargs={
                                            "geotag_field_name" : "point",
                                           })
                                  )
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context[0]["places"].count(), 3)

class TestGeotagsUrls(TestCase):
    def setUp(self):
        add_postgis_srs(900913)
        self.dummy_obj = DummyModel(name="foo")
        self.dummy_obj.save()
        self.dummy_model_contenttype = ContentType.objects.get(name="dummy model")
    def test_geotagging_add_view(self):
        response = self.client.get(reverse("geotagging-add_edit_point",
                                           kwargs={
                                            "content_type_id" : self.dummy_model_contenttype.id,
                                            "object_id" : self.dummy_obj.id
                                            })
                                   )
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context[0]["object"].name, "foo")
        response = self.client.post(reverse("geotagging-add_edit_point",
                                           kwargs={
                                            "content_type_id" : self.dummy_model_contenttype.id,
                                            "object_id" : self.dummy_obj.id
                                            }),
                                    {"point" : "SRID=900913;POINT(792499.1091503906 919690.3241992169)"}
                                   )
        self.assertEqual(response.status_code,302)
        pnt = Point.objects.get(
            content_type=ContentType.objects.get(model=self.dummy_obj._meta.module_name),
            object_id=self.dummy_obj.id)
        self.failUnlessEqual(pnt.object, self.dummy_obj)



__test__ = {"doctest": """
# Check that GeoIP is properly installed and configured
>>> from django.contrib.gis.utils import GeoIP
>>> g = GeoIP()
>>> g.country('google.com')
{'country_name': 'United States', 'country_code': 'US'}
>>> g.city('google.com')
{'city': 'Mountain View', 'region': 'CA', 'area_code': 650, 'longitude': -122.05740356445312, 'country_code3': 'USA', 'latitude': 37.419200897216797, 'postal_code': '94043', 'dma_code': 807, 'country_code': 'US', 'country_name': 'United States'}

"""}
