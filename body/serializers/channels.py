from rest_framework import serializers
from body.models import UserChat, ChatCategory, ChatInitCategory
from custom_auth.serializers import CustomUserSerializer


class UserChatSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = UserChat
        fields = ['id', 'user', 'chat_id', 'chat_type', 'init_date']


class ChatCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatCategory
        fields = ['id', 'title']


class ChatInitCategorySerializer(serializers.ModelSerializer):
    category = ChatCategorySerializer()

    class Meta:
        model = ChatInitCategory
        fields = ['id', 'chat_id', 'category']


class MyChannelsSerializer(serializers.ModelSerializer):
    subscription = serializers.SerializerMethodField()
    gifts = serializers.SerializerMethodField()

    def get_subscription(self, obj):
        from body.serializers import UserSubscriptionSerializer
        subscription = obj.usersubscription_set.first()
        return UserSubscriptionSerializer(subscription).data if subscription else None

    def get_gifts(self, obj):
        from body.serializers import GiftSerializer
        return GiftSerializer(obj.gift_set.all(), many=True).data

    class Meta:
        model = UserChat
        fields = ['id', 'chat_id', 'chat_type', 'init_date', 'subscription', 'gifts']
