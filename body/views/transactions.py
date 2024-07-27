from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from body.models import Transaction, UserSubscription
from body.serializers import TransactionSerializer, TopUpBalanceSerializer, UserSubscriptionSerializer, \
    BuySubscriptionSerializer


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # user_id = self.request.query_params.get('user_id')
        # if user_id:
        #     user = User.objects.get(user_id=user_id)
        user = self.request.user
        return user.transactions.all().order_by('-timestamp')[:10]


class TopUpBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=TopUpBalanceSerializer,
                         responses={201: TransactionSerializer, 400: 'Bad Request'})
    def post(self, request):
        serializer = TopUpBalanceSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']

            # Pul miqdori plusdaligini tekshirish
            if amount <= 0:
                return Response({"detail": "Amount must be positive."}, status=status.HTTP_400_BAD_REQUEST)

            # Userni balansni yangilash
            user = request.user
            user.balance += amount
            user.save()

            # Tranzaksiya yaratish
            transaction = Transaction.objects.create(
                user=user,
                amount=amount,
                transaction_type='top_up'
            )

            return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BuySubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=BuySubscriptionSerializer,
                         responses={201: UserSubscriptionSerializer, 400: 'Bad Request'})
    def post(self, request):
        serializer = BuySubscriptionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            plan = serializer.validated_data['plan']
            user_chat = serializer.validated_data['user_chat']

            # Foydalanuvchi soqqasi yetishini tekshirish
            if request.user.balance < plan.price:
                return Response({"detail": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)

            # Deduct the price from the user's balance
            request.user.balance -= plan.price
            request.user.save()

            # Yangi obunani yaratish
            subscription = UserSubscription.objects.create(
                user=request.user,
                user_chat=user_chat,
                plan=plan,
            )

            #Tranzaksiya yaratish
            transaction = Transaction.objects.create(
                user=request.user,
                amount=-plan.price,
                transaction_type='subscription'
            )

            return Response(UserSubscriptionSerializer(subscription).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
