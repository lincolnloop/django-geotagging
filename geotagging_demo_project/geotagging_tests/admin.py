from django.contrib.gis import admin

from geotagging.admin.options import GeotagsInline

from geotagging_tests.models import DummyModel

class DummyModelAdmin(admin.ModelAdmin):
    inlines = [GeotagsInline,]

admin.site.register(DummyModel, DummyModelAdmin)
