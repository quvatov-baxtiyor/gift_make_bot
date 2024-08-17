from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions
from body.models import Gift, GiftPostingChats, GiftSubChats, GiftCustomLinks, GiftParticipant
from body.serializers import GiftSerializer, GiftPostingChatsSerializer, GiftCustomLinksSerializer, \
    GiftSubChatsSerializer, GiftParticipantSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


@swagger_auto_schema(tags=['Gifts'])
class GiftViewSet(viewsets.ModelViewSet):
    queryset = Gift.objects.all()
    serializer_class = GiftSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can interact

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(user_id=self.request.user)
        else:
            return Gift.objects.none()  # Ёки бошқа мос келадиган queryset


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
