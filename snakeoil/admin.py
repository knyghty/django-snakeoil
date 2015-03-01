from __future__ import unicode_literals

from django.contrib import admin

from .models import SeoUrl
from .utils import get_seo_model


class SeoAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        fields = list(super(SeoAdmin, self).get_fields(request, obj))
        seo_fields = [field.name for field in get_seo_model()._meta.fields]
        fields = [field for field in fields if field not in seo_fields]
        return fields + seo_fields


class SeoUrlAdmin(SeoAdmin):
    pass


admin.site.register(SeoUrl, SeoUrlAdmin)
