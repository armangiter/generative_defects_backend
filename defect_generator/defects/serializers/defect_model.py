from rest_framework import serializers

from defect_generator.defects.models import DefectModel
from defect_generator.defects.services.defect_model import DefectModelService
from defect_generator.defects.utils import get_real_url


class DefectModelInputSerializer(serializers.Serializer):
    file = serializers.FileField()


class DefectModelOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefectModel
        fields = ("id", "name")


class DefectModelDetailOutputSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = DefectModel
        fields = ("id", "name")
