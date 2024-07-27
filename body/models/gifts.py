from django.db import models
from django.contrib.auth import get_user_model
from body.models import UserChat

User = get_user_model()


class Gift(models.Model):
    POST_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('audio', 'Audio'),
        ('video', 'Video'),
    ]
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gifts')
    title = models.CharField(max_length=255)
    post_id = models.PositiveIntegerField()
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default='text')
    button_text = models.CharField(max_length=100, null=True, blank=True)
    winners_count = models.PositiveIntegerField()
    captcha = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='active', choices=[
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ])
    RESULT_CALCULATE_TYPE_CHOICES = [
        ('by_date', 'By Date'),
        ('by_manual', 'By Manual'),
        ('by_participant_count', 'By Participant Count'),
    ]
    result_calculate_type = models.CharField(max_length=20, choices=RESULT_CALCULATE_TYPE_CHOICES, default='by_date')
    result_calculate_date = models.DateTimeField(null=True, blank=True)
    result_calculate_participant_count = models.PositiveIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class GiftCustomLinks(models.Model):
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return f"Custom Link for Gift {self.gift}: {self.url}"


class GiftPostingChats(models.Model):
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    chat = models.ForeignKey(UserChat, on_delete=models.CASCADE)

    def __str__(self):
        return f"Posting Chat for Gift {self.gift}: {self.chat}"


class GiftSubChats(models.Model):
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    chat = models.ForeignKey(UserChat, on_delete=models.CASCADE)

    def __str__(self):
        return f"Sub Chat for Gift {self.gift}: {self.chat}"


class GiftParticipant(models.Model):
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE, related_name='participants')
    date = models.DateTimeField(auto_now_add=True)
    is_winner = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='participating', choices=[
        ('participating', 'Participating'),
        ('winner', 'Winner'),
        ('disqualified', 'Disqualified'),
    ])

    def __str__(self):
        return f"Participant in Gift {self.gift}"
