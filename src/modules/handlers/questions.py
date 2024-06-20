from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from modules.utils.calculations import calculate_daily_calories, calculate_bju

class Form(StatesGroup):
    age = State()
    height = State()
    weight = State()
    activity = State()
    goal = State()

router = Router()  # [1]

@router.message(Command("start"))  # [2]
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Привет! Я помогу тебе следить за питанием. Сколько тебе лет?")
    await state.set_state(Form.age)

@router.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer("Какой у тебя рост (в см)?")
    await state.set_state(Form.height)

@router.message(Form.height)
async def process_height(message: Message, state: FSMContext):
    await state.update_data(height=int(message.text))
    await message.answer("Какой у тебя вес (в кг)?")
    await state.set_state(Form.weight)

@router.message(Form.weight)
async def process_weight(message: Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    await message.answer("Какой у тебя уровень физической активности? (низкий, средний, высокий)")
    await state.set_state(Form.activity)

@router.message(Form.activity)
async def process_activity(message: Message, state: FSMContext):
    await state.update_data(activity=message.text.lower())
    await message.answer("Какая у тебя цель? (похудение, поддержание веса, набор веса)")
    await state.set_state(Form.goal)

@router.message(Form.goal)
async def process_goal(message: Message, state: FSMContext):
    await state.update_data(goal=message.text.lower())

    data = await state.get_data()
    daily_calories = calculate_daily_calories(data)
    bju = calculate_bju(daily_calories)

    await message.answer(
        f"Твоя дневная норма калорий: {daily_calories} ккал\n"
        f"Белки: {bju['proteins']} г\n"
        f"Жиры: {bju['fats']} г\n"
        f"Углеводы: {bju['carbs']} г"
    )

    await state.clear()
  
def register_handlers_start(router: Router):
    router.message.register(cmd_start, Command(commands="start"))
    router.message.register(process_age, Form.age)
    router.message.register(process_height, Form.height)
    router.message.register(process_weight, Form.weight)
    router.message.register(process_activity, Form.activity)
    router.message.register(process_goal, Form.goal)