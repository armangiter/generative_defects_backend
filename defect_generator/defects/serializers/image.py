from rest_framework import serializers

from defect_generator.defects.models import Image
from defect_generator.defects.utils import get_real_url


class ImageInputSerializer(serializers.Serializer):
    file = serializers.FileField()
    mask_file = serializers.FileField()
    defect_type_id = serializers.IntegerField()


class ImageOutputSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    mask_file = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ("id", "file", "mask_file", "defect_type")

    def get_file(self, obj: Image):
        if bool(obj.file) is True:
            return get_real_url(obj.file.url)
        return None

    def get_mask_file(self, obj: Image):
        if bool(obj.mask_file) is True:
            return get_real_url(obj.mask_file.url)
        return None


class ImageDetailInputSerializer(serializers.Serializer):
    file = serializers.FileField()
    mask_file = serializers.FileField()
    defect_type_id = serializers.IntegerField()


class ImageDetailOutputSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    mask_file = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ("id", "file", "mask_file", "defect_type")

    def get_file(self, obj: Image):
        if bool(obj.file) is True:
            return get_real_url(obj.file.url)
        return None

    def get_mask_file(self, obj: Image):
        if bool(obj.mask_file) is True:
            return get_real_url(obj.mask_file.url)
        return None
