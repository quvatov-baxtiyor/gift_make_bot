from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserChatViewSet, ChatCategoryViewSet, ChatInitCategoryViewSet, UserSubscriptionViewSet,
    PlanViewSet, AdViewSet, GiftViewSet, AdViewViewSet, AdClickViewSet, GiftCustomLinksViewSet,
    GiftPostingChatsViewSet, GiftSubChatsViewSet, GiftParticipantViewSet, TransactionViewSet, MyContestsViewSet,
)
from .views.transactions import TopUpBalanceView, BuySubscriptionView

# Router for User and Chat
user_chat_router = DefaultRouter()
user_chat_router.register(r'user_chats', UserChatViewSet, basename='user_chat')

# Router for Chat Categories
chat_category_router = DefaultRouter()
chat_category_router.register(r'chat_init_categories', ChatInitCategoryViewSet, basename='chat_init_category')
chat_category_router.register(r'chat_categories', ChatCategoryViewSet, basename='chat_category')

# Router for Subscriptions and Plans
subscription_router = DefaultRouter()
subscription_router.register(r'user_subscriptions', UserSubscriptionViewSet, basename='user_subscription')
subscription_router.register(r'plans', PlanViewSet, basename='plan')

# Router for Ads
ad_router = DefaultRouter()
ad_router.register(r'ads', AdViewSet, basename='ad')
ad_router.register(r'ad_views', AdViewViewSet, basename='ad_view')
ad_router.register(r'ad_clicks', AdClickViewSet, basename='ad_click')

# Router for Gifts
gift_router = DefaultRouter()
gift_router.register(r'gifts', GiftViewSet, basename='gift')
gift_router.register(r'gift_custom_links', GiftCustomLinksViewSet, basename='gift_custom_link')
gift_router.register(r'gift_posting_chats', GiftPostingChatsViewSet, basename='gift_posting_chat')
gift_router.register(r'gift_sub_chats', GiftSubChatsViewSet, basename='gift_sub_chat')
gift_router.register(r'gift_participants', GiftParticipantViewSet, basename='gift_participant')

transaction_router = DefaultRouter()
transaction_router.register(r'transactions', TransactionViewSet, basename='transaction')

my_contests_router = DefaultRouter()
my_contests_router.register(r'my_contests', MyContestsViewSet, basename='my_contests')

# Include the routers in urlpatterns with appropriate prefixes
urlpatterns = [
    path('users/', include(user_chat_router.urls)),
    path('chat_categories/', include(chat_category_router.urls)),
    path('subscriptions/', include(subscription_router.urls)),
    path('ads/', include(ad_router.urls)),
    path('gifts/', include(gift_router.urls)),
    path('top_up/', TopUpBalanceView.as_view()),
    path('buy_subscription/', BuySubscriptionView.as_view()),

    path('my_contests/<int:pk>/create_gift/', MyContestsViewSet.as_view({'post': 'create_gift'}), name='create_gift'),
    path('my_contests/<int:pk>/update_gift/<int:gift_pk>/',
         MyContestsViewSet.as_view({'put': 'update_gift', 'patch': 'update_gift'}), name='update_gift'),
    path('my_contests/<int:pk>/delete_gift/<int:gift_pk>/', MyContestsViewSet.as_view({'delete': 'delete_gift'}),
         name='delete_gift'),
    path('my_contests/<int:pk>/update_gift_settings/<int:gift_pk>/',
         MyContestsViewSet.as_view({'put': 'update_gift_settings', 'patch': 'update_gift_settings'}),
         name='update_gift_settings'),
    path('my_contests/<int:pk>/determine_winners/', MyContestsViewSet.as_view({'post': 'determine_winners'}),
         name='determine_winners'),
]
