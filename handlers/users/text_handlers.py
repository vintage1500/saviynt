from telebot.types import Message
from data.loader import bot, manager
from keyboards.default import start_menu, teams_menu_nan, profile_menu, what_change, add_task_team
from keyboards.inline import teams_menu, join_teams, back_all_team, refuse_task
from datetime import datetime
import re


@bot.message_handler(func=lambda msg: msg.text == "Регистрация")
def start_register(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Как вас зовут?")
    bot.register_next_step_handler(message, get_user_name)


def get_user_name(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Сколько вам лет?")
    bot.register_next_step_handler(message, get_user_age, message.text)


def get_user_age(message: Message, name):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Напишите вашу почту")
    bot.register_next_step_handler(message, get_user_email, name, message.text)


def get_user_email(message: Message, name, age):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Напишите о себе и какими знаниями вы обладаете")
    bot.register_next_step_handler(message, get_user_description, name, age, message.text)


def get_user_description(message: Message, name, age, email):
    chat_id = message.chat.id
    username = message.chat.username
    description = message.text
    manager.user.add_user(name, age, email, description, username, chat_id)
    bot.send_message(chat_id, 'Регистрация прошла успешно', reply_markup=start_menu(chat_id))


@bot.message_handler(func=lambda msg: msg.text == "Мой профиль" or msg.text == "Отмена")
def show_profile(message: Message):
    chat_id = message.chat.id
    user_info = manager.user.get_user_info(chat_id)
    string = ""
    string += f"""Ваш профиль\n\n
Имя: {user_info[0][0]} \n
Возраст: {user_info[0][1]} \n
Почта: {user_info[0][2]} \n 
Описание: {user_info[0][3]}\n\n"""
    user_team_id = manager.user.get_user_team_id(chat_id)
    if user_team_id[0] != 0 and user_team_id[0] is not None:
        user_team_name = manager.user.get_user_team_name(chat_id)
        string += f"Команда: {user_team_name[0]}"
    else:
        string += "Команда: У вас нет команды"
    bot.send_message(chat_id, string, reply_markup=profile_menu(chat_id))


@bot.message_handler(func=lambda msg: msg.text == "Изменить профиль")
def start_change_profile(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f"Что вы хотите изменить?", reply_markup=what_change(chat_id))


@bot.message_handler(
    func=lambda msg: msg.text == "Имя" or msg.text == "Возраст" or msg.text == "Почта" or msg.text == "Описание")
def start_change_profile(message: Message):
    chat_id = message.chat.id
    if message.text == "Имя":
        bot.send_message(chat_id, "Введите новое имя")
        bot.register_next_step_handler(message, get_new_name)
    if message.text == "Возраст":
        bot.send_message(chat_id, "Введите ваш возраст")
        bot.register_next_step_handler(message, get_new_age)
    if message.text == "Почта":
        bot.send_message(chat_id, "Введите новую почту")
        bot.register_next_step_handler(message, get_new_email)
    if message.text == "Описание":
        bot.send_message(chat_id, "Введите новое описание профиля")
        bot.register_next_step_handler(message, get_new_description)


def get_new_name(message: Message):
    chat_id = message.chat.id
    manager.user.change_name(message.text, chat_id)
    bot.send_message(chat_id, "Ваше имя было обновлено", reply_markup=profile_menu(chat_id))


def get_new_age(message: Message):
    chat_id = message.chat.id
    manager.user.change_age(message.text, chat_id)
    bot.send_message(chat_id, "Ваш возраст был обновлен", reply_markup=profile_menu(chat_id))


def get_new_email(message: Message):
    chat_id = message.chat.id
    manager.user.change_email(message.text, chat_id)
    bot.send_message(chat_id, "Ваша почта была обновлена", reply_markup=profile_menu(chat_id))


def get_new_description(message: Message):
    chat_id = message.chat.id
    manager.user.change_description(message.text, chat_id)
    bot.send_message(chat_id, "Ваше описание была обновлено", reply_markup=profile_menu(chat_id))


@bot.message_handler(func=lambda msg: msg.text == "Моя команда")
def show_teams(message: Message):
    chat_id = message.chat.id
    team_name = manager.user.get_user_team_name(chat_id)
    if not team_name:
        bot.send_message(chat_id, "Вы не состоите ни в одной команде", reply_markup=teams_menu_nan(chat_id))
    else:
        string = f"Вы состоите в команде {team_name[0]}"
        bot.send_message(chat_id, string, reply_markup=teams_menu(chat_id))


@bot.message_handler(func=lambda msg: msg.text == "Назад")
def return_main_menu(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Вы возвращены в главное меню', reply_markup=start_menu(chat_id))


@bot.message_handler(func=lambda msg: msg.text == "Создать команду")
def create_team(message: Message):
    chat_id = message.chat.id
    team_id = manager.user.get_user_team_id(chat_id)
    if team_id[0] != 0:
        bot.send_message(chat_id, "Вы уже состоите в команде", reply_markup=start_menu(chat_id))
    else:
        bot.send_message(chat_id, f"Круто! Вы решили создать свою команду. Я готов вам помочь с этим. "
                                  "Как вы назовете свою команду?")
        bot.register_next_step_handler(message, get_team_name)


def get_team_name(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Хорошо. Какой проект вы будете реализовывать в этой команде?")
    bot.register_next_step_handler(message, get_team_project, message.text)


def get_team_project(message: Message, team_name):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Отлично. Теперь расскажите немного об этом проекте!")
    bot.register_next_step_handler(message, get_team_project_description, team_name, message.text)


def get_team_project_description(message: Message, team_name, team_project):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Прекрасно. Кто тебе необходим в команду?")
    bot.register_next_step_handler(message, get_team_user, team_name, team_project, message.text)


def get_team_user(message: Message, team_name, team_project, team_project_description):
    chat_id = message.chat.id
    who_need = message.text
    manager.team.add_team(team_name, team_project, team_project_description, who_need, chat_id)
    bot.send_message(chat_id, "Команда создана успешно!", reply_markup=start_menu(chat_id))


@bot.message_handler(func=lambda msg: msg.text == "Вступить в команду")
def start_join_team(message: Message):
    chat_id = message.chat.id
    string = "Список команд:\n\n"
    user_team = manager.user.get_user_team_name(chat_id)
    if user_team is None:
        teams_without_user = manager.team.get_teams_info_without_user(chat_id)
        count = 0
        for i in teams_without_user:
            string += f"Команда {teams_without_user[count][0]}\n" \
                      f"Проект команды {teams_without_user[count][1]}\n" \
                      f"{teams_without_user[count][2]}\n" \
                      f"Команде требуются {teams_without_user[count][3]} \n\n"
            count += 1
        bot.send_message(chat_id, string, reply_markup=join_teams(chat_id))
    else:
        bot.send_message(chat_id, "Вы состоите в команде", reply_markup=start_menu(chat_id))


@bot.message_handler(func=lambda msg: msg.text == "Мои задачи")
def get_tasks(message: Message):
    chat_id = message.chat.id
    task_id = manager.task.get_task_user(chat_id)
    team_id = manager.user.get_user_team_id(chat_id)
    if task_id is None:
        bot.send_message(chat_id, "У вас нет задач", reply_markup=add_task_team(chat_id))
    elif len(task_id) == 0:
        bot.send_message(chat_id, "У вас нет задач", reply_markup=add_task_team(chat_id))
    else:
        task_info = manager.task.get_task_info(task_id[0], team_id[0])
        if task_info is None:
            bot.send_message(chat_id, "У вас нет задач", reply_markup=add_task_team(chat_id))
        else:
            remaining_time = task_info[3] - datetime.now()
            remaining_days = remaining_time.days
            string = f"Ваша задача: {task_info[0]}. {task_info[1]}. Задача была выдана {task_info[2]}, " \
                     f"ее дедлайн {task_info[3]}\nДо дедлайна осталось {remaining_days} дней"
            bot.send_message(chat_id, string, reply_markup=refuse_task(chat_id, task_id[0]))


@bot.message_handler(func=lambda msg: msg.text == "Добавить задачу в команду")
def start_add_tasks(message: Message):
    chat_id = message.chat.id
    team_id = manager.user.get_user_team_id(chat_id)
    if team_id is None or team_id[0] == 0:
        bot.send_message(chat_id, "Вы не состоите в команде. Действие невозможно", reply_markup=add_task_team(chat_id))
    else:
        bot.send_message(chat_id, "Вы решили создать задачу! Как кратко ее назовем?")
        bot.register_next_step_handler(message, get_task_name)


def get_task_name(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Теперь опиши что нужно сделать для ее выполнения поподробнее!")
    bot.register_next_step_handler(message, get_task_description, message.text)


def get_task_description(message: Message, task_name):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Хорошо, теперь укажи дедлайн для задачи в формате DD-MM-YYYY HH:MM")
    bot.register_next_step_handler(message, get_task_deadline, task_name, message.text)


date_time_regex = re.compile(r'^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$')


def get_task_deadline(message, task_name, task_description):
    chat_id = message.chat.id
    task_deadline = message.text
    if date_time_regex.match(task_deadline):
        try:
            deadline = datetime.strptime(task_deadline, '%d-%m-%Y %H:%M')
            current_time = datetime.now()
            if deadline < current_time:
                bot.reply_to(message, "Указанная дата уже прошла. Пожалуйста, введите будущую дату и время.")
                bot.register_next_step_handler(message, get_task_deadline, task_name, task_description)
            else:
                team_id = manager.user.get_user_team_id(chat_id)
                manager.task.add_task(task_name, task_description, deadline, team_id)
                bot.send_message(chat_id,
                                 f"Задача успешно добавлена! Чтобы принять задачу перейдите в меню задач команды",
                                 reply_markup=back_all_team(chat_id, team_id[0]))
        except ValueError:
            bot.send_message(chat_id, "Некорректная дата и время. Пожалуйста, введите в формате DD-MM-YYYY HH:MM")
            bot.register_next_step_handler(message, get_task_deadline, task_name, task_description)
    else:
        bot.send_message(chat_id, "Некорректный формат. Пожалуйста, введите дату и время в формате DD-MM-YYYY HH:MM")
        bot.register_next_step_handler(message, get_task_deadline, task_name, task_description)
