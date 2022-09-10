import logging
import requests
import os
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler

load_dotenv()
token = os.getenv('TOKEN')
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

URL = 'https://api.thecatapi.com/v1/images/search'


def get_new_image():
    try:
        response = requests.get(URL)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)

    random_cat = response.json()[0].get('url')
    return random_cat


def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    # За счёт параметра resize_keyboard=True сделаем кнопки поменьше
    buttons = ReplyKeyboardMarkup([['/newcat'],
                                  ['/start']],
                                  resize_keyboard=True)
    context.bot.send_message(chat_id=chat.id,
                             text=f'Привет, {name}. '
                                  'Посмотри, какого котика я тебе нашёл!',
                             reply_markup=buttons)
    context.bot.send_photo(chat.id, get_new_image())


def main():
    updater = Updater(token)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))
    updater.start_polling()


if __name__ == '__main__':
    main()
