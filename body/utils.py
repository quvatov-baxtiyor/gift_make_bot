from django.db.models import Q

from body.models import UserChat, UserSubscription, Gift


def filter_contests_for_ad(ad):
    # Odatiy tarif uchun barcha gifting chatlardagi konkurslar
    contests = Gift.objects.filter(posting_chats__chat__chat_type='gifting')

    if ad.target_type == 'advanced':
        # Professional tarif uchun maqsadli kategoriyadagi chatlarni filtrlash
        contests = contests.filter(
            Q(posting_chats__chat__chatinitcategory__category__title__in=ad.target_categories.split(','))
        )

    # Faqat premium obunasi bo'lmagan foydalanuvchilarning konkurslarini olish
    contests = contests.exclude(
        posting_chats__chat__user__usersubscription__status='active'  # Obunasi faol bo'lmaganlar
    ).distinct()  # Takroriy konkurslarni olib tashlash

    return contests
