from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("snakeoil", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="seopath",
            name="meta_tags",
            field=models.JSONField(blank=True, default=dict, verbose_name="meta tags"),
        ),
    ]
