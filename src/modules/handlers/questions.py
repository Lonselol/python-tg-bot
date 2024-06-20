from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from modules.utils.calculations import calculate_daily_calories, calculate_bju

activity_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="низкий"), KeyboardButton(text="средний"), KeyboardButton(text="высокий")]
    ],
    resize_keyboard=True
)

goal_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="похудение"), KeyboardButton(text="поддержание веса"), KeyboardButton(text="набор веса")]
    ],
    resize_keyboard=True
)

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
    if not message.text.isdigit() or not (10 <= int(message.text) <= 300):
        await message.answer("Пожалуйста, введите корректный вес.")
        return
    await state.update_data(weight=int(message.text))
    await message.answer("Какой у тебя уровень физической активности?", reply_markup=activity_kb)
    await state.set_state(Form.activity)

@router.message(Form.activity)
async def process_activity(message: Message, state: FSMContext):
    if message.text.lower() not in ["низкий", "средний", "высокий"]:
        await message.answer("Пожалуйста, выберите уровень физической активности из предложенных вариантов.", reply_markup=activity_kb)
        return
    await state.update_data(activity=message.text.lower())
    await message.answer("Какая у тебя цель?", reply_markup=goal_kb)
    await state.set_state(Form.goal)

@router.message(Form.goal)
async def process_goal(message: Message, state: FSMContext):
    if message.text.lower() not in ["похудение", "поддержание веса", "набор веса"]:
        await message.answer("Пожалуйста, выберите цель из предложенных вариантов.", reply_markup=goal_kb)
        return
    await state.update_data(goal=message.text.lower())

    data = await state.get_data()
    daily_calories = calculate_daily_calories(data)
    bju = calculate_bju(daily_calories)

    await message.answer(
        f"Твоя дневная норма калорий: {daily_calories} ккал\n"
        f"Белки: {bju['proteins']} г\n"
        f"Жиры: {bju['fats']} г\n"
        f"Углеводы: {bju['carbs']} г",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.clear()
  
def register_handlers_start(router: Router):
    router.message.register(cmd_start, Command(commands="start"))
    router.message.register(process_age, Form.age)
    router.message.register(process_height, Form.height)
    router.message.register(process_weight, Form.weight)
    router.message.register(process_activity, Form.activity)
    router.message.register(process_goal, Form.goal)
