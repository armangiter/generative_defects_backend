from django.db import models

from defect_generator.defects.utils import (
    defect_models_file_generate_upload_path,
    image_file_generate_upload_path,
    inference_images_file_generate_upload_path,
    mask_file_generate_upload_path,
)


class DefectType(models.Model):
    name = models.CharField(max_length=127)

    def __str__(self) -> str:
        return f"{self.id}, {self.name}"


class Image(models.Model):
    file = models.FileField(
        upload_to=image_file_generate_upload_path,
        null=True,
        blank=True,
        max_length=600,
    )
    defect_type = models.ForeignKey(
        DefectType, on_delete=models.CASCADE, related_name="images"
    )

    def __str__(self) -> str:
        return f"{self.id}, {self.file.name}"


class MaskImage(models.Model):
    file = models.FileField(
        upload_to=mask_file_generate_upload_path,
        null=True,
        blank=True,
        max_length=600,
    )
    image = models.ForeignKey(
        Image, related_name="mask_images", on_delete=models.CASCADE
    )
    defect_type = models.ForeignKey(
        DefectType, on_delete=models.CASCADE, related_name="mask_images"
    )

    def __str__(self) -> str:
        return f"{self.id}, {self.file.name}"


class DefectModel(models.Model):
    file = models.FileField(
        upload_to=defect_models_file_generate_upload_path,
        null=True,
        blank=True,
        max_length=600,
    )

    def __str__(self) -> str:
        return f"{self.id}, {self.file.name}"


class Inference(models.Model):
    image = models.ForeignKey(
        Image, related_name="inference_results", on_delete=models.CASCADE
    )
    mask_image = models.ForeignKey(
        MaskImage, related_name="inference_results", on_delete=models.CASCADE
    )
    defect_type = models.ForeignKey(
        DefectType, on_delete=models.CASCADE, related_name="inference_results"
    )
    defect_model = models.ForeignKey(
        DefectModel, on_delete=models.CASCADE, related_name="inference_results"
    )

    def __str__(self) -> str:
        return f"{self.id}"


class TimeStamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class InferenceImage(TimeStamp):
    inference = models.ForeignKey(
        Inference, related_name="inference_images", on_delete=models.CASCADE
    )
    file = models.FileField(
        upload_to=inference_images_file_generate_upload_path,
        null=True,
        blank=True,
        max_length=600,
    )

    def __str__(self) -> str:
        return f"{self.id}"
