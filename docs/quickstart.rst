###########
Quick Start
###########


************
Installation
************

1. ``pip install django-snakeoil``
2. Add ``django.core.context_processors.request`` to
   ``TEMPLATE_CONTEXT_PROCESSORS``
3. Add ``'snakeoil'`` to ``INSTALLED_APPS``


*****
Usage
*****

Inherit your models from ``SeoModel``:

.. code-block:: python

  from snakeoil.models import SeoModel

  class MyModel(SeoModel):
      ...
      def get_absolute_url(self):
          ...

Make sure you have a ``get_absolute_url()`` set - this is how snakeoil knows
its on the page for the model instance.

Run ``manage.py makemigrations`` and ``migrate``.

Stick something like this in your templates:

.. code-block:: html

  {% load snakeoil %}
  {% get_seo_data %}
  <title>{{ seo.head_title }}</title>
  <meta name="description" content="{{ seo.meta_description }}">

Now you can edit your SEO your data per model instance or per URL in the admin
and it will show up on the right pages.
