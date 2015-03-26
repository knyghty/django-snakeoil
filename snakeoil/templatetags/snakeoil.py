from __future__ import unicode_literals

import logging

from django import template

from ..utils import get_seo_model
from ..models import SeoUrl


logger = logging.getLogger(__name__)
register = template.Library()


class SeoDataNode(template.Node):
    def __init__(self, variable_name):
        self.variable_name = variable_name

    def render(self, context):
        seo_model = get_seo_model()
        flat_context = context.flatten()
        path = flat_context['request'].path

        logger.debug('Looking for SEO object')
        for obj in flat_context.values():
            if (hasattr(obj, 'get_absolute_url') and
                    obj.get_absolute_url() == path):
                logger.debug('Found object: `{}`'.format(obj))
                seo = {}
                for field in seo_model._meta.fields:
                    if getattr(obj, field.name, '') != '':
                        logger.debug('Adding field `{}` to SEO dict'
                                     .format(field.name))
                        seo[field.name] = getattr(obj, field.name)
                if seo:
                    context[self.variable_name] = seo
                    logger.debug('Returning with object data')
                    return ''

        logger.debug('Looking for SEO URL')
        try:
            seo_url = SeoUrl.objects.get(url=path)
        except SeoUrl.DoesNotExist:
            logger.debug('No SEO URL found')
            return ''

        logger.debug('SEO URL found')
        seo = {}
        for field in seo_model._meta.fields:
            if getattr(seo_url, field.name, '') != '':
                seo[field.name] = getattr(seo_url, field.name)
                logger.debug('Adding field `{}` to SEO dict'
                             .format(field.name))

        context[self.variable_name] = seo
        logger.debug('Returning with URL data')
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
