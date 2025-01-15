from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Рассчитать')],
        [KeyboardButton(text='Информация')],
        [KeyboardButton(text="Купить!")]
    ],resize_keyboard=True
)



ik = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')],
        [InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')],

    ]
)

buy_ik_key = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product1', callback_data="product_buying")],
        [InlineKeyboardButton(text='Product2', callback_data="product_buying")],
        [InlineKeyboardButton(text='Product3', callback_data="product_buying")],
        [InlineKeyboardButton(text='Product4', callback_data="product_buying")]
    ]
)




class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(f'Привет! {message.from_user.username}', reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=ik)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    calories = int(10 * weight + 6.25 * growth - 5 * age + 5)
    await message.answer(f'Ваша норма калорий в день {calories}')
    await state.finish()

@dp.message_handler(text='Купить!')
async def get_buying_list(message):
    with open("files\i.jpg", "rb") as img:
        await message.answer_photo(img, f"Название: Product1 | Описание: Ракетки для бадминтон  | Цена: {1*100}")
    with open("files\i (1).jpg", "rb") as img:
        await message.answer_photo(img, f"Название: Product2 | Описание: Мяч с кольцом  | Цена: {2*100}")
    with open("files\i (2).jpg", "rb") as img:
        await message.answer_photo(img, f"Название: Product3 | Описание: Мяч футбольный  | Цена: {5 * 100}")
    with open("files\i (3).jpg", "rb") as img:
        await message.answer_photo(img, f"Название: Product4 | Описание: Мяч баскетбольный  | Цена: {4 * 100}")
    await message.answer("Выберите продукт для покупки: ", reply_markup=buy_ik_key)


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
