# import logging
# from telegram import Update
# from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
# from telegram import Update
# from telegram.ext import ContextTypes
# from django.conf import settings
#
# from custom_auth import views
#
# # Logging'ни созлаш
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )
#
#
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text="Assalomu alaykum! Men Konkurs botman.")
#
#
# async def my_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """
#     Фойдаланувчи учун статистикани қайтаради
#     """
#     user_id = update.effective_user.id
#     data = views.get_user_stats(user_id)
#     # data'ни чиройли форматировка қилиб, фойдаланувчига юбориш
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=format_user_stats(data))
#
#
# async def all_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """
#     Админ учун умумий статистикани қайтаради
#     """
#     user_id = update.effective_user.id
#     if not views.is_admin(user_id):  # Админ эканлигини текшириш
#         await context.bot.send_message(chat_id=update.effective_chat.id, text="Ушбу буйруқ фақат админлар учун!")
#         return
#
#     data = views.get_all_stats()
#     # data'ни чиройли форматировка қилиб, админга юбориш
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=format_all_stats(data))
#
#
# def run_bot():
#     application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()
#
#     # ... (аввалги хендлерлар) ...
#
#     my_stats_handler = CommandHandler('my_stats', my_stats)
#     all_stats_handler = CommandHandler('all_stats', all_stats)
#     application.add_handler(my_stats_handler)
#     application.add_handler(all_stats_handler)
#
#     application.run_polling()
#
#
# # Статистикани чиройли форматировка қиладиган функциялар
# def format_user_stats(data):
#     pass
#
#
# # ... (статистикани чиройли кўринишга келтириш)
#
# def format_all_stats(data):
#     pass
# # ... (статистикани чиройли кўринишга келтириш)
