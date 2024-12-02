from datetime import datetime, time

import telebot
import webbrowser
from telebot import types
import sqlite3
import requests
import json
from currency_converter import CurrencyConverter

# Подключение к боту
bot = telebot.TeleBot('7934285611:AAGApFH48rcjbuk3QfFnsY8ua_WfCyziIpw')
name = ''

# API = "9fbad35bd5b70d3238c5f55b332ef163"
# geonames_url = 'http://download.geonames.org/export/dump/'
# basename = 'cities15000'
# filename = basename + '.zip'


# Время в городах где проводятся гонки Hero League

time_city = {"Альметьевск": 0, "": 0, "": 0, "": 0, "": 0, "": 0, "": 0, "": 0, "": 0, "": 0,
             "": 0, "": 0, "": 0, "": 0, "": 0, "": 0, "": 0, "": 0, "": 0, "": 0,
             "": 0, "": 0, "": 0, "": 0, "": 0, "": 0, "": 0, "": 0, "": 0, "": 0,
             "": 0, "": 0, "": 0, "": 0, "": 0, "": 0, "": 0, "": 0, "": 0, "": 0}


currency = CurrencyConverter()
amount = 0


# Создание таблцы бд
@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('botbd.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users '
                '(id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, "Приветствуем, зарегестрируйтесь или войдите в аккаунт! Введите имя")
    bot.register_next_step_handler(message, user_name)


# Регистрация имени
def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, "Введите пароль")
    bot.register_next_step_handler(message, user_pass)


# Регистрация пароля
def user_pass(message):
    password = message.text.strip()
    conn = sqlite3.connect('botbd.sql')
    cur = conn.cursor()

    cur.execute('INSERT INTO users (name, pass) VALUES ("%s", "%s")' % (name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Users', callback_data='users'))
    bot.send_message(message.chat.id, "Вы успешно зарегестрированы!", reply_markup=markup)


# Помощь и отзывы
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '<b>Help</b> <em><u>information</u></em>', parse_mode='html')


# Информация о боте
@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id, '<b>Bot information</b> <em><u>information</u></em>', parse_mode='html')


# Погода
@bot.message_handler(commands=["weather"])
def weather(message):
    bot.send_message(message.chat.id, "Hi, write your city")


# Предстоящие гонки Hero League
@bot.message_handler(commands=['will_race'])
def will_race(message):
    webbrowser.open('https://heroleague.ru/calendar')


# Предстоящие гонки Hero League
@bot.message_handler(commands=['need_for_race'])
def wneed_for_race(message):
    bot.send_message(message.chat.id, "Need")


# Переход на сайт Hero League
@bot.message_handler(commands=['site'])
def site(message):
    webbrowser.open('https://heroleague.ru')


# Фото Hero League
@bot.message_handler(commands=['photo'])
def photo(message):
    webbrowser.open('https://vk.com/heroleague')


# Переход на базу препятствий Hero League
@bot.message_handler(commands=['show'])
def show(message):
    webbrowser.open('https://shop.heroleague.ru')


bot.infinity_polling()
