# Generated by Django 4.2.2 on 2023-07-19 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("defects", "0026_weight_remove_defectmodel_file_defecttype_weight"),
    ]

    operations = [
        migrations.AddField(
            model_name="result",
            name="weight",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="results",
                to="defects.weight",
            ),
        ),
    ]
