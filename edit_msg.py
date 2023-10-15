import telebot

API_TOKEN = '6230998049:AAGQXPGDRAE3vWW1JQYZGvfyQPGkjameiXo'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    var_data = bot.send_message(message.from_user.id, "Hi there, I am EchoBot.")
    #print(var_data)
    bot.edit_message_text("Hi, " + str(message.from_user.first_name), var_data.chat.id, var_data.message_id)

bot.polling(none_stop=True, interval=0)