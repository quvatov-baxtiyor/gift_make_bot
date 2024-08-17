from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions
from body.models import Plan, UserSubscription
from body.serializers import PlanSerializer, UserSubscriptionSerializer

@swagger_auto_schema(tags=['Plans'])
class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [permissions.IsAdminUser]


@swagger_auto_schema(tags=['Plans'])
class UserSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
