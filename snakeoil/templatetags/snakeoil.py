from __future__ import unicode_literals

from django import template

from ..utils import get_seo_model
from ..models import SeoUrl


register = template.Library()


class SeoDataNode(template.Node):
    def __init__(self, variable_name):
        self.variable_name = variable_name

    def render(self, context):
        seo_model = get_seo_model()
        flat_context = context.flatten()
        path = flat_context['request'].path

        for obj in flat_context.itervalues():
            if (hasattr(obj, 'get_absolute_url') and
                    obj.get_absolute_url() == path):
                seo = {}
                for field in seo_model._meta.fields:
                    if getattr(obj, field.name) != '':
                        seo[field.name] = getattr(obj, field.name)

                if not seo:
                    try:
                        seo_url = SeoUrl.objects.get(url=path)
                    except SeoUrl.DoesNotExist:
                        seo_url = None

                    if seo_url:
                        for field in seo_model._meta.fields:
                            seo[field.name] = getattr(seo_url, field.name)

                context[self.variable_name] = seo
                return ''
        return ''


def do_get_seo_data(parser, token):
    bits = token.split_contents()
    if len(bits) > 1 and (len(bits) > 3 or bits[1] != 'as'):
        raise template.TemplateSyntaxError(('Format is {} [as variable] '
                                            .format(bits[0])))
    try:
        variable_name = bits[2]
    except IndexError:
        variable_name = 'seo'
    return SeoDataNode(variable_name)


register.tag('get_seo_data', do_get_seo_data)
