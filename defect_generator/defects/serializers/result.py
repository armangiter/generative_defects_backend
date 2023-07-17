from rest_framework import serializers

from defect_generator.api.utils import inline_serializer

from defect_generator.defects.models import DefectModel, Result, ResultImage
from defect_generator.defects.utils import get_real_url


class ResultFilterSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Result.STATUS_CHOICES, required=False)
    user_id = serializers.IntegerField(min_value=1, required=False)


class ResultInputSerializer(serializers.Serializer):
    image = serializers.FileField()
    mask = serializers.FileField()
    defect_type_id = serializers.IntegerField()
    defect_model_id = serializers.IntegerField()


class ResultOutputSerializer(serializers.ModelSerializer):
    class ResultImageSerializer(serializers.ModelSerializer):
        file = serializers.SerializerMethodField()

        class Meta:
            model = ResultImage
            fields = ["id", "file"]

        def get_file(self, obj: ResultImage):
            if bool(obj.file) is True:
                return get_real_url(obj.file.url)
            return None

    result_images = ResultImageSerializer(many=True)

    class DefectModelInResultsSerializer(serializers.ModelSerializer):
        file = serializers.SerializerMethodField()

        class Meta:
            model = DefectModel
            fields = ["id", "name", "file"]

        def get_file(self, obj: DefectModel):
            if bool(obj.file) is True:
                return get_real_url(obj.file.url)
            return None
    defect_model = DefectModelInResultsSerializer()
    
    defect_type = inline_serializer(
        name="defect_type_in_results_serializer",
        fields={
            "id": serializers.IntegerField(),
            "name": serializers.CharField(),
        },
    )

    image = serializers.SerializerMethodField()

    class Meta:
        model = Result
        fields = (
            "id",
            "image",
            "defect_type",
            "defect_model",
            "result_images",
            "status",
            "user_id",
            "error",
            "created",
        )

    def get_image(self, obj: Result):
        if bool(obj.image) is True:
            return get_real_url(obj.image.url)
        return None


# used for updating a Result
class ResultDetailInputSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Result.STATUS_CHOICES, required=False)
    error = serializers.CharField(required=False)


class ResultDetailOutputSerializer(serializers.ModelSerializer):
    class ResultImageSerializer2(serializers.ModelSerializer):
        file = serializers.SerializerMethodField()

        class Meta:
            model = ResultImage
            fields = ["id", "file"]

        def get_file(self, obj: ResultImage):
            return get_real_url(obj.file.url)

    result_images = ResultImageSerializer2(many=True)

    class DefectModelInResultsDetailSerializer(serializers.ModelSerializer):
        file = serializers.SerializerMethodField()

        class Meta:
            model = DefectModel
            fields = ["id", "name", "file"]

        def get_file(self, obj: DefectModel):
            if bool(obj.file) is True:
                return get_real_url(obj.file.url)
            return None
    defect_model = DefectModelInResultsDetailSerializer()

    defect_type = inline_serializer(
        name="defect_type_in_results_detail_serializer",
        fields={
            "id": serializers.IntegerField(),
            "name": serializers.CharField(),
        },
    )

    class Meta:
        model = Result
        fields = (
            "id",
            "image",
            "defect_type",
            "defect_model",
            "result_images",
            "status",
            "user_id",
            "created",
        )
