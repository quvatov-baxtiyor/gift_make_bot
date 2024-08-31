import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

bot_token = "7345715040:AAFiaO0darTdi_SmFXz--vKpLB2353KxE0k"

bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# Register a handler for the /start command
@dp.message(Command("start"))
async def start(message):
    markup = ReplyKeyboardMarkup()
    markup.add(KeyboardButton("👋 Saytga kirish", web_app=WebAppInfo(url='https://nuqtauz.com/')))
    await message.answer("Assalomu alaykum. Botimizga xush kelibsiz.", reply_markup=markup)


async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
