from __future__ import unicode_literals

from django.test import TestCase

from snakeoil.models import SeoUrl


class SeoUrlTests(TestCase):
    def test_str(self):
        obj = SeoUrl.objects.create(url='/')
        self.assertEquals(obj.__str__(), '/')
