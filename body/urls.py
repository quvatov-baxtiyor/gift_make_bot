# body/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    PlanViewSet, ChatCategoryViewSet, UserViewSet, ChatViewSet, UserChatViewSet,
    UserSubscriptionViewSet, GiftViewSet, GiftCustomLinkViewSet, GiftPostingChatViewSet,
    GiftSubChatViewSet, GiftParticipantViewSet, AdViewSet, AdViewViewSet, AdClickViewSet
)

router = DefaultRouter()
router.register(r'plans', PlanViewSet)
router.register(r'chat-categories', ChatCategoryViewSet)
router.register(r'users', UserViewSet)
router.register(r'chats', ChatViewSet)
router.register(r'user-chats', UserChatViewSet)
router.register(r'user-subscriptions', UserSubscriptionViewSet)
router.register(r'gifts', GiftViewSet)
router.register(r'gift-custom-links', GiftCustomLinkViewSet)
router.register(r'gift-posting-chats', GiftPostingChatViewSet)
router.register(r'gift-sub-chats', GiftSubChatViewSet)
router.register(r'gift-participants', GiftParticipantViewSet)
router.register(r'ads', AdViewSet)
router.register(r'ad-views', AdViewViewSet)
router.register(r'ad-clicks', AdClickViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
