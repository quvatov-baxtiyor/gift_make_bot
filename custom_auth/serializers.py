from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from django.contrib.auth.models import update_last_login
from custom_auth.models import CustomUser
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'reg_date', 'lang', 'balance', 'full_name', 'avatar_url', 'country']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    user_id = serializers.IntegerField(write_only=True, required=True)
    full_name = serializers.CharField(max_length=255, required=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'user_id',
            'full_name',
            'password',
            'reg_date',
            'lang',
            'country',
            'is_admin',
            'is_active',
            'is_staff'
        ]

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        password = validated_data.pop('password')
        full_name = validated_data.pop('full_name')

        # Ensure that user_id and full_name are unique
        if CustomUser.objects.filter(user_id=user_id).exists():
            raise serializers.ValidationError({'user_id': 'User ID already exists.'})
        if CustomUser.objects.filter(full_name=full_name).exists():
            raise serializers.ValidationError({'full_name': 'Full name already exists.'})

        user = CustomUser(
            user_id=user_id,
            full_name=full_name,
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user
    


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims if needed
        token['user_id'] = user.user_id
        token['full_name'] = user.full_name
        return token

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class AccessRefreshSerializer(TokenRefreshSerializer):
    def validate(self, data):
        data = super().validate(data)
        access_token_instance = AccessToken(data['access'])
        user_id = access_token_instance['user_id']
        user = get_object_or_404(User, uuid = user_id)
        update_last_login(None, user)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ["id"]
