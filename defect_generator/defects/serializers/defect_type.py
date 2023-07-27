from rest_framework import serializers

from defect_generator.defects.models import DefectType



class DefectTypeFilterSerializer(serializers.Serializer):
    defect_model_id = serializers.IntegerField(min_value=1)


class DefectTypeInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=127)
    command = serializers.CharField(max_length=512)
    icon_image = serializers.FileField()


class DefectTypeOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefectType
        fields = ("id", "name", "command", "defect_model_id")


class DefectTypeDetailInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=127)
    command = serializers.CharField(max_length=512)


class DefectTypeDetailOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefectType
        fields = ("id", "name", "command")
