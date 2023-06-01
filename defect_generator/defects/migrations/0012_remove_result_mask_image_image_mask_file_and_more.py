# Generated by Django 4.1.8 on 2023-05-31 14:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("defects", "0011_image_model"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="result",
            name="mask_image",
        ),
        migrations.AddField(
            model_name="image",
            name="mask_file",
            field=models.FileField(blank=True, max_length=600, null=True, upload_to=""),
        ),
        migrations.AlterField(
            model_name="image",
            name="file",
            field=models.FileField(blank=True, max_length=600, null=True, upload_to=""),
        ),
        migrations.DeleteModel(
            name="MaskImage",
        ),
    ]
