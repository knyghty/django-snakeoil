from django.db import models

from snakeoil.models import SeoModel


class TestModel(SeoModel):
    test_field = models.IntegerField(default=1)

    def get_absolute_url(self):
        return '/'
