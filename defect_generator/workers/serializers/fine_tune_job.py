from rest_framework import serializers

from defect_generator.defects.services.fine_tune import FineTuneService

from defect_generator.defects.utils import get_real_url
from defect_generator.defects.models import FineTune, Image


class _ImageInFineTuneImagesInFineTuneJobSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    mask_file = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ("file", "mask_file", "defect_type", "model")

    def get_file(self, obj: Image):
        if bool(obj.file) is True:
            return get_real_url(obj.file.url)
        return None

    def get_mask_file(self, obj: Image):
        if bool(obj.mask_file) is True:
            return get_real_url(obj.mask_file.url)
        return None


class FineTuneJobOutputSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(source="fine_tune_images")

    class Meta:
        model = FineTune
        fields = ("id", "name", "status", "images")

    def get_images(self, obj: FineTune):
        images = FineTuneService.get_related_images(fine_tune=obj)
        return _ImageInFineTuneImagesInFineTuneJobSerializer(images, many=True).data
