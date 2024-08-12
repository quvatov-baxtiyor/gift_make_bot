from rest_framework import serializers
from body.models import Plan,UserSubscription


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'title', 'price', 'due', 'is_active']


class UserSubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()

    class Meta:
        model = UserSubscription
        fields = ['id', 'user', 'user_chat', 'subscription_date', 'plan', 'status']
        read_only_fields = ['user']

