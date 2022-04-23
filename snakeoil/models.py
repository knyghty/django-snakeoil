from django.db import models
from django.utils.translation import gettext_lazy as _


class SEOModel(models.Model):
    meta_tags = models.JSONField(blank=True, default=dict, verbose_name=_("meta tags"))

    class Meta:
        abstract = True


class SEOPath(SEOModel):
    path = models.CharField(primary_key=True, max_length=255, verbose_name=_("path"))

    class Meta:
        verbose_name = _("SEO path")
        verbose_name_plural = _("SEO paths")

    def __str__(self) -> str:
        return self.path
