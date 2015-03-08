from snakeoil.models import SeoModel


class TestModel(SeoModel):
    def get_absolute_url(self):
        return '/'
