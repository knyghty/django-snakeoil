=====
Usage
=====

There are several ways to use snakeoil.

Global metadata
===============

Usually, you will have some metadata that will be the same on every page,
or at least a majority of them. You can set these in your ``settings.py``::

    SNAKEOIL_DEFAULT_TAGS={
        "default": [
            {"name": "author", "content": "Tom Carrick"},
            {"property": "og:site_name", "content": "My Website"},
            {"property": "og:type", "content": "website"}
        ]
        "eo": [
            {"property": "og:site_name", "content": "Mia Ratejo"},
        ]
    }

.. note::
    The ``default`` key here is for the language. If you're not using
    internationalization, you need only use the ``default`` key.

This will set the Open Graph site name property to ``Mia Ratejo`` if the
page is requested in Esperanto, or ``My Website`` for any other language.
Additionally, the ``meta author`` tag will be set to ``Tom Carrick`` on
every page.

It's possible to set both the meta ``name`` and ``property`` for the same
tag::

    {
        "default": [
            {
                "name": "description",
                "property": "og:description",
                "content": "My meta description.",
            }
        ]

Per-object metadata
===================

Metadata can be set and overridden per-object.

First, inherit your model from ``SEOModel``::

    from snakeoil.models import SEOModel

    class MyModel(SEOModel):
        title = models.CharField(max_length=200)
        author = models.ForeignKey(User, on_delete=models.CASCADE)
        main_image = models.Imagefield()

        @property
        def author_name(self):
            return self.author.get_full_name()


Then you can build a JSON object (perhaps in a code-editor) and add this
into the ``meta_tags`` field of the object in the Django Admin, or with
code. For example:

.. code-block:: JSON

    {
        "default": [
            {"property": "og:type", "content": "article"}
        ]
    }

This will override the type from ``website`` (defined in the global config)
to ``article``.

Setting metadata from object attributes
---------------------------------------

You can also set metadata from object attributes with the ``attribute``
key::

    {
        "default": [
            {"name": "author", "attribute": "author"},
            {"property": "og:image", "attribute": "main_image"},
            {"property": "og:title", "attribute": "title"}
        ]
    }

For images using ``ImageField`` in an ``og:image``, this will automatically
populate the ``og:image:width`` and ``og:image:height`` properties.

Per-URL metadata
================

Sometimes you don't have an object, or can't add anything to it, if for
example you're using ``django.contrib.flatpages`` or are using static views.
For this, you can use the ``SEOPath`` model, added to the Django admin.

Using static files
==================

You can also get files by their static path. However, this won't
auatomatically add ``og:image:width`` and ``og:image:height`` properties,
so these need to be added manually if needed::

    {
        "default": [
            {"property": "og:image", "static": "img/default_image.jpg"},
            {"property": "og:image:width", "content": "600"},
            {"property": "og:image:height", "content": "480"},
        ]
    }
