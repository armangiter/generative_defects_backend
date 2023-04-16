from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema

from defect_generator.defects.models import Image
from defect_generator.defects.services.image import ImageService


# POST api/defects/types
class ImageApi(APIView):

    class InputSerializer(serializers.Serializer):
        file = serializers.FileField()
        defect_type_id = serializers.IntegerField()

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Image
            fields = ("file", "defect_type")


    @extend_schema(request=InputSerializer)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            ImageService.image_create(
                **serializer.validated_data
            )
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)

    @extend_schema(responses=OutputSerializer)
    def get(self, request):
        query = ImageService.image_list()

        serializer = self.OutputSerializer(query, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

# # GET api/defects/images/
# class ImageListApi(APIView):
    


# GET api/defects/images/{image_id}/
class ImageDetailApi(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Image
            fields = ("file", "defect_type")

    @extend_schema(responses=OutputSerializer)
    def get(self, request, image_id):
        image = ImageService.image_get(id=image_id)

        serializer = self.OutputSerializer(image)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, image_id):
        try:
            ImageService.image_delete(image_id=image_id)
        except Exception as ex:
            return Response(f"Error {ex}", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)


# # DELETE api/defects/image/{image_id}/
# class ImageDeleteApi(APIView):
    
