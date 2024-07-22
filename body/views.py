from rest_framework import viewsets
from .models import (
    Plan, ChatCategory, User, Chat, UserChat, UserSubscription,
    Gift, GiftCustomLink, GiftPostingChat, GiftSubChat, GiftParticipant,
    Ad, AdView, AdClick
)
from .serializers import (
    PlanSerializer, ChatCategorySerializer, UserSerializer, ChatSerializer,
    UserChatSerializer, UserSubscriptionSerializer, GiftSerializer, GiftCustomLinkSerializer,
    GiftPostingChatSerializer, GiftSubChatSerializer, GiftParticipantSerializer, AdSerializer,
    AdViewSerializer, AdClickSerializer
)


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


class ChatCategoryViewSet(viewsets.ModelViewSet):
    queryset = ChatCategory.objects.all()
    serializer_class = ChatCategorySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class UserChatViewSet(viewsets.ModelViewSet):
    queryset = UserChat.objects.all()
    serializer_class = UserChatSerializer


class UserSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer


class GiftViewSet(viewsets.ModelViewSet):
    queryset = Gift.objects.all()
    serializer_class = GiftSerializer


class GiftCustomLinkViewSet(viewsets.ModelViewSet):
    queryset = GiftCustomLink.objects.all()
    serializer_class = GiftCustomLinkSerializer


class GiftPostingChatViewSet(viewsets.ModelViewSet):
    queryset = GiftPostingChat.objects.all()
    serializer_class = GiftPostingChatSerializer


class GiftSubChatViewSet(viewsets.ModelViewSet):
    queryset = GiftSubChat.objects.all()
    serializer_class = GiftSubChatSerializer


class GiftParticipantViewSet(viewsets.ModelViewSet):
    queryset = GiftParticipant.objects.all()
    serializer_class = GiftParticipantSerializer


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class AdViewViewSet(viewsets.ModelViewSet):
    queryset = AdView.objects.all()
    serializer_class = AdViewSerializer


class AdClickViewSet(viewsets.ModelViewSet):
    queryset = AdClick.objects.all()
    serializer_class = AdClickSerializer
