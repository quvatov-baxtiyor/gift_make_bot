from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    ad_type = models.CharField(max_length=10, choices=[
        ('text', 'Text'),
        ('image', 'Image')
    ])
    ad_text = models.TextField(blank=True, null=True)
    ad_image_url = models.URLField(blank=True, null=True)
    target_url = models.URLField(blank=True, null=True)
    target_type = models.CharField(max_length=10, choices=[
        ('basic', 'Basic'),
        ('advanced', 'Advanced')
    ])
    target_categories = models.CharField(
        max_length=255)
    target_views = models.PositiveIntegerField()
    reached_views = models.PositiveIntegerField(default=0)
    unique_views = models.PositiveIntegerField(default=0)
    reached_clicks = models.PositiveIntegerField(default=0)
    unique_clicks = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='pending')

    def __str__(self):
        return self.title


class AdView(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='views')
    gift = models.ForeignKey('body.Gift', on_delete=models.CASCADE, null=True, blank=True)  # Optional relation
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ad View for Ad {self.ad} by {self.user}"


class AdClick(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='clicks')
    gift = models.ForeignKey('body.Gift', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ad Click for Ad {self.ad} by {self.user}"
