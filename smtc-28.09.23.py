import telebot
from telebot import types

bot = telebot.TeleBot('6230998049:AAGQXPGDRAE3vWW1JQYZGvfyQPGkjameiXo')

user_dict = {}  # {1234567890: {'photo': photo_id, 'caption': some_text}}

TEXT_PUBLICATE = 'Напишите "отправить", чтобы опубликовать объявление в АваБарахолке'
TEXT_FOR_ADD_TEXT = 'Теперь введите описание объявления'
TEXT_FOR_ADD_IMG = 'Добавляйте одну фотографию, остальные можно добавить в комментарии к объявлению'


def start_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    send = types.InlineKeyboardButton(text='send photo', callback_data='send')
    keyboard.add(send)
    return keyboard


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(
        message.chat.id,
        'Выберите действие ⤵', reply_markup=start_keyboard()
    )


@bot.callback_query_handler(func=lambda call: call.data == 'send')
def admin_send(call):
    bot.send_message(call.from_user.id, TEXT_FOR_ADD_IMG)
    bot.register_next_step_handler(call.message, photo_handler)


def photo_handler(message):
    try:
        # если изображение есть в словаре - заменяем его и убираем описание
        if user_dict.get(message.chat.id) is not None:
            user_dict[message.chat.id]['photo'] = message.photo[len(message.photo) - 1].file_id
            user_dict[message.chat.id]['caption'] = ''
        else:
            # если фото нет - создаем словарь и добавляем изображение
            user_dict[message.chat.id] = {'photo': '', 'caption': ''}
            user_dict[message.chat.id]['photo'] = message.photo[len(message.photo) - 1].file_id
    except Exception as e:
        bot.reply_to(message, e)
    else:
        bot.send_message(message.chat.id, TEXT_FOR_ADD_TEXT)
        bot.register_next_step_handler(message, text_handler)


def text_handler(message):
    # добавляем описание изображения фото в словарь
    user_dict[message.chat.id]['caption'] = message.text
    bot.send_message(message.chat.id, TEXT_PUBLICATE)
    bot.register_next_step_handler(message, send_to_users)


def send_to_users(message):
    if message.text.lower() == 'отправить':
        # здесь можно добавить отправку в цикле
        bot.send_photo(
            #message.chat.id,
            #photo=user_dict[message.chat.id]['photo'],
            #caption=user_dict[message.chat.id]['caption'],
            #parse_mode='HTML'

            "-1001853283383",
            photo = user_dict[message.chat.id]['photo'],
            caption = user_dict[message.chat.id]['caption'],
            parse_mode = 'HTML'
        )
    else:
        bot.send_message(message.chat.id, TEXT_PUBLICATE)
        bot.register_next_step_handler(message, send_to_users)


bot.polling(none_stop=True, interval=0)