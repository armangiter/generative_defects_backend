# Generated by Django 4.2.2 on 2023-06-29 13:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("defects", "0016_remove_defecttype_model_defecttype_defect_model"),
    ]

    operations = [
        migrations.AddField(
            model_name="result",
            name="used",
            field=models.BooleanField(default=False),
        ),
    ]
