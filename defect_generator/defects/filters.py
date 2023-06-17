import django_filters

from defect_generator.defects.models import DefectType


class DefectTypeFilter(django_filters.FilterSet):
    class Meta:
        model = DefectType
        fields = ("defect_model_id",)
