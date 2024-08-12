from datetime import timedelta
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, status
from body.models import UserChat, ChatInitCategory, ChatCategory, UserSubscription, Gift, Transaction, Plan
from body.serializers import UserChatSerializer, ChatInitCategorySerializer, ChatCategorySerializer, \
    UserSubscriptionSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Prefetch, Count
from body.serializers.channels import MyChannelsSerializer


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


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def subscribe_channel(request, channel_id):
    user = request.user
    plan_id = request.data.get('plan_id')  # Frontenddan tanlangan plan ID'si
    try:
        user_chat = UserChat.objects.get(id=channel_id, user=user)
    except UserChat.DoesNotExist:
        return Response({'error': 'Kanal topilmadi.'}, status=status.HTTP_404_NOT_FOUND)

    try:
        plan = Plan.objects.get(id=plan_id, is_active=True)
    except Plan.DoesNotExist:
        return Response({'error': 'Reja topilmadi.'}, status=status.HTTP_404_NOT_FOUND)

    # Mavjud obunani tekshirish
    existing_subscription = UserSubscription.objects.filter(user_chat=user_chat, status='active').first()

    if existing_subscription:
        # Mavjud obuna bor bo'lsa, yangilash
        existing_subscription.plan = plan
        if plan.title == 'Free':  # Free reja bo'lsa, tugash sanasini olib tashlash
            existing_subscription.subscription_end_date = None
        else:
            # Boshqa reja bo'lsa, tugash sanasini hisoblash
            existing_subscription.subscription_end_date = (
                    existing_subscription.subscription_date + timedelta(days=plan.due)
            )
        existing_subscription.save()
        subscription = existing_subscription
    else:
        # Yangi obuna yaratish
        subscription_end_date = None if plan.title == 'Free' else timezone.now() + timedelta(days=plan.due)
        subscription = UserSubscription.objects.create(
            user=user,
            user_chat=user_chat,
            plan=plan,
            subscription_end_date=subscription_end_date,
        )
    # Tranzaksiya yaratish
    if plan.title == 'Free':
        amount = 0
    else:
        amount = plan.price
    Transaction.objects.create(
        user=user,
        amount=-amount,
        transaction_type='subscription'
    )
    serializer = UserSubscriptionSerializer(subscription)
    return Response(serializer.data, status=status.HTTP_200_OK)
