import random
from datetime import datetime
import telegram
from django.conf import settings
from django.core.exceptions import BadRequest
from lazr.restfulclient.errors import Unauthorized
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.db.models import Count
from telegram import Bot

from body.models import Gift, GiftCustomLinks, GiftPostingChats, GiftSubChats, GiftParticipant, UserChat
from body.serializers import (
    GiftSerializer, GiftCustomLinksSerializer, GiftParticipantSerializer, UserChatSerializer
)


class MyContestsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        # Foydalanuvchi tomonidan yaratilgan konkurslarni olish
        user_contests = Gift.objects.filter(user_id=request.user)

        # Har bir konkurs uchun ishtirokchilar sonini qo'shish
        contests_with_participants = user_contests.annotate(participants_count=Count('participants'))

        serializer = GiftSerializer(contests_with_participants, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        # Konkursni batafsil ma'lumotlarini olish
        contest = Gift.objects.get(pk=pk, user_id=request.user)
        serializer = GiftSerializer(contest)
        return Response(serializer.data)

    def create(self, request):
        # Yangi konkurs yaratish
        serializer = GiftSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        # Konkursni yangilash
        contest = Gift.objects.get(pk=pk, user_id=request.user)
        serializer = GiftSerializer(contest, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        # Konkursni o'chirish
        contest = Gift.objects.get(pk=pk, user_id=request.user)
        contest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def gift_settings(self, request, pk=None):
        # Konkurs sovg'alarini boshqarish
        gifts = Gift.objects.filter(contest_id=pk, user_id=request.user)
        serializer = GiftSerializer(gifts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def custom_links(self, request, pk=None):
        # Konkurs uchun maxsus havolalarni boshqarish
        links = GiftCustomLinks.objects.filter(gift_id=pk)
        serializer = GiftCustomLinksSerializer(links, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def posting_chats(self, request, pk=None):
        # E'lon qilish kanallarini boshqarish
        chats = GiftPostingChats.objects.filter(gift_id=pk)
        serializer = UserChatSerializer(chats, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def sub_chats(self, request, pk=None):
        # Obuna kanallarini boshqarish
        chats = GiftSubChats.objects.filter(gift_id=pk)
        serializer = UserChatSerializer(chats, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def create_gift(self, request, pk=None):
        contest = get_object_or_404(Gift, post_id=pk, user_id=request.user)
        serializer = GiftSerializer(data=request.data, context={'contest': contest})

        if serializer.is_valid():
            # Ma'lumotlarni to'liqligi va to'g'riligini tekshirish (qo'shimcha tekshiruvlar qo'shish mumkin)
            if not all([
                request.data.get('title'),
                request.data.get('post_type'),
                # ... boshqa kerakli maydonlar
            ]):
                return Response({'error': 'Barcha maydonlar to\'ldirilishi shart.'}, status=status.HTTP_400_BAD_REQUEST)

            gift = serializer.save()

            # Konkurs postini yaratish va uni tanlangan kanallarga yuborish
            try:
                bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
                for posting_chat in contest.giftpostingchats_set.all():
                    chat_id = posting_chat.chat.chat_id
                    # post_type ga qarab turli xil kontent yuborish
                    if gift.post_type == 'text':
                        bot.send_message(chat_id=chat_id, text=gift.title)
                    elif gift.post_type == 'image':
                        bot.send_photo(chat_id=chat_id, photo=gift.image)  # image maydoni bor deb faraz qilamiz
                    # ... boshqa post turlari uchun logikani qo'shish
            except telegram.error.TelegramError as e:
                return Response({'error': f'Telegram xatosi: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put', 'patch'])
    def update_gift(self, request, pk=None, gift_pk=None):
        # Sovg'ani yangilash
        gift = get_object_or_404(Gift, pk=gift_pk, post_id=pk, user_id=request.user)
        serializer = GiftSerializer(gift, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_gift(self, request, pk=None, gift_pk=None):
        # Sovg'ani o'chirish
        gift = get_object_or_404(Gift, pk=gift_pk, post_id=pk, user_id=request.user)
        gift.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['put', 'patch'])
    def update_gift_settings(self, request, pk=None, gift_pk=None):
        gift = get_object_or_404(Gift, pk=pk, user_id=request.user)
        self.check_object_permissions(request, gift)  # Foydalanuvchi huquqini tekshirish

        allowed_fields = ['title', 'button_text', 'winners_count', 'captcha']
        if not any(field in request.data for field in allowed_fields):
            raise ValidationError("Hech qanday sozlama o'zgartirilmadi.")

        serializer = GiftSerializer(gift, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def determine_winners(self, request, pk=None):
        contest = get_object_or_404(Gift, pk=pk, user_id=request.user)

        if contest.status != 'active':
            raise ValidationError("Faol bo'lmagan konkurs uchun g'oliblarni aniqlab bo'lmaydi.")

        participants = GiftParticipant.objects.filter(gift=contest, status='participating')

        if contest.result_calculate_type == 'by_date':
            if not contest.result_calculate_date:
                raise ValidationError("G'oliblarni aniqlash sanasi belgilanmagan.")
            if contest.result_calculate_date > datetime.now():
                raise ValidationError("G'oliblarni aniqlash sanasi hali kelmagan.")

        winners_count = contest.winners_count
        if winners_count > participants.count():
            winners_count = participants.count()

        if contest.result_calculate_type == 'by_manual':
            # Qo'lda tanlash uchun ishtirokchilar ro'yxatini qaytarish
            serializer = GiftParticipantSerializer(participants, many=True)
            return Response(serializer.data)

        # G'oliblarni tasodifiy tanlash
        winners = random.sample(list(participants), winners_count)

        for winner in winners:
            winner.is_winner = True
            winner.status = 'winner'
            winner.save()

        contest.status = 'completed'
        contest.save()

        return Response({'message': f'{winners_count} ta g\'olib aniqlandi.'})

    @action(detail=True, methods=['post'])
    def announce_winners(self, request, pk=None):
        contest = get_object_or_404(Gift, pk=pk, user_id=request.user)

        if contest.status != 'completed':
            raise ValidationError("Faqat yakunlangan konkurslar uchun g'oliblarni e'lon qilish mumkin.")

        winners = GiftParticipant.objects.filter(gift=contest, is_winner=True)

        # Telegram botni sozlash
        bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)

        for winner in winners:
            # Telegramda xabar yuborish
            if winner.user.telegram_chat_id:  # Telegram chat ID mavjudligini tekshirish
                message = f"Tabriklaymiz, {winner.user.username}! Siz {contest.title} konkursida g'olib bo'ldingiz!"
                try:
                    bot.send_message(chat_id=winner.user.telegram_chat_id, text=message)
                except telegram.error.TelegramError as e:
                    print(f"Telegram xatosi: {e}")

    @action(detail=False, methods=['post'])  # detail=False, chunki bu action alohida obyektga bog'liq emas
    def connect_channel(self, request):
        """
        Kanalni botga ulaydi.
        """
        user = request.user
        channel_link = request.data.get('channel_link')

        try:
            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            chat = bot.get_chat(channel_link)

            # Kanal mavjudligini va turini tekshirish
            if not chat.type in ['channel', 'supergroup']:
                return Response({'error': 'Faqat kanallar yoki superguruhlarni ulash mumkin.'},
                                status=status.HTTP_400_BAD_REQUEST)

            chat_id = chat.id

            # Bot administrator ekanligini tekshirish
            admins = bot.get_chat_administrators(chat_id)
            bot_is_admin = any(admin.user.is_bot and admin.user.id == bot.id for admin in admins)
            if not bot_is_admin:
                return Response({'error': 'Botni kanalga admin qiling.'}, status=status.HTTP_400_BAD_REQUEST)

            # Kanalni saqlash
            user_chat, created = UserChat.objects.get_or_create(
                user=user,
                chat_id=chat_id,
                defaults={'chat_type': 'gifting'}
            )
            if not created:
                return Response({'error': 'Kanal allaqachon biriktirilgan.'}, status=status.HTTP_400_BAD_REQUEST)

            # Kanal ma'lumotlarini menejerlarga yuborish (ixtiyoriy)
            # ...

            serializer = UserChatSerializer(user_chat)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except BadRequest:
            return Response({'error': 'Kanal havolasi noto\'g\'ri.'}, status=status.HTTP_400_BAD_REQUEST)
        except Unauthorized:
            return Response({'error': 'Bot kanalga qo\'shila olmadi. Iltimos, botni admin qiling.'},
                            status=status.HTTP_400_BAD_REQUEST)
        except telegram.error.TelegramError as e:
            return Response({'error': f'Telegram xatosi: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
