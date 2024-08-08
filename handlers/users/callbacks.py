from telebot.types import CallbackQuery
from data.loader import bot, manager
from keyboards.default import start_menu, add_task_team
from keyboards.inline import back_all_team, sure_exit, back_team, join_teams, teams_menu, only_back, only_return, \
    show_team_task, return_tasks, show_deleting_task_button


@bot.callback_query_handler(func=lambda call: "info" in call.data)
def show_team_description(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    string = ""
    user_team_id = manager.user.get_user_team_id(chat_id)
    if user_team_id[0] != 0:
        team_info = manager.team.show_team_info(user_team_id)
        string += f"""Команда {team_info[0]} была создана {team_info[1]}
Команда работает над данным проектом: {team_info[2]}. Более подробнее о нем: {team_info[3]} 
Команде требуются {team_info[4]}
В команде {team_info[5]} человек.
"""
        bot.edit_message_text(string, chat_id, callback.message.message_id,
                              reply_markup=back_all_team(chat_id, user_team_id[0]))
    else:
        string += "Вы не состоите в командах"
        bot.edit_message_text(string, chat_id, callback.message.message_id,
                              reply_markup=only_return(chat_id))


@bot.callback_query_handler(func=lambda call: "returnmain" in call.data)
def return_main_menu(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    bot.delete_message(chat_id, callback.message.message_id)
    bot.send_message(chat_id, "Вы возвращены в главное меню", reply_markup=start_menu(chat_id))


@bot.callback_query_handler(func=lambda call: "return" in call.data)
def return_main_menu(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    string = ""
    team_name = manager.user.get_user_team_name(chat_id)
    if not team_name:
        string += f"Вы не состоите в команде"
        bot.edit_message_text(string, chat_id, callback.message.message_id, reply_markup=teams_menu(chat_id))
    else:
        string = f"Вы состоите в команде {team_name[0]}"
        bot.edit_message_text(string, chat_id, callback.message.message_id, reply_markup=teams_menu(chat_id))


@bot.callback_query_handler(func=lambda call: "exit" in call.data)
def sure_exit_from_team(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    _, team_id = callback.data.split("_")
    bot.edit_message_text("Вы уверены?", chat_id, callback.message.message_id,
                          reply_markup=sure_exit(chat_id, team_id))


@bot.callback_query_handler(func=lambda call: "wtf" in call.data)
def finally_exit_from_team(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    user_id = manager.user.get_user_id(chat_id)
    _, team_id = callback.data.split("_")
    manager.team.delete_user_from_team(user_id)
    necessity = manager.team.need_delete_team(int(team_id))
    bot.edit_message_text("Вы успешно вышли из команды", chat_id, callback.message.message_id,
                          reply_markup="")
    if int(necessity[0]) == 0:
        manager.team.finally_delete_team(int(team_id))
        bot.send_message(chat_id, "В команде не осталось людей, команда была удалена. Возвращены в главное меню",
                         reply_markup=start_menu(chat_id))
    else:
        bot.send_message(chat_id, "Вы Возвращены в меню команд", reply_markup=start_menu(chat_id))


@bot.callback_query_handler(func=lambda call: "others" in call.data)
def create_new_team(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    string = "Список команд:\n\n"
    teams_without_user = manager.team.get_teams_info_without_user(chat_id)
    count = 0
    for i in teams_without_user:
        string += f"Команда {teams_without_user[count][0]}\n" \
                  f"Проект команды {teams_without_user[count][1]}\n" \
                  f"{teams_without_user[count][2]}\n" \
                  f"Команде требуются {teams_without_user[count][3]} \n\n"
        count += 1
    bot.edit_message_text(string, chat_id, callback.message.message_id, reply_markup=join_teams(chat_id))


@bot.callback_query_handler(func=lambda call: "team" in call.data)
def team_description(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    _, team_name = callback.data.split("_")
    team_id = manager.team.get_team_id_by_team_name(team_name)
    team_info = manager.team.show_team_info(team_id[0])
    string = f"Команда {team_info[0]} насчитывает {team_info[5]} человек\n" \
             f"Проект команды называется {team_info[2]}. Его цель: {team_info[3]}\n" \
             f"Проект был создан {team_info[1]}"
    bot.edit_message_text(string, chat_id, callback.message.message_id, reply_markup=back_team(chat_id, team_name))


@bot.callback_query_handler(func=lambda call: "join" in call.data)
def join_team(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    _, team_name = callback.data.split("_")
    user_has_team = manager.user.get_user_team_id(chat_id)[0]
    if user_has_team != 0:
        bot.edit_message_text("Вы уже состоите из команды. Сначала покиньте свою команду", chat_id,
                              callback.message.message_id, reply_markup=only_back(chat_id))
    else:
        team_id = manager.team.get_team_id_by_team_name(team_name)
        manager.user.add_user_into_team(team_id, chat_id)
        bot.edit_message_text(f"Вы успешно вступили в команду {team_name}", chat_id, callback.message.message_id,
                              reply_markup=only_back(chat_id))


@bot.callback_query_handler(func=lambda call: "members" in call.data)
def see_members(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    _, team_id = callback.data.split("_")
    members = manager.team.get_members(team_id)
    team_name = manager.team.get_team_name_by_team_id(team_id)[0]
    string = f"Участники проекта {team_name}:\n"
    for i in range(len(members)):
        string += members[i][0] + ", @" + members[i][1] + "\n"
    bot.edit_message_text(string, chat_id, callback.message.message_id, reply_markup=only_return(chat_id))


@bot.callback_query_handler(func=lambda call: "tasks" in call.data)
def show_tasks(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    _, team_id = callback.data.split("_")
    team_name = manager.team.get_team_name_by_team_id(team_id)[0]
    string = f"Задачи команды {team_name}\n\n"
    task_info = manager.task.task_by_team(team_id)
    if len(task_info) == 0:
        string += "У команды нет задач"
    for i in range(len(task_info)):
        string += task_info[i][0] + ". Описание: " + task_info[i][1] + "\n\n"
    if len(task_info) != 0:
        string += "Внимание! На данный момент пользователь может иметь только одну активную задачу\n"
        task_name = manager.task.get_task_name_by_chat_id(chat_id)
        if task_name is None:
            string += "У пользователя нет активных задач"
        elif len(task_name) == 0:
            string += "У пользователя нет активных задач"
        else:
            string += f"Пользователь занимается данной задачей: {task_name[0]}"
    bot.edit_message_text(string, chat_id, callback.message.message_id,
                          reply_markup=show_team_task(chat_id, team_id))


@bot.callback_query_handler(func=lambda call: "description" in call.data)
def show_task_info(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    _, team_id, task_name = callback.data.split("_")
    task_id = manager.task.get_task_id_by_task_name(task_name)
    task_info = manager.task.get_task_info(task_id, team_id)

    if task_info is None:
        string = "Информация о задаче не получена"
    else:
        string = f"Задача {task_info[0]}. {task_info[1]}. Была создана {task_info[2]}," \
                 f" должна быть закончена {task_info[3]}. Ее статуc: {task_info[4]}. "
        if task_info[5] == 0:
            string += "Задача не имеет исполнителя"
        else:
            user_name = manager.user.get_user_name(chat_id)
            string += f"Исполнителем задачи является {user_name[0]}, @{user_name[1]}"
    bot.edit_message_text(string, chat_id, callback.message.message_id,
                          reply_markup=return_tasks(chat_id, team_id, task_id))


@bot.callback_query_handler(func=lambda call: "refuse" in call.data)
def refuse_the_team(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    _, task_id = callback.data.split("_")
    manager.task.update_user_dont_have_task(task_id)
    bot.delete_message(chat_id, callback.message.message_id)
    bot.send_message(chat_id, "Вы успешно отказались от задачи", reply_markup=start_menu(chat_id))


@bot.callback_query_handler(func=lambda call: "accept" in call.data)
def accept_the_team(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    _, task_id = callback.data.split('_')
    manager.task.update_user_accept(chat_id, task_id)
    bot.delete_message(chat_id, callback.message.message_id)
    bot.send_message(chat_id, "Вы успешно приняли задачу", reply_markup=start_menu(chat_id))


@bot.callback_query_handler(func=lambda call: "delete" in call.data)
def delete_task(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    _, team_id = callback.data.split("_")
    # task_id = manager.task.get_task_id_by_task_name(task_name)[0]
    bot.edit_message_text("Выберите задачу, которую хотите удалить", chat_id, callback.message.message_id,
                          reply_markup=show_deleting_task_button(chat_id, team_id))


@bot.callback_query_handler(func=lambda call: "deleting" in call.data)
def finally_delete_task(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    _, team_id, task_name = callback.data.split("_")
    task_id = manager.task.get_task_id_by_task_name(task_name)[0]
    manager.task.delete_task_line(task_id)
    bot.delete_message(chat_id, callback.message.message_id)
    bot.send_message(chat_id, "Вы успешно удалили задачу", reply_markup=back_all_team(chat_id, team_id))


@bot.callback_query_handler(func=lambda call: "adds" in call.data)
def add_tasks(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    bot.delete_message(chat_id, callback.message.message_id)
    bot.send_message(chat_id, "Добавление задачи", reply_markup=add_task_team(chat_id))


# @bot.callback_query_handler(func=lambda call: "change" in call.data)
# def change_teams(callback: CallbackQuery):
#     chat_id = callback.message.chat.id
#     _, team_name = callback.data.split("_")
#     print(team_name)
#     team_id = manager.team.get_team_id_by_team_name(team_name)
#     print(team_id)
#     if team_id is None:
#         string = f"Ошибка. Командa {team_name} не найдена"
#         bot.edit_message_text(string, chat_id, callback.message.message_id,
#                               reply_markup=back_all_team(chat_id, team_name))
#     team_info = manager.team.show_team_info(team_id)
#     if len(team_info) == 0:
#         string = f"Ошибка. О команде {team_name} ничего не найдено"
#         bot.edit_message_text(string, chat_id, callback.message.message_id,
#                               reply_markup=back_all_team(chat_id, team_name))
#     string = f"Команда {team_name} была создана {team_info[0][1]}\n" \
#              f"В описание было описано это: {team_info[0][0]}\n" \
#              f"Команда насчитывает {team_info[0][2]} участников \n" \
#              f"Что вы хотите изменить?"
#     bot.edit_message_text(string, chat_id, callback.message.message_id, reply_markup=change_team(chat_id, team_name))

