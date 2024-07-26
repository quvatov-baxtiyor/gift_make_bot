from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, status
from django.db import models
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from body.models import Gift, GiftPostingChats, GiftSubChats, GiftCustomLinks, GiftParticipant, UserChat
from body.serializers import GiftSerializer, GiftPostingChatsSerializer, GiftCustomLinksSerializer, \
    GiftSubChatsSerializer, GiftParticipantSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class GiftViewSet(viewsets.ModelViewSet):
    queryset = Gift.objects.all()
    serializer_class = GiftSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can interact

    @swagger_auto_schema(tags=['Gifts'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Gifts'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Gifts'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Gifts'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Gifts'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Gifts'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        # The perform_create() method allows you to modify the object creation behavior
        # Set the current user as the creator of the gift.
        serializer.save(user=self.request.user)


class GiftCustomLinksViewSet(viewsets.ModelViewSet):
    queryset = GiftCustomLinks.objects.all()
    serializer_class = GiftCustomLinksSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=['Gifts'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Gifts'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Gifts'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Gifts'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Gifts'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Gifts'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class GiftPostingChatsViewSet(viewsets.ModelViewSet):
    queryset = GiftPostingChats.objects.all()
    serializer_class = GiftPostingChatsSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=['Gifts'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Gifts'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Gifts'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Gifts'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Gifts'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Gifts'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class GiftSubChatsViewSet(viewsets.ModelViewSet):
    queryset = GiftSubChats.objects.all()
    serializer_class = GiftSubChatsSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=['Gifts'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Gifts'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Gifts'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Gifts'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Gifts'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Gifts'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class GiftParticipantViewSet(viewsets.ModelViewSet):
    queryset = GiftParticipant.objects.all()
    serializer_class = GiftParticipantSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=['Gifts'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Gifts'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Gifts'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Gifts'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Gifts'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Gifts'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Gifts'])
    def create(self, request, *args, **kwargs):
        participant_user_id = request.data.get('participant_user_id')
        gift_id = request.data.get('gift')

        try:
            # Fetch the gift object
            gift = get_object_or_404(Gift, pk=gift_id)
        except Gift.DoesNotExist:
            return Response({"detail": "Gift not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check eligibility based on participant_user_id and gift
        user = get_object_or_404(User, user_id=participant_user_id)

        if GiftParticipant.objects.filter(user=user, gift=gift).exists():
            return Response({"detail": "User has already participated in this gift."},
                            status=status.HTTP_400_BAD_REQUEST)

        if not UserChat.objects.filter(user=user, chat_id=gift.chat.chat_id).exists():
            return Response({"detail": "User is not a member of the required chat."},
                            status=status.HTTP_400_BAD_REQUEST)

        gift.participants_count = models.F('participants_count') + 1
        gift.save(update_fields=['participants_count'])

        return Response({"detail": "Participation recorded."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    @swagger_auto_schema(tags=['Gifts'])
    def participants_by_gift(self, request):
        gift_id = request.query_params.get('gift_id')

        try:
            gift = get_object_or_404(Gift, pk=gift_id)
        except Gift.DoesNotExist:
            return Response({"detail": "Gift not found."}, status=status.HTTP_404_NOT_FOUND)

        participants = GiftParticipant.objects.filter(gift=gift)
        serializer = GiftParticipantSerializer(participants, many=True)
        return Response(serializer.data)
