# body/serializers.py
from rest_framework import serializers
from .models import (
    Plan, ChatCategory, User, Chat, UserChat, UserSubscription,
    Gift, GiftCustomLink, GiftPostingChat, GiftSubChat, GiftParticipant,
    Ad, AdView, AdClick
)

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class ChatCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatCategory
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

class UserChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChat
        fields = '__all__'

class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = '__all__'

class GiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gift
        fields = '__all__'

class GiftCustomLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftCustomLink
        fields = '__all__'

class GiftPostingChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftPostingChat
        fields = '__all__'

class GiftSubChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftSubChat
        fields = '__all__'

class GiftParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftParticipant
        fields = '__all__'

class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'

class AdViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdView
        fields = '__all__'

class AdClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdClick
        fields = '__all__'
