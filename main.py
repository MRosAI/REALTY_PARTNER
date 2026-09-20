import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from dotenv import load_dotenv


# =========================
# НАСТРОЙКИ
# =========================

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

dp = Dispatcher()


# =========================
# ТЕСТОВЫЕ ДАННЫЕ
# =========================

APARTMENTS = {
    "1": [
        {
            "id": "1_1",
            "title": "1-комнатная №101",
            "area": "42.5 м²",
            "layout": "Евроформат",
            "floor": "12 из 24",
            "view": "Во двор",
            "price": "12 500 000 ₽",
            "payment": "от 65 000 ₽/мес.",
        },
        {
            "id": "1_2",
            "title": "1-комнатная №102",
            "area": "48.8 м²",
            "layout": "Евроформат",
            "floor": "8 из 24",
            "view": "На город",
            "price": "14 200 000 ₽",
            "payment": "от 74 000 ₽/мес.",
        },
        {
            "id": "1_3",
            "title": "1-комнатная №103",
            "area": "51.2 м²",
            "layout": "Свободная планировка",
            "floor": "19 из 24",
            "view": "Панорамный вид",
            "price": "15 100 000 ₽",
            "payment": "от 79 000 ₽/мес.",
        },
    ],

    "2": [
        {
            "id": "2_1",
            "title": "2-комнатная №201",
            "area": "63.4 м²",
            "layout": "Евроформат",
            "floor": "7 из 24",
            "view": "На парк",
            "price": "18 900 000 ₽",
            "payment": "от 99 000 ₽/мес.",
        },
        {
            "id": "2_2",
            "title": "2-комнатная №202",
            "area": "71.8 м²",
            "layout": "Классическая",
            "floor": "14 из 24",
            "view": "На город",
            "price": "21 500 000 ₽",
            "payment": "от 112 000 ₽/мес.",
        },
        {
            "id": "2_3",
            "title": "2-комнатная №203",
            "area": "78.6 м²",
            "layout": "Master Bedroom",
            "floor": "21 из 24",
            "view": "Панорамный вид",
            "price": "24 800 000 ₽",
            "payment": "от 129 000 ₽/мес.",
        },
    ],

    "3": [
        {
            "id": "3_1",
            "title": "3-комнатная №301",
            "area": "92.1 м²",
            "layout": "Семейная",
            "floor": "6 из 24",
            "view": "На парк",
            "price": "27 900 000 ₽",
            "payment": "от 145 000 ₽/мес.",
        },
        {
            "id": "3_2",
            "title": "3-комнатная №302",
            "area": "105.7 м²",
            "layout": "Master Bedroom",
            "floor": "15 из 24",
            "view": "На город",
            "price": "32 500 000 ₽",
            "payment": "от 169 000 ₽/мес.",
        },
        {
            "id": "3_3",
            "title": "3-комнатная №303",
            "area": "118.3 м²",
            "layout": "Premium",
            "floor": "22 из 24",
            "view": "Панорамный вид",
            "price": "38 900 000 ₽",
            "payment": "от 203 000 ₽/мес.",
        },
    ],

    "4": [
        {
            "id": "4_1",
            "title": "4-комнатная №401",
            "area": "132.5 м²",
            "layout": "Family Premium",
            "floor": "9 из 24",
            "view": "На парк",
            "price": "42 500 000 ₽",
            "payment": "от 221 000 ₽/мес.",
        },
        {
            "id": "4_2",
            "title": "4-комнатная №402",
            "area": "148.9 м²",
            "layout": "Master Block",
            "floor": "17 из 24",
            "view": "На город",
            "price": "49 800 000 ₽",
            "payment": "от 259 000 ₽/мес.",
        },
        {
            "id": "4_3",
            "title": "4-комнатная №403",
            "area": "165.4 м²",
            "layout": "Premium",
            "floor": "23 из 24",
            "view": "Панорамный вид",
            "price": "58 900 000 ₽",
            "payment": "от 307 000 ₽/мес.",
        },
    ],
}


# =========================
# ГЛАВНОЕ МЕНЮ
# =========================

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🏙 Secret Garden"),
                KeyboardButton(text="🏙 ЖК №2"),
            ],
            [
                KeyboardButton(text="🏙 ЖК №3"),
                KeyboardButton(text="🏙 ЖК №4"),
            ],
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
                KeyboardButton(text="1️⃣ 1-комнатные"),
                KeyboardButton(text="2️⃣ 2-комнатные"),
            ],
            [
                KeyboardButton(text="3️⃣ 3-комнатные"),
                KeyboardButton(text="4️⃣ 4-комнатные"),
            ],
            [
                KeyboardButton(text="📑 Презентация"),
                KeyboardButton(text="📄 Условия продажи"),
            ],
            [
                KeyboardButton(text="🏦 Ипотечные программы"),
            ],
            [
                KeyboardButton(text="⬅️ Назад"),
            ],
        ],
        resize_keyboard=True
    )


# =========================
# МЕНЮ СПИСКА КВАРТИР
# =========================

def apartments_menu(room_count):
    apartments = APARTMENTS[room_count]

    buttons = []

    for apartment in apartments:
        buttons.append([
            KeyboardButton(
                text=f"🏠 {apartment['title']} — {apartment['area']}"
            )
        ])

    buttons.append([
        KeyboardButton(text=f"⬅️ К списку {room_count}-комнатных")
    ])

    buttons.append([
        KeyboardButton(text="🏢 В меню Secret Garden")
    ])

    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )


# =========================
# МЕНЮ КОНКРЕТНОЙ КВАРТИРЫ
# =========================

def apartment_menu(room_count):
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📞 Получить консультацию")
            ],
            [
                KeyboardButton(
                    text=f"⬅️ К списку {room_count}-комнатных"
                )
            ],
            [
                KeyboardButton(text="🏢 В меню Secret Garden")
            ],
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
        resize_keyboard=True
    )

    await message.answer(
        "Добро пожаловать в Realty Partner.\n\n"
        "Здесь вы можете подобрать квартиру "
        "в современных жилых комплексах.\n\n"
        "Для начала отправьте ваш номер телефона.",
        reply_markup=keyboard
    )


# =========================
# ПОЛУЧЕНИЕ КОНТАКТА
# =========================

@dp.message(F.contact)
async def contact_handler(message: Message):

    await message.answer(
        "Спасибо!\n\n"
        "Добро пожаловать в Realty Partner 🏙\n\n"
        "Выберите жилой комплекс:",
        reply_markup=main_menu()
    )


# =========================
# SECRET GARDEN
# =========================

@dp.message(F.text == "🏙 Secret Garden")
async def secret_garden_handler(message: Message):

    await message.answer(
        "🏙 SECRET GARDEN\n\n"
        "Премиальная недвижимость для жизни в своём ритме.\n\n"
        "Secret Garden объединяет выразительную архитектуру, "
        "продуманные пространства и высокий уровень комфорта. "
        "Здесь каждая деталь подчинена одной идее — создать "
        "пространство, которое соответствует современному "
        "представлению о качественной жизни.\n\n"
        "Выберите категорию квартир и ознакомьтесь "
        "с доступными предложениями:",
        reply_markup=secret_garden_menu()
    )


# =========================
# СПИСОК 1-КОМНАТНЫХ
# =========================

@dp.message(F.text == "1️⃣ 1-комнатные")
async def one_room_handler(message: Message):

    await message.answer(
        "🏠 1-КОМНАТНЫЕ КВАРТИРЫ\n\n"
        "Доступные варианты в Secret Garden:",
        reply_markup=apartments_menu("1")
    )


# =========================
# СПИСОК 2-КОМНАТНЫХ
# =========================

@dp.message(F.text == "2️⃣ 2-комнатные")
async def two_room_handler(message: Message):

    await message.answer(
        "🏠 2-КОМНАТНЫЕ КВАРТИРЫ\n\n"
        "Доступные варианты в Secret Garden:",
        reply_markup=apartments_menu("2")
    )


# =========================
# СПИСОК 3-КОМНАТНЫХ
# =========================

@dp.message(F.text == "3️⃣ 3-комнатные")
async def three_room_handler(message: Message):

    await message.answer(
        "🏠 3-КОМНАТНЫЕ КВАРТИРЫ\n\n"
        "Доступные варианты в Secret Garden:",
        reply_markup=apartments_menu("3")
    )


# =========================
# СПИСОК 4-КОМНАТНЫХ
# =========================

@dp.message(F.text == "4️⃣ 4-комнатные")
async def four_room_handler(message: Message):

    await message.answer(
        "🏠 4-КОМНАТНЫЕ КВАРТИРЫ\n\n"
        "Доступные варианты в Secret Garden:",
        reply_markup=apartments_menu("4")
    )


# =========================
# ФУНКЦИЯ ПОИСКА КВАРТИРЫ
# =========================

def find_apartment(button_text):

    for room_count, apartments in APARTMENTS.items():

        for apartment in apartments:

            expected_text = (
                f"🏠 {apartment['title']} — {apartment['area']}"
            )

            if button_text == expected_text:
                return room_count, apartment

    return None, None


# =========================
# ОТКРЫТИЕ КВАРТИРЫ
# =========================

@dp.message(
    F.text.in_([
        "🏠 1-комнатная №101 — 42.5 м²",
        "🏠 1-комнатная №102 — 48.8 м²",
        "🏠 1-комнатная №103 — 51.2 м²",

        "🏠 2-комнатная №201 — 63.4 м²",
        "🏠 2-комнатная №202 — 71.8 м²",
        "🏠 2-комнатная №203 — 78.6 м²",

        "🏠 3-комнатная №301 — 92.1 м²",
        "🏠 3-комнатная №302 — 105.7 м²",
        "🏠 3-комнатная №303 — 118.3 м²",

        "🏠 4-комнатная №401 — 132.5 м²",
        "🏠 4-комнатная №402 — 148.9 м²",
        "🏠 4-комнатная №403 — 165.4 м²",
    ])
)
async def apartment_handler(message: Message):

    room_count, apartment = find_apartment(message.text)

    if not apartment:
        return

    text = (
        f"🏠 {apartment['title']}\n\n"
        f"📐 Площадь: {apartment['area']}\n"
        f"🛋 Планировка: {apartment['layout']}\n"
        f"🏢 Этаж: {apartment['floor']}\n"
        f"🌆 Вид: {apartment['view']}\n\n"
        f"💰 Стоимость: {apartment['price']}\n"
        f"🏦 Ипотека: до 30 лет\n"
        f"💳 Платёж: {apartment['payment']}\n\n"
        "🔗 Подробнее: https://example.com\n\n"
        "ℹ️ Все данные в данном разделе являются "
        "тестовыми и будут заменены на актуальные."
    )

    await message.answer(
        text,
        reply_markup=apartment_menu(room_count)
    )


# =========================
# КОНСУЛЬТАЦИЯ
# =========================

@dp.message(F.text == "📞 Получить консультацию")
async def consultation_handler(message: Message):

    await message.answer(
        "📞 КОНСУЛЬТАЦИЯ\n\n"
        "Оставьте заявку, и специалист Realty Partner "
        "свяжется с вами для уточнения стоимости, "
        "наличия квартир и условий покупки.\n\n"
        "ℹ️ Функция находится в разработке."
    )


# =========================
# ПРЕЗЕНТАЦИЯ
# =========================

@dp.message(F.text == "📑 Презентация")
async def presentation_handler(message: Message):

    await message.answer(
        "📑 ПРЕЗЕНТАЦИЯ SECRET GARDEN\n\n"
        "Презентация жилого комплекса будет доступна здесь.\n\n"
        "ℹ️ Раздел находится в разработке."
    )


# =========================
# УСЛОВИЯ ПРОДАЖИ
# =========================

@dp.message(F.text == "📄 Условия продажи")
async def sale_terms_handler(message: Message):

    await message.answer(
        "📄 УСЛОВИЯ ПРОДАЖИ\n\n"
        "Здесь будут размещены актуальные "
        "условия покупки квартир.\n\n"
        "ℹ️ Данные пока тестовые."
    )


# =========================
# ИПОТЕКА
# =========================

@dp.message(F.text == "🏦 Ипотечные программы")
async def mortgage_handler(message: Message):

    await message.answer(
        "🏦 ИПОТЕЧНЫЕ ПРОГРАММЫ\n\n"
        "👨‍👩‍👧 Семейная ипотека — от 3,99%\n"
        "🏦 Стандартная ипотека — от 15,5%\n"
        "💳 Рассрочка — индивидуальные условия\n\n"
        "ℹ️ Ставки указаны в качестве тестовых "
        "и будут заменены на актуальные."
    )


# =========================
# НАЗАД В SECRET GARDEN
# =========================

@dp.message(F.text == "🏢 В меню Secret Garden")
async def back_secret_garden(message: Message):

    await message.answer(
        "🏙 SECRET GARDEN\n\n"
        "Выберите интересующую категорию квартир:",
        reply_markup=secret_garden_menu()
    )


# =========================
# НАЗАД К СПИСКУ КВАРТИР
# =========================

@dp.message(F.text == "⬅️ К списку 1-комнатных")
async def back_one_room(message: Message):

    await message.answer(
        "🏠 1-КОМНАТНЫЕ КВАРТИРЫ\n\n"
        "Выберите квартиру:",
        reply_markup=apartments_menu("1")
    )


@dp.message(F.text == "⬅️ К списку 2-комнатных")
async def back_two_room(message: Message):

    await message.answer(
        "🏠 2-КОМНАТНЫЕ КВАРТИРЫ\n\n"
        "Выберите квартиру:",
        reply_markup=apartments_menu("2")
    )


@dp.message(F.text == "⬅️ К списку 3-комнатных")
async def back_three_room(message: Message):

    await message.answer(
        "🏠 3-КОМНАТНЫЕ КВАРТИРЫ\n\n"
        "Выберите квартиру:",
        reply_markup=apartments_menu("3")
    )


@dp.message(F.text == "⬅️ К списку 4-комнатных")
async def back_four_room(message: Message):

    await message.answer(
        "🏠 4-КОМНАТНЫЕ КВАРТИРЫ\n\n"
        "Выберите квартиру:",
        reply_markup=apartments_menu("4")
    )


# =========================
# НАЗАД В ГЛАВНОЕ МЕНЮ
# =========================

@dp.message(F.text == "⬅️ Назад")
async def back_main_menu(message: Message):

    await message.answer(
        "Выберите жилой комплекс:",
        reply_markup=main_menu()
    )


# =========================
# ВРЕМЕННЫЕ ЖК
# =========================

@dp.message(F.text.in_([
    "🏙 ЖК №2",
    "🏙 ЖК №3",
    "🏙 ЖК №4"
]))
async def other_complexes_handler(message: Message):

    await message.answer(
        f"{message.text}\n\n"
        "Раздел находится в разработке.\n\n"
        "Сейчас полностью доступен Secret Garden.",
        reply_markup=main_menu()
    )


# =========================
# ЗАПУСК БОТА
# =========================

async def main():

    if not TOKEN:
        raise ValueError(
            "Не найден BOT_TOKEN в файле .env"
        )

    bot = Bot(token=TOKEN)

    print("Бот запущен. Start polling")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())