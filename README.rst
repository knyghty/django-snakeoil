===============
django-snakeoil
===============

django-snakeoil helps manage your ``<meta>`` tags. It works on all supported
Django versions and databases.

It offers full internationalization support (tags for multiple languages),
content set dynamically from object attributes, automatic Opengraph image
width and heights for ``ImageField``, and more.

`Full documentation <https://django-snakeoil.readthedocs.io/en/latest/index.html>`_

Getting started
===============

To install, ``pip install django-snakeoil`` or use your favourite package
manager.

You can use Snakeoil in two ways. If you'd like to attach metadata to an
object, you can use the model abstract base class:

.. code-block:: python

    from snakeoil.models import SEOModel

    class Article(SEOModel):
        title = models.CharField(max_length=200)
        author = models.ForeignKey(User, on_delete=models.CASCADE)
        main_image = models.Imagefield(blank=True, null=True)

        @property
        def author_name(self):
            return

        @property
        def snakeoil_metadata(self):
            metadata = {
                "default": [
                    {
                        "name": "author",
                        "content": self.author.get_full_name(),
                    },
                    {"property": "og:title", "content": self.title},
                ]
            }
            if self.main_image:
                metadata["default"].append(
                    {"property": "og:image", "attribute": "main_image"}
                )
            return metadata

You can also override these tags in the admin per-object.

For situations where you can't change the model (flatpages, third party apps)
or don't have one at all, there is an ``SEOPath`` model that maps paths to
your meta tags.

Tags are added in the admin (or however else you like) as JSON. For example:

.. code-block:: JSON

    {
        "default": [
            {"name": "description", "property": "og:description", "content": "Meta description"},
            {"property": "og:title", "content": "My blog post"},
            {"name": "author", "attribute": "author_name"},
            {"property": "og:image", "static": "img/default.jpg"}
        ]
    }

Where ``default`` will work for any language. You can replace ``default``
with a language code, e.g. "nl_NL", and these tags will only display if the
current language is Dutch. This will generate something like:

.. code-block:: html

    <meta name="description" property="og:description" content="Meta description">
    <meta property="og:title" "content="My blog post">
    <!-- from my_object.author_name -->
    <meta name="author" content="Tom Carrick">
    <!-- build a static URL -->
    <meta property="og:image" content="/static/img/default.jpg">

Note that when using ``static``, width and height are not added, but you may
add these yourself. For ``ImageField``, this will be added automatically:

.. code-block:: JSON

    {
        "default": [
            {"property": "og:image", "attribute": "main_image"}
        ]
    }

Results in:

.. code-block:: html

    <meta property="og:image" content="/media/blog_1_main_image.jpg">
    <meta property="og:image:width" content="640">
    <meta property="og:image:height" content="480">

Django Templates
----------------

Add ``snakeoil`` to your ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = [
        "snakeoil",
        # ...
    ]

In your base template, add this where you want the tags to appear:

.. code-block:: html

    {% load snakeoil %}
    {% block head %}
        {% meta %}
    {% endblock %}

This will automatically find an object based on the ``get_absolute_url()``
of your model, by looking in the request context. If nothing is found,
snakeoil will check for an ``SEOPath`` object for the current path. If
you have an object, it is recommended to pass it into the tag directly
to short-circuit the tag finding mechanisms:

.. code-block:: html

    {% meta my_obj %}

Jinja2
------

Set your environment:

.. code-block:: python

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

In your template:

.. code-block:: html

    {% block meta %}
        {% with meta_tags=get_meta_tags() %}
            {% include "snakeoil/seo.jinja2" %}
        {% endwith %}
    {% endblock meta %}

To pass in an object:

.. code-block:: html

    {% block meta %}
        {% with meta_tags=get_meta_tags(my_object) %}
            {% include "snakeoil/seo.jinja2" %}
        {% endwith %}
    {% endblock meta %}

Notes
=====

Thanks to kezabelle for the name. For those wondering:

Metadata is often used for SEO purposes. A lot of people (rightly or not)
consider SEO to be snakeoil. Also, SnakEOil. Very clever, I know.

The old version of django-snakeoil can be found on the ``old`` branch, but
won't be updated.
