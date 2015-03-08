from __future__ import unicode_literals

from importlib import import_module

from django.conf import settings


def get_seo_model():
    model = getattr(settings, 'SNAKEOIL_MODEL', 'snakeoil.models.SeoModel')
    module, class_name = model.rsplit('.', 1)
    return getattr(import_module(module), class_name)
