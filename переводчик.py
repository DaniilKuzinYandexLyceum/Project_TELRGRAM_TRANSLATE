from pprint import pprint
import requests
import random
import json
import sqlite3

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = 'API_TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
con = sqlite3.connect('db.db')



@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    greeting = '''Привет! Я бот переводчик.
Вы можете написать мне сообщение на русском или английском языке и получить в ответ перевод на противоположном языке.
🇷🇺🔁🇺🇸'''
    await message.answer(greeting, reply_markup=None)


@dp.message_handler()
async def mes(message: types.Message):
    text = message.text
    en, ru = 0, 0
    for i in text:
        if i.lower() in 'qwertyuiopasdfghjklzxcvbnm':
            en += 1
        elif i.lower() in 'йцукенгшщзхъфывапролджэячсмитьбю':
            ru += 1
            
    url = "https://translated-mymemory---translation-memory.p.rapidapi.com/api/get"

    querystring = {"langpair":f"{'ru' if ru>en else 'en'}|{'en' if ru>en else 'ru'}","q":message.text,"mt":"1","onlyprivate":"0","de":"a@b.c"}

    headers = {
        'x-rapidapi-key': "x-rapidapi-key",
        'x-rapidapi-host': "translated-mymemory---translation-memory.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    await message.answer(response.json()['responseData']['translatedText'])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)