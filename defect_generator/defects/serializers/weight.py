from rest_framework import serializers

from defect_generator.defects.models import Weight
from defect_generator.defects.utils import get_real_url


class WeightInputSerializer(serializers.Serializer):
    file = serializers.FileField()


class WeightOutputSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = Weight
        fields = ("id", "file")

    def get_file(self, obj: Weight):
        if bool(obj.file) is True:
            return get_real_url(obj.file.url)
        return None


class WeightDetailOutputSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = Weight
        fields = ("id", "file")

    def get_file(self, obj: Weight):
        if bool(obj.file) is True:
            return get_real_url(obj.file.url)
        return None
