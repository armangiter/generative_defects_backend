from rest_framework import serializers

from defect_generator.api.utils import inline_serializer

from defect_generator.defects.models import DefectModel, Result, ResultImage
from defect_generator.defects.utils import get_real_url
from defect_generator.workers.models import FineTune



class FineTuneJobOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = FineTune
        fields = ("id", "")