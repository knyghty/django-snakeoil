from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    initial = True

    dependencies: list[tuple[str, str]] = []

    operations = [
        migrations.CreateModel(
            name="SEOPath",
            fields=[
                ("meta_tags", models.JSONField(default=dict, verbose_name="meta tags")),
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
            },
        ),
    ]
