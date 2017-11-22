#-*- coding: utf-8 -*-
import json
import telebot
import sys
import datetime
import time
from time import gmtime, strftime
from telebot import types
import urllib.request
import codecs
separator = '  -------  '
token = codecs.open("D:\weather\weather_nsu_token.txt", "r", "utf-8").read()
bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def welcome(message):
    user_name = message.from_user.first_name
    now_time = datetime.datetime.now()
    now_hour = now_time.hour
    if 6 <= now_hour < 12:
        welcome_message = 'Доброе утро, ' + user_name
    elif 12 <= now_hour < 17:
        welcome_message = 'Добрый день,' + user_name
    elif 17 <= now_hour < 23:
        welcome_message = 'Добрый вечер, ' + user_name
    sent = bot.send_message(message.chat.id, welcome_message)
@bot.message_handler(commands=['help'])
def start(message):
    sent = bot.send_message(message.chat.id, 'Напишу текущую температуру рядом с НГУ')
@bot.message_handler(commands=['weather'])
def send_weather_nsu(message):
    current_time = datetime.datetime.now()
    try:
        usock = urllib.request.urlopen("http://nsuweather.appspot.com/full", data=None)
    except:
        bot.send_message(message.chat.id, "Сайт лежит, подожди :)")
        send_weather_nsu(message)
        time.sleep(10)
    nsu_json_string = usock.read()
    nsu_json_dict= json.loads(nsu_json_string)
    current_temperature_nsu = str(nsu_json_dict ['current'])
    temperature_to_message = "Температура около НГУ: " + current_temperature_nsu + " °C"
    bot.send_message(message.chat.id, temperature_to_message)
    user_name = message.from_user.first_name
    output = codecs.open("D:\weather\logfile.txt", "a", "utf-8")
    output.write('\n' + separator + str(current_time) + separator + str(message.chat.id) + separator + user_name + separator + '\n')
    usock.close()
    output.close()
def bot_launch():
    try:
        if __name__ == '__main__':
            bot.polling(none_stop=True)
    except:
        time.sleep(60)
        bot_launch()
bot_launch()