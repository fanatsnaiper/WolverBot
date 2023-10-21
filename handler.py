from consts import *
from engine.botError import *
from engine.valid import *
import telebot
from telebot import types
import os.path
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

@bot.message_handler(commands=['restart'])
def send_restart(message):
    buttons_list=['/start']
    restart_keyboard=Keyboard(buttons_list)
    for user in ADMINS_ID_LIST:
        bot.send_message(chat_id=user,text='Для возобновления работы с ботом нажмите на кнопку стандартного меню', reply_markup=restart_keyboard.get_keyboard())
@bot.message_handler(commands=['start'])
def send_start(message,initial = True ):
    """ Начало взаимодействия с ботом
            - данные пользователя сверяются с данными игроков команды
            - заправшиваются дополнительные данные, сохраняются в бд
    """


    if message.chat.id not in PLAYERS_ID_LIST: 
        if message.chat.id not in ADMINS_ID_LIST :
            if initial == True:
                bot.reply_to(message, f'Привет, для доступа обратись к админам команды')

        if message.chat.id in ADMINS_ID_LIST:
            user=User(message)
            if initial ==True:
                bot.send_message(chat_id=message.chat.id,text=f'Привет, {user.name}!')
            MAIN_ADMIN(message)

    else:
        user = User(message)
        if initial == True:

            bot.send_message(chat_id=message.chat.id,text=f'Привет, {user.name}!')

        buttons_list = ['Моя статистика','Команда']
        menu_keyboard = Keyboard(buttons_list)

        bot.send_message(chat_id=message.chat.id,text='Главное меню',reply_markup=menu_keyboard.get_keyboard())
        bot.register_next_step_handler(message,main_menu)
"""
----------------------------------------------ГЛАВНОЕ МЕНЮ АДМИНИСТРАТОРА----------------------------------
"""
def MAIN_ADMIN(message):
    buttons_list = ['Моя статистика','Команда','Управление командой']
    menu_keyboard = Keyboard(buttons_list)

    bot.send_message(chat_id=message.chat.id, text='Главное меню', reply_markup=menu_keyboard.get_keyboard())
    bot.register_next_step_handler(message,main_admin_menu)

def main_admin_menu(message):

    command=message.text
    if command =="Моя статистика":
        STAT(message)
    if command =="Команда":
        TEAM(message)
    if command=="Управление командой":
        TEAM_MANAGEMENT(message)
"""
--------------------------------------------ГЛАВНОЕ МЕНЮ ПОЛЬЗОВАТЕЛЯ--------------------------------------------------
"""
def MAIN(message):
    buttons_list = ['Моя статистика','Команда']
    menu_keyboard = Keyboard(buttons_list)

    bot.send_message(chat_id=message.chat.id, text='Главное меню', reply_markup=menu_keyboard.get_keyboard())
    bot.register_next_step_handler(message,main_menu)

def main_menu(message):
    if message.text =="Моя статистика":
        STAT(message)
    if message.text =="Команда":
        TEAM(message)
"""
-----------------------------------------------СТАТИСТИКА---------------------------------------
"""
def STAT(message):
    buttons_list = ['Моя статистика по сезонам', 'Моя статистика за всё время','Назад']
    my_stat_keyboard = Keyboard(buttons_list)
    bot.send_message(chat_id=message.chat.id, text='Выберите период', reply_markup=my_stat_keyboard.get_keyboard())
    bot.register_next_step_handler(message,stat_menu)

def stat_menu(message):
    if message.text =='Моя статистика за всё время':
        my_stat_all_time(message)
    if message.text=='Моя статистика по сезонам':
        my_stat_by_season_pt1(message)
    if message.text=='Назад':
        if message.chat.id in ADMINS_ID_LIST:
            MAIN_ADMIN(message)
        else:
            MAIN(message)

def my_stat_by_season_pt1(message):
    button_list=['Моя статистика за текущий сезон','Моя статистика за сезон 2022', 'Назад']
    my_stat_by_season_keyboard=Keyboard(button_list)
    bot.send_message(chat_id=message.chat.id, text="Выберите сезон", reply_markup=my_stat_by_season_keyboard.get_keyboard())
    bot.register_next_step_handler(message, my_stat_by_season_pt2)

def my_stat_by_season_pt2(message):
    if message.text=='Моя статистика за текущий сезон':
        my_stat_current_season(message)
    if message.text=='Моя статистика за сезон 2022':
        my_stat_season_2022(message)
    if message.text=='Назад':
        STAT(message)

def my_stat_current_season(message):
    tg_id=message.chat.id
    player_info=[]
    player_info.append(tg_id)

    button_list=['Назад']
    current_season_keyboard=Keyboard(button_list)
    text=db_player_season_2023_stat(db_session,player_info)
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=current_season_keyboard.get_keyboard())
    bot.register_next_step_handler(message, my_stat_by_season_pt1)

def my_stat_season_2022(message):
    tg_id=message.chat.id
    player_info=[]
    player_info.append(tg_id)

    button_list=['Назад']
    season_2022_keyboard=Keyboard(button_list)
    text=db_player_season_2022_stat(db_session,player_info)
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=season_2022_keyboard.get_keyboard())
    bot.register_next_step_handler(message, my_stat_by_season_pt1)

def my_stat_all_time(message):
    tg_id=message.chat.id
    player_info=[]
    player_info.append(tg_id)

    text = db_player_all_time_stat(db_session,player_info)
    bot.send_message(chat_id=message.chat.id, text=text)
    STAT(message)

"""
-----------------------------------------------КОМАНДА---------------------------------------
"""
def TEAM(message):
    buttons_list = ['Турнирные таблицы', 'Список игроков','Статистика команды', 'Статистика игроков', 'Назад']
    team_keyboard = Keyboard(buttons_list)
    bot.send_message(chat_id=message.chat.id, text='Выберите раздел', reply_markup=team_keyboard.get_keyboard())
    bot.register_next_step_handler(message, team_menu)

def team_menu(message = None):
    if message.text=='Турнирные таблицы':
        tournament_table(message)
    if message.text=='Список игроков':
        players_list(message)
    if message.text=='Статистика команды':
        team_stat(message)
    if message.text=='Статистика игроков':
        players_stat(message)
    if message.text=='Назад':
        if message.chat.id in PLAYERS_ID_LIST:
            MAIN(message)
        else:
            MAIN_ADMIN(message)
"""
ТУРНИРНЫЕ ТАБЛИЦЫ
"""
def tournament_table(message):
    bot.send_message(chat_id=message.chat.id, text='http://oflm.ru/league/vtoraya23/')
    TEAM(message)
"""
СПИСОК ИГРОКОВ
"""
def players_list(message):
    text=db_players_list(db_session)
    bot.send_message(chat_id=message.chat.id, text=text)
    TEAM(message)
"""
СТАТИСТИКА КОМАНДЫ
"""
def team_stat(message):
    buttons_list = ['Статистика команды по сезонам', 'Статистика команды за всё время','Назад']
    team_stat_keyboard = Keyboard(buttons_list)
    bot.send_message(chat_id=message.chat.id, text='Выберите период', reply_markup=team_stat_keyboard.get_keyboard())
    bot.register_next_step_handler(message, team_stat_menu)

def team_stat_menu(message):
    if message.text=='Статистика команды по сезонам':
        team_stat_by_season(message)
    if message.text=='Статистика команды за всё время':
        text=db_team_all_time_stat(db_session)
        bot.send_message(chat_id=message.chat.id, text=text)
        team_stat(message)
    if message.text=='Назад':
        TEAM(message)

def team_stat_by_season(message):
    buttons_list = ['Статистика команды за сезон 2022', 'Статистика команды за текущий сезон', 'Назад']
    team_stat_by_season_keyboard = Keyboard(buttons_list)

    bot.send_message(chat_id=message.chat.id, text='Выберите сезон' , reply_markup=team_stat_by_season_keyboard.get_keyboard())
    bot.register_next_step_handler(message,team_stat_by_season_menu)

def team_stat_by_season_menu(message):
    if message.text=='Статистика команды за текущий сезон':
        team_stat_current_season(message)
    if message.text=='Статистика команды за сезон 2022':
        team_stat_season_2022(message)
    if message.text=='Назад':
        team_stat(message)

def team_stat_current_season(message):
    text=db_team_season_2023_stat(db_session)
    bot.send_message(chat_id=message.chat.id, text=text)
    team_stat_by_season(message)

def team_stat_season_2022(message):
    text=db_team_season_2022_stat(db_session)
    bot.send_message(chat_id=message.chat.id, text=text)
    team_stat_by_season(message)
"""
СТАТИСТИКА ИГРОКОВ
"""

def players_stat(message):
    list=get_names_and_numbers(db_session)
    markup = types.InlineKeyboardMarkup()
    buttons_list=[]
    for i in range(0,len(list)):
        name=list[i][1]
        number=list[i][0]
        btn=types.InlineKeyboardButton(text=f"{name}", callback_data=f"{number}")
        buttons_list.append(btn)
    markup = types.InlineKeyboardMarkup()
    markup.add(*buttons_list)
    buttons_list=['Назад']
    keyboard=Keyboard(buttons_list)
    bot.send_message(chat_id=message.chat.id, text='Выберите игрока', reply_markup=markup)
    bot.send_message(chat_id=message.chat.id, text="Для выхода из раздела воспользуйтесь кнопкой 'Назад' стандартного меню",reply_markup=keyboard.get_keyboard())
    bot.register_next_step_handler(message, players_stat_menu)

def players_stat_menu(message):
    if message.text=="Назад":
        TEAM_MANAGEMENT(message)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data=="да":
        confirm_lineup(call)
        print("Прошло")
    if call.data=="нет":
        print("Не прошло")
        TEAM_MANAGEMENT(call.message)
        open("lineup.txt", "w")
    list=get_names_and_numbers(db_session)
    name_list=[]
    for i in range(0,len(list)):
        name=list[i][1]
        number=list[i][0]
        name_list.append(name)
        player_info=[]
        if call.data == f"{number}":
            player_info.append(name)
            tg_id=get_player_tg(db_session,player_info)
            player_info[0]=tg_id
            output= db_player_all_time_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За всё время:\n"+output)
            output= db_player_season_2022_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2022:\n"+output)
            output= db_player_season_2023_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2023:\n"+output)
    for name in name_list:
        if call.data==f"{name}":         
            create_lineup(call,name)
    if call.data=="Готово":
        check_lineup(call)

def create_lineup(call,name):
    path = "lineup.txt"
    if os.path.isfile(path) ==True:
        file = open("lineup.txt", "r")
        lines = [line.rstrip() for line in file]
        file.close
        print("прочитано")
        if not lines:
            file=open("lineup.txt", "a+")
            file.write(f"{name}")
            file.write("\n")
            file.close
            bot.send_message(chat_id=call.message.chat.id, text=f"Игрок {name} добавлен в состав")
            print("добавлен")
        else:
            if name in lines:
                bot.send_message(chat_id=call.message.chat.id, text=f"Игрок {name} уже есть в составе")
                file.close
                print("уже есть")
            else:
                file=open("lineup.txt", "a+")
                file.write(f"{name}")
                file.write("\n")
                file.close
                bot.send_message(chat_id=call.message.chat.id, text=f"Игрок {name} добавлен в состав")
    else:
        bot.send_message(chat_id=call.message.chat.id, text="В данный момент работа модуля невозможна")

def check_lineup(call):
    path = "lineup.txt"
    if os.path.isfile(path) ==False:
        bot.send_message(chat_id=call.message.chat.id, text="Состав не укомплектован")
        #дописать ветку
    if os.path.isfile(path) ==True:
        file = open("lineup.txt", "r")
        lines = [line.rstrip() for line in file]
        file.close
        output=""
        if len(lines)>=6:
            for i in range(0,len(lines)):
                output+=f"{lines[i]}\n"
            markup = types.InlineKeyboardMarkup()
            btn=types.InlineKeyboardButton(text="Подтвердить", callback_data="да")
            markup.add(btn)
            btn=types.InlineKeyboardButton(text="Отменить", callback_data="нет")
            markup.add(btn)
            bot.send_message(chat_id=call.message.chat.id, text=f"Подтвердите состав:\n{output}", reply_markup=markup)
        else:
            bot.send_message(chat_id=call.message.chat.id, text="Состав не укомплектован")

def confirm_lineup(call):
    """file = open("lineup.txt", "r")
    lines = [line.rstrip() for line in file]
    file.close
    player_info=[]
    for i in range(0, len(lines)):
        player_info.append(f"{lines[i]}")
    db_insert_games(db_session, player_info)"""
    bot.send_message(chat_id=call.message.chat.id, text="Состав сформирован")
    game_result(call.message)
"""
------------------------------------------УПРАВЛЕНИЕ КОМАНДОЙ---------------------------------
"""
def TEAM_MANAGEMENT(message):
    buttons_list = ['День игры','Состав на матч', 'Результат матча','Подготовить рассылку','Изменить состав команды','Редактировать профиль игрока','Назад']
    team_management_keyboard = Keyboard(buttons_list)
    bot.send_message(chat_id=message.chat.id, text='Меню управления командой',reply_markup=team_management_keyboard.get_keyboard())
    bot.register_next_step_handler(message, team_management_menu)

def team_management_menu(message):
    if message.text=='Состав на матч':
        team_list(message)
    if message.text=='Результат матча':
        game_result(message)
    if message.text=='Подготовить рассылку':
        mailing(message)
    if message.text=='Изменить состав команды':
        change_squad_list(message)
    if message.text=='Редактировать профиль игрока':
        edit_profile(message)
    if message.text=='Назад':
        MAIN_ADMIN(message)
"""
Состав на матч
"""
def team_list(message):
    bot.send_photo(chat_id=message.chat.id,photo=InputFile(FIELD_PHOTO))
    list=get_names_and_numbers(db_session)
    markup = types.InlineKeyboardMarkup()
    buttons_list=[]
    for i in range(0,len(list)):
        name=list[i][1]
        btn=types.InlineKeyboardButton(text=f"{name}", callback_data=f"{name}")
        buttons_list.append(btn)
    btn=types.InlineKeyboardButton(text="Готово", callback_data="Готово")
    buttons_list.append(btn)
    markup = types.InlineKeyboardMarkup()
    markup.add(*buttons_list)
    buttons_list=['Назад']
    keyboard=Keyboard(buttons_list)
    bot.send_message(chat_id=message.chat.id, text='Соберите состав', reply_markup=markup)
    bot.send_message(chat_id=message.chat.id, text="Для выхода из раздела воспользуйтесь кнопкой 'Назад' стандартного меню",reply_markup=keyboard.get_keyboard())
    bot.register_next_step_handler(message, team_list_menu)

def team_list_menu(message):
    if message.text=="Назад":
        TEAM_MANAGEMENT(message)

"""
РЕДАКТИРОВАТЬ ПРОФИЛЬ ИГРОКА
"""
def edit_profile(message):
    buttons_list = ['Назад']
    keyboard = Keyboard(buttons_list)

    bot.send_message(chat_id=message.chat.id, text='Введите номер игрока', reply_markup=keyboard.get_keyboard())
    bot.register_next_step_handler(message,type_number)

def type_number(message):
    if message.text=="Назад":
        TEAM_MANAGEMENT(message)
    else:
        number=message.text
        player_info=[]
        player_info.append(number)
        if IntValidator.validateValue(number) == True:
            if check_number(db_session,player_info)!=False:
                if check_vk_id(db_session,player_info)==False:
                    name=get_name_by_number(db_session, player_info)
                    bot.send_message(chat_id=message.chat.id, text=f'Введите ссылку на профиль игрока {name} в соц.сети Вконтакте')
                    bot.register_next_step_handler(message, type_vk_id,player_info)
                else:
                    buttons_list = ['Да', 'Нет']
                    keyboard = Keyboard(buttons_list)
                    bot.send_message(chat_id=message.chat.id, text=f'Ссылка на профиль уже сохранена. Хотите изменить?',reply_markup=keyboard.get_keyboard())
                    bot.register_next_step_handler(message, change_link, player_info)
            else:
                bot.send_message(chat_id=message.chat.id, text='Игрока с таким номером не существует')
        else:
            output=BotValueError.process()
            return(output)

def change_link(message, player_info):
    if message.text=='Да':
        bot.send_message(chat_id=message.chat.id, text='Вставьте новую ссылку на профиль')
        bot.register_next_step_handler(message, type_vk_id, player_info)
    if message.text=='Нет':
        TEAM_MANAGEMENT(message)

def confirm_edit(message,player_info):
    if message.text =='Подтвердить':
        db_insert_vk_id(db_session,player_info)
        bot.send_message(chat_id=message.chat.id, text="Профиль отредактирован")
        TEAM_MANAGEMENT(message)
    if message.text =='Отменить':
        TEAM_MANAGEMENT(message)

def type_vk_id(message, player_info):
    vk_id=message.text
    player_info.append(vk_id)

    buttons_list = ['Подтвердить', 'Отменить']
    keyboard = Keyboard(buttons_list)
    bot.send_message(chat_id=message.chat.id, text='Подтвердить изменение',reply_markup=keyboard.get_keyboard())
    bot.register_next_step_handler(message, confirm_edit, player_info)
"""
ИЗМЕНИТЬ СОСТАВ КОМАНДЫ
"""
def change_squad_list(message):
    buttons_list = ['Добавить игрока', 'Удалить игрока', 'Назад']
    change_squad_list_keyboard = Keyboard(buttons_list)
    bot.send_message(chat_id=message.chat.id, text='Выберите нужное',reply_markup=change_squad_list_keyboard.get_keyboard())
    bot.register_next_step_handler(message, change_squad_list_menu)

def change_squad_list_menu(message):
    if message.text=='Добавить игрока':
        add_player(message)
    if message.text=='Удалить игрока':
        delete_player_pt1(message)
    if message.text=='Назад':
        TEAM_MANAGEMENT(message)
"""
ДОБАВИТЬ ИГРОКА
"""
def add_player(message):
    button_list=['Назад']
    add_player_keyboard=Keyboard(button_list)
    player_info=[]
    bot.send_message(chat_id=message.chat.id,text='Введите информацию об игроке:\nФамилия Имя\nИгровой номер\ntelegram_id\nvk_id',reply_markup=add_player_keyboard.get_keyboard())
    bot.register_next_step_handler(message, type_info,player_info)

def type_info(message,player_info):
    if message.text=='Назад':
        change_squad_list(message)
    else:
        info=message.text
        x=info.split("\n")
        y=0
        for i in x:
            if i:
                y+= 1
        if y<3:
            bot.send_message(chat_id=message.chat.id,text="Не хватает данных")
        if y==3:
            name=info.split("\n")[0]
            number=info.split("\n")[1]
            tg_id=info.split("\n")[2]
            vk_id="отсутствует"
            if IntValidator.validateValue(number)==True:
                player_info.append(number)
                if check_number(db_session, player_info)==False:
                    if TextValidator.validateValue(name)==True:
                        if TextValidator.validatePlayerName(name)==True:
                            player_info.append(name)
                            if check_name(db_session, player_info)==False:
                                if IntValidator.validateValue(tg_id)==True:
                                    player_info.append(tg_id)
                                    if check_tg_id(db_session,player_info)==False:
                                        player_info.append(vk_id)
                                        db_insert_player(db_session,player_info)
                                        bot.send_message(chat_id=message.chat.id,text="Данные об игроке внесены\nНе забудьте добавить ссылку на страницу игрока в сети Вконтакте")
                                    else:
                                        bot.send_message(chat_id=message.chat.id,text='Игрок с таким telegram_id уже есть в таблице')
                                else:
                                    output=BotValueError.process()
                                    bot.send_message(chat_id=message.chat.id, text=output)
                            else:
                                bot.send_message(chat_id=message.chat.id,text='Игрок с таким именем уже есть в таблице')
                        else:
                            output=BotValueError.process()
                            bot.send_message(chat_id=message.chat.id, text=output)
                    else:
                        output=BotValueError.process()
                        bot.send_message(chat_id=message.chat.id, text=output)
                else:
                    bot.send_message(chat_id=message.chat.id,text='Данный номер занят')
            else:
                output=BotValueError.process()
                bot.send_message(chat_id=message.chat.id, text=output)
        if y==4:
            name=info.split("\n")[0]
            number=info.split("\n")[1]
            tg_id=info.split("\n")[2]
            vk_id=info.split("\n")[3]
            if IntValidator.validateValue(number)==True:
                player_info.append(number)
                if check_number(db_session, player_info)==False:
                    if TextValidator.validateValue(name)==True:
                        if TextValidator.validatePlayerName(name)==True:
                            player_info.append(name)
                            if check_name(db_session, player_info)==False:
                                if IntValidator.validateValue(tg_id)==True:
                                    player_info.append(tg_id)
                                    if check_tg_id(db_session,player_info)==False:
                                        player_info.append(vk_id)
                                        db_insert_player(db_session,player_info)
                                        bot.send_message(chat_id=message.chat.id,text="Данные об игроке внесены")
                                    else:
                                        bot.send_message(chat_id=message.chat.id,text='Игрок с таким telegram_id уже есть в таблице')
                                else:
                                    output=BotValueError.process()
                                    bot.send_message(chat_id=message.chat.id, text=output)
                            else:
                                bot.send_message(chat_id=message.chat.id,text='Игрок с таким именем уже есть в таблице')
                        else:
                            output=BotValueError.process()
                            bot.send_message(chat_id=message.chat.id, text=output)
                    else:
                        output=BotValueError.process()
                        bot.send_message(chat_id=message.chat.id, text=output)
                else:
                    bot.send_message(chat_id=message.chat.id,text='Данный номер занят')
            else:
                output=BotValueError.process()
                bot.send_message(chat_id=message.chat.id, text=output)
        if y>4:
            bot.send_message(chat_id=message.chat.id,text="Ошибки всегда поджидают, чтобы их допускали.")
"""
УДАЛИТЬ ИГРОКА
"""
def delete_player_pt1(message):
    button_list=['Назад']
    delete_player_keyboard=Keyboard(button_list)
    bot.send_message(chat_id=message.chat.id, text='Введите номер игрока', reply_markup=delete_player_keyboard.get_keyboard())
    bot.register_next_step_handler(message, delete_player_pt2)

def delete_player_pt2(message):
    if message.text=='Назад':
        change_squad_list(message)
    else:
        number=message.text
        if IntValidator.validateValue(number) == True:
            number=int(number)
            player_info=[]
            player_info.append(number)
            if check_number(db_session,player_info)==False:
                bot.send_message(chat_id=message.chat.id, text='Игрока с таким номером не существует')
                delete_player_pt1(message)

            else:
                name=get_name_by_number(db_session,player_info)
                markup = ReplyKeyboardMarkup
                button_list = ['Подтвердить', 'Отменить']
                markup=Keyboard(button_list)
                bot.send_message(chat_id=message.chat.id, text=f'Подтвердите удаление игрока\t{name}',reply_markup=markup.get_keyboard())
                bot.register_next_step_handler(message, delete_player_confirm, player_info)
        else:
            output=BotValueError.process()
            bot.send_message(chat_id=message.chat.id, text=output)

def delete_player_confirm(message,player_info):
    if message.text == "Подтвердить":
        db_delete_player(db_session,player_info)
        bot.send_message(message.chat.id, text=f"Игрок удалён")
        delete_player_pt1(message)
    if message.text == "Отменить":
        bot.send_message(message.chat.id, text="Удаление отменено")
        delete_player_pt1(message)

"""
РЕЗУЛЬТАТ МАТЧА
"""
def game_result(message):
    button_list=['Назад']
    game_result_keyboard=Keyboard(button_list)
    game_info=[]
    bot.send_message(chat_id=message.chat.id, text='Счёт игры (забито : пропущено):', reply_markup=game_result_keyboard.get_keyboard())
    bot.register_next_step_handler(message, team_stat_pt1 ,game_info)

def team_stat_pt1(message,game_info):
    if message.text=='Назад':
        game_result(message)
    else:
        string=message.text
        if string.count(":")!=1:
            output=BotValueError.process()
            bot.send_message(chat_id=message.chat.id, text=output)
            game_result(message)
        else:
            if IntValidator.validateValue(string.split(":")[0]) == True:
                scored=string.split(":")[0]
                if IntValidator.validateValue(string.split(":")[1]) == True:
                    conceded=string.split(":")[1]
                    wins=0
                    loses=0
                    draws=0
                    if scored!=conceded:
                        if scored>conceded:
                            wins=1
                            loses=0
                            draws=0
                            result="победа"

                        if scored<conceded:
                            wins=0
                            loses=1
                            draws=0
                            result="поражение"
                    else:
                        wins=0
                        loses=0
                        draws=1
                        result="ничья"
                    game_info.append(result)
                    game_info.append(wins)
                    game_info.append(loses)
                    game_info.append(draws)
                    game_info.append(scored)
                    game_info.append(conceded)

                    bot.send_message(chat_id=message.chat.id, text='Карточки(жёлтые:красные):')
                    bot.register_next_step_handler(message, team_stat_pt2 ,game_info)
                else:
                    output=BotValueError.process()
                    bot.send_message(chat_id=message.chat.id, text=output)
            else:
                output=BotValueError.process()
                bot.send_message(chat_id=message.chat.id, text=output)

def team_stat_pt2(message,game_info):
    string=message.text
    if not string.find(":"):
        output=BotValueError.process()
        bot.send_message(chat_id=message.chat.id, text=output)
    else:

        yellow=string.split(":")[0]
        red=string.split(":")[1]
        if IntValidator.validateValue(yellow) == True:
            if IntValidator.validateValue(red) == True:
                game_info.append(yellow)
                game_info.append(red)

                bot.send_message(chat_id=message.chat.id, text='Введите персональные результаты:\n(Игрок:гол:передача:жёлтые:красные)')
                bot.register_next_step_handler(message, team_stat_pt3 ,game_info)
        else:
            output=BotValueError.process()
            bot.send_message(chat_id=message.chat.id, text=output)

def team_stat_pt3(message,game_info):
    info=message.text
    x=info.split("\n")
    y=0
    for i in x:
        if i:
            y+= 1
    personal_info=[]
    for i in range(y):
        name=x[i].split(":")[0]
        goals=x[i].split(":")[1]
        assists=x[i].split(":")[2]
        yc=x[i].split(":")[3]
        rc=x[i].split(":")[4]
        if TextValidator.validateValue(name)==True:
            if TextValidator.validatePlayerName(name)==True:
                if IntValidator.validateValue(goals)==True:
                    if IntValidator.validateValue(assists)==True:
                        if IntValidator.validateValue(yc)==True:
                            if IntValidator.validateValue(rc)==True:
                                personal_info.append(x[i])
                            else:
                                output=BotValueError.process()
                                bot.send_message(chat_id=message.chat.id, text=output)
                        else:
                            output=BotValueError.process()
                            bot.send_message(chat_id=message.chat.id, text=output)
                    else:
                        output=BotValueError.process()
                        bot.send_message(chat_id=message.chat.id, text=output)
                else:
                    output=BotValueError.process()
                    bot.send_message(chat_id=message.chat.id, text=output)
            else:
                output=BotValueError.process()
                bot.send_message(chat_id=message.chat.id, text=output)
        else:
            output=BotValueError.process()
            bot.send_message(chat_id=message.chat.id, text=output)
    game_info.append(personal_info)
    team_stat_pt4(message,game_info)

def team_stat_pt4(message, game_info):
    if game_info[0]=="поражение":
        text=f"Поражение\nЗабито: {game_info[4]}\nПропущено: {game_info[5]}\nЖёлтые карточки: {game_info[6]}\nКрасные карточки: {game_info[7]}\n\nЛичная статистика:\n{game_info[8]}"
    if game_info[0]=="победа":
        text=f"Победа\nЗабито: {game_info[4]}\nПропущено: {game_info[5]}\nЖёлтые карточки: {game_info[6]}\nКрасные карточки: {game_info[7]}\n\nЛичная статистика:\n{game_info[8]}"
    if game_info[0]=="ничья":
        text=f"Ничья\nЗабито: {game_info[4]}\nПропущено: {game_info[5]}\nЖёлтые карточки: {game_info[6]}\nКрасные карточки: {game_info[7]}\n\nЛичная статистика:\n{game_info[8]}"

    buttons_list = ['Подтвердить', 'Отменить']
    keyboard = Keyboard(buttons_list)
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard.get_keyboard())
    bot.register_next_step_handler(message, team_stat_pt5 ,game_info)

def team_stat_pt5(message,game_info):
    if message.text =="Подтвердить":
        insert_game_result_team(db_session, game_info)
        insert_game_result_player(db_session,game_info)
        #confirm_file = open("c:/applications/new.txt", "w")
        with open("c:/applications/change_stat.txt", "w", encoding='utf-8') as file:
            for  i in range(0,9):
                file.write(f'{game_info[i]}\n')
            file.write('Ожидает подтверждения')
        bot.send_message(chat_id=message.chat.id, text="Статистика ожидает подтверждения")
        for row in ADMINS_ID_LIST:
            bot.send_message(chat_id=row, text="Информация ожидает подтверждения")
        TEAM_MANAGEMENT(message)
    if message.text =="Отменить":
        TEAM_MANAGEMENT(message)
"""
РАССЫЛКА
"""
def mailing(message):
    buttons_list = ['Игра','Тренировка', 'Объявление', 'Назад']
    add_new_player_keyboard = Keyboard(buttons_list)

    bot.send_message(chat_id=message.chat.id, text='Выберите мероприятие',reply_markup=add_new_player_keyboard.get_keyboard())
    bot.register_next_step_handler(message, mailing_menu)

def mailing_menu(message):
    if message.text=='Игра':
        prepair_game_mailing(message)
    if message.text=='Тренировка':
        prepair_training_mailing(message)
    if message.text=='Объявление':
        prepair_advertisment(message)
    if message.text=='Назад':
        TEAM_MANAGEMENT(message)

def prepair_game_mailing(message):
    button_list=['Назад']
    prepair_game_mailing_keyboard=Keyboard(button_list)
    bot.send_message(chat_id=message.chat.id, text='Введите день', reply_markup=prepair_game_mailing_keyboard.get_keyboard())
    info=[]
    bot.register_next_step_handler(message,type_game_day, info)

def type_game_day(message,info):
    if message.text=='Назад':
        mailing(message)
    else:
        date=message.text
        info.append(date)

        bot.send_message(chat_id=message.chat.id,text='Введите время в формате HH:MM')
        bot.register_next_step_handler(message, type_game_time, info)

def type_game_time(message, info):
    time=message.text
    info.append(time)

    bot.send_message(chat_id=message.chat.id,text='Вставьте адрес')
    bot.register_next_step_handler(message, type_game_address, info)

def type_game_address(message, info):
    address=message.text
    info.append(address)

    bot.send_message(chat_id=message.chat.id, text='Вставьте ссылку на опрос')
    bot.register_next_step_handler(message, type_game_link, info)

def type_game_link(message,info):

    link = message.text
    info.append(link)
    bot.send_message(chat_id=message.chat.id,text="Проверьте данные:")
    check_game_mailing(message, info)

def check_game_mailing(message, info):
    buttons_list = ['Подтвердить', 'Отменить']
    keyboard = Keyboard(buttons_list)

    str_game=f'Время игры:{info[0]} {info[1]}\nАдрес:{info[2]}\nОпрос:{info[3]}'
    info[0]=str_game
    bot.send_message(chat_id=message.chat.id,text=str_game,reply_markup=keyboard.get_keyboard())
    bot.register_next_step_handler(message, confirm_game_mailing ,info)

def confirm_game_mailing(message,info):
    if message.text =="Подтвердить":
        send_mailing(info)
        mailing(message)
    if message.text =="Отменить":
        mailing(message)

def prepair_training_mailing(message):
    button_list=['Назад']
    prepair_training_mailing_keyboard=Keyboard(button_list)
    bot.send_message(chat_id=message.chat.id, text='Введите день', reply_markup=prepair_training_mailing_keyboard.get_keyboard())

    info=[]
    bot.register_next_step_handler(message,type_training_day, info)

def type_training_day(message, info):
    if message.text=='Назад':
        mailing(message)
    else:
        date=message.text
        info.append(date)

        bot.send_message(chat_id=message.chat.id,text='Введите время в формате HH:MM')
        bot.register_next_step_handler(message, type_training_time, info)

def type_training_time(message, info):
    time=message.text
    info.append(time)

    bot.send_message(chat_id=message.chat.id,text='Вставьте адрес')
    bot.register_next_step_handler(message, type_training_address, info)

def type_training_address(message, info):
    address=message.text
    info.append(address)

    bot.send_message(chat_id=message.chat.id, text='Вставьте ссылку на опрос')
    bot.register_next_step_handler(message, type_training_link, info)

def type_training_link(message,info):

    link = message.text
    info.append(link)
    bot.send_message(chat_id=message.chat.id,text="Проверьте данные:")
    check_train_mailing(message,info)

def check_train_mailing(message, info):
    buttons_list = ['Подтвердить', 'Отменить']
    keyboard = Keyboard(buttons_list)

    str_training=f'Время тренировки:{info[0]} {info[1]}\nАдрес:{info[2]}\nОпрос:{info[3]}'
    info[0]=str_training
    bot.send_message(chat_id=message.chat.id,text=str_training,reply_markup=keyboard.get_keyboard())

    bot.register_next_step_handler(message, confirm_training_mailing ,info)

def confirm_training_mailing(message,info):
    if message.text =="Подтвердить":
        send_mailing(info)
        mailing(message)
    if message.text =="Отменить":
        mailing(message)

def prepair_advertisment(message):
    button_list=['Назад']
    prepair_advertisment_keyboard=Keyboard(button_list)
    bot.send_message(chat_id=message.chat.id, text='Введите текст', reply_markup=prepair_advertisment_keyboard.get_keyboard())
    bot.register_next_step_handler(message,type_advertisement)

def type_advertisement(message):
    if message.text=='Назад':
        mailing(message)
    else:
        text=message.text
        info=[]
        info.append(text)
        bot.send_message(chat_id=message.chat.id,text="Проверьте данные:")
        check_advertisment(message,info)

def check_advertisment(message, info):
    buttons_list = ['Подтвердить', 'Отменить']
    keyboard = Keyboard(buttons_list)

    bot.send_message(chat_id=message.chat.id,text=f'{info[0]}',reply_markup=keyboard.get_keyboard())
    bot.register_next_step_handler(message, confirm_advertisment_mailing ,info)

def confirm_advertisment_mailing(message, info):
    if message.text =="Подтвердить":
        send_mailing(info)
        mailing(message)
    if message.text =="Отменить":
        mailing(message)

def send_mailing(info):
    text=info[0]
    for user in ADMINS_ID_LIST:
        bot.send_message(text = text, chat_id = user)