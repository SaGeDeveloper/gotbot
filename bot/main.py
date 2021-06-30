import telebot

bot = telebot.TeleBot("1823960671:AAFfKfCcYmZATgT8FoIuNoDiIOJQ5SVgfKU")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing? \nP.S. \"авня\" is a great start for every conversation!")

@bot.message_handler(func=lambda message: True if message.text == "авня" else False)
def echo_all(message):
	bot.reply_to(message, 'лох')

bot.polling()