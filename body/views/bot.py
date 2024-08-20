from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings

from telegram import Update
from telegram.ext import Application

@csrf_exempt
def telegram_webhook(request):
    bot = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    update = Update.de_json(request.body.decode("utf-8"), bot)
    bot.process_update(update)
    return HttpResponse("OK")