from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from .utils import get_seo_model


class SeoModel(models.Model):
    head_title = models.CharField(blank=True, max_length=55)
    meta_description = models.TextField(blank=True, max_length=255)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class SeoUrl(get_seo_model()):
    url = models.CharField(primary_key=True, max_length=255, unique=True)

    def __str__(self):
        return self.url
