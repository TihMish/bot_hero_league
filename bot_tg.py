import pyowm
import telebot
import webbrowser
from telebot import types
from googletrans import Translator, constants
from pprint import pprint
import sqlite3
import requests
import json
from pyowm import *


# Подключение к боту
bot = telebot.TeleBot('7934285611:AAGApFH48rcjbuk3QfFnsY8ua_WfCyziIpw')
name = ''
city = "London"
owm = pyowm.OWM('9fbad35bd5b70d3238c5f55b332ef163')
mgr = owm.weather_manager()
observation = mgr.weather_at_place(city)
w = observation.weather
temperature = w.temperature('celsius')['temp']


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
    bot.send_message(message.chat.id, "Успешная Регистрация!")


# Помощь и отзывы
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '<b>Help</b> <em><u>По всем вопросам обращайтесь к @tihaya_mishka</u></em>',
                     parse_mode='html')


# Информация о боте
@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id, '<b>Bot information</b> С этим ботом вы можете посмотреть 3D модели '
                                      'препятствий чтобы лучше подготовиться к гонке, а так же увидеть памятку'
                                      'участника, перейти на <em><u>сайт Hero League</u></em> и узнать погоду в '
                                      'городах, где проводятся Гонки Героев', parse_mode='html')


# Погода
@bot.message_handler(commands=["weather"])
def weather(message):
    global city
    markup = types.ReplyKeyboardMarkup()
    b1 = types.KeyboardButton("Альметьевск")
    b2 = types.KeyboardButton("Великий Новгород")
    b3 = types.KeyboardButton("Владивосток")
    b4 = types.KeyboardButton("Вологда")
    b5 = types.KeyboardButton("Волгоград")
    b6 = types.KeyboardButton("Екатеринбург")
    b7 = types.KeyboardButton("Зарайск")
    b8 = types.KeyboardButton("Иркутск")
    b9 = types.KeyboardButton("Казань")
    b10 = types.KeyboardButton("Калининград")
    b11 = types.KeyboardButton("Кемерово")
    b12 = types.KeyboardButton("Красногорск")
    b13 = types.KeyboardButton("Красноярск")
    b14 = types.KeyboardButton("Москва")
    b15 = types.KeyboardButton("Мурманск")
    b16 = types.KeyboardButton("Нижний Новгород")
    b17 = types.KeyboardButton("Новосибирск")
    b18 = types.KeyboardButton("Омск")
    b19 = types.KeyboardButton("Петропавловск-Камчатский")
    b20 = types.KeyboardButton("Псков")
    b21 = types.KeyboardButton("Ростов-на-Дону")
    b22 = types.KeyboardButton("Самара")
    b23 = types.KeyboardButton("Санкт-Петербург")
    b24 = types.KeyboardButton("Саратов")
    b25 = types.KeyboardButton("Сочи")
    b26 = types.KeyboardButton("Тамбов")
    b27 = types.KeyboardButton("Тверь")
    b28 = types.KeyboardButton("Тула")
    b29 = types.KeyboardButton("Ульяновск")
    b30 = types.KeyboardButton("Уфа")
    b31 = types.KeyboardButton("Хабаровск")
    b32 = types.KeyboardButton("Челябинск")
    b33 = types.KeyboardButton("Чита")
    b34 = types.KeyboardButton("Якутск")
    b35 = types.KeyboardButton("Ялта")
    b36 = types.KeyboardButton("Ярославль")
    markup.row(b1, b2, b3, b4, b5, b6)
    markup.row(b7, b8, b9, b10, b11, b12)
    markup.row(b13, b14, b15, b16, b17, b18)
    markup.row(b19, b20, b21, b22, b23, b24)
    markup.row(b25, b26, b27, b28, b29, b30)
    markup.row(b31, b32, b33, b34, b35, b36)
    bot.send_message(message.chat.id, "Выберете город", reply_markup=markup)
    bot.register_next_step_handler(message, inf_plen)


def inf_plen(message):
    city = message.text
    translator = Translator()
    weath = w.detailed_status
    get_weath = translator.translate(weath, dest="ru")
    bot.send_message(message.chat.id, f"В городе {message.text} температура {temperature} и {get_weath.text}")


# Предстоящие гонки Hero League
@bot.message_handler(commands=['will_race'])
def will_race(message):
    markup = types.InlineKeyboardMarkup()  # создаём кнопку
    button1 = types.InlineKeyboardButton("Ближайшие Гонки", url='https://heroleague.ru/calendar')
    markup.add(button1)  # добавляем кнопку
    bot.send_message(message.chat.id, "Посмотреть ближайшие Гонки", reply_markup=markup)


# Памятка Hero League
@bot.message_handler(commands=['need_for_race'])
def need_for_race(message):
    bot.send_message(message.chat.id, "После покупки слота на забег от Hero League вы получите памятку(на почту) с"
                                      "подробным описанием вещей, которые вам будут нужны для успешного участия в гонке"
                                      "\n"
                                      "<b>Вы увидите</b>\n"
                                      "Карту гонки с помеченными препятствиями, пунктами питания и маршрутом\n"
                                      "<b>Необходимые документы</b>\n"
                                      "<em><u>Медицинская справка</u></em>\n с 2/3 печатями, ФИО, вид спорта, дистанция,"
                                      "дата действительности справки в день гонки и дата выдачи\n"
                                      "<em><u>Документ удостоверяющий личность</u></em>\n паспорт/копия/фото, "
                                      "водительские права, военный билет\n"
                                      "<em><u>Согласие на обработку персональных данных</u></em>\n можно написать при "
                                      "регистрации на месте гонки\n", parse_mode="html")


# Переход на сайт Hero League
@bot.message_handler(commands=['site'])
def site(message):
    markup = types.InlineKeyboardMarkup()  # создаём кнопку
    button1 = types.InlineKeyboardButton("Сайт Hero League", url='https://heroleague.ru')
    markup.add(button1)  # добавляем кнопку
    bot.send_message(message.chat.id, "Перейти на сайт", reply_markup=markup)


# Фото Hero League
@bot.message_handler(commands=['photo'])
def photo(message):
    markup = types.InlineKeyboardMarkup()  # создаём кнопку
    button1 = types.InlineKeyboardButton("Фото с гонок Hero League VK", url='https://vk.com/heroleague')
    btn2 = types.InlineKeyboardButton("Фото с гонок Hero League Telegram", url="https://t.me/heroleague_official")
    btn3 = types.InlineKeyboardButton("Фото с гонок Hero League Tg/Hero Race", url="https://t.me/herorace_info")
    markup.row(button1)
    markup.row(btn2)
    markup.row(btn3)
    bot.send_message(message.chat.id, "Перейти на сайт", reply_markup=markup)


# Переход на базу препятствий Hero League

@bot.message_handler(commands=['show'])
def show(message):
    markup = types.InlineKeyboardMarkup()  # создаём кнопку
    button1 = types.InlineKeyboardButton("Сайт с базй 3D моделей препятствий", url='https://vk.com/heroleague')
    markup.add(button1)  # добавляем кнопку
    bot.send_message(message.chat.id, "Перейти на сайт", reply_markup=markup)

    webbrowser.open('https://shop.heroleague.ru')


bot.infinity_polling()
