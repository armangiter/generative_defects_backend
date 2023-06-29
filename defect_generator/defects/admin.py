from django.contrib import admin

from defect_generator.defects.models import (
    DefectModel,
    DefectType,
    Image,
    Result,
    ResultImage,
)


@admin.register(DefectType)
class DefectTypeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "command",
        "defect_model_id",
    )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "defect_type_id", "tuned")
    list_filter = ("defect_type_id", "tuned")


@admin.register(DefectModel)
class DefectModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "file",
    )


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "image",
        "used",
        "defect_type_id",
        "defect_model_id",
    )
    list_filter = ("defect_type_id",)


@admin.register(ResultImage)
class ResultImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "result_id",
        "file",
    )
