# Generated by Django 4.1.8 on 2023-05-09 13:21

import defect_generator.defects.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("defects", "0006_defectmodel_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Result",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "defect_model",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="results",
                        to="defects.defectmodel",
                    ),
                ),
                (
                    "defect_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="results",
                        to="defects.defecttype",
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="results",
                        to="defects.image",
                    ),
                ),
                (
                    "mask_image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="results",
                        to="defects.maskimage",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ResultImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "file",
                    models.FileField(
                        blank=True,
                        max_length=600,
                        null=True,
                        upload_to=defect_generator.defects.utils.result_images_file_generate_upload_path,
                    ),
                ),
                (
                    "result",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="result_images",
                        to="defects.result",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.RemoveField(
            model_name="inferenceimage",
            name="inference",
        ),
        migrations.DeleteModel(
            name="Inference",
        ),
        migrations.DeleteModel(
            name="InferenceImage",
        ),
    ]
