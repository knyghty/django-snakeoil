from django.db import migrations, models

try:
    from django.db.models import JSONField

    postgres_only = False
except ImportError:
    from django.contrib.postgres.fields import JSONField

    postgres_only = True


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SEOPath",
            fields=[
                ("meta_tags", JSONField(default=dict, verbose_name="meta tags")),
                (
                    "path",
                    models.CharField(
                        max_length=255,
                        primary_key=True,
                        serialize=False,
                        verbose_name="path",
                    ),
                ),
            ],
            options={
                "verbose_name": "SEO path",
                "verbose_name_plural": "SEO paths",
                "required_db_vendor": "postgresql" if postgres_only else None,
            },
        ),
    ]
