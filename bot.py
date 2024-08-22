import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types.web_app_info import WebAppInfo

bot_token = "7345715040:AAFiaO0darTdi_SmFXz--vKpLB2353KxE0k"

bot = Bot(token=bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton("👋 Saytga kirish", web_app=WebAppInfo(url='https://university.pdp.uz/')))
    await message.answer("Assalomu alaykum. Botimizga xush kelibsiz.", reply_markup=markup)


async def main():
    try:
        await dp.start_polling()
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
