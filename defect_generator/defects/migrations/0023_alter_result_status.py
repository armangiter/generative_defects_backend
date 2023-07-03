# Generated by Django 4.2.2 on 2023-07-03 06:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("defects", "0022_result_mask_mode_result_number_of_images"),
    ]

    operations = [
        migrations.AlterField(
            model_name="result",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[("p", "Pending"), ("g", "Generating"), ("f", "Finished")],
                default=None,
                max_length=1,
                null=True,
            ),
        ),
    ]
