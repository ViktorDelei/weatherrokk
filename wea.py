import telebot
import requests
from bs4 import BeautifulSoup as BS
from telebot import types

r = requests.get('https://ua.sinoptik.ua/погода-рокитне-303022581')
html = BS(r.content, 'html.parser')
bot = telebot.TeleBot("1699419640:AAH3SfpW-Lz-eK9mQ7N8me6bq95-C0J3Vvs")

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton('Погода сьогодні')
item2 = types.KeyboardButton('Мінімальна та максимальна температури')
item3 = types.KeyboardButton('Опис погоди на весь день')
item4 = types.KeyboardButton('Народний прогноз погоди')
item5 = types.KeyboardButton('Схід та захід сонця')
item6 = types.KeyboardButton('Цікаві відомості')
markup.add(item1, item2, item3, item4, item5, item6)

for el in html.select('#content'):
	t_min = el.select('.temperature .min')[0].text
	t_max = el.select('.temperature .max')[0].text
	desc = el.select('.wDescription .description')[0].text
	ttime = el.select('.lSide .today-time')[0].text
	ttemp = el.select('.lSide .today-temp')[0].text
	odesc = el.select('.oDescription .description')[0].text
	day = el.select('.tabs .day-link ')[0].text
	date = el.select('.tabs .date ')[0].text
	month = el.select('.tabs .month ')[0].text
	shzh = el.select('.lSide .infoDaylight ')[0].text
	pic = el.select('.tabs .weatherIco ')[0].text
	ihist = el.select('.oDescription .infoHistory')[0].text
	ihist1 = el.select('.oDescription .infoHistoryval')[0].text

@bot.message_handler(commands=['start'])
def send_welcome(message):
	st = open('welcome.webp', 'rb')
	bot.send_sticker(message.chat.id, st)

	bot.send_message(message.chat.id, "Натискайте на клавіши щоб дізнатись саме те що вас цікавить:", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def send_echo(message):

	if message.text == 'Погода сьогодні':
		bot.send_message(message.chat.id,'Погода в смт.Рокитне' + '\n' + date + '  ' + month + "\n" + day + '\n' + ttime + ': ' + '\n' + ttemp + pic)
	elif message.text == 'Мінімальна та максимальна температури':
		bot.send_message(message.chat.id,'Температури на сьогодні ' + '\n' + t_min + ' та ' + t_max)
	elif message.text == 'Опис погоди на весь день':
		bot.send_message(message.chat.id, desc )
	elif message.text == 'Народний прогноз погоди':
		bot.send_message(message.chat.id, odesc)
	elif message.text == 'Схід та захід сонця':
		bot.send_message(message.chat.id, shzh)
	elif message.text == 'Цікаві відомості':
		bot.send_message(message.chat.id, ihist + '\n' +ihist1)

bot.polling(none_stop=True)
