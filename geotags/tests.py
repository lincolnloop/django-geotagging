from django import template
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point

from geotags.models import Geotag

class TagTestCase(TestCase):
    """Helper class with some tag helper functions"""
    
    def installTagLibrary(self, library):
        template.libraries[library] = __import__(library)
        
    def renderTemplate(self, tstr, **context):
        t = template.Template(tstr)
        c = template.Context(context)
        return t.render(c)

class OutputTagTest(TagTestCase):
    
    def setUp(self):
        self.installTagLibrary('geotags.templatetags.geotags')
        denver_user = User.objects.create(username='denver')
        dia_user = User.objects.create(username='dia')
        aa_user = User.objects.create(username='annarbor')
        self.denver = Geotag.objects.create(object=denver_user,
                            point=Point(-104.9847034, 39.739153600000002))
        dia = Geotag.objects.create(object=dia_user,
                            point=Point(-104.673856, 39.849511999999997))
        aa = Geotag.objects.create(object=aa_user,
                            point=Point(-83.726329399999997, 42.2708716))
        
    def testOutput(self):
        "get_objects_nearby tag has no output"
        template = "{% load geotags %}"\
                   "{% get_objects_nearby obj.point as nearby_objs %}"
        o = self.renderTemplate(template, obj=self.denver)
        self.assertEqual(o.strip(), "")
        
    def testAsVar(self):
        template = "{% load geotags %}"\
                   "{% get_objects_nearby obj.point as nearby_objs %}"\
                   "{{ nearby_objs|length }}"
        o = self.renderTemplate(template, obj=self.denver)
        self.assertEqual(o.strip(), "1")

    def testShortDistance(self):
        # DIA is about 18 miles from downtown Denver
        short_template = "{% load geotags %}"\
                   "{% get_objects_nearby obj.point as nearby_objs within 17 %}"\
                   "{{ nearby_objs|length }}"
        o = self.renderTemplate(short_template, obj=self.denver)
        self.assertEqual(o.strip(), "1")
        long_template = short_template.replace("17", "19")
        o = self.renderTemplate(long_template, obj=self.denver)
        self.assertEqual(o.strip(), "2")

    def testLongDistance(self):
        # Ann Arbor is about 1122 miles from Denver
        short_template = "{% load geotags %}"\
                   "{% get_objects_nearby obj.point within 1115 as nearby_objs %}"\
                   "{{ nearby_objs|length }}"
        o = self.renderTemplate(short_template, obj=self.denver)
        self.assertEqual(o.strip(), "2")
        long_template = short_template.replace("1115", "1125")
        o = self.renderTemplate(long_template, obj=self.denver)
        self.assertEqual(o.strip(), "3")
        
class SyntaxTagTest(TestCase):
    
    def getNode(self, str):
        from geotags.templatetags.geotags import get_objects_nearby
        return get_objects_nearby(None, template.Token(template.TOKEN_BLOCK, str))
        
    def assertNodeException(self, str):
        self.assertRaises(template.TemplateSyntaxError, self.getNode, str)

    def testInvalidSyntax(self):
        self.assertNodeException("get_objects_nearby as")
        self.assertNodeException("get_objects_nearby notas objects_nearby")
