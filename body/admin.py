# body/admin.py
from django.contrib import admin
from .models import (
    Plan, ChatCategory, User, Chat, UserChat, UserSubscription,
    Gift, GiftCustomLink, GiftPostingChat, GiftSubChat, GiftParticipant,
    Ad, AdView, AdClick
)

admin.site.register(Plan)
admin.site.register(ChatCategory)
admin.site.register(User)
admin.site.register(Chat)
admin.site.register(UserChat)
admin.site.register(UserSubscription)
admin.site.register(Gift)
admin.site.register(GiftCustomLink)
admin.site.register(GiftPostingChat)
admin.site.register(GiftSubChat)
admin.site.register(GiftParticipant)
admin.site.register(Ad)
admin.site.register(AdView)
admin.site.register(AdClick)
