# Generated by Django 4.1.8 on 2023-05-08 15:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("defects", "0003_inference_maskimage_inferenceimages_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="inferenceimages",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
