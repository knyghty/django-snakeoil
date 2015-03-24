from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SnakeoilConfig(AppConfig):
    label = 'seo'
    name = 'snakeoil'
    verbose_name = _('SEO')
