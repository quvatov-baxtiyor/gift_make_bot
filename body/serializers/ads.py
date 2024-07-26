from rest_framework import serializers
from body.models import Ad, AdView, AdClick
from custom_auth.serializers import CustomUserSerializer

class AdSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Ad
        fields = '__all__'


class AdViewSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = AdView
        fields = '__all__'


class AdClickSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = AdClick
        fields = '__all__'
