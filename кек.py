import requests
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = '6853840346:AAF4apUhzB6vd6YpVqcicmxVAZthDdza0fk'
URL = 'https://api.openweathermap.org/data/2.5/weather'
API_KEY = 'https://api.openweathermap.org/data/2.5/weather'
bot = telebot.TeleBot(TOKEN)
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton('Получить погоду', request_location=True))
keyboard.add(KeyboardButton('О проекте'))


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    text = 'Отправь мне свое местоположение и я отправлю тебе погоду'
    bot.send_message(message.chat.id, text, reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def send_weather(message):
    lon = message.location.longitude
    lat = message.location.latitude
    rez = get_weather(lat, lon)
    if rez:
        bot.send_message(message.chat.id, rez, reply_markup=keyboard)


def get_weather(lat, lon):
    params = {'lat': lat,
              'lon': lon,
              'lang': 'ru',
              'units': 'metric',
              'appid': API_KEY}
    response = requests.get(url=URL, params=params).json()
    print(response)
    city_name = response['name']
    description = response['weather'][0]['description']
    code = response['weather'][0]['id']
    temp = response['main']['temp']
    temp_feels_like = response['main']['feels_like']
    humidity = response['main']['humidity']
    message = f'Погода в {city_name}\n'
    message += f'Температура {temp} °C.\n'
    message += f'Ощущается как {temp_feels_like}°C.\n'
    message += f'Влажность{humidity}%.\n'
    return message


@bot.message_handler(regexp='О проекте')
def send_about(message):
    soob = 'Бота сделал Матвеев Станислав'
    bot.send_message(message.chat.id, soob, reply_markup=keyboard)


bot.infinity_polling()
