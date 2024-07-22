# body/models.py
from django.db import models

class Plan(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    due = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class ChatCategory(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class User(models.Model):
    user_id = models.CharField(max_length=100)
    req_date = models.DateTimeField(auto_now_add=True)
    lang = models.CharField(max_length=10)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    full_name = models.CharField(max_length=100)
    avatar_url = models.URLField(max_length=200)
    country = models.CharField(max_length=50)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name

class Chat(models.Model):
    chat_id = models.CharField(max_length=100)
    category = models.ForeignKey(ChatCategory, on_delete=models.CASCADE)
    init_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.chat_id

class UserChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    chat_type = models.CharField(max_length=10, choices=[('posting', 'Posting'), ('sub', 'Sub')])
    init_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.chat}"

class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    subscription_date = models.DateTimeField(auto_now_add=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')])

    def __str__(self):
        return f"{self.user} - {self.plan}"

class Gift(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    post_id = models.CharField(max_length=100)
    button_text = models.CharField(max_length=100)
    winners_count = models.IntegerField()
    captcha = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('complete', 'Complete'), ('draft', 'Draft')])
    result_calculate_type = models.CharField(max_length=20, choices=[('by_date', 'By Date'), ('by_manual', 'By Manual'), ('by_winners_count', 'By Winners Count')])
    result_calculate_date = models.DateTimeField(null=True, blank=True)
    result_calculate_winners_count = models.IntegerField(null=True, blank=True)
    ads = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class GiftCustomLink(models.Model):
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.url

class GiftPostingChat(models.Model):
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.gift} - {self.chat}"

class GiftSubChat(models.Model):
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.gift} - {self.chat}"

class GiftParticipant(models.Model):
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    participant_user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    is_winner = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('approved', 'Approved')])

    def __str__(self):
        return f"{self.gift} - {self.participant_user}"

class Ad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    ad_type = models.CharField(max_length=20, choices=[('text', 'Text'), ('image', 'Image')])
    ad_text = models.TextField()
    ad_image_url = models.URLField(max_length=200, null=True, blank=True)
    target_url = models.URLField(max_length=200)
    target_type = models.CharField(max_length=20, choices=[('basic', 'Basic'), ('advanced', 'Advanced')])
    target_categories = models.CharField(max_length=200)
    target_views = models.IntegerField()
    reached_views = models.IntegerField()
    unique_views = models.IntegerField()
    reached_clicks = models.IntegerField()
    unique_clicks = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')])

    def __str__(self):
        return self.title

class AdView(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ad} - {self.user}"

class AdClick(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ad} - {self.user}"
