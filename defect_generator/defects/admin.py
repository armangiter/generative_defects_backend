from django.contrib import admin

from defect_generator.defects.models import (
    DefectModel,
    DefectType,
    Image,
    Result,
    ResultImage,
    FineTune,
    FineTuneImage,
    Weight,
)


@admin.register(DefectType)
class DefectTypeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "command",
        "defect_model_id",
        "weight_id",
    )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "defect_type_id", "tuned")
    list_filter = ("defect_type_id", "tuned")


@admin.register(DefectModel)
class DefectModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )


@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "file",
    )


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "defect_type_id",
        "defect_model_id",
        "status",
        "number_of_images",
        "mask_mode",
        "error",
    )
    list_filter = ("user_id", "defect_type_id", "defect_model_id")


@admin.register(ResultImage)
class ResultImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "result_id",
        "file",
    )
    list_filter = ("result_id",)


@admin.register(FineTune)
class FineTuneAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "status",
    )
    list_filter = ("status",)


@admin.register(FineTuneImage)
class FineTuneImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "fine_tune_id",
        "image_id",
    )
    list_filter = ("fine_tune_id",)
