from django.db import migrations

try:
    from django.db.models import JSONField

except ImportError:
    from django.contrib.postgres.fields import JSONField


class Migration(migrations.Migration):

    dependencies = [
        ("snakeoil", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="seopath",
            name="meta_tags",
            field=JSONField(blank=True, default=dict, verbose_name="meta tags"),
        ),
    ]
