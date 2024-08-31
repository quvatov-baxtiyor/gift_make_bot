from aiogram.enums import ChatMemberStatus
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions
from body.models import GiftSubChats, GiftCustomLinks, GiftParticipant
from body.serializers import GiftSerializer, GiftPostingChatsSerializer, GiftCustomLinksSerializer, \
    GiftSubChatsSerializer, GiftParticipantSerializer
from django.utils import timezone
from celery import shared_task
from body.models import Gift, GiftPostingChats
from django.contrib.auth import get_user_model

from bot import bot

User = get_user_model()


@swagger_auto_schema(tags=['Gifts'])
class GiftViewSet(viewsets.ModelViewSet):
    queryset = Gift.objects.all()
    serializer_class = GiftSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(user_id=self.request.user)
        else:
            return Gift.objects.none()


@shared_task
def check_and_post_contests():
    now = timezone.now()
    gifts = Gift.objects.filter(status='pending', started_date__lte=now, end_date__gte=now)

    for gift in gifts:
        # Konkurs vaqtiga yetganligini tekshiramiz
        if gift.started_date <= now <= gift.end_date:
            post_gift_to_channel(gift)


def check_bot_is_admin(chat):
    # Bot adminligini tekshirish
    chat_member = bot.get_chat_member(chat_id=chat.chat.chat_id, user_id=bot.id)
    return chat_member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]


def post_gift_to_channel(gift):
    # Kanalga post qilish logikasi
    for chat in GiftPostingChats.objects.filter(gift=gift):
        if check_bot_is_admin(chat):
            # Telegram API orqali post qilish logikasi
            text = f"Konkurs boshlandi: {gift.title}\nQo'shimcha ma'lumotlar: {gift.description}"
            bot.send_message(chat_id=chat.chat.chat_id, text=text)
            # Konkurs statusini yangilash
            gift.status = 'active'
            gift.save()


@swagger_auto_schema(tags=['Gifts'])
class GiftCustomLinksViewSet(viewsets.ModelViewSet):
    queryset = GiftCustomLinks.objects.all()
    serializer_class = GiftCustomLinksSerializer
    permission_classes = [permissions.IsAuthenticated]


@swagger_auto_schema(tags=['Gifts'])
class GiftPostingChatsViewSet(viewsets.ModelViewSet):
    queryset = GiftPostingChats.objects.all()
    serializer_class = GiftPostingChatsSerializer
    permission_classes = [permissions.IsAuthenticated]


@swagger_auto_schema(tags=['Gifts'])
class GiftSubChatsViewSet(viewsets.ModelViewSet):
    queryset = GiftSubChats.objects.all()
    serializer_class = GiftSubChatsSerializer
    permission_classes = [permissions.IsAuthenticated]


@swagger_auto_schema(tags=['Gifts'])
class GiftParticipantViewSet(viewsets.ModelViewSet):
    queryset = GiftParticipant.objects.all()
    serializer_class = GiftParticipantSerializer
    permission_classes = [permissions.IsAuthenticated]
