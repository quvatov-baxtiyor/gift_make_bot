from rest_framework import serializers
from body.models import UserChat
from custom_auth.serializers import CustomUserSerializer


class UserChatSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = UserChat
        fields = ['id', 'user', 'chat_id', 'chat_type', 'init_date']


from rest_framework import serializers
from body.models import ChatInitCategory, ChatCategory


class ChatCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatCategory
        fields = ['id', 'title']


class ChatInitCategorySerializer(serializers.ModelSerializer):
    category = ChatCategorySerializer()

    class Meta:
        model = ChatInitCategory
        fields = ['id', 'chat_id', 'category']
