from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command

from modules.utils.data import get_product_info, calculate_meal_bju

class BJUForm(StatesGroup):
    product = State()
    meal = State()

router = Router()

@router.message(Command("bju_product"))
async def cmd_bju_product(message: Message, state: FSMContext):
    await message.answer("Введите название продукта:")
    await state.set_state(BJUForm.product)

@router.message(BJUForm.product)
async def process_bju_product(message: Message, state: FSMContext):
    product_name = message.text
    product_info = get_product_info(product_name)
    if product_info:
        await message.answer(f"КБЖУ продукта {product_name}:\n"
                             f"Калории: {product_info['calories']} ккал\n"
                             f"Белки: {product_info['proteins']} г\n"
                             f"Жиры: {product_info['fats']} г\n"
                             f"Углеводы: {product_info['carbs']} г")
    else:
        await message.answer("Продукт не найден, попробуйте другой.")
    await state.clear()

@router.message(Command("bju_meal"))
async def cmd_bju_meal(message: Message, state: FSMContext):
    await message.answer("Введите список продуктов и их количество (например, 'творог 200г, яблоко 100г'):")
    await state.set_state(BJUForm.meal)

@router.message(BJUForm.meal)
async def process_bju_meal(message: Message, state: FSMContext):
    meal_description = message.text
    meal_bju = calculate_meal_bju(meal_description)
    if meal_bju:
        await message.answer(f"КБЖУ приёма пищи:\n"
                             f"Калории: {meal_bju['calories']} ккал\n"
                             f"Белки: {meal_bju['proteins']} г\n"
                             f"Жиры: {meal_bju['fats']} г\n"
                             f"Углеводы: {meal_bju['carbs']} г")
    else:
        await message.answer("Не удалось рассчитать КБЖУ, проверьте правильность ввода.")
    await state.clear()

def register_handlers_bju(router: Router):
    router.message.register(cmd_bju_product, Command(commands="bju_product"))
    router.message.register(process_bju_product, BJUForm.product)
    router.message.register(cmd_bju_meal, Command(commands="bju_meal"))
    router.message.register(process_bju_meal, BJUForm.meal)