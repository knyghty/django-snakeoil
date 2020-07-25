from django import template

from ..utils import get_meta_tags


register = template.Library()


@register.inclusion_tag("snakeoil/seo.html", takes_context=True)
def meta(context, obj=None):
    return get_meta_tags(context, obj)
