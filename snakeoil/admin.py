from django.contrib import admin

from .models import SeoUrl


class SeoAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        fields = list(super(SeoAdmin, self).get_fields(request, obj))
        seo_fields = ['head_title', 'meta_description']
        fields = [field for field in fields if field not in seo_fields]
        return fields + seo_fields


class SeoUrlAdmin(SeoAdmin):
    pass


admin.site.register(SeoUrl, SeoUrlAdmin)
