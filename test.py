import telebot
from telebot import types

bot = telebot.TeleBot('6230998049:AAGQXPGDRAE3vWW1JQYZGvfyQPGkjameiXo')

mm = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
button1 = types.KeyboardButton("🐣 Привет")
button2 = types.KeyboardButton("😀 Как дела?")
mm.add(button1,button2)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello World!", reply_markup=mm)

@bot.message_handler(content_types=['text'])
def handler(message):
    if message.text == "🐣 Привет":
        bot.send_message(message.chat.id, "Привет!")
    if message.text == "😀 Как дела?":
        otvet = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton("😎 Хорошо", callback_data='good')
        button2 = types.InlineKeyboardButton("😥 Плохо", callback_data='bad')
        otvet.add(button1,button2)
        bot.send_message(message.chat.id, "Отлично! А у тебя?", reply_markup=otvet)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == "good":
                bot.send_message(call.message.chat.id, "Круто!")
            if call.data == "bad":
                bot.send_message(call.message.chat.id, "Ничего, все наладится!")
    except Exception as e:
        print(repr(e))

bot.polling(none_stop=True)