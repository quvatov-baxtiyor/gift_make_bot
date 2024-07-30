from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, serializers
from body.models import UserChat, ChatInitCategory, ChatCategory, UserSubscription, Gift
from body.serializers import UserChatSerializer, ChatInitCategorySerializer, ChatCategorySerializer, GiftSerializer, \
    UserSubscriptionSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Prefetch, Count

from custom_auth.serializers import CustomUserSerializer


class UserChatViewSet(viewsets.ModelViewSet):
    queryset = UserChat.objects.all()
    serializer_class = UserChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=['Channels'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ChatInitCategoryViewSet(viewsets.ModelViewSet):
    queryset = ChatInitCategory.objects.all()
    serializer_class = ChatInitCategorySerializer
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(tags=['Channels'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ChatCategoryViewSet(viewsets.ModelViewSet):
    queryset = ChatCategory.objects.all()
    serializer_class = ChatCategorySerializer
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(tags=['Channels'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Channels'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


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


class UserChatSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = UserChat
        fields = ['id', 'user', 'chat_id', 'chat_type', 'init_date']


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_channels(request):
    user = request.user

    user_chats = UserChat.objects.filter(
        user=user, chat_type__in=['gifting', 'sub']
    ).prefetch_related(
        Prefetch('usersubscription_set', queryset=UserSubscription.objects.select_related('plan')),
        Prefetch('gift_set', queryset=Gift.objects.annotate(
            participants_count=Count('participants', distinct=True)
        )),
    )

    data = []
    for user_chat in user_chats:
        chat_serializer = MyChannelsSerializer(user_chat)
        chat_data = chat_serializer.data

        # Kanal statistikasi (misol uchun)
        chat_data['statistics'] = {
            'subscribers_count': user_chat.subscribers.count(),
            'contests_count': user_chat.gift_set.count(),
        }

        # Kanal rejalari (agar mavjud bo'lsa)
        subscription = user_chat.usersubscription_set.first()
        chat_data['plan'] = {
            'title': subscription.plan.title,
            'price': subscription.plan.price,
            'due_date': subscription.subscription_date + subscription.plan.due,  # Obunaning tugash sanasi
        } if subscription else None

        # Sovg'alar (Gifts)
        gifts_data = []
        for gift in user_chat.gift_set.all():
            gift_data = {
                'id': gift.id,
                'title': gift.title,
                'participants_count': gift.participants_count,
                'status': gift.status,
            }
            gifts_data.append(gift_data)
        chat_data['gifts'] = gifts_data

        data.append(chat_data)

    return Response(data)
