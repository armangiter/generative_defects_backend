from rest_framework import serializers


class GenerateInputSerializer(serializers.Serializer):
    image_file = serializers.FileField()
    mask_file = serializers.FileField()
    defect_type_id = serializers.IntegerField()
    defect_model_id = serializers.IntegerField()
    mask_mode = serializers.ChoiceField(
        [("random", "Random"), ("in_paint", "In Paint")]
    )
    number_of_images = serializers.IntegerField()
