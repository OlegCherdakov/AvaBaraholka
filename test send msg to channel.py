import telebot


bot = telebot.TeleBot("6230998049:AAGQXPGDRAE3vWW1JQYZGvfyQPGkjameiXo")


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Введите описание:")

@bot.message_handler(content_types=["text"])
def description(message):
    bot.send_message("-1001853283383", message.text)

bot.polling()




