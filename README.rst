django-snakeoil
===============

django-snakeoil provides SEO data (meta description, etc.) to your templates.
You can associate data with model instances or for any URL on your site.


Features
--------

* Fast. Data for objects doesn't require any extra database queries.
* Flexible. Associate data with any URL.
* Extensible. Provide your own model with your own fields.


Installation
------------

1. `pip install django-snakeoil`
2. Add request to your context processors::

        from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
        TEMPLATE_CONTEXT_PROCESSORS = TCP + ('django.core.context_processors.request',)
3. Add 'snakeoil' to your INSTALLED_APPS


Configuration
-------------

By default, django-snakeoil provides an abstract base model,
`snakeoil.models.SeoModel`, that provides two fields: `head_title` and
`meta_description`. If that's all you need, simply inherit the models you
wish to associate SEO data with from this model and define a get_absolute_url()
method for each model.

If you want to provide your own fields, create your own abstract base model
and inherit your objects from this. Then set `SNAKEOIL_MODEL` to your model
in your settings file. For example:

my_app/models.py
::
    class MyData(models.Model):
        my_field = models.CharField(...)

        class Meta:
            abstract = True

        def get_absolute_url(self):
            ...

settings.py
::
    SNAKEOIL_MODEL = 'my_app.models.MyData'


Usage
-----

A template tag is provided to access the data in your templates. This can
be used on a template by template basis, or included in your `base.html` to
work everywhere:
::
    {% load snakeoil %}
    {% get_seo_data %}
    <title>{{ seo.head_title }}</title>
    <meta name="description" content="{{ seo.meta_description }}">

You can also use {% get_seo_data as my_variable %} if you'd like a different
variable name to use in your template.


Credits
-------

Thanks to kezabelle for the name.
