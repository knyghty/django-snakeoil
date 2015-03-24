from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .utils import get_seo_model


class SeoModel(models.Model):
    head_title = models.CharField(blank=True, max_length=55,
                                  verbose_name=_('head title'))
    meta_description = models.TextField(blank=True, max_length=160,
                                        verbose_name=_('meta description'))

    class Meta:
        abstract = True


@python_2_unicode_compatible
class SeoUrl(get_seo_model()):
    url = models.CharField(primary_key=True, max_length=255, unique=True,
                           verbose_name=_('URL'))

    class Meta:
        verbose_name = _('SEO URL')
        verbose_name_plural = _('SEO URLs')

    def __str__(self):
        return self.url
