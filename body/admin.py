from django.contrib import admin
from body.models import UserChat, ChatCategory, ChatInitCategory, Plan, UserSubscription, Ad, AdView, AdClick, Gift, \
    GiftParticipant, GiftCustomLinks, GiftSubChats, GiftPostingChats


admin.site.register(UserChat)
admin.site.register(ChatCategory)
admin.site.register(ChatInitCategory)
admin.site.register(Plan)
admin.site.register(UserSubscription)
admin.site.register(Ad)
admin.site.register(AdView)
admin.site.register(AdClick)
admin.site.register(Gift)
admin.site.register(GiftParticipant)
admin.site.register(GiftCustomLinks)
admin.site.register(GiftSubChats)
admin.site.register(GiftPostingChats)



