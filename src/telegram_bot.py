import json
import time
from parser import collect_data
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from auth_data import token

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Ситилинк']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Выберите сайт', reply_markup=keyboard)


@dp.message_handler(Text(equals='Ситилинк'))
async def get_citilink_data(message: types.Message):
    await message.answer('Пожалуйста подождите!')
    collect_data()

    with open("../out/json/result.json", encoding="utf-8") as file:
        data = json.load(file)

        for index, item in enumerate(data):
            card = f'{hlink(item.get("title"), item.get("url"))}\n' \
                f'{hbold("Скидка: ")}{item.get("discount")}\n' \
                f'{hbold("Старая цена: ")}{item.get("old_price")}\n' \
                f'{hbold("Цена: ")}{item.get("price")}'

            if index % 20 == 0:
                time.sleep(3)

            await message.answer(card)