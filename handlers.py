from glob import glob
import os
from random import choice

from db import db, get_or_create_user
from utils import is_cat2, play_random_numbers, main_keyboard


def greet_user(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    print("Вызван /start")
    update.message.reply_text(
                    f"Здравствуй, пользователь {context.user_data['emoji']}!",
                    reply_markup=main_keyboard()
                    )


def talk_to_me(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    text = update.message.text
    print(text)
    update.message.reply_text(f"{text} {user['emoji']}", reply_markup=main_keyboard())


def guess_number(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите число"
    update.message.reply_text(message, reply_markup=main_keyboard())


def send_cat_picture(update, context):
    cat_photos_list = glob('images/cat*.jp*g')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'), reply_markup=main_keyboard())


def user_coordinates(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    coords = update.message.location
    update.message.reply_text(
            f"Ваши координаты {coords} {user['emoji']}!",
            reply_markup=main_keyboard()
    )


def check_user_photo(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    update.message.reply_text("Обрабатываем фотографию")
    os.makedirs("downloads", exist_ok=True)
    user_photo = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join("downloads", f"{user_photo.file_id}.jpg")
    user_photo.download(file_name)
    update.message.reply_text("Фото сохранено на диск")
    url = user_photo['file_path']
    if is_cat2(url):
        update.message.reply_text("Обнаружен котик, добавляю в библиотеку")
        new_filename = os.path.join("images", f"cat_{user_photo.file_id}.jpg")
        os.rename(file_name, new_filename)
    else:
        update.message.reply_text("Тревога, котик на фото не обнаружен")
        os.remove(file_name)
        update.message.reply_text("Фото удалено с диска!")
