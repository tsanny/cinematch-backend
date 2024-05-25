from django.contrib.auth import password_validation as validators
from rest_framework.serializers import (
        ModelSerializer,
        CharField,
        EmailField,
        SerializerMethodField
)
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email

        return token


class RegisterSerializer(ModelSerializer):
    password = CharField(
        write_only=True, required=True, validators=[validators.validate_password])
    email = EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all(), message=
                                    "Email already exists.")]
    )
    username = CharField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all(), message=
                                    "Username already exists.")]
    )
    token = SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'token')
        
    def get_token(self, user):
        refresh = MyTokenObtainPairSerializer.get_token(user)

        return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        
        return user

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
