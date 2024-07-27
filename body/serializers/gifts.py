from rest_framework import serializers
from body.models import Gift, GiftSubChats, GiftPostingChats, GiftCustomLinks, GiftParticipant
from custom_auth.serializers import CustomUserSerializer


class GiftSerializer(serializers.ModelSerializer):
    user_id = CustomUserSerializer(read_only=True)
    post_type = serializers.ChoiceField(choices=Gift.POST_TYPE_CHOICES)

    class Meta:
        model = Gift
        fields = '__all__'
        read_only_fields = ['user_id']


class GiftCustomLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftCustomLinks
        fields = ['id', 'gift', 'url']


class GiftPostingChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftPostingChats
        fields = ['id', 'gift', 'chat']


class GiftSubChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftSubChats
        fields = ['id', 'gift', 'chat']


class GiftParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftParticipant
        fields = ['id', 'gift', 'date', 'is_winner', 'status']
