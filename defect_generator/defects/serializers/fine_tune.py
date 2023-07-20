from rest_framework import serializers

from defect_generator.defects.models import (
    FineTune,
    Image,
    Result,
)
from defect_generator.defects.services.fine_tune import FineTuneService
from defect_generator.defects.utils import get_real_url


class FineTuneFilterSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Result.STATUS_CHOICES, required=False)
    user_id = serializers.IntegerField(min_value=1, required=False)


class FineTuneInputSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=FineTune.STATUS_CHOICES)


class _ImageInFineTuneImagesInFineTuneSerializer(serializers.ModelSerializer):
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


class FineTuneOutputSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = FineTune
        fields = (
            "id",
            "name",
            "user_id",
            "status",
            "images",
            "created",
        )

    def get_images(self, obj: FineTune):
        images = FineTuneService.get_related_images(fine_tune=obj)
        return _ImageInFineTuneImagesInFineTuneSerializer(images, many=True).data


class FineTuneDetailInputSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=FineTune.STATUS_CHOICES)


class _ImageInFineTuneImagesInFineTuneDetailSerializer(serializers.ModelSerializer):
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


class FineTuneDetailOutputSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = FineTune
        fields = (
            "id",
            "name",
            "user_id",
            "status",
            "images",
            "created",
        )

    def get_images(self, obj: FineTune):
        images = FineTuneService.get_related_images(fine_tune=obj)
        return _ImageInFineTuneImagesInFineTuneDetailSerializer(images, many=True).data
