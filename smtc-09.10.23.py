import telebot
import math
from telebot import types

bot = telebot.TeleBot('6230998049:AAGQXPGDRAE3vWW1JQYZGvfyQPGkjameiXo')

user_dict = {}  # {1234567890: {'photo': photo_id, 'caption': some_text}}

TEXT_BEFORE_ADD_IMG = "Привет! Я бот, и помогу тебе разместить объявление в АваБарахолке. Приступим?"
TEXT_FOR_ADD_IMG = 'Добавьте одну фотографию, остальные фотографии можно добавить в комментарии к объявлению'
TEXT_FOR_ADD_TEXT = 'Теперь введите описание объявления'
TEXT_BEFORE_CHECK_BTN = "Проверяем объявление перед публикацией"
TEXT_BEFORE_SEND_EDIT = "Если всё ОК, жмём ОПУБЛИКОВАТЬ,\nесли описание необходимо исправить, жмём РЕДАКТИРОВАТЬ"
TEXT_BEFORE_EDIT = "Напишите описание заново"
TEXT_AFTER_PUBLICATION = "Объявление опубликовано.\n Для того, чтобы добавть новое объявление, напишите /start"
TEXT_IF_TOO_LONG = "Текст должен быть короче 1000 символов. Пожалуйста, введите текст заново."


# Стартовая клавиатура
def start_keyboard():
   keyboard = types.InlineKeyboardMarkup()
   send = types.InlineKeyboardButton(text='Поехали!', callback_data='send')
   keyboard.add(send)
   return keyboard

# Приветственное сообщение
@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(
        message.chat.id,
        TEXT_BEFORE_ADD_IMG, reply_markup=start_keyboard()
    )

# Вызывается по нажатию кнопки "Поехали!"
@bot.callback_query_handler(func=lambda call: call.data == 'send')
def admin_send(call):
    bot.send_message(call.from_user.id, TEXT_FOR_ADD_IMG)
    bot.register_next_step_handler(call.message, photo_handler)


# Загружаем фото
def photo_handler(message):

    elif message.photo:
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
        bot.send_message(message.chat.id, TEXT_FOR_ADD_TEXT)
        bot.register_next_step_handler(message, text_handler)
    else:
        bot.send_message(message.chat.id,
                         "Загрузите одну фотографию",
                         bot.register_next_step_handler(message, photo_handler)
        )



# Добавляем текст как описание к картинке
def text_handler(message):
    # проверяем, чтобы текст объявления не был слишком длинным
    if len(message.text) < 1000:
        # добавляем описание изображения фото в словарь
        user_dict[message.chat.id]['caption'] = message.text
        bot.send_message(
            message.chat.id,
            "Введите стоимость (число), либо напишите 'бесплатно'",
        )
        bot.register_next_step_handler(message, add_cost)
    else:
        bot.send_message(
            message.chat.id,
            TEXT_IF_TOO_LONG,
            bot.register_next_step_handler(message, text_handler)
        )

# Добавляем запрос стоимости
def add_cost(message):
    if message.text.isdigit():
        user_dict[message.chat.id]['caption'] = user_dict[message.chat.id]['caption'] + "\n \n" + "Стоимость - " + message.text + " рублей"
        bot.send_message(
            message.chat.id,
            TEXT_BEFORE_CHECK_BTN, reply_markup=check_keyboard()
        )
    elif message.text.lower() == "бесплатно":
        print(message.text.lower())
        user_dict[message.chat.id]['caption'] = user_dict[message.chat.id]['caption'] + "\n \n" + "Отдам бесплатно"
        bot.send_message(
            message.chat.id,
            TEXT_BEFORE_CHECK_BTN, reply_markup=check_keyboard()
        )
    elif message.text.lower() == "'бесплатно'":
        print(message.text.lower())
        user_dict[message.chat.id]['caption'] = user_dict[message.chat.id]['caption'] + "\n \n" + "Отдам бесплатно"
        bot.send_message(
            message.chat.id,
            TEXT_BEFORE_CHECK_BTN, reply_markup=check_keyboard()
        )
    else:
        bot.send_message(
            message.chat.id,
            "Введите число или напишите 'бесплатно'")
        bot.register_next_step_handler(message, add_cost)


# добавляем кнопику "проверить объявление перед публикацией"
def check_keyboard():
   keyboard = types.InlineKeyboardMarkup()
   check = types.InlineKeyboardButton(text='Проверить', callback_data='check')
   keyboard.add(check)
   return keyboard

# функция публикации объявления
@bot.callback_query_handler(func=lambda call: call.data == 'publish')
def send_to_users(call):
    bot.send_photo(
        "-1001853283383",
        photo = user_dict[call.from_user.id]['photo'],
        caption = user_dict[call.from_user.id]['caption'],
        parse_mode = 'HTML'
    )
    # пишем сообщение после отправки объявления "объявление отправлено, чтобы добавть новое объявление, напишите /start"
    bot.send_message(call.from_user.id, TEXT_AFTER_PUBLICATION)


# функция редактирования текста объявления
@bot.callback_query_handler(func=lambda call: call.data == 'edit')
def edit_text(call):
    bot.send_message(call.from_user.id, TEXT_BEFORE_EDIT)
    bot.register_next_step_handler(call.message, text_handler)


# проверка объявления
@bot.callback_query_handler(func=lambda call: call.data == 'check')
def send_to_users(call):
    bot.send_photo(
        call.from_user.id,
        photo = user_dict[call.from_user.id]['photo'],
        caption = user_dict[call.from_user.id]['caption'],
        parse_mode = 'HTML'
    )
    # Если всё ОК, жмём ОПУБЛИКОВАТЬ, если описание необходимо исправить, жмём РЕДАКТИРОВАТЬ
    bot.send_message(call.from_user.id,
                     TEXT_BEFORE_SEND_EDIT,
                     reply_markup=last_keyboard()
    )

# клавиатура с кнопками опубликовать и редактировать
def last_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    publish = types.InlineKeyboardButton(text='Опубликовать', callback_data='publish')
    edit = types.InlineKeyboardButton(text='Редактировать', callback_data='edit')
    keyboard.add(publish, edit)
    return keyboard

bot.polling(none_stop=True, interval=0)