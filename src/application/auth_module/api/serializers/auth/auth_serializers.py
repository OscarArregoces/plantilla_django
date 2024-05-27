from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.response import Response
User = get_user_model()

class LoginSerializers(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(label="username")
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials Passed.")
    