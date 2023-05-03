# Generated by Django 4.1.8 on 2023-04-29 12:34

import defect_generator.defects.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("defects", "0002_alter_defectmodel_file_alter_image_file"),
    ]

    operations = [
        migrations.CreateModel(
            name="Inference",
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
                        related_name="inference_results",
                        to="defects.defectmodel",
                    ),
                ),
                (
                    "defect_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="inference_results",
                        to="defects.defecttype",
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="inference_results",
                        to="defects.image",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MaskImage",
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
                    "file",
                    models.FileField(
                        blank=True,
                        max_length=600,
                        null=True,
                        upload_to=defect_generator.defects.utils.mask_file_generate_upload_path,
                    ),
                ),
                (
                    "defect_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mask_images",
                        to="defects.defecttype",
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mask_images",
                        to="defects.image",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="InferenceImages",
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
                    "file",
                    models.FileField(
                        blank=True,
                        max_length=600,
                        null=True,
                        upload_to=defect_generator.defects.utils.inference_images_file_generate_upload_path,
                    ),
                ),
                (
                    "inference",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="inference_images",
                        to="defects.inference",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="inference",
            name="mask_image",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="inference_results",
                to="defects.maskimage",
            ),
        ),
    ]