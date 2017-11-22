#-*- coding: utf-8 -*-
import telebot
import sys
import datetime
import time
from time import gmtime, strftime
from telebot import types
import urllib.request
import codecs
from bs4 import BeautifulSoup
separator = '  -------  '
token = codecs.open("D:\weather\weather_nsu_token.txt", "r", "utf-8").read()
bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def welcome(message):
    sent = bot.send_message(message.chat.id, 'Доброго дня!')
@bot.message_handler(commands=['help'])
def start(message):
    sent = bot.send_message(message.chat.id, 'Напишу текущую температуру рядом с НГУ')
@bot.message_handler(commands=['weather'])
def send_weather_nsu(message):
    current_time = datetime.datetime.now()
    try:
        usock = urllib.request.urlopen("http://weather.nsu.ru/weather.xml", data=None)
    except:
        bot.send_message(message.chat.id, "Сайт лежит, подожди :)")
        time.sleep(10)
        send_weather_nsu(message)

    data = usock.read()
    soup = BeautifulSoup(data, "lxml")
    temperature_nsu = soup.find('current').text
    usock.close()
    temperature_to_message = "Температура около НГУ: " + temperature_nsu + " °C"
    bot.send_message(message.chat.id, temperature_to_message)
    #bot.send_message(241118222, 'да я тебя по айди вычислю!')
    output = codecs.open("D:\weather\logfile.txt", "a", "utf-8")
    output.write('\n' + separator + str(current_time) + separator + str(message.chat.id) + separator + '\n')
    output.close()
def bot_launch():
    try:
        if __name__ == '__main__':
            bot.polling(none_stop=True)
    except:
        time.sleep(60)
        bot_launch()
bot_launch()
