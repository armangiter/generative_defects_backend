from django.contrib import admin

from defect_generator.defects.models import DefectModel, DefectType, Image

@admin.register(DefectType)
class DefectTypeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )


@admin.register(Image)
class DefectTypeAdmin(admin.ModelAdmin):
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