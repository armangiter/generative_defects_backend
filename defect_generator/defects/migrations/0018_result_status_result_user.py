# Generated by Django 4.2.2 on 2023-07-01 15:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("defects", "0017_result_used"),
    ]

    operations = [
        migrations.AddField(
            model_name="result",
            name="status",
            field=models.CharField(
                choices=[("p", "Pending"), ("g", "Generating"), ("f", "Finished")],
                default="p",
                max_length=1,
            ),
        ),
        migrations.AddField(
            model_name="result",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="results",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
