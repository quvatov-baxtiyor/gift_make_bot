from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from telegram import Bot

from body.models import Ad, AdView, AdClick
from body.serializers import AdSerializer, AdViewSerializer, AdClickSerializer
from body.permissions import IsAdminOrReadOnly
from body.utils import filter_contests_for_ad


@swagger_auto_schema(tags=['Ads'])
class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_ads(self, request):
        ads = Ad.objects.filter(user=request.user)
        serializer = self.get_serializer(ads, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def place_ad(self, request, pk=None):
        ad = self.get_object()
        if ad.status != 'approved':
            return Response({'error': 'Faqat tasdiqlangan reklamalarni joylashtirish mumkin.'},
                            status=status.HTTP_400_BAD_REQUEST)

        contests = filter_contests_for_ad(ad)

        for contest in contests:
            try:
                bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
                if ad.ad_type == 'text':
                    bot.send_message(chat_id=contest.posting_chats.first().chat_id, text=ad.ad_text)
                elif ad.ad_type == 'image':
                    bot.send_photo(chat_id=contest.posting_chats.first().chat_id, photo=ad.ad_image_url)
            except Exception as e:
                return Response({'error': f'Reklama joylashtirishda xatolik yuz berdi: {e}'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': f'Reklama {len(contests)} ta konkursga joylashtirildi.'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def ad_stats(request, ad_id):
    ad = get_object_or_404(Ad, pk=ad_id, user=request.user)
    views_count = AdView.objects.filter(ad=ad).count()
    unique_views_count = AdView.objects.filter(ad=ad).values('user').distinct().count()
    clicks_count = AdClick.objects.filter(ad=ad).count()
    unique_clicks_count = AdClick.objects.filter(ad=ad).values('user').distinct().count()

    return Response({
        'views': views_count,
        'unique_views': unique_views_count,
        'clicks': clicks_count,
        'unique_clicks': unique_clicks_count,
    })


@swagger_auto_schema(tags=['Ads'])
class AdViewViewSet(viewsets.ModelViewSet):
    queryset = AdView.objects.all()
    serializer_class = AdViewSerializer
    permission_classes = [permissions.IsAuthenticated]


@swagger_auto_schema(tags=['Ads'])
class AdClickViewSet(viewsets.ModelViewSet):
    queryset = AdClick.objects.all()
    serializer_class = AdClickSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def ad_stats(request, ad_id):
    ad = get_object_or_404(Ad, pk=ad_id, user=request.user)

    views_count = AdView.objects.filter(ad=ad).count()
    clicks_count = AdClick.objects.filter(ad=ad).count()

    return Response({
        'views': views_count,
        'clicks': clicks_count,
    })
