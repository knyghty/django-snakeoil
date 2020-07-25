=====
Setup
=====

Installation
============

To install::

    pip install django-snakeoil

Configuration
=============

If you're using Django templates, add ``snakeoil`` to your installed apps::

    INSTALLED_APPS = [
        "myapp",
        "snakeoil",
        # ...
    ]

If you're using Jinja2, you need to add the ``get_meta_tags`` function to
your environment::

    from jinja2 import Environment
    from snakeoil.jinja2 import get_meta_tags

    def environment(**options):
        env = Environment(**options)
        env.globals.update(
            {
                "get_meta_tags": get_meta_tags,
                # ...
            }
        )
        return env
