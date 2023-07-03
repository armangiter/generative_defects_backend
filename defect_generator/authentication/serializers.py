from django.contrib.auth import get_user_model

from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()


class UserSignupInputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"message": "entered passwords does not match."}
            )
        return attrs


class CurrentUserOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "is_admin")


class LoginInputSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs[self.username_field] = attrs[self.username_field].lower()
        return super().validate(attrs)
