from rest_framework import serializers

from defect_generator.defects.models import DefectModel


class DefectModelInputSerializer(serializers.Serializer):
    file = serializers.FileField()


class DefectModelOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefectModel
        fields = ("id", "name")


class DefectModelDetailOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefectModel
        fields = ("id", "name")
