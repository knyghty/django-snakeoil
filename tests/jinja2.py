from jinja2 import Environment

from snakeoil.jinja2 import get_meta_tags


def environment(**options):
    env = Environment(**options)
    env.globals.update({"get_meta_tags": get_meta_tags})
    return env
