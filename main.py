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


# =========================
# ГЛАВНОЕ МЕНЮ — 4 ЖК
# =========================

def main_menu():
    return ReplyKeyboardMarkup(
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


# =========================
# МЕНЮ SECRET GARDEN
# =========================

def secret_garden_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="1-комн. квартира"),
                KeyboardButton(text="2-комн. квартира")
            ],
            [
                KeyboardButton(text="3-комн. квартира"),
                KeyboardButton(text="4-комн. квартира")
            ],
            [
                KeyboardButton(text="📄 Презентация"),
                KeyboardButton(text="📄 Условия реализации")
            ],
            [
                KeyboardButton(text="🏦 Ипотечные программы")
            ],
            [
                KeyboardButton(text="⬅️ Вернуться в меню")
            ]
        ],
        resize_keyboard=True
    )


# =========================
# МЕНЮ НАЗАД ИЗ КВАРТИРЫ
# =========================

def apartment_back_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="⬅️ Назад в Secret Garden")
            ]
        ],
        resize_keyboard=True
    )


# =========================
# START
# =========================

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


# =========================
# ПОЛУЧЕНИЕ ТЕЛЕФОНА
# =========================

@dp.message(F.contact)
async def contact_handler(message: Message):

    phone = message.contact.phone_number

    await message.answer(
        "🏢 REALTY PARTNER\n\n"
        "Ваш персональный помощник в выборе недвижимости.\n\n"
        "Здесь собраны актуальные предложения от застройщиков: "
        "жилые комплексы, планировки квартир, цены, "
        "ипотечные программы и условия покупки.\n\n"
        "Выберите интересующий жилой комплекс, "
        "чтобы ознакомиться с предложениями и подобрать подходящий вариант.\n\n"
        "🏠 Выберите жилой комплекс:",
        reply_markup=main_menu()
    )


# =========================
# SECRET GARDEN
# =========================

@dp.message(F.text == "🏢 Secret Garden")
async def secret_garden_handler(message: Message):

    await message.answer(
        "🏢 SECRET GARDEN\n\n"
        "Премиальный жилой комплекс в современном формате.\n\n"
        "Здесь вы можете ознакомиться с доступными "
        "квартирами, планировками, стоимостью, "
        "условиями покупки и ипотечными программами.\n\n"
        "Выберите интересующий вариант:",
        reply_markup=secret_garden_menu()
    )


# =========================
# 1-КОМНАТНАЯ КВАРТИРА
# =========================

@dp.message(F.text == "1-комн. квартира")
async def one_room_handler(message: Message):

    await message.answer(
        "🏠 1-КОМНАТНАЯ КВАРТИРА\n\n"
        "📐 Площадь: 42,5 м²\n"
        "🛋 Планировка: евроформат\n"
        "🏢 Этаж: 12\n"
        "💰 Стоимость: 12 500 000 ₽\n\n"
        "🏦 Ипотека:\n"
        "Срок: до 30 лет\n"
        "Ориентировочный платёж: 65 000 ₽/мес.\n\n"
        "🔗 Подробнее о квартире:\n"
        "https://example.com\n\n"
        "🌐 Сайт застройщика:\n"
        "https://example.com",
        reply_markup=apartment_back_menu()
    )


# =========================
# НАЗАД В SECRET GARDEN
# =========================

@dp.message(F.text == "⬅️ Назад в Secret Garden")
async def back_secret_garden_handler(message: Message):

    await message.answer(
        "🏢 SECRET GARDEN\n\n"
        "Выберите интересующий вариант:",
        reply_markup=secret_garden_menu()
    )


# =========================
# НАЗАД В ГЛАВНОЕ МЕНЮ
# =========================

@dp.message(F.text == "⬅️ Вернуться в меню")
async def back_to_main_menu_handler(message: Message):

    await message.answer(
        "🏢 REALTY PARTNER\n\n"
        "🏠 Выберите жилой комплекс:",
        reply_markup=main_menu()
    )


# =========================
# ЗАПУСК
# =========================

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