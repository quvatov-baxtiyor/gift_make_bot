from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Count, Sum, Avg, Max, Q, F
from body.models import UserChat, Gift, GiftParticipant
from datetime import timedelta
from django.utils import timezone

from body.serializers import GiftSerializer, UserChatSerializer


# ... boshqa importlar

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def admin_dashboard_stats(request):
    """
    Admin uchun dashbord statistikasi.
    """

    # Faol, yakunlangan va qoralama sovg'alar (barcha foydalanuvchilar uchun)
    gift_stats = Gift.objects.aggregate(
        active_gifts=Count('id', filter=Q(status='active')),
        completed_gifts=Count('id', filter=Q(status='completed')),
        draft_gifts=Count('id', filter=Q(status='draft')),
    )

    # O'rtacha va maksimal ishtirokchilar soni (barcha foydalanuvchilar uchun)
    all_completed_gifts = Gift.objects.filter(status='completed')
    participant_counts = GiftParticipant.objects.filter(gift__in=all_completed_gifts).values('gift').annotate(
        count=Count('id', distinct=True)  # Ishtirokchilarni takrorlamasdan sanash
    )
    avg_reach = participant_counts.aggregate(Avg('count'))['count__avg'] or 0
    max_reach = participant_counts.aggregate(Max('count'))['count__max'] or 0

    data = {
        'avg_reach': avg_reach,
        'max_reach': max_reach,
        'active_gifts': gift_stats['active_gifts'],
        'completed_gifts': gift_stats['completed_gifts'],
        'draft_gifts': gift_stats['draft_gifts'],
    }

    return Response(data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_dashboard_stats(request):
    """
    Oddiy foydalanuvchi uchun dashbord statistikasi.
    """
    user = request.user

    # Foydalanuvchiga tegishli ma'lumotlarni filtrlash
    user_chats = UserChat.objects.filter(user=user)
    user_gifts = Gift.objects.filter(user_id=user)
    user_active_gifts = user_gifts.filter(status='active')
    user_completed_gifts = user_gifts.filter(status='completed')
    user_draft_gifts = user_gifts.filter(status='draft')

    user_participant_counts = GiftParticipant.objects.filter(gift__in=user_completed_gifts).values('gift').annotate(
        count=Count('id', distinct=True)
    )
    user_avg_reach = user_participant_counts.aggregate(Avg('count'))['count__avg'] or 0
    user_max_reach = user_participant_counts.aggregate(Max('count'))['count__max'] or 0

    # Yangi yaratilgan va biriktirilgan kanallar
    recently_created_gifts = user_gifts.filter(created_date__gte=timezone.now() - timedelta(days=7))
    recently_connected_channels = user_chats.filter(init_date__gte=timezone.now() - timedelta(days=7))

    data = {
        'my_avg_reach': user_avg_reach,
        'my_max_reach': user_max_reach,
        'my_active_gifts': user_active_gifts.count(),
        'my_completed_gifts': user_completed_gifts.count(),
        'my_draft_gifts': user_draft_gifts.count(),
        'recently_created_gifts': GiftSerializer(recently_created_gifts, many=True).data,
        'recently_connected_channels': UserChatSerializer(recently_connected_channels, many=True).data,
    }

    return Response(data)
