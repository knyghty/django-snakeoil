import typing

import jinja2
from django.db import models
from django.template import Context

from . import types
from . import utils


@jinja2.pass_context
def get_meta_tags(
    context: jinja2.runtime.Context, obj: typing.Optional[models.Model] = None
) -> types.MetaTagList:
    # Jinja2's context doesn't have Django's `flatten()` method,
    # so we convert it to a Django context to get this.
    return utils.get_meta_tags(Context(context), obj)["meta_tags"]
