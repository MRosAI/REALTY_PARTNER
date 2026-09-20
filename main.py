import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


# ============================================================
# НАСТРОЙКИ
# ============================================================

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# ============================================================
# СОСТОЯНИЯ
# ============================================================

class RealtyState(StatesGroup):
    browsing = State()


# ============================================================
# ДАННЫЕ ЖК
# ============================================================

COMPLEXES = {
    "Secret Garden": {
        "description": (
            "🏙 SECRET GARDEN\n\n"
            "Премиальная недвижимость для жизни в своём ритме.\n\n"
            "Secret Garden объединяет выразительную архитектуру, "
            "продуманные пространства и высокий уровень комфорта. "
            "Здесь каждая деталь подчинена одной идее — создать "
            "пространство, которое соответствует современному "
            "представлению о качественной жизни.\n\n"
            "Выберите категорию квартир и ознакомьтесь "
            "с доступными предложениями:"
        ),
        "apartments": {
            "1": [
                {
                    "title": "1-комнатная №101",
                    "area": "42.5 м²",
                    "layout": "Евроформат",
                    "floor": "12 из 24",
                    "view": "Во двор",
                    "price": "12 500 000 ₽",
                    "payment": "от 65 000 ₽/мес.",
                },
                {
                    "title": "1-комнатная №102",
                    "area": "48.8 м²",
                    "layout": "Евроформат",
                    "floor": "8 из 24",
                    "view": "На город",
                    "price": "14 200 000 ₽",
                    "payment": "от 74 000 ₽/мес.",
                },
                {
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
                    "title": "2-комнатная №201",
                    "area": "63.4 м²",
                    "layout": "Евроформат",
                    "floor": "7 из 24",
                    "view": "На парк",
                    "price": "18 900 000 ₽",
                    "payment": "от 99 000 ₽/мес.",
                },
                {
                    "title": "2-комнатная №202",
                    "area": "71.8 м²",
                    "layout": "Классическая",
                    "floor": "14 из 24",
                    "view": "На город",
                    "price": "21 500 000 ₽",
                    "payment": "от 112 000 ₽/мес.",
                },
                {
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
                    "title": "3-комнатная №301",
                    "area": "92.1 м²",
                    "layout": "Семейная",
                    "floor": "6 из 24",
                    "view": "На парк",
                    "price": "27 900 000 ₽",
                    "payment": "от 145 000 ₽/мес.",
                },
                {
                    "title": "3-комнатная №302",
                    "area": "105.7 м²",
                    "layout": "Master Bedroom",
                    "floor": "15 из 24",
                    "view": "На город",
                    "price": "32 500 000 ₽",
                    "payment": "от 169 000 ₽/мес.",
                },
                {
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
                    "title": "4-комнатная №401",
                    "area": "132.5 м²",
                    "layout": "Family Premium",
                    "floor": "9 из 24",
                    "view": "На парк",
                    "price": "42 500 000 ₽",
                    "payment": "от 221 000 ₽/мес.",
                },
                {
                    "title": "4-комнатная №402",
                    "area": "148.9 м²",
                    "layout": "Master Block",
                    "floor": "17 из 24",
                    "view": "На город",
                    "price": "49 800 000 ₽",
                    "payment": "от 259 000 ₽/мес.",
                },
                {
                    "title": "4-комнатная №403",
                    "area": "165.4 м²",
                    "layout": "Premium",
                    "floor": "23 из 24",
                    "view": "Панорамный вид",
                    "price": "58 900 000 ₽",
                    "payment": "от 307 000 ₽/мес.",
                },
            ],
        },
    },

    "ЖК№2-Tutorial": {
        "description": (
            "🏙 ЖК№2-Tutorial\n\n"
            "Современный жилой комплекс для комфортной городской жизни.\n\n"
            "Продуманные планировки, удобная инфраструктура "
            "и разнообразие квартир позволяют подобрать вариант "
            "под разные задачи и образ жизни.\n\n"
            "Выберите категорию квартир и ознакомьтесь "
            "с доступными предложениями:"
        ),
        "apartments": {
            "1": [
                {
                    "title": "1-комнатная №101",
                    "area": "39.8 м²",
                    "layout": "Евроформат",
                    "floor": "9 из 22",
                    "view": "Во двор",
                    "price": "9 800 000 ₽",
                    "payment": "от 51 000 ₽/мес.",
                },
                {
                    "title": "1-комнатная №102",
                    "area": "44.6 м²",
                    "layout": "Евроформат",
                    "floor": "13 из 22",
                    "view": "На город",
                    "price": "11 200 000 ₽",
                    "payment": "от 58 000 ₽/мес.",
                },
                {
                    "title": "1-комнатная №103",
                    "area": "49.2 м²",
                    "layout": "Свободная планировка",
                    "floor": "18 из 22",
                    "view": "Панорамный вид",
                    "price": "12 900 000 ₽",
                    "payment": "от 67 000 ₽/мес.",
                },
            ],
            "2": [
                {
                    "title": "2-комнатная №201",
                    "area": "58.4 м²",
                    "layout": "Евроформат",
                    "floor": "6 из 22",
                    "view": "На парк",
                    "price": "14 900 000 ₽",
                    "payment": "от 77 000 ₽/мес.",
                },
                {
                    "title": "2-комнатная №202",
                    "area": "66.7 м²",
                    "layout": "Классическая",
                    "floor": "11 из 22",
                    "view": "На город",
                    "price": "17 100 000 ₽",
                    "payment": "от 89 000 ₽/мес.",
                },
                {
                    "title": "2-комнатная №203",
                    "area": "73.5 м²",
                    "layout": "Master Bedroom",
                    "floor": "19 из 22",
                    "view": "Панорамный вид",
                    "price": "19 600 000 ₽",
                    "payment": "от 102 000 ₽/мес.",
                },
            ],
            "3": [
                {
                    "title": "3-комнатная №301",
                    "area": "87.2 м²",
                    "layout": "Семейная",
                    "floor": "5 из 22",
                    "view": "На парк",
                    "price": "21 900 000 ₽",
                    "payment": "от 114 000 ₽/мес.",
                },
                {
                    "title": "3-комнатная №302",
                    "area": "98.4 м²",
                    "layout": "Master Bedroom",
                    "floor": "14 из 22",
                    "view": "На город",
                    "price": "25 800 000 ₽",
                    "payment": "от 134 000 ₽/мес.",
                },
                {
                    "title": "3-комнатная №303",
                    "area": "111.6 м²",
                    "layout": "Premium",
                    "floor": "20 из 22",
                    "view": "Панорамный вид",
                    "price": "29 900 000 ₽",
                    "payment": "от 155 000 ₽/мес.",
                },
            ],
            "4": [
                {
                    "title": "4-комнатная №401",
                    "area": "125.8 м²",
                    "layout": "Family Premium",
                    "floor": "8 из 22",
                    "view": "На парк",
                    "price": "34 500 000 ₽",
                    "payment": "от 179 000 ₽/мес.",
                },
                {
                    "title": "4-комнатная №402",
                    "area": "139.4 м²",
                    "layout": "Master Block",
                    "floor": "15 из 22",
                    "view": "На город",
                    "price": "39 800 000 ₽",
                    "payment": "от 207 000 ₽/мес.",
                },
                {
                    "title": "4-комнатная №403",
                    "area": "154.2 м²",
                    "layout": "Premium",
                    "floor": "21 из 22",
                    "view": "Панорамный вид",
                    "price": "44 900 000 ₽",
                    "payment": "от 233 000 ₽/мес.",
                },
            ],
        },
    },

    "ЖК№3-GQR": {
        "description": (
            "🏙 ЖК№3-GQR\n\n"
            "Современное пространство для жизни, отдыха и развития.\n\n"
            "Комплекс объединяет функциональную архитектуру, "
            "разнообразие планировок и комфортную городскую среду.\n\n"
            "Выберите категорию квартир и ознакомьтесь "
            "с доступными предложениями:"
        ),
        "apartments": {
            "1": [
                {
                    "title": "1-комнатная №101",
                    "area": "37.5 м²",
                    "layout": "Евроформат",
                    "floor": "7 из 20",
                    "view": "Во двор",
                    "price": "8 900 000 ₽",
                    "payment": "от 46 000 ₽/мес.",
                },
                {
                    "title": "1-комнатная №102",
                    "area": "43.2 м²",
                    "layout": "Евроформат",
                    "floor": "12 из 20",
                    "view": "На город",
                    "price": "10 400 000 ₽",
                    "payment": "от 54 000 ₽/мес.",
                },
                {
                    "title": "1-комнатная №103",
                    "area": "47.8 м²",
                    "layout": "Свободная планировка",
                    "floor": "17 из 20",
                    "view": "Панорамный вид",
                    "price": "11 900 000 ₽",
                    "payment": "от 62 000 ₽/мес.",
                },
            ],
            "2": [
                {
                    "title": "2-комнатная №201",
                    "area": "56.9 м²",
                    "layout": "Евроформат",
                    "floor": "5 из 20",
                    "view": "На парк",
                    "price": "13 800 000 ₽",
                    "payment": "от 72 000 ₽/мес.",
                },
                {
                    "title": "2-комнатная №202",
                    "area": "64.5 м²",
                    "layout": "Классическая",
                    "floor": "10 из 20",
                    "view": "На город",
                    "price": "16 200 000 ₽",
                    "payment": "от 84 000 ₽/мес.",
                },
                {
                    "title": "2-комнатная №203",
                    "area": "72.1 м²",
                    "layout": "Master Bedroom",
                    "floor": "18 из 20",
                    "view": "Панорамный вид",
                    "price": "18 700 000 ₽",
                    "payment": "от 97 000 ₽/мес.",
                },
            ],
            "3": [
                {
                    "title": "3-комнатная №301",
                    "area": "84.6 м²",
                    "layout": "Семейная",
                    "floor": "4 из 20",
                    "view": "На парк",
                    "price": "20 500 000 ₽",
                    "payment": "от 106 000 ₽/мес.",
                },
                {
                    "title": "3-комнатная №302",
                    "area": "96.8 м²",
                    "layout": "Master Bedroom",
                    "floor": "13 из 20",
                    "view": "На город",
                    "price": "24 300 000 ₽",
                    "payment": "от 126 000 ₽/мес.",
                },
                {
                    "title": "3-комнатная №303",
                    "area": "108.9 м²",
                    "layout": "Premium",
                    "floor": "19 из 20",
                    "view": "Панорамный вид",
                    "price": "28 600 000 ₽",
                    "payment": "от 148 000 ₽/мес.",
                },
            ],
            "4": [
                {
                    "title": "4-комнатная №401",
                    "area": "120.4 м²",
                    "layout": "Family Premium",
                    "floor": "6 из 20",
                    "view": "На парк",
                    "price": "32 900 000 ₽",
                    "payment": "от 171 000 ₽/мес.",
                },
                {
                    "title": "4-комнатная №402",
                    "area": "137.6 м²",
                    "layout": "Master Block",
                    "floor": "14 из 20",
                    "view": "На город",
                    "price": "37 500 000 ₽",
                    "payment": "от 195 000 ₽/мес.",
                },
                {
                    "title": "4-комнатная №403",
                    "area": "149.8 м²",
                    "layout": "Premium",
                    "floor": "19 из 20",
                    "view": "Панорамный вид",
                    "price": "42 800 000 ₽",
                    "payment": "от 222 000 ₽/мес.",
                },
            ],
        },
    },

    "ЖК№4-MMM": {
        "description": (
            "🏙 ЖК№4-MMM\n\n"
            "Новый уровень комфорта в современной городской среде.\n\n"
            "Разнообразие квартир, продуманные пространства "
            "и современные решения позволяют выбрать подходящий "
            "вариант для жизни или инвестиций.\n\n"
            "Выберите категорию квартир и ознакомьтесь "
            "с доступными предложениями:"
        ),
        "apartments": {
            "1": [
                {
                    "title": "1-комнатная №101",
                    "area": "40.2 м²",
                    "layout": "Евроформат",
                    "floor": "8 из 25",
                    "view": "Во двор",
                    "price": "10 200 000 ₽",
                    "payment": "от 53 000 ₽/мес.",
                },
                {
                    "title": "1-комнатная №102",
                    "area": "46.3 м²",
                    "layout": "Евроформат",
                    "floor": "14 из 25",
                    "view": "На город",
                    "price": "12 100 000 ₽",
                    "payment": "от 63 000 ₽/мес.",
                },
                {
                    "title": "1-комнатная №103",
                    "area": "52.6 м²",
                    "layout": "Свободная планировка",
                    "floor": "21 из 25",
                    "view": "Панорамный вид",
                    "price": "14 000 000 ₽",
                    "payment": "от 73 000 ₽/мес.",
                },
            ],
            "2": [
                {
                    "title": "2-комнатная №201",
                    "area": "61.7 м²",
                    "layout": "Евроформат",
                    "floor": "7 из 25",
                    "view": "На парк",
                    "price": "17 500 000 ₽",
                    "payment": "от 91 000 ₽/мес.",
                },
                {
                    "title": "2-комнатная №202",
                    "area": "70.4 м²",
                    "layout": "Классическая",
                    "floor": "13 из 25",
                    "view": "На город",
                    "price": "20 100 000 ₽",
                    "payment": "от 104 000 ₽/мес.",
                },
                {
                    "title": "2-комнатная №203",
                    "area": "79.3 м²",
                    "layout": "Master Bedroom",
                    "floor": "22 из 25",
                    "view": "Панорамный вид",
                    "price": "23 600 000 ₽",
                    "payment": "от 123 000 ₽/мес.",
                },
            ],
            "3": [
                {
                    "title": "3-комнатная №301",
                    "area": "90.8 м²",
                    "layout": "Семейная",
                    "floor": "6 из 25",
                    "view": "На парк",
                    "price": "26 800 000 ₽",
                    "payment": "от 139 000 ₽/мес.",
                },
                {
                    "title": "3-комнатная №302",
                    "area": "103.5 м²",
                    "layout": "Master Bedroom",
                    "floor": "15 из 25",
                    "view": "На город",
                    "price": "31 200 000 ₽",
                    "payment": "от 162 000 ₽/мес.",
                },
                {
                    "title": "3-комнатная №303",
                    "area": "116.8 м²",
                    "layout": "Premium",
                    "floor": "23 из 25",
                    "view": "Панорамный вид",
                    "price": "36 900 000 ₽",
                    "payment": "от 192 000 ₽/мес.",
                },
            ],
            "4": [
                {
                    "title": "4-комнатная №401",
                    "area": "129.6 м²",
                    "layout": "Family Premium",
                    "floor": "9 из 25",
                    "view": "На парк",
                    "price": "40 900 000 ₽",
                    "payment": "от 212 000 ₽/мес.",
                },
                {
                    "title": "4-комнатная №402",
                    "area": "143.7 м²",
                    "layout": "Master Block",
                    "floor": "17 из 25",
                    "view": "На город",
                    "price": "46 700 000 ₽",
                    "payment": "от 243 000 ₽/мес.",
                },
                {
                    "title": "4-комнатная №403",
                    "area": "161.2 м²",
                    "layout": "Premium",
                    "floor": "24 из 25",
                    "view": "Панорамный вид",
                    "price": "53 900 000 ₽",
                    "payment": "от 280 000 ₽/мес.",
                },
            ],
        },
    },
}


# ============================================================
# ГЛАВНОЕ МЕНЮ
# ============================================================

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🏙 Secret Garden"),
            ],
            [
                KeyboardButton(text="🏙 ЖК№2-Tutorial"),
                KeyboardButton(text="🏙 ЖК№3-GQR"),
            ],
            [
                KeyboardButton(text="🏙 ЖК№4-MMM"),
            ],
        ],
        resize_keyboard=True,
    )


# ============================================================
# МЕНЮ ЖК
# ============================================================

def complex_menu():
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
            ],
            [
                KeyboardButton(text="📄 Условия продажи"),
            ],
            [
                KeyboardButton(text="🏦 Ипотечные программы"),
            ],
            [
                KeyboardButton(text="⬅️ Назад"),
            ],
        ],
        resize_keyboard=True,
    )


# ============================================================
# МЕНЮ КВАРТИР
# ============================================================

def apartments_menu(apartments, room_count):
    buttons = []

    for apartment in apartments:
        buttons.append(
            [
                KeyboardButton(
                    text=f"🏠 {apartment['title']} — {apartment['area']}"
                )
            ]
        )

    buttons.append(
        [
            KeyboardButton(
                text=f"⬅️ К списку {room_count}-комнатных"
            )
        ]
    )

    buttons.append(
        [
            KeyboardButton(text="⬅️ В меню ЖК")
        ]
    )

    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
    )


# ============================================================
# МЕНЮ КВАРТИРЫ
# ============================================================

def apartment_menu(room_count):
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📞 Получить консультацию"),
            ],
            [
                KeyboardButton(
                    text=f"⬅️ К списку {room_count}-комнатных"
                ),
            ],
            [
                KeyboardButton(text="🏢 В меню ЖК"),
            ],
        ],
        resize_keyboard=True,
    )


# ============================================================
# ПОКАЗ МЕНЮ ЖК
# ============================================================

async def show_complex(
    message: Message,
    state: FSMContext,
    complex_name: str,
):
    await state.set_state(RealtyState.browsing)

    await state.update_data(
        complex_name=complex_name,
        room_count=None,
        apartment=None,
    )

    complex_data = COMPLEXES[complex_name]

    await message.answer(
        complex_data["description"],
        reply_markup=complex_menu(),
    )


# ============================================================
# ПОКАЗ СПИСКА КВАРТИР
# ============================================================

async def show_room_list(
    message: Message,
    state: FSMContext,
    room_count: str,
):
    data = await state.get_data()
    complex_name = data.get("complex_name")

    if not complex_name or complex_name not in COMPLEXES:
        await message.answer(
            "Сначала выберите жилой комплекс.",
            reply_markup=main_menu(),
        )
        return

    apartments = COMPLEXES[complex_name]["apartments"].get(
        room_count,
        [],
    )

    await state.update_data(
        room_count=room_count,
        apartment=None,
    )

    room_names = {
        "1": "1-комнатных",
        "2": "2-комнатных",
        "3": "3-комнатных",
        "4": "4-комнатных",
    }

    await message.answer(
        f"🏠 {complex_name}\n\n"
        f"Доступные {room_names[room_count]} квартиры:",
        reply_markup=apartments_menu(
            apartments,
            room_count,
        ),
    )


# ============================================================
# START
# ============================================================

@dp.message(CommandStart())
async def start_handler(
    message: Message,
    state: FSMContext,
):
    await state.clear()

    await message.answer(
        "🏠 Добро пожаловать в каталог недвижимости.\n\n"
        "Выберите жилой комплекс:",
        reply_markup=main_menu(),
    )


# ============================================================
# ВЫБОР ЖК
# ============================================================

@dp.message(F.text == "🏙 Secret Garden")
async def secret_garden_handler(
    message: Message,
    state: FSMContext,
):
    await show_complex(
        message,
        state,
        "Secret Garden",
    )


@dp.message(F.text == "🏙 ЖК№2-Tutorial")
async def tutorial_handler(
    message: Message,
    state: FSMContext,
):
    await show_complex(
        message,
        state,
        "ЖК№2-Tutorial",
    )


@dp.message(F.text == "🏙 ЖК№3-GQR")
async def gqr_handler(
    message: Message,
    state: FSMContext,
):
    await show_complex(
        message,
        state,
        "ЖК№3-GQR",
    )


@dp.message(F.text == "🏙 ЖК№4-MMM")
async def mmm_handler(
    message: Message,
    state: FSMContext,
):
    await show_complex(
        message,
        state,
        "ЖК№4-MMM",
    )


# ============================================================
# ВЫБОР КОЛИЧЕСТВА КОМНАТ
# ============================================================

@dp.message(F.text == "1️⃣ 1-комнатные")
async def one_room_handler(
    message: Message,
    state: FSMContext,
):
    await show_room_list(
        message,
        state,
        "1",
    )


@dp.message(F.text == "2️⃣ 2-комнатные")
async def two_room_handler(
    message: Message,
    state: FSMContext,
):
    await show_room_list(
        message,
        state,
        "2",
    )


@dp.message(F.text == "3️⃣ 3-комнатные")
async def three_room_handler(
    message: Message,
    state: FSMContext,
):
    await show_room_list(
        message,
        state,
        "3",
    )


@dp.message(F.text == "4️⃣ 4-комнатные")
async def four_room_handler(
    message: Message,
    state: FSMContext,
):
    await show_room_list(
        message,
        state,
        "4",
    )


# ============================================================
# ПРОСМОТР КВАРТИРЫ
# ============================================================

@dp.message(F.text.startswith("🏠 "))
async def apartment_handler(
    message: Message,
    state: FSMContext,
):
    data = await state.get_data()

    complex_name = data.get("complex_name")
    room_count = data.get("room_count")

    if not complex_name or not room_count:
        await message.answer(
            "Сначала выберите жилой комплекс.",
            reply_markup=main_menu(),
        )
        return

    apartments = COMPLEXES[complex_name]["apartments"].get(
        room_count,
        [],
    )

    selected_text = message.text

    selected_apartment = None

    for apartment in apartments:
        button_text = (
            f"🏠 {apartment['title']} — "
            f"{apartment['area']}"
        )

        if button_text == selected_text:
            selected_apartment = apartment
            break

    if not selected_apartment:
        await message.answer(
            "Квартира не найдена.",
            reply_markup=complex_menu(),
        )
        return

    await state.update_data(
        apartment=selected_apartment,
    )

    apartment_text = (
        f"🏠 {selected_apartment['title']}\n\n"
        f"🏙 ЖК: {complex_name}\n"
        f"📐 Площадь: {selected_apartment['area']}\n"
        f"🛋 Планировка: {selected_apartment['layout']}\n"
        f"🏢 Этаж: {selected_apartment['floor']}\n"
        f"🌆 Вид: {selected_apartment['view']}\n\n"
        f"💰 Стоимость: {selected_apartment['price']}\n"
        f"🏦 Ипотека: до 30 лет\n"
        f"💳 Платёж: {selected_apartment['payment']}\n\n"
        f"🔗 Подробнее: https://example.com\n\n"
        f"ℹ️ Информация является тестовой."
    )

    await message.answer(
        apartment_text,
        reply_markup=apartment_menu(room_count),
    )


# ============================================================
# НАЗАД К СПИСКУ КВАРТИР
# ============================================================

@dp.message(F.text == "⬅️ К списку 1-комнатных")
async def back_one_room(
    message: Message,
    state: FSMContext,
):
    await show_room_list(message, state, "1")


@dp.message(F.text == "⬅️ К списку 2-комнатных")
async def back_two_room(
    message: Message,
    state: FSMContext,
):
    await show_room_list(message, state, "2")


@dp.message(F.text == "⬅️ К списку 3-комнатных")
async def back_three_room(
    message: Message,
    state: FSMContext,
):
    await show_room_list(message, state, "3")


@dp.message(F.text == "⬅️ К списку 4-комнатных")
async def back_four_room(
    message: Message,
    state: FSMContext,
):
    await show_room_list(message, state, "4")


# ============================================================
# В МЕНЮ ЖК
# ============================================================

@dp.message(F.text == "⬅️ В меню ЖК")
async def back_to_complex_from_list(
    message: Message,
    state: FSMContext,
):
    data = await state.get_data()
    complex_name = data.get("complex_name")

    if not complex_name or complex_name not in COMPLEXES:
        await message.answer(
            "Выберите жилой комплекс:",
            reply_markup=main_menu(),
        )
        return

    await state.update_data(
        room_count=None,
        apartment=None,
    )

    await message.answer(
        COMPLEXES[complex_name]["description"],
        reply_markup=complex_menu(),
    )


@dp.message(F.text == "🏢 В меню ЖК")
async def back_to_complex_from_apartment(
    message: Message,
    state: FSMContext,
):
    data = await state.get_data()
    complex_name = data.get("complex_name")

    if not complex_name or complex_name not in COMPLEXES:
        await message.answer(
            "Выберите жилой комплекс:",
            reply_markup=main_menu(),
        )
        return

    await state.update_data(
        room_count=None,
        apartment=None,
    )

    await message.answer(
        COMPLEXES[complex_name]["description"],
        reply_markup=complex_menu(),
    )


# ============================================================
# НАЗАД В ГЛАВНОЕ МЕНЮ
# ============================================================

@dp.message(F.text == "⬅️ Назад")
async def back_to_main(
    message: Message,
    state: FSMContext,
):
    await state.clear()

    await message.answer(
        "🏠 Выберите жилой комплекс:",
        reply_markup=main_menu(),
    )


# ============================================================
# ПРЕЗЕНТАЦИЯ
# ============================================================

@dp.message(F.text == "📑 Презентация")
async def presentation_handler(
    message: Message,
    state: FSMContext,
):
    data = await state.get_data()
    complex_name = data.get("complex_name", "жилого комплекса")

    await message.answer(
        f"📑 Презентация\n\n"
        f"{complex_name}\n\n"
        f"Файл презентации будет добавлен позже.\n\n"
        f"Сейчас используется тестовый раздел."
    )


# ============================================================
# УСЛОВИЯ ПРОДАЖИ
# ============================================================

@dp.message(F.text == "📄 Условия продажи")
async def sale_terms_handler(
    message: Message,
    state: FSMContext,
):
    data = await state.get_data()
    complex_name = data.get("complex_name", "жилого комплекса")

    await message.answer(
        f"📄 Условия продажи\n\n"
        f"{complex_name}\n\n"
        f"Документ с условиями продажи будет добавлен позже.\n\n"
        f"Сейчас используется тестовый раздел."
    )


# ============================================================
# ИПОТЕЧНЫЕ ПРОГРАММЫ
# ============================================================

@dp.message(F.text == "🏦 Ипотечные программы")
async def mortgage_handler(
    message: Message,
    state: FSMContext,
):
    data = await state.get_data()
    complex_name = data.get("complex_name", "жилого комплекса")

    await message.answer(
        f"🏦 Ипотечные программы\n\n"
        f"{complex_name}\n\n"
        f"👨‍👩‍👧 Семейная ипотека — от 3.99%\n"
        f"🏦 Стандартная ипотека — от 15.5%\n"
        f"💳 Рассрочка — индивидуальные условия\n\n"
        f"ℹ️ Ставки указаны для тестовой версии."
    )


# ============================================================
# КОНСУЛЬТАЦИЯ
# ============================================================

@dp.message(F.text == "📞 Получить консультацию")
async def consultation_handler(
    message: Message,
    state: FSMContext,
):
    data = await state.get_data()

    complex_name = data.get(
        "complex_name",
        "жилого комплекса",
    )

    apartment = data.get("apartment")

    if apartment:
        await message.answer(
            f"📞 Консультация\n\n"
            f"Вы выбрали:\n"
            f"{complex_name}\n"
            f"{apartment['title']}\n"
            f"{apartment['area']}\n\n"
            f"Функция связи с менеджером "
            f"будет добавлена позже."
        )
    else:
        await message.answer(
            f"📞 Консультация по объекту\n\n"
            f"{complex_name}\n\n"
            f"Функция связи с менеджером "
            f"будет добавлена позже."
        )


# ============================================================
# НЕИЗВЕСТНАЯ КОМАНДА
# ============================================================

@dp.message()
async def unknown_handler(message: Message):
    await message.answer(
        "Пожалуйста, используйте кнопки меню.",
        reply_markup=main_menu(),
    )


# ============================================================
# ЗАПУСК
# ============================================================

async def main():
    print("Бот запускается...")
    print("Подключение к Telegram...")

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        print("Webhook очищен.")

        print("Запускаем polling...")
        await dp.start_polling(bot)

    except Exception as e:
        print(f"ОШИБКА: {e}")

    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())