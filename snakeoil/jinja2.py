import jinja2
from django.template import Context

from . import utils


@jinja2.contextfunction
def get_meta_tags(context, obj=None):
    # Jinja2's context doesn't have Django's `flatten()` method,
    # so we convert it to a Django context to get this.
    context = Context(context)
    return utils.get_meta_tags(context, obj)["meta_tags"]
