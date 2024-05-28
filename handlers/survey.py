from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import database

survey_router = Router()


class Survey(StatesGroup):
    name = State()
    age = State()
    occupation = State()
    salary = State()
    grade = State()
    rating = State()


@survey_router.message(Command("survey"))
async def start_survey(message: types.Message, state: FSMContext):
    await state.set_state(Survey.name)
    await message.answer("Как вас зовут?")


@survey_router.message(Survey.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await state.set_state(Survey.age)
    await message.answer("Сколько вам лет?")


@survey_router.message(Survey.age)
async def process_age(message: types.Message, state: FSMContext):
    age = message.text
    if not age.isdigit():
        await message.answer("Пожалуйста, введите число")
        return
    age = int(age)
    if age < 7 or age > 60:
        await message.answer("Пожалуйста, введите возраст от 7 до 60")
        return
    await state.update_data(age=age)

    if age > 18:
        await state.set_state(Survey.salary)
        await message.answer("Какова ваша заработная плата?")
    else:
        await state.set_state(Survey.grade)
        await message.answer("Какая у вас средняя оценка в школе?")

        await state.set_state(Survey.rating)


ratings = ["мегахарош", "харош", "мегаплох"]


@survey_router.message(Command("stop"))
@survey_router.message(Survey.rating, F.text.lower().in_(ratings))
async def process_rating(message: types.Message, state: FSMContext):
    rating = message.text
    rating = ratings.index(rating) + 3
    await state.update_data(rating=rating)
    await message.answer(f"Спасибо за прохождение опроса, {message.from_user.full_name}!")
    data = await state.get_data()
    print(data)
    await database.execute(
        "INSERT INTO surveys (name, age, occupation, salary, grade, rating) VALUES (?, ?, ?, ?, ?)",
        (data["name"], data["age"], data["occupation"], data["salary"], data["grade"], data["rating"]),
    )
    await state.clear()
