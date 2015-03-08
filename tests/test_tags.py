from __future__ import unicode_literals

from django.http import HttpRequest
from django.template import Context, Template, TemplateSyntaxError
from django.test import TestCase

from snakeoil.models import SeoUrl

from .models import TestModel


class GetSeoDataTagTests(TestCase):
    def test_invalid_syntax(self):
        request = HttpRequest()
        request.path = '/'

        with self.assertRaises(TemplateSyntaxError):
            Template(
                '{% load snakeoil %}'
                '{% get_seo_data spam %}'
                '{{ seo.head_title }}'
                '{{ seo.meta_description }}'
            ).render(Context({'request': request}))

    def test_no_data(self):
        request = HttpRequest()
        request.path = '/'

        out = Template(
            '{% load snakeoil %}'
            '{% get_seo_data %}'
            '{{ seo.head_title }}'
            '{{ seo.meta_description }}'
        ).render(Context({'request': request}))

        self.assertEqual(out, '')

    def test_data_from_url(self):
        SeoUrl.objects.create(url='/', head_title='spam',
                              meta_description='eggs')
        request = HttpRequest()
        request.path = '/'

        out = Template(
            '{% load snakeoil %}'
            '{% get_seo_data %}'
            '{{ seo.head_title }}'
            '{{ seo.meta_description }}'
        ).render(Context({'request': request}))

        self.assertEqual(out, 'spameggs')

    def test_as_parameter(self):
        SeoUrl.objects.create(url='/', head_title='spam',
                              meta_description='eggs')
        request = HttpRequest()
        request.path = '/'

        out = Template(
            '{% load snakeoil %}'
            '{% get_seo_data as spam %}'
            '{{ spam.head_title }}'
            '{{ spam.meta_description }}'
        ).render(Context({'request': request}))

        self.assertEqual(out, 'spameggs')

    def test_data_from_model(self):
        obj = TestModel.objects.create(head_title='spam',
                                       meta_description='eggs')
        request = HttpRequest()
        request.path = '/'

        out = Template(
            '{% load snakeoil %}'
            '{% get_seo_data %}'
            '{{ seo.head_title }}'
            '{{ seo.meta_description }}'
        ).render(Context({'request': request, 'obj': obj}))

        self.assertEqual(out, 'spameggs')
