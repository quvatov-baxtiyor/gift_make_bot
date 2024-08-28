from django.urls import path, include
from orca.settings import profile
from rest_framework.routers import DefaultRouter
from . import views
from gift_make_bot import settings
from .views import (
    UserChatViewSet, ChatCategoryViewSet, ChatInitCategoryViewSet, UserSubscriptionViewSet,
    PlanViewSet, AdViewSet, GiftViewSet, AdViewViewSet, AdClickViewSet, GiftCustomLinksViewSet,
    GiftPostingChatsViewSet, GiftSubChatsViewSet, GiftParticipantViewSet, MyContestsViewSet, ProfileStatsView
)
from .views.channels import my_channels

user_chat_router = DefaultRouter()
user_chat_router.register(r'user_chats', UserChatViewSet, basename='user_chat')

chat_category_router = DefaultRouter()
chat_category_router.register(r'chat_init_categories', ChatInitCategoryViewSet, basename='chat_init_category')
chat_category_router.register(r'chat_categories', ChatCategoryViewSet, basename='chat_category')

subscription_router = DefaultRouter()
subscription_router.register(r'user_subscriptions', UserSubscriptionViewSet, basename='user_subscription')
subscription_router.register(r'plans', PlanViewSet, basename='plan')

ad_router = DefaultRouter()
ad_router.register(r'ads', AdViewSet, basename='ad')
ad_router.register(r'ad_views', AdViewViewSet, basename='ad_view')
ad_router.register(r'ad_clicks', AdClickViewSet, basename='ad_click')

gift_router = DefaultRouter()
gift_router.register(r'gifts', GiftViewSet, basename='gift')
gift_router.register(r'gift_custom_links', GiftCustomLinksViewSet, basename='gift_custom_link')
gift_router.register(r'gift_posting_chats', GiftPostingChatsViewSet, basename='gift_posting_chat')
gift_router.register(r'gift_sub_chats', GiftSubChatsViewSet, basename='gift_sub_chat')
gift_router.register(r'gift_participants', GiftParticipantViewSet, basename='gift_participant')

my_contests_router = DefaultRouter()
my_contests_router.register(r'my_contests', MyContestsViewSet, basename='my_contests')


urlpatterns = [
    path('users/', include(user_chat_router.urls)),
    path('chat_categories/', include(chat_category_router.urls)),
    path('subscriptions/', include(subscription_router.urls)),
    path('ads/', include(ad_router.urls)),
    path('gifts/', include(gift_router.urls)),

    path('my_contests/', include(my_contests_router.urls)),
    path('my_contests/<int:pk>/connect_channel/', MyContestsViewSet.as_view({'post': 'connect_channel'}),
         name='connect_channel'),
    path('my_contests/<int:pk>/create_contest/', MyContestsViewSet.as_view({'post': 'create_contest'}),name='create_contest'),
    path('my_contests/<int:pk>/start_contest/', MyContestsViewSet.as_view({'post': 'start_contest'}),name='start_contest'),
    path('my_contests/<int:pk>/end_contest/', MyContestsViewSet.as_view({'post': 'end_contest'}),name='end_contest'),

    path('my_contests/<int:pk>/determine_winners/', MyContestsViewSet.as_view({'post': 'determine_winners'}),
         name='determine_winners'),
    path('my_contests/<int:pk>/announce_winners/', MyContestsViewSet.as_view({'post': 'announce_winners'}),
         name='announce_winners'),

    path('my-channels/', my_channels, name='my_channels'),

    path('profile', views.ProfileStatsView.as_view(), name='profile_stats'),
]
