from django.contrib import admin

from defect_generator.defects.models import DefectType, Image

@admin.register(DefectType)
class DefectTypeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )


@admin.register(Image)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "file",
        "defect_type_id",
    )
    list_filter = ("defect_type_id",)