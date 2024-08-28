import random
from datetime import datetime
import telegram
from django.conf import settings
from django.core.exceptions import BadRequest
from lazr.restfulclient.errors import Unauthorized
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

from body.models import Gift, GiftPostingChats, GiftSubChats, GiftParticipant, UserChat
from body.serializers import (
    GiftSerializer, GiftParticipantSerializer, UserChatSerializer
)


class MyContestsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def create_contest(self, request):
        """
        Янги танлов яратади ва уни бириктирилган каналларга жойлаштиради
        """
        serializer = GiftSerializer(data=request.data)
        if serializer.is_valid():
            # Танлов параметрларини текшириш ва тўлдириш
            contest_data = serializer.validated_data
            contest_data['user_id'] = request.user  # Танловни яратган фойдаланувчи
            contest_data['status'] = 'draft'  # Янги танлов "draft" ҳолатида бўлади

            # result_calculate_type'га қараб қўшимча текширувлар
            if contest_data['result_calculate_type'] == 'by_date':
                if not contest_data.get('result_calculate_date'):
                    raise ValidationError("Автоматик якунлаш учун санани киритинг.")
            elif contest_data['result_calculate_type'] == 'by_participants_count':
                if not contest_data.get('result_calculate_participant_count'):
                    raise ValidationError("Иштирокчилар сони бўйича якунлаш учун иштирокчилар сонини киритинг.")

            # Танловни яратиш
            contest = Gift.objects.create(**contest_data)

            # Эълон қилиш ва обуна каналларини бириктириш
            posting_chat_ids = request.data.get('posting_chat_ids', [])
            sub_chat_ids = request.data.get('sub_chat_ids', [])
            for chat_id in posting_chat_ids:
                user_chat = get_object_or_404(UserChat, chat_id=chat_id, user=request.user)
                GiftPostingChats.objects.create(gift=contest, chat=user_chat)
            for chat_id in sub_chat_ids:
                user_chat = get_object_or_404(UserChat, chat_id=chat_id, user=request.user)
                GiftSubChats.objects.create(gift=contest, chat=user_chat)

            return Response(GiftSerializer(contest).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def start_contest(self, request, pk=None):
        """
        Танловни бошлайди ва танлов постини каналларга жойлаштиради
        """
        contest = get_object_or_404(Gift, pk=pk, user_id=request.user)

        if contest.status != 'draft':
            raise ValidationError("Фақат 'draft' ҳолатидаги танловни бошлаш мумкин.")

        # Танлов постини яратиш ва уни каналларга жойлаш
        try:
            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            for posting_chat in contest.giftpostingchats_set.all():
                chat_id = posting_chat.chat.chat_id

                # Inline tugma qo'shish (webapp uchun)
                keyboard = [[InlineKeyboardButton("Конкурсга қатнашиш", url="https://YOUR_WEBAPP_URL")]]
                reply_markup = InlineKeyboardMarkup(keyboard)

                # post_type'га қараб турли хил контент юбориш
                if contest.post_type == 'text':
                    message = bot.send_message(chat_id=chat_id, text=contest.title, reply_markup=reply_markup)
                elif contest.post_type == 'image':
                    # image maydoni bor deb faraz qilamiz
                    message = bot.send_photo(chat_id=chat_id, photo=contest.image, caption=contest.title,
                                             reply_markup=reply_markup)

                # Танловнинг post_id'сини сақлаш
                contest.post_id = message.message_id
                contest.save()

        except telegram.error.TelegramError as e:
            return Response({'error': f'Telegram xatosi: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Танлов ҳолатини 'active'га ўзгартириш
        contest.status = 'active'
        contest.save()

        return Response(GiftSerializer(contest).data)

    @action(detail=True, methods=['post'])
    def end_contest(self, request, pk=None):
        """
        Танловни қўлда якунлайди
        """
        contest = get_object_or_404(Gift, pk=pk, user_id=request.user)

        if contest.status != 'active':
            raise ValidationError("Фақат 'active' ҳолатидаги танловни якунлаш мумкин.")

        if contest.result_calculate_type != 'by_manual':
            raise ValidationError("Бу танлов қўлда якунланмайди.")

        # Танлов ҳолатини 'completed'га ўзгартириш
        contest.status = 'completed'
        contest.save()

        return Response(GiftSerializer(contest).data)

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
            serializer = GiftParticipantSerializer(participants, many=True)
            return Response(serializer.data)

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

    @action(detail=False, methods=['post'])
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
            if not chat.type in ['channel', 'chat']:
                return Response({'error': 'Faqat kanallar yoki chat ulash mumkin.'},
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

            serializer = UserChatSerializer(user_chat)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except BadRequest:
            return Response({'error': 'Kanal havolasi noto\'g\'ri.'}, status=status.HTTP_400_BAD_REQUEST)
        except Unauthorized:
            return Response({'error': 'Bot kanalga qo\'shila olmadi. Iltimos, botni admin qiling.'},
                            status=status.HTTP_400_BAD_REQUEST)
        except telegram.error.TelegramError as e:
            return Response({'error': f'Telegram xatosi: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





