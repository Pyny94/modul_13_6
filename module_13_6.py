from aiogram.filters.command import CommandStart
from aiogram import Bot, Dispatcher, types,F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import logging
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


logging.basicConfig(level=logging.INFO)
api = ""
bot = Bot(token= api)
dp = Dispatcher()




class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()



@dp.message(CommandStart())
async def cmd_start(message: types.Message):
        await message.answer('Здравствуйте! Вас приветствует калькулятор подсчета калорий! ',
          reply_markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Рассчитать"),

                ]
            ],
            resize_keyboard=True,
        ),
    )
@dp.message(F.text == "Рассчитать")
async def main_menu(message):
    await message.answer('Выберите опцию:',
                         reply_markup=InlineKeyboardMarkup(
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="Рассчитать норму калорий'", callback_data='calories'),
                                     InlineKeyboardButton(text="Формулы расчёта", callback_data='formulas'),
                                 ]
                             ],
                             resize_keyboard=True,
                         ),
                 )



@dp.callback_query(F.data =='formulas')
async def get_formulas(call: types.CallbackQuery):
    await call.message.answer("Расчет калоррий по формуле Миффлина - Сан Жеора ")
    await call.answer()

@dp.callback_query(F.data =='calories')
async def set_age(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Введите свой возраст:')
    await state.set_state(UserState.age)
    await call.answer()


@dp.message(UserState.age)
async def set_growth(message: types.Message,  state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост(см):')
    await state.set_state(UserState.growth)

@dp.message(UserState.growth)
async def set_weight(message: types.Message,  state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await state.set_state(UserState.weight)

@dp.message(UserState.weight)
async def send_calories(message: types.Message,  state: FSMContext):
    await state.update_data(weight=message.text)
    await message.answer('Введите свой пол (м/ж):')
    await state.set_state(UserState.gender)

@dp.message(UserState.gender)
async def set_gender(message: types.Message, state: FSMContext):
    global calories
    await state.update_data(gender=message.text)
    data = await state.get_data()
    age_ = int(data['age'])
    growth_ = int(data['growth'])
    weight_ = int(data['weight'])

    if data["gender"].upper() == 'Ж':
        calories = (weight_ * 10) + (6.25 * growth_) - (5 * age_) - 161

    elif data["gender"].upper() == 'М':
        calories =(weight_*10) + (6.25 * growth_) - (5* age_) + 5

    await message.answer(f"Ваша норма калорий:{calories}")
    await state.finish()


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

