from typing import Optional

from django import template
from django.db.models import Model

from .. import types
from .. import utils

register = template.Library()


@register.inclusion_tag("snakeoil/seo.html", takes_context=True)
def meta(
    context: template.Context, obj: Optional[Model] = None
) -> types.MetaTagContext:
    return utils.get_meta_tags(context, obj)
