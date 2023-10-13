from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
