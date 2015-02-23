from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.encoding import python_2_unicode_compatible


class SeoModel(models.Model):
    head_title = models.CharField(blank=True, max_length=55)
    meta_description = models.TextField(blank=True, max_length=255)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class SeoUrl(SeoModel):
    url = models.CharField(primary_key=True, max_length=255, unique=True)

    def __str__(self):
        return self.url

    def clean(self):
        if not self.head_title and not self.meta_description:
            raise ValidationError('You must provide either title or '
                                  'meta description')
