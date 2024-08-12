from rest_framework import serializers
from body.models import Transaction, Plan, UserChat


class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Transaction
        fields = '__all__'


class BuySubscriptionSerializer(serializers.Serializer):
    plan = serializers.PrimaryKeyRelatedField(queryset=Plan.objects.filter(is_active=True))
    user_chat = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate(self, attrs):
        request = self.context.get('request')
        if not request or not request.user:
            raise serializers.ValidationError('User is not authenticated.')

        user_chat = attrs['user_chat']
        user = request.user

        # Premium versiyani faqta adminkamiz o'zini kanaliga olsa bo'ladi,birovno kanaliga sotib ola olmaydi
        if user_chat.user != user:
            raise serializers.ValidationError('You can only subscribe to your own chats.')

        return attrs


class TopUpBalanceSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
