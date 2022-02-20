import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Article",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("meta_tags", JSONField(default=dict, verbose_name="meta tags")),
                ("slug", models.SlugField(unique=True)),
                ("title", models.CharField(max_length=500)),
                (
                    "main_image",
                    models.ImageField(
                        blank=True,
                        height_field="main_image_height",
                        null=True,
                        upload_to="",
                        width_field="main_image_width",
                    ),
                ),
                (
                    "main_image_width",
                    models.PositiveSmallIntegerField(blank=True, null=True),
                ),
                (
                    "main_image_height",
                    models.PositiveSmallIntegerField(blank=True, null=True),
                ),
                (
                    "secondary_image",
                    models.ImageField(blank=True, null=True, upload_to=""),
                ),
                ("content", models.TextField()),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="articles",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False},
        ),
    ]
