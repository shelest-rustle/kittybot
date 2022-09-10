import requests
from telegram import Bot

bot = Bot(token='5684496744:AAHVoS6GH0RJRt20Ewa57FS81abmV2Fvg3w')

URL = 'https://api.thecatapi.com/v1/images/search'
response = requests.get(URL).json()
random_cat_url = response[0].get('url')
chat_id = '540181178'
bot.send_photo(chat_id, random_cat_url)
