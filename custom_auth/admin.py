from django.contrib import admin

from custom_auth.models import CustomUser

admin.site.register(CustomUser)
