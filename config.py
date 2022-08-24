import telebot
import requests
from bs4 import BeautifulSoup

bot_token = 'bot_token'
bot = telebot.TeleBot(bot_token)

api_key = 'api_key'
url = f'https://v6.exchangerate-api.com/v6/{api_key}/'

# Так как в API нет вызова для получения списка валют, то данные получаем со страницы описания с помощью BeautifulSoup
list_of_currencies_url = r'https://www.exchangerate-api.com/docs/supported-currencies'

