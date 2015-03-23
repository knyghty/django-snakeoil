########
Examples
########


**********************
Adding Open Graph data
**********************

Adding arbitrary data is simple, just construct the model however you want:

.. code-block:: python
  from snakeoil.models import SeoModel

  class MySeoModel(SeoModel):
      og_title = models.CharField(max_length=255)
      og_type = models.CharField(max_length=255, default='website')
      ...

      class Meta:
          abstract = True

You don't have to inherit from SeoModel if you don't want the default
head_title and meta_description fields. Your new fields are accessible by their
name, ie. ``{{ seo.og_title }}``.


*****************************
Making life easier for admins
*****************************

It's great that our admins can add SEO data for any object or URL, but we
can make their life even easier by adding sensible defaults. If you're using
class-based views, you can provide a default based on the
``__str__()``/``__unicode__()`` methods of your models by constructing your
base.html like so:

.. code-block:: html
  {% load snakeoil %}
  {% get_seo_data %}
  <head>
      <title>
          {% block title %}{% firstof seo.head_title object %}{% endblock %}
          | My Website
      </title>
      ...
  </head>

Note that even if you override ``context_object_name`` in your view, you can
still access it as ``object`` in the template.

Now we have default values for our objects, but what about our
non-``DetailView`` pages? No problem, just override the block with whatever you want:

.. code-block:: html
  {% block title %}{% firstof seo.head_title 'Home' %}{% endblock %}
