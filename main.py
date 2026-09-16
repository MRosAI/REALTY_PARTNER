import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📱 Отправить номер телефона",
                    request_contact=True
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(
        "Добро пожаловать в бот «Недвижимость»!\n\n"
        "Для продолжения отправьте, пожалуйста, ваш номер телефона.",
        reply_markup=keyboard
    )


@dp.message(F.contact)
async def contact_handler(message: Message):
    phone = message.contact.phone_number

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🏢 Secret Garden"),
                KeyboardButton(text="🏢 ЖК №2")
            ],
            [
                KeyboardButton(text="🏢 ЖК №3"),
                KeyboardButton(text="🏢 ЖК №4")
            ]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "🏢 REALTY PARTNER\n\n"
        "Ваш персональный помощник в выборе недвижимости.\n\n"
        "Здесь собраны актуальные предложения от застройщиков: "
        "жилые комплексы, планировки квартир, цены, "
        "ипотечные программы и условия покупки.\n\n"
        "Выберите интересующий жилой комплекс, "
        "чтобы ознакомиться с предложениями и подобрать подходящий вариант.\n\n"
        "🏠 Выберите жилой комплекс:",
        reply_markup=keyboard
    )


async def main():
    logging.basicConfig(level=logging.INFO)

    if not TOKEN:
        print("ОШИБКА: токен не найден в файле .env")
        return

    bot = Bot(token=TOKEN)

    print("Бот запущен!")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())