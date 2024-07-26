from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'reg_date', 'lang', 'balance', 'full_name', 'avatar_url', 'country']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['full_name', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            full_name=validated_data['full_name'],
            password=validated_data['password'],
        )
        return user


class CustomTokenObtainPairSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        full_name = attrs.get('full_name')
        password = attrs.get('password')
        user = authenticate(full_name=full_name, password=password)

        if user is None:
            raise serializers.ValidationError('Invalid credentials')

        refresh = RefreshToken.for_user(user)
        # Include all necessary information in the token payload
        refresh['user_id'] = user.user_id
        refresh['full_name'] = user.full_name

        access_token = refresh.access_token

        data = {
            'refresh': str(refresh),
            'access': str(access_token),
        }

        # Get the requested fields from the query parameters
        fields = self.context['request'].query_params.get('fields')
        if fields:
            fields = fields.split(',')
        else:
            fields = ['user_id', 'reg_date', 'lang', 'balance', 'full_name', 'avatar_url', 'country']
        # Serialize the user data based on requested fields
        data["user_data"] = CustomUserSerializer(user, fields=fields).data

        return data


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ["id"]
