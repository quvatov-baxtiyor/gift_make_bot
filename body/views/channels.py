from datetime import timedelta

from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, status
from body.models import UserChat, ChatInitCategory, ChatCategory, UserSubscription, Gift, Plan
from body.serializers import UserChatSerializer, ChatInitCategorySerializer, ChatCategorySerializer, \
    UserSubscriptionSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Prefetch, Count
from body.serializers.channels import MyChannelsSerializer


@swagger_auto_schema(tags=['Channels'])
class UserChatViewSet(viewsets.ModelViewSet):
    queryset = UserChat.objects.all()
    serializer_class = UserChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Foydalanuvchi anonim bo'lsa, bo'sh queryset qaytarish
        if isinstance(self.request.user, AnonymousUser):
            return UserChat.objects.none()
        # Foydalanuvchining o'ziga tegishli kanallarni ko'rishini ta'minlash
        return self.queryset.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        Kanalni o'chirib tashlaydi
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        """
        Yangi kanal qo'shadi (hozircha Telegram integratsiyasi holda)
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@swagger_auto_schema(tags=['Channels'])
class ChatInitCategoryViewSet(viewsets.ModelViewSet):
    queryset = ChatInitCategory.objects.all()
    serializer_class = ChatInitCategorySerializer
    permission_classes = [permissions.IsAdminUser]


@swagger_auto_schema(tags=['Channels'])
class ChatCategoryViewSet(viewsets.ModelViewSet):
    queryset = ChatCategory.objects.all()
    serializer_class = ChatCategorySerializer
    permission_classes = [permissions.IsAdminUser]


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
    """
    Фойдаланувчини каналга обуна қилади ёки обунасини янгилайди.
    """
    user = request.user  # Сўров юборган фойдаланувчи
    plan_id = request.data.get('plan_id')  # Фронтенддан танланган тариф режасининг ID'си

    try:
        user_chat = UserChat.objects.get(id=channel_id, user=user)  # Канални топамиз
    except UserChat.DoesNotExist:
        return Response({'error': 'Kanal topilmadi.'},
                        status=status.HTTP_404_NOT_FOUND)  # Канал топилмаса, хато қайтарамиз

    try:
        plan = Plan.objects.get(id=plan_id, is_active=True)  # Тариф режасини топамиз
    except Plan.DoesNotExist:
        return Response({'error': 'Reja topilmadi.'},
                        status=status.HTTP_404_NOT_FOUND)  # Тариф режаси топилмаса, хато қайтарамиз

    # Мавжуд обунани текшириш
    existing_subscription = UserSubscription.objects.filter(user_chat=user_chat, status='active').first()

    if existing_subscription:
        # Агар мавжуд обуна бўлса, уни янгилаймиз
        existing_subscription.plan = plan
        if plan.title == 'Free':  # Free тариф бўлса, обунанинг тугаш санасини олиб ташлаймиз
            existing_subscription.subscription_end_date = None
        else:
            # Бошқа тариф бўлса, обунанинг янги тугаш санасини ҳисоблаймиз
            existing_subscription.subscription_end_date = (
                    existing_subscription.subscription_date + timedelta(days=plan.due.days)
            )
        existing_subscription.save()
        subscription = existing_subscription
    else:
        # Агар мавжуд обуна бўлмаса, янги обуна яратамиз
        subscription_end_date = None if plan.title == 'Free' else timezone.now() + timedelta(days=plan.due.days)
        subscription = UserSubscription.objects.create(
            user=user,
            user_chat=user_chat,
            plan=plan,
            subscription_end_date=subscription_end_date,
        )

    # Обуна объектини сериализация қилиб, жавоб қайтарамиз
    serializer = UserSubscriptionSerializer(subscription)
    return Response(serializer.data, status=status.HTTP_200_OK)
