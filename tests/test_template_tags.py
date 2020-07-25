import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from snakeoil.models import SEOPath

from .models import Article


User = get_user_model()


class MetaTemplateTagTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="tom", first_name="Tom", last_name="Carrick"
        )
        cls.article = Article.objects.create(
            author=cls.user,
            slug="an-article",
            title="A test article",
            meta_tags={
                "default": [{"name": "description", "content": "default description"}],
                "en": [
                    {"name": "description", "content": "hello"},
                    {"property": "og:description", "content": "opengraph hello"},
                ],
            },
        )

    def test_meta_template_tag_with_seo_model(self):
        response = self.client.get(f"/articles/{self.article.slug}/")

        self.assertContains(
            response, '<meta name="description" content="hello">', html=True
        )
        self.assertContains(
            response,
            '<meta property="og:description" content="opengraph hello">',
            html=True,
        )

    def test_meta_template_tag_with_attr(self):
        self.article.meta_tags["en"].append(
            {"name": "author", "attribute": "author_name"}
        )
        self.article.save()

        response = self.client.get(f"/articles/{self.article.slug}/")

        self.assertTemplateUsed(response, "tests/article_detail.html")
        self.assertContains(
            response, '<meta name="author" content="Tom Carrick">', html=True
        )

    def test_attr_with_object_from_context(self):
        self.article.meta_tags["en"].append(
            {"name": "author", "attribute": "author_name"}
        )
        self.article.save()

        response = self.client.get(
            f"/articles/{self.article.slug}/", {"template_without_obj": True}
        )

        self.assertTemplateUsed(response, "tests/article_detail_without_obj.html")
        self.assertContains(
            response, '<meta name="author" content="Tom Carrick">', html=True
        )

    def test_path(self):
        SEOPath.objects.create(
            path="/test-page/",
            meta_tags={"en": [{"name": "description", "content": "path description"}]},
        )

        response = self.client.get("/test-page/")

        self.assertContains(
            response, '<meta name="description" content="path description">', html=True
        )

    def test_attr_not_allowed_for_path(self):
        SEOPath.objects.create(
            path="/test-page/",
            meta_tags={
                "default": [{"name": "description", "attribute": "author_name"}]
            },
        )
        with self.assertLogs("snakeoil.utils", level=logging.ERROR):
            self.client.get("/test-page/")

    @override_settings(USE_I18N=False)
    def test_without_i18n(self):
        response = self.client.get(f"/articles/{self.article.slug}/")

        self.assertContains(
            response,
            '<meta name="description" content="default description">',
            html=True,
        )

    @override_settings(LANGUAGE_CODE="en_GB")
    def test_more_specific_language_wins(self):
        self.article.meta_tags["en_GB"] = [
            {"name": "description", "content": "yorrite m8"}
        ]
        self.article.save()

        response = self.client.get(f"/articles/{self.article.slug}/")

        self.assertContains(
            response, '<meta name="description" content="yorrite m8">', html=True
        )

    @override_settings(LANGUAGE_CODE="en_GB")
    def test_fallback_to_generic_language(self):
        response = self.client.get(f"/articles/{self.article.slug}/")

        self.assertContains(
            response, '<meta name="description" content="hello">', html=True
        )

    @override_settings(LANGUAGE_CODE="eo")
    def test_fallback_to_default(self):
        response = self.client.get(f"/articles/{self.article.slug}/")

        self.assertContains(
            response,
            '<meta name="description" content="default description">',
            html=True,
        )

    def test_image_field_with_width_and_height_fields(self):
        with open(settings.TESTS_DIR / "data" / "kitties.jpg", "rb") as f:
            self.article.main_image = SimpleUploadedFile(
                name="kitties.jpg", content=f.read(), content_type="image/jpeg",
            )
        self.article.meta_tags["en"] = [
            {"property": "og:image", "attribute": "main_image"}
        ]
        self.article.save()

        response = self.client.get(f"/articles/{self.article.slug}/")

        self.assertContains(
            response,
            (
                '<meta property="og:image" '
                f'content="http://testserver{self.article.main_image.url}">'
            ),
            html=True,
        )
        self.assertContains(
            response, '<meta property="og:image:width" content="1577">', html=True
        )
        self.assertContains(
            response, '<meta property="og:image:height" content="889">', html=True
        )

    def test_image_field_without_width_and_height_fields(self):
        with open(settings.TESTS_DIR / "data" / "kitties.jpg", "rb") as f:
            self.article.secondary_image = SimpleUploadedFile(
                name="kitties.jpg", content=f.read(), content_type="image/jpeg",
            )
        self.article.meta_tags["en"] = [
            {"property": "og:image", "attribute": "secondary_image"}
        ]
        self.article.save()

        response = self.client.get(f"/articles/{self.article.slug}/")

        self.assertContains(
            response,
            (
                '<meta property="og:image" '
                f'content="http://testserver{self.article.secondary_image.url}">'
            ),
            html=True,
        )
        self.assertContains(
            response, '<meta property="og:image:width" content="1577">', html=True
        )
        self.assertContains(
            response, '<meta property="og:image:height" content="889">', html=True
        )

    def test_attr_manual_image(self):
        # The field here doesn't matter. It should just get passed through.
        # This is to handle URLFields, etc.
        self.article.meta_tags["en"] = [{"property": "og:image", "attribute": "slug"}]
        self.article.save()

        response = self.client.get(f"/articles/{self.article.slug}/")

        self.assertContains(
            response, '<meta property="og:image" content="an-article">', html=True
        )

    def test_static(self):
        # The default finder doesn't care if the file exists or not.
        self.article.meta_tags["en"] = [
            {"property": "og:image", "static": "foo/dummy.png"}
        ]
        self.article.save()

        response = self.client.get(f"/articles/{self.article.slug}/")

        self.assertContains(
            response,
            (
                '<meta property="og:image" '
                'content="http://testserver/static/foo/dummy.png">'
            ),
            html=True,
        )

    @override_settings(
        SNAKEOIL_DEFAULT_TAGS={
            "default": [{"property": "og:site_name", "content": "My Site"}]
        }
    )
    def test_default_tags(self):
        response = self.client.get(f"/articles/{self.article.slug}/")

        self.assertNotIn("og:site_name", self.article.meta_tags.get("en", {}))
        self.assertNotIn("og:site_name", self.article.meta_tags.get("default", {}))
        self.assertContains(
            response, '<meta property="og:site_name" content="My Site">', html=True
        )
        self.assertContains(
            response, '<meta name="description" content="hello">', html=True
        )
        self.assertContains(
            response,
            '<meta property="og:description" content="opengraph hello">',
            html=True,
        )

    @override_settings(
        SNAKEOIL_DEFAULT_TAGS={
            "default": [{"property": "og:site_name", "content": "My Site"}]
        }
    )
    def test_model_beats_defaults(self):
        self.article.meta_tags["default"] = [
            {"property": "og:site_name", "content": "Not really my site"}
        ]
        self.article.save()

        response = self.client.get(f"/articles/{self.article.slug}/")

        self.assertNotContains(
            response, '<meta property="og:site_name" content="My Site">', html=True
        )
        self.assertContains(
            response,
            '<meta property="og:site_name" content="Not really my site">',
            html=True,
        )

    @override_settings(
        LANGUAGE_CODE="eo",
        SNAKEOIL_DEFAULT_TAGS={
            "eo": [{"property": "og:site_name", "content": "Mia Esperanta Retejo"}]
        },
    )
    def test_language_default_beats_model(self):
        self.article.meta_tags["default"].append(
            {"property": "og:site_name", "content": "My Site"}
        )
        self.article.save()

        response = self.client.get(f"/articles/{self.article.slug}/")

        self.assertNotContains(
            response, '<meta property="og:site_name" content="My Site">', html=True
        )
        self.assertContains(
            response,
            '<meta property="og:site_name" content="Mia Esperanta Retejo">',
            html=True,
        )

    def test_seo_path_root_url(self):
        SEOPath.objects.create(
            path="/",
            meta_tags={"default": [{"name": "description", "content": "home page"}]},
        )
        response = self.client.get("/")
        self.assertContains(
            response, '<meta name="description" content="home page">', html=True
        )
