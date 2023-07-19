from rest_framework import serializers

from defect_generator.api.utils import inline_serializer

from defect_generator.defects.models import DefectModel, DefectType, Result, ResultImage, Weight
from defect_generator.defects.utils import get_real_url



class GenerateJobOutputSerializer(serializers.ModelSerializer):

    class DefectModelInGenerateJobSerializer(serializers.ModelSerializer):
        class Meta:
            model = DefectModel
            fields = ["id", "name"]

    defect_model = DefectModelInGenerateJobSerializer()

    class DefectTypeInGenerateJobSerializer(serializers.ModelSerializer):
        class WeightInDefectTypeGenerateJobSerializer(serializers.ModelSerializer):

            class Meta:
                model = Weight
                fields = ["id", "file"]
        
            def get_file(self, obj: Weight):
                if bool(obj.file) is True:
                    return get_real_url(obj.file.url)
                return None
        
        weight = WeightInDefectTypeGenerateJobSerializer()

        class Meta:
            model = DefectType
            fields = ["id", "name", "command", "weight"]

        
    defect_type = DefectTypeInGenerateJobSerializer()

    image = serializers.SerializerMethodField()
    mask = serializers.SerializerMethodField()

    class Meta:
        model = Result
        fields = (
            "id",
            "image",
            "mask",
            "defect_type",
            "defect_model",
            "number_of_images",
            "status",
            "user_id",
        )

    def get_image(self, obj: Result):
        if bool(obj.image) is True:
            return get_real_url(obj.image.url)
        return None

    def get_mask(self, obj: Result):
        if bool(obj.mask) is True:
            return get_real_url(obj.mask.url)
        return None

# used for updating a Result
class ResultDetailInputSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Result.STATUS_CHOICES, required=False)
