def receive_photos(message):
    photos = []
    for photo in message.photo:
        print(photo.file_id)
        file_info = bot.get_file(photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open(photo.file_id + '.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)

        photos.append(photo.file_id + '.jpg')

    try:
        for photo in photos:
            with open(photo, 'rb') as f:
                bot.send_photo(chat_id= "-1001853283383", photo = f)
                os.remove(photo)
    except:
        bot.send_message(
            message.chat.id,
            'Произошла ошибка при отправке фотографий. Повторите попытку позже.'
        )


bot.polling()