import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

bot = Bot("7345715040:AAFiaO0darTdi_SmFXz--vKpLB2353KxE0k")
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


@dp.message(Command("start"))
async def start(message):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👋 Saytga kirish", web_app=WebAppInfo(url='https://nuqtateam.uz/'))]
        ],
        resize_keyboard=True
    )
    await message.answer("Assalomu alaykum. Botimizga xush kelibsiz.", reply_markup=markup)


async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
