# Generated by Django 4.1.8 on 2023-05-10 13:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("defects", "0008_remove_resultimage_created_result_created"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="tuned",
            field=models.BooleanField(default=False),
        ),
    ]
