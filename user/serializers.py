from rest_framework_simplejwt import TokenObtainPairSerializer
from rest_framework.serializers import (
        ModelSerializer,
        CharField,
        EmailField,
        ValidationError
)
from rest_framework.validators import validate_password, UniqueValidator

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
        write_only=True, required=True, validators=[validate_password])
    password2 = CharField(write_only=True, required=True)
    email = EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2', 'bio',
                  'cover_photo')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            bio=validated_data['bio'],
            cover_photo=validated_data['cover_photo']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
