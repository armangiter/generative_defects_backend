import django_filters as filters

from defect_generator.defects.models import DefectType, Result


class DefectTypeFilter(filters.FilterSet):
    class Meta:
        model = DefectType
        fields = ("defect_model_id",)


class ResultFilter(filters.FilterSet):
    status = filters.CharFilter(lookup_expr="exact")
    
    class Meta:
        model = Result
        fields = ["status", "user_id"]
