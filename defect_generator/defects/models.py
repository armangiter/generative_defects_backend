from django.db import models
from django.conf import settings
from django.db.models import Q, UniqueConstraint

from defect_generator.common.models import TimeStamp
from defect_generator.defects.utils import (
    image_file_generate_upload_path,
    mask_file_generate_upload_path,
    weights_file_generate_upload_path,
    result_images_file_generate_upload_path,
    results_file_generate_upload_path,
    results_mask_file_generate_upload_path,
    zip_file_generate_upload_path,
)


class DefectModel(models.Model):
    name = models.CharField(max_length=127)

    def __str__(self) -> str:
        return f"{self.id}"


class Weight(models.Model):
    file = models.FileField(
        upload_to=weights_file_generate_upload_path,
        null=True,
        blank=True,
        max_length=600,
    )

    def __str__(self) -> str:
        return f"{self.id}"


class DefectType(models.Model):
    name = models.CharField(max_length=127)
    command = models.CharField(max_length=512)
    defect_model = models.ForeignKey(
        DefectModel, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    weight = models.ForeignKey(
        Weight, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )

    def __str__(self) -> str:
        return f"{self.id}, {self.name}"


class Image(models.Model):
    file = models.FileField(
        null=True,
        blank=True,
        max_length=600,
        # upload_to=image_file_generate_upload_path
    )
    mask_file = models.FileField(
        null=True,
        blank=True,
        max_length=600,
        # upload_to=mask_file_generate_upload_path
    )
    defect_type = models.ForeignKey(
        DefectType, on_delete=models.CASCADE, related_name="images"
    )
    model = models.ForeignKey(
        DefectModel,
        on_delete=models.SET_NULL,
        related_name="images",
        null=True,
        blank=True,
        default=None,
    )
    tuned = models.BooleanField(default=False, db_index=True)

    def __str__(self) -> str:
        return f"{self.id}, {self.file.name}"


class Result(TimeStamp):
    STATUS_PENDING = "p"
    STATUS_GENERATING = "g"
    STATUS_FINISHED = "f"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_GENERATING, "Generating"),
        (STATUS_FINISHED, "Finished"),
    )
    # keep track of image sent for generate which is came from inference backbone
    image = models.FileField(
        upload_to=results_file_generate_upload_path,
        null=True,
        blank=True,
        max_length=600,
    )
    mask = models.FileField(
        upload_to=results_mask_file_generate_upload_path,
        null=True,
        blank=True,
        max_length=600,
    )
    defect_type = models.ForeignKey(
        DefectType, on_delete=models.CASCADE, related_name="results"
    )
    defect_model = models.ForeignKey(
        DefectModel, on_delete=models.CASCADE, related_name="results"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="results"
    )
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=None, blank=True, null=True
    )
    number_of_images = models.IntegerField()
    mask_mode = models.CharField(
        choices=[("random", "Random"), ("in_paint", "In Paint")], max_length=8
    )
    generated_at = models.DateTimeField(auto_now=True)
    error = models.TextField(null=True, blank=True, default=None)
    zip_file = models.FileField(
        upload_to=zip_file_generate_upload_path,
        null=True,
        blank=True,
        max_length=600,
    )

    class Meta:
        ordering = (
            "created",
            "id",
        )
        # constraints = [
        #     UniqueConstraint(
        #         fields=["status"],
        #         condition=Q(status="g"),
        #         name="unique_generating_result",
        #     )
        # ]

    def __str__(self) -> str:
        return f"{self.id}"


class ResultImage(models.Model):
    result = models.ForeignKey(
        Result, related_name="result_images", on_delete=models.CASCADE
    )
    file = models.FileField(
        upload_to=result_images_file_generate_upload_path,
        null=True,
        blank=True,
        max_length=600,
    )

    def __str__(self) -> str:
        return f"{self.id}"


class FineTune(TimeStamp):
    STATUS_PENDING = "p"
    STATUS_TUNING = "t"
    STATUS_FINISHED = "f"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_TUNING, "Tuning"),
        (STATUS_FINISHED, "Finished"),
    )
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="fine_tunes"
    )
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=None, blank=True, null=True
    )

    class Meta:
        ordering = (
            "created",
            "id",
        )
        constraints = [
            UniqueConstraint(
                fields=["status"],
                condition=Q(status="t"),
                name="unique_tuning_fine_tune",
            )
        ]
        verbose_name = "Fine Tune"

    def __str__(self) -> str:
        return f"{self.id}"


class FineTuneImage(models.Model):
    fine_tune = models.ForeignKey(
        FineTune, on_delete=models.CASCADE, related_name="fine_tune_images"
    )
    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name="fine_tune_images"
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "Fine Tune Image"

    def __str__(self) -> str:
        return f"{self.id}"
