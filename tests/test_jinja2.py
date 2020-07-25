from django.test import TestCase

from snakeoil.models import SEOPath


class MetaTemplateTagTestCase(TestCase):
    def test_jinja2(self):
        SEOPath.objects.create(
            path="/jinja2/",
            meta_tags={
                "en": [{"name": "description", "content": "jinja2 path description"}]
            },
        )
        response = self.client.get("/jinja2/")
        self.assertContains(
            response,
            '<meta name="description" content="jinja2 path description">',
            html=True,
        )
