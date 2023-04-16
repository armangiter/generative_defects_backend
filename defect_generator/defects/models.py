from django.db import models

from defect_generator.defects.utils import file_generate_upload_path


class DefectType(models.Model):
    name = models.CharField(max_length=127)

    def __str__(self) -> str:
        return f"{self.id}, {self.name}"


class Image(models.Model):
    file = models.FileField(
        upload_to=file_generate_upload_path,
        null=True,
        blank=True,
        max_length=600,
    )
    defect_type = models.ForeignKey(
        DefectType, on_delete=models.CASCADE, related_name="images"
    )

    def __str__(self) -> str:
        return f"{self.id}, {self.file.name}"


class DefectModel(models.Model):
    file = models.FileField()

    def __str__(self) -> str:
        return f"{self.id}, {self.file.name}"