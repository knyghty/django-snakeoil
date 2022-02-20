import django
from django.db import models
from django.utils.translation import gettext_lazy as _

if django.VERSION <= (3, 0):
    postgres_only = True
    from django.contrib.postgres.fields import JSONField
else:
    postgres_only = False
    from django.db.models import JSONField


class SEOModel(models.Model):
    meta_tags = JSONField(blank=True, default=dict, verbose_name=_("meta tags"))

    class Meta:
        abstract = True
        if postgres_only:
            required_db_vendor = "postgresql"


class SEOPath(SEOModel):
    path = models.CharField(primary_key=True, max_length=255, verbose_name=_("path"))

    class Meta:
        verbose_name = _("SEO path")
        verbose_name_plural = _("SEO paths")
        if postgres_only:
            required_db_vendor = "postgresql"

    def __str__(self):
        return self.path
