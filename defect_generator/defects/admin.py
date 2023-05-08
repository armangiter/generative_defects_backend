from django.contrib import admin

from defect_generator.defects.models import (
    DefectModel,
    DefectType,
    Image,
    Inference,
    InferenceImage,
    MaskImage,
)


@admin.register(DefectType)
class DefectTypeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "file",
        "defect_type_id",
    )
    list_filter = ("defect_type_id",)


@admin.register(DefectModel)
class DefectModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "file",
    )


@admin.register(MaskImage)
class MaskImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "file",
        "image_id",
        "defect_type_id",
    )


@admin.register(Inference)
class InferenceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "image",
        "mask_image_id",
        "defect_type_id",
        "defect_model_id",
    )
    list_filter = ("defect_type_id",)


@admin.register(InferenceImage)
class InferenceImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "inference_id",
        "file",
    )