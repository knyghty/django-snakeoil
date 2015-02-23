from __future__ import unicode_literals

from django import template


register = template.Library()


class SeoDataNode(template.Node):
    def __init__(self, variable_name):
        self.variable_name = variable_name

    def render(self, context):
        flat_context = context.flatten()
        path = flat_context['request'].path

        for obj in flat_context.itervalues():
            try:
                if obj.get_absolute_url() == path:
                    seo = {}
                    if obj.head_title:
                        seo['head_title'] = obj.head_title,
                    if obj.meta_description:
                        seo['meta_description'] = obj.meta_description,
                    context[self.variable_name] = seo
                    return ''
            except (AttributeError):
                pass
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
