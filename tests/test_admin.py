# from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from snakeoil.admin import SeoAdmin
from .models import TestModel


class MockRequest(object):
    pass

request = MockRequest()


class AdminTests(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.seo_model = TestModel.objects.create()

    def test_get_fields(self):
        ma = SeoAdmin(TestModel, self.site)
        self.assertEqual(ma.get_fields(request, self.seo_model),
                         ['test_field', 'head_title', 'meta_description'])
