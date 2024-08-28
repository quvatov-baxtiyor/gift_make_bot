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

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
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


