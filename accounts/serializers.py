from rest_framework import serializers
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'password1',
            'password2',
            'full_name'
        )

    def save(self):
        validated_data = self.validated_data
        if validated_data['password1'] != validated_data['password2']:
            return "Passwords do not match"

        validated_data['password'] = validated_data['password1']

        del validated_data['password1']
        del validated_data['password2']

        if CustomUser.objects.filter(email=validated_data['email']).exists():
            return "Email already exists"

        user = CustomUser.objects._create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'full_name',
        )
