###############
Reference Guide
###############


************
Installation
************

1. ``pip install django-snakeoil``
2. Add request to your context processors::
  .. code-block:: python
    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
    TEMPLATE_CONTEXT_PROCESSORS = TCP +
    ('django.core.context_processors.request',)
3. Add ``'snakeoil'`` to your INSTALLED_APPS


*************
Configuration
*************

Snakeoil takes a single configuration option.

Set ``SNAKEOIL_MODEL`` to an abstract model containing the fields you wish to
have. By default, this model is:

.. code-block:: python
  class SeoModel(models.Model):
      head_title = models.CharField(blank=True, max_length=55)
      meta_description = models.TextField(blank=True, max_length=160)

      class Meta:
          abstract = True

Make sure you set ``abstract = True``. Feel free to inherit from this model if
 you just want to add more fields.


*****
Usage
*****

Setting up your data
====================

Model instances
---------------

To attach SEO data to your model instances, inherit your models from
``snakeoil.models.SeoModel``, or from your own model if you're overriding
``SNAKEOIL_MODEL``.

Make sure you set a ``get_absolute_url()`` function on your model. This is how
snakeoil knows its on the page for the model instance.

Make sure you run ``manage.py makemigrations`` and ``manage.py migrate`` to
update your database with the new fields.

URLs
----

You shouldn't have to do anything special to attach SEO data to an arbitrary
URL. Just make sure to run ``manage.py migrate`` and you can add SEO data for
your URLs in the admin. Note that if snakeoil finds SEO data for a model
instance at the same URL, it won't look for URL data to save queries. Put
simply, model instance SEO data overrides URL SEO data.

Accessing your data from templates
==================================

Now that you have your data, you want to get it in your templates.

The simplest way is to simply add everything once in your ``base.html``:

.. code-block:: html

  {% load snakeoil %}
  {% get_seo_data %}
  <title>{{ seo.head_title }}</title>
  <meta name="description" content="{{ seo.meta_description }}">

Of course, if you're using your own model, replace these with your own fields.

It might be useful to provide sensible defaults, such as:

.. code-block:: html

  <title>{% firstof seo.head_title object.title %} - My Site</title>

If you want to name your variable something else, maybe because you're already
using seo for something else, or are using snakeoil for non-SEO data, the
``{% get_seo_data %}`` tag takes an optional ``as`` keyword.

.. code-block:: html

  {% get_seo_data as my_var %}
  <title>{{ my_var.head_title }}</title>

Optional admin nicety
=====================

If you get annoyed that the field show at the top of the field list, inherit
your ``AdminModel``'s from ``snakeoil.admin.SeoAdmin`` and your SEO fields will
be moved to the bottom. This likely won't work if you customise the fields or
fieldsets in the ``ModelAdmin`` yourself.
