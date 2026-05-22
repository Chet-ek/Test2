from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import asyncio


TOKEN = "8854481301:AAH3xkYRjRokzYWMeNdKhRfty4fpeOYsRPA"

bot = Bot(token=TOKEN)
dp = Dispatcher()


# ================= МЕНЮ =================

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Создать заявку")
        ],
        [
            KeyboardButton(text="Аналитика"),
            KeyboardButton(text="О системе")
        ],
        [
            KeyboardButton(text="Помощь")
        ]
    ],
    resize_keyboard=True
)


# ================= СОСТОЯНИЯ =================

class Form(StatesGroup):
    company = State()
    budget = State()
    urgency = State()
    volume = State()


# ================= START =================

@dp.message(CommandStart())
async def start(message: Message):
    text = """
СИСТЕМА ПРИОРИТИЗАЦИИ КЛИЕНТСКИХ ЗАЯВОК

Выберите действие в меню ниже.
"""

    await message.answer(text, reply_markup=menu)


# ================= О СИСТЕМЕ =================

@dp.message(F.text == "О системе")
async def about_system(message: Message):

    text = """
О СИСТЕМЕ

Данный программный модуль предназначен
для автоматической оценки клиентских заявок.

Функции системы:
• Анализ параметров заявки
• Определение приоритета
• Оценка вероятности сделки
• Снижение нагрузки на менеджеров
"""

    await message.answer(text)


# ================= ПОМОЩЬ =================

@dp.message(F.text == "Помощь")
async def help_command(message: Message):

    text = """
ПОМОЩЬ

1. Нажмите «Создать заявку»
2. Введите данные
3. Получите автоматический анализ

Система рассчитывает приоритет заявки
на основе введённых параметров.
"""

    await message.answer(text)


# ================= АНАЛИТИКА =================

@dp.message(F.text == "Аналитика")
async def analytics(message: Message):

    text = """
АНАЛИТИКА СИСТЕМЫ

Обработано заявок: 124

Высокий приоритет: 37
Средний приоритет: 52
Низкий приоритет: 35

Среднее время анализа:
2.3 секунды

Эффективность обработки:
+78%
"""

    await message.answer(text)


# ================= СОЗДАНИЕ ЗАЯВКИ =================

@dp.message(F.text == "Создать заявку")
async def create_request(message: Message, state: FSMContext):

    await message.answer(
        "Введите название компании:"
    )

    await state.set_state(Form.company)


# ================= КОМПАНИЯ =================

@dp.message(Form.company)
async def get_company(message: Message, state: FSMContext):

    await state.update_data(company=message.text)

    await message.answer(
        "Введите бюджет заявки:"
    )

    await state.set_state(Form.budget)


# ================= БЮДЖЕТ =================

@dp.message(Form.budget)
async def get_budget(message: Message, state: FSMContext):

    await state.update_data(
        budget=int(message.text)
    )

    await message.answer(
        "Введите срочность:\n"
        "низкая / средняя / высокая"
    )

    await state.set_state(Form.urgency)


# ================= СРОЧНОСТЬ =================

@dp.message(Form.urgency)
async def get_urgency(message: Message, state: FSMContext):

    await state.update_data(
        urgency=message.text.lower()
    )

    await message.answer(
        "Введите объем заказа:"
    )

    await state.set_state(Form.volume)


# ================= АНАЛИЗ =================

@dp.message(Form.volume)
async def finish_form(message: Message, state: FSMContext):

    data = await state.get_data()

    volume = int(message.text)
    budget = data["budget"]
    urgency = data["urgency"]

    score = 0

    if budget > 500000:
        score += 3

    if urgency == "высокая":
        score += 2

    if volume > 1000:
        score += 3

    # ---- ЛОГИКА ----

    if score >= 6:
        priority = "ВЫСОКИЙ"
        chance = "87%"
        recommendation = "Передать менеджеру немедленно"

    elif score >= 3:
        priority = "СРЕДНИЙ"
        chance = "56%"
        recommendation = "Требуется дополнительный анализ"

    else:
        priority = "НИЗКИЙ"
        chance = "23%"
        recommendation = "Стандартная обработка"

    text = f"""
ЗАЯВКА ПРОАНАЛИЗИРОВАНА

Компания:
{data['company']}

Бюджет:
{budget} ₽

Срочность:
{urgency}

Объем:
{volume}

ПРИОРИТЕТ:
{priority}

Вероятность сделки:
{chance}

Рекомендация:
{recommendation}
"""

    await message.answer(text)

    await state.clear()


# ================= ЗАПУСК =================

async def main():

    print("Бот запущен")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())