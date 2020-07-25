from django.contrib.auth import get_user_model
from django.test import TestCase

from snakeoil.models import SEOPath

from .models import Article


User = get_user_model()


class SeoModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="tom")
        cls.article = Article.objects.create(
            author=cls.user, slug="an-article", title="A test article"
        )

    def test_add_meta_tags_to_model(self):
        self.article.meta_tags = {
            "en": [
                {
                    "name": "description",
                    "property": "og:description",
                    "content": "hello",
                }
            ]
        }
        self.article.save()
        self.article.refresh_from_db()
        meta_tags = self.article.meta_tags
        self.assertEqual(meta_tags["en"][0]["name"], "description")
        self.assertEqual(meta_tags["en"][0]["property"], "og:description")
        self.assertEqual(meta_tags["en"][0]["content"], "hello")

    def test_add_seo_path(self):
        seo_path = SEOPath.objects.create(
            path="/test-page/",
            meta_tags={"default": [{"name": "description", "content": "hello"}]},
        )
        self.assertEqual(str(seo_path), "/test-page/")
