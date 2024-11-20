from rest_framework import serializers

from accounts.dto_models import SignInUserModel, SignUpUserModel


class SignUpUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def create(self, validated_data):
        return SignUpUserModel(**validated_data)


class SignInUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def create(self, validated_data):
        return SignInUserModel(**validated_data)
