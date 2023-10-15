import telebot
from telebot import types

bot = telebot.TeleBot('6230998049:AAGQXPGDRAE3vWW1JQYZGvfyQPGkjameiXo')

user_dict = {}  # {1234567890: {'photo': photo_id, 'caption': some_text}}

TEXT_PUBLICATE = 'Напишите "отправить", чтобы опубликовать объявление в АваБарахолке'
TEXT_PUBLICATE_BTN = "Нажимте нопку опубликовать, если описание верное"
TEXT_FOR_ADD_TEXT = 'Теперь введите описание объявления'
TEXT_FOR_ADD_IMG = 'Добавьте одну фотографию, остальные фотографии можно добавить в комментарии к объявлению'
TEXT_BEFORE_ADD_IMG = "Привет, житель планеты Ава-Петер. Я бот, и помогу тебе разместить объявление в АваБарахолке. Приступим?"
TEXT_AFTER_PULLICATION = "Объявление опубликовано. Для того, чтобы добавть новое объявление, напишите /start"


def start_keyboard():
   keyboard = types.InlineKeyboardMarkup()
   send = types.InlineKeyboardButton(text='Поехали!', callback_data='send')
   keyboard.add(send)
   return keyboard


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(
        message.chat.id,
        TEXT_BEFORE_ADD_IMG, reply_markup=start_keyboard()
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
    bot.send_message(
        message.chat.id,
        TEXT_PUBLICATE_BTN, reply_markup=send_to_channel_keyboard()
    )


def send_to_channel_keyboard():
   keyboard = types.InlineKeyboardMarkup()
   publish = types.InlineKeyboardButton(text='Опубликовать', callback_data='publish')
   keyboard.add(publish)
   return keyboard


@bot.callback_query_handler(func=lambda call: call.data == 'publish')
def send_to_users(call):
    bot.send_photo(
        "-1001853283383",
        photo = user_dict[call.from_user.id]['photo'],
        caption = user_dict[call.from_user.id]['caption'],
        parse_mode = 'HTML'
    )
    # пишем сообщение после отправки объявления "объявление отправлено, чтобы добавть новое объявление, напишите /start"
    bot.send_message(call.from_user.id, TEXT_AFTER_PULLICATION)

bot.polling(none_stop=True, interval=0)