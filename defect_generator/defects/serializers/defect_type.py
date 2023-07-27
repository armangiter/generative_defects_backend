from rest_framework import serializers

from defect_generator.defects.models import DefectType
from defect_generator.defects.utils import get_real_url



class DefectTypeFilterSerializer(serializers.Serializer):
    defect_model_id = serializers.IntegerField(min_value=1)


class DefectTypeInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=127)
    command = serializers.CharField(max_length=512)
    icon_image = serializers.FileField()


class DefectTypeOutputSerializer(serializers.ModelSerializer):
    icon_image = serializers.SerializerMethodField()    

    class Meta:
        model = DefectType
        fields = ("id", "name", "command", "defect_model_id", "icon_image")

    def get_icon_image(self, obj: DefectType):
        if bool(obj.icon_image) is True:
            return get_real_url(obj.icon_image.url)
        return None


class DefectTypeDetailInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=127)
    command = serializers.CharField(max_length=512)


class DefectTypeDetailOutputSerializer(serializers.ModelSerializer):
    icon_image = serializers.SerializerMethodField() 

    class Meta:
        model = DefectType
        fields = ("id", "name", "command", "icon_image")

    def get_icon_image(self, obj: DefectType):
        if bool(obj.icon_image) is True:
            return get_real_url(obj.icon_image.url)
        return None
