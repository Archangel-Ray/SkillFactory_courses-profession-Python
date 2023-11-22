import telebot

TOKEN = "6888696355:AAE6QKVoqX6mv0kXDhjNAet1tYokXfAu8DE"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Welcome, {message.chat.username}")


@bot.message_handler(content_types=['photo', ])
def say_lmao(message: telebot.types.Message):
    bot.reply_to(message, 'Nice meme XDD')


bot.polling(none_stop=True)
