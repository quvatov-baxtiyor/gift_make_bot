from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Plan(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    due = models.DurationField()  # Duration in days
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_chat = models.ForeignKey('body.UserChat', on_delete=models.CASCADE)
    subscription_date = models.DateTimeField(auto_now_add=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='active', choices=[
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
    ])

    def __str__(self):
        return f"Subscription for {self.user} on {self.subscription_date}"
