from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from data.loader import manager


def start_menu(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    user_id = manager.user.get_user_id(chat_id)
    if not user_id:
        markup.row(
            KeyboardButton(text="Регистрация")
        )
        return markup

    markup.row(
        KeyboardButton(text="Моя команда"),
        KeyboardButton(text="Мои задачи"),
        KeyboardButton(text="Мой профиль")
    )
    return markup


def teams_menu_nan(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(
        KeyboardButton(text="Вступить в команду"),
        KeyboardButton(text="Создать команду")
    )
    markup.add(KeyboardButton(text="Назад"))
    return markup


def profile_menu(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        KeyboardButton(text="Изменить профиль"),
        KeyboardButton(text="Назад")
    )
    return markup


def what_change(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(
        KeyboardButton(text="Имя"),
        KeyboardButton(text="Возраст")
    )
    markup.add(
        KeyboardButton(text="Почта"),
        KeyboardButton(text="Описание")
    )
    markup.add(
        KeyboardButton(text="Назад")
    )
    return markup


def add_task_team(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(
        KeyboardButton(text="Добавить задачу в команду"),
        KeyboardButton(text="Назад")
    )
    return markup



