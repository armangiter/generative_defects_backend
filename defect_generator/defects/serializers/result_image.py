from rest_framework import serializers

from defect_generator.defects.models import Image, ResultImage
from defect_generator.defects.utils import get_real_url


class ResultImageInputSerializer(serializers.Serializer):
    file = serializers.ListField(
        child=serializers.FileField(
            max_length=500, allow_empty_file=False, use_url=False
        )
    )
    result_id = serializers.IntegerField()


class ResultImageOutputSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = ResultImage
        fields = ("id", "result_id", "file")

    def get_file(self, obj: Image):
        if bool(obj.file) is True:
            return get_real_url(obj.file.url)
        return None


class ResultImageDetailInputSerializer(serializers.Serializer):
    file = serializers.FileField()
    result_id = serializers.IntegerField()


class ResultImageDetailOutputSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = ResultImage
        fields = ("id", "result_id", "file")

    def get_file(self, obj: Image):
        if bool(obj.file) is True:
            return get_real_url(obj.file.url)
        return None
