#-*- coding: utf-8 -*-
import telebot
import sys
import time
import urllib.request
import codecs
from bs4 import BeautifulSoup
output = codecs.open('D:\weather\logfile.txt', 'w', 'utf-8')
token = "368398616:AAHS8gGl9K1hcIgbjWV4EP6e9Gvfn01DlRU"
bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start', 'hello'])
def welcome(message):
    sent = bot.send_message(message.chat.id, '')
@bot.message_handler(commands=['help'])
def start(message):
    sent = bot.send_message(message.chat.id, 'Жми /weather')
@bot.message_handler(commands=['weather'])
def send_weather_nsu (message):
    try:
        usock = urllib.request.urlopen("http://weather.nsu.ru/weather.xml", data=None)
    except:
        bot.send_message(message.chat.id, "Сайт лежит, подожди :)")
        time.sleep(120)
        send_weather_nsu(message)
    data = usock.read()
    soup = BeautifulSoup(data, "lxml")
    temperature_nsu = soup.find('current').text
    usock.close()
    temperature_to_message = "Температура около НГУ: " + temperature_nsu + " °C"
    bot.send_message(message.chat.id, temperature_to_message)
    output.write('----', message.chat.id, '----', time.clock(), '----', '\n')
    print ('----', message.chat.id, '----', time.clock(), '----', '\n')
def bot_launch():
    try:
        if __name__ == '__main__':
            bot.polling(none_stop=True)
    except:
        time.sleep(120)
        bot_launch()
bot_launch()