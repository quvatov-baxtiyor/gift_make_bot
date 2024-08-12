from django.db.models import Count, Avg, Max
from rest_framework import serializers
from body.models import UserChat, ChatCategory, ChatInitCategory, GiftParticipant
from body.serializers import UserSubscriptionSerializer, GiftSerializer, PlanSerializer
from custom_auth.serializers import CustomUserSerializer


class UserChatSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    plan = serializers.SerializerMethodField()

    def get_plan(self, obj):
        subscription = obj.usersubscription_set.filter(status='active').first()
        return PlanSerializer(subscription.plan).data if subscription else None

    class Meta:
        model = UserChat
        fields = ['id', 'user', 'chat_id', 'chat_type', 'init_date', 'plan']


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
    subscription = UserSubscriptionSerializer(read_only=True)
    gifts = GiftSerializer(many=True, read_only=True)

    def get_subscription(self, obj):
        subscription = obj.usersubscription_set.first()
        return UserSubscriptionSerializer(subscription).data if subscription else None

    def get_gifts(self, obj):
        return GiftSerializer(obj.gift_set.all(), many=True).data

    class Meta:
        model = UserChat
        fields = ['id', 'chat_id', 'chat_type', 'init_date', 'subscription', 'gifts']


class ChannelStatsSerializer(serializers.ModelSerializer):
    subscribers_count = serializers.IntegerField()
    contests_count = serializers.IntegerField()
    avg_reach = serializers.SerializerMethodField()
    max_reach = serializers.SerializerMethodField()

    def get_avg_reach(self, obj):
        completed_gifts = obj.gift_set.filter(status='completed')
        participant_counts = GiftParticipant.objects.filter(gift__in=completed_gifts).values('gift').annotate(
            count=Count('id', distinct=True)
        )
        return participant_counts.aggregate(Avg('count'))['count__avg'] or 0

    def get_max_reach(self, obj):
        completed_gifts = obj.gift_set.filter(status='completed')
        participant_counts = GiftParticipant.objects.filter(gift__in=completed_gifts).values('gift').annotate(
            count=Count('id', distinct=True)
        )
        return participant_counts.aggregate(Max('count'))['count__max'] or 0

    class Meta:
        model = UserChat
        fields = ['subscribers_count', 'contests_count', 'avg_reach', 'max_reach']
