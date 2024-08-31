from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions, status
from django.db.models import Count, Sum, Avg, Max, Q, F
from rest_framework.views import APIView
from body.models import UserChat, Gift, GiftParticipant
from datetime import timedelta
from django.utils import timezone
from body.serializers import GiftSerializer, UserChatSerializer


class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        try:
            active_gifts = Gift.objects.filter(status='active').count()
            completed_gifts = Gift.objects.filter(status='completed').count()
            draft_gifts = Gift.objects.filter(status='draft').count()
            all_gifts = Gift.objects.count()

            participant_counts = GiftParticipant.objects.filter(gift__status='completed').values('gift').annotate(
                count=Count('id', distinct=True)
            )
            avg_reach = participant_counts.aggregate(Avg('count'))['count__avg'] or 0
            max_reach = participant_counts.aggregate(Max('count'))['count__max'] or 0

            auditory = UserChat.objects.aggregate(Sum('chat_member_count'))['chat_member_count__sum'] or 0

            data = {
                'auditory': auditory,
                'avg_reach': avg_reach,
                'max_reach': max_reach,
                'all_gifts': all_gifts,
                'active_gifts': active_gifts,
                'completed_gifts': completed_gifts,
                'draft_gifts': draft_gifts,
            }

            return Response(data)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_dashboard_stats(request):
    try:
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

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
