import asyncio
import json

import logging
import requests

import yandex_weather_api
from aiogram import Bot, Dispatcher, types
from aiogram import html
from aiogram.filters import Command
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
from geopy import Nominatim

import configparser
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)




config = configparser.ConfigParser()
config.sections()
config.read('config.ini')
bot_token = config['tg_token']['token']
yandex_key = config['yandex']['api_key']
# Объект бота
bot = Bot(token=bot_token)
# Диспетчер
dp = Dispatcher()


def get_coordonats(sity: str):
    geolocator = Nominatim(user_agent="Tester")
    location = geolocator.geocode(sity)  # Создаем переменную, которая состоит из нужного нам адреса
    return location.latitude, location.longitude


# новый импорт!
from datetime import datetime

temp_mess = []


@dp.message()
async def echo_with_time(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="узнать погоду?",
        callback_data="get_weather")
    )
    await message.answer(
        f"хотите узнать погоду в {message.text}? {message.message_id}",
        reply_markup=builder.as_markup(), reply_to_message_id=message.message_id,
    )
    temp_mess.append(message.text)


@dp.callback_query(F.data == "get_weather")
async def get_weather(callback: types.CallbackQuery, temp_mess=temp_mess):
    #
    if temp_mess:
        temp2_mess = temp_mess[0]
        print(temp2_mess)
        temp_mess.clear()
        try:
            l1, l2 = get_coordonats(temp2_mess)
            api_key = yandex_key  #
            weather_now = yandex_weather_api.get(api_key=api_key, session=requests, lat=l1, lon=l2)['forecast']
            print(weather_now[0])
            weather_today = json.dumps(weather_now[0])
            weather_today = json.loads(weather_today)
            weather_today = weather_today['parts']['day']['temp_avg']
            await callback.message.answer(f'Сегодня средняя темпрература в {temp2_mess} : {weather_today} градусов')
        except AttributeError:
            return await callback.message.answer(f'город  не найден')

    else:
        await callback.message.answer(f'город {temp_mess[0]} не найден')


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
