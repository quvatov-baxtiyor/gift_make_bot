from django.db import models
from django.contrib.auth import get_user_model  # Use this to get your custom user model

User = get_user_model()


class UserChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_id = models.BigIntegerField()  # Telegram's chat_id
    chat_type = models.CharField(max_length=20, choices=[('gifting', 'Gifting'), ('sub', 'Subscription')])
    init_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - Chat {self.chat_id} ({self.chat_type})"


class ChatCategory(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class ChatInitCategory(models.Model):
    chat_id = models.ForeignKey(UserChat, on_delete=models.CASCADE)  # Telegram chat_id
    category = models.ForeignKey(ChatCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"Chat {self.chat_id} - Category: {self.category}"


