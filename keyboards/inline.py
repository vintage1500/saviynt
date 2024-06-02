from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.loader import manager


def teams_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=True)
    markup.add(
        InlineKeyboardButton(text="Подробнее о команде", callback_data=f'info'),
        InlineKeyboardButton(text="Другие команды", callback_data=f"others"),
        InlineKeyboardButton(text="Назад", callback_data=f"returnmain")
    )
    return markup


def back_all_team(chat_id, team_id):
    markup = InlineKeyboardMarkup(row_width=True)
    markup.add(
        InlineKeyboardButton(text="Задачи команды", callback_data=f"tasks_{team_id}"),
        InlineKeyboardButton(text="Участники команды", callback_data=f"members_{team_id}"),
        InlineKeyboardButton(text="Выйти из команды", callback_data=f"exit_{team_id}"),
        InlineKeyboardButton(text="Назад", callback_data=f"return")
    )
    return markup


def sure_exit(chat_id, team_id):
    markup = InlineKeyboardMarkup(row_width=True)
    markup.add(
        InlineKeyboardButton(text="Да, выйти из команды", callback_data=f"wtf_{team_id}"),
        InlineKeyboardButton(text='Назад', callback_data=f"info")
    )
    return markup


def join_teams(chat_id):
    markup = InlineKeyboardMarkup(row_width=True)
    teams_without_user = manager.team.get_team_name(chat_id)
    buttons = [InlineKeyboardButton(text=team_name[0], callback_data=f'team_{team_name[0]}') for team_name in
               teams_without_user]
    markup.add(*buttons)
    markup.add(
        InlineKeyboardButton(text="Назад", callback_data=f"return")
    )
    return markup


def back_team(chat_id, team_name):
    markup = InlineKeyboardMarkup(row_width=True)
    markup.add(
        InlineKeyboardButton(text="Присоединиться к команде", callback_data=f"join_{team_name}"),
        InlineKeyboardButton(text="Назад", callback_data=f"others")
    )
    return markup


def refuse_task(chat_id, task_id):
    markup = InlineKeyboardMarkup(row_width=True)
    markup.add(
        InlineKeyboardButton(text="Отказаться от задачи", callback_data=f"refuse_{task_id}"),
        InlineKeyboardButton(text="Назад", callback_data="returnmain")
    )
    return markup


def only_back(chat_id):
    markup = InlineKeyboardMarkup(row_width=True)
    markup.add(
        InlineKeyboardButton(text="Моя команда", callback_data="info"),
        InlineKeyboardButton(text="Назад", callback_data="return")
    )
    return markup


def only_return(chat_id):
    markup = InlineKeyboardMarkup(row_width=True)
    markup.add(
        InlineKeyboardButton(text="Назад", callback_data="return")
    )
    return markup


def show_team_task(chat_id, team_id):
    markup = InlineKeyboardMarkup(row_width=True)
    tasks_info = manager.task.task_by_team(team_id)
    if tasks_info is None or len(tasks_info) == 0:
        markup.add(
            InlineKeyboardButton(text="Нет задач", callback_data=f"return")
        )
    # else:
    #     buttons = [InlineKeyboardButton(text=task_info, callback_data=f"description_{team_id}_{task_info}") for task_info in tasks_info]
    #     markup.add(*buttons)
    markup.add(
        InlineKeyboardButton(text="Разработка стартового меню", callback_data=f"none?"),
        InlineKeyboardButton(text="Удалить задачу", callback_data=f"delete_{team_id}"),
        InlineKeyboardButton(text="Назад", callback_data=f"info")
    )
    return markup


def show_deleting_task_button(chat_id, team_id):
    markup = InlineKeyboardMarkup(row_width=True)
    tasks_info = manager.task.task_by_team(team_id)
    buttons = [InlineKeyboardButton(text=task_info[0], callback_data=f"deleting_{team_id}_{task_info[0]}") for
               task_info in tasks_info]
    markup.add(*buttons)
    markup.add(
        InlineKeyboardButton(text="Назад", callback_data=f"info")
    )
    return markup


def return_tasks(chat_id, team_id, task_id):
    markup = InlineKeyboardMarkup(row_width=True)
    user_accept = manager.task.get_task_user(chat_id)
    if user_accept is None:
        markup.add(
            InlineKeyboardButton(text="Принять задачу", callback_data=f"accept_{task_id}")
        )
    markup.add(
        InlineKeyboardButton(text="Назад", callback_data=f"tasks_{team_id}")
    )
    return markup

# def change_team(chat_id, team_name):
#     markup = InlineKeyboardMarkup(row_width=True)
#     team_id = manager.team.get_team_id_by_team_name(team_name)
#     markup.row(
#         InlineKeyboardButton(text="Название команды", callback_data=f"nameteam_{team_id}"),
#         InlineKeyboardButton(text="Описание команды", callback_data=f'description?'),
#     )
#     markup.add(
#         InlineKeyboardButton(text="Назад", callback_data=f'info')
#     )
#     return markup
