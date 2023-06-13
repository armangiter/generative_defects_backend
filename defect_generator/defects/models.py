from django.db import models

from defect_generator.defects.utils import (
    defect_models_file_generate_upload_path,
    result_images_file_generate_upload_path,
    results_file_generate_upload_path,
)


class DefectType(models.Model):
    name = models.CharField(max_length=127)
    command = models.CharField(max_length=512)

    def __str__(self) -> str:
        return f"{self.id}, {self.name}"


class DefectModel(models.Model):
    name = models.CharField(max_length=127)
    file = models.FileField(
        upload_to=defect_models_file_generate_upload_path,
        null=True,
        blank=True,
        max_length=600,
    )

    def __str__(self) -> str:
        return f"{self.id}, {self.file.name}"


class Image(models.Model):
    file = models.FileField(
        null=True,
        blank=True,
        max_length=600,
    )
    mask_file = models.FileField(
        null=True,
        blank=True,
        max_length=600,
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


class TimeStamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Result(TimeStamp):
    # keep track of image sent for generate which is came from inference backbone
    image = models.FileField(
        upload_to=results_file_generate_upload_path,
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
