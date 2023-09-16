from consts import *
from engine.botError import *
from engine.valid import *
import telebot
from telebot import types
TREE = []

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

    #bot.send_photo(chat_id=message.chat.id,photo=InputFile(MAIN_PHOTO))
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

    #bot.send_photo(chat_id=message.chat.id,photo=InputFile(MAIN_PHOTO))
    bot.send_message(chat_id=message.chat.id, text='Главное меню', reply_markup=menu_keyboard.get_keyboard())
    bot.register_next_step_handler(message,main_menu)

def main_menu(message):

    command=message.text
    if command =="Моя статистика":
        STAT(message)
    if command =="Команда":
        TEAM(message)
"""
-----------------------------------------------СТАТИСТИКА---------------------------------------
"""
def STAT(message):
    buttons_list = ['Моя статистика по сезонам', 'Моя статистика за всё время','Вернуться']
    my_stat_keyboard = Keyboard(buttons_list)
    bot.send_message(chat_id=message.chat.id, text='Выберите период', reply_markup=my_stat_keyboard.get_keyboard())
    bot.register_next_step_handler(message,stat_menu)

def stat_menu(message):
    if message.text =='Моя статистика за всё время':
        my_stat_all_time(message)
    if message.text=='Моя статистика по сезонам':
        my_stat_by_season_pt1(message)
    if message.text=='Вернуться':
        if message.chat.id in ADMINS_ID_LIST:
            MAIN_ADMIN(message)
        else:
            MAIN(message)

def my_stat_by_season_pt1(message):
    button_list=['Моя статистика за текущий сезон','Моя статистика за сезон 2022', 'Вернуться']
    my_stat_by_season_keyboard=Keyboard(button_list)
    bot.send_message(chat_id=message.chat.id, text="Выберите сезон", reply_markup=my_stat_by_season_keyboard.get_keyboard())
    bot.register_next_step_handler(message, my_stat_by_season_pt2)

def my_stat_by_season_pt2(message):
    if message.text=='Моя статистика за текущий сезон':
        my_stat_current_season(message)
    if message.text=='Моя статистика за сезон 2022':
        my_stat_season_2022(message)
    if message.text=='Вернуться':
        STAT(message)

def my_stat_current_season(message):
    tg_id=message.chat.id
    player_info=[]
    player_info.append(tg_id)
    
    button_list=['Вернуться']
    current_season_keyboard=Keyboard(button_list)
    text=db_player_season_2023_stat(db_session,player_info)
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=current_season_keyboard.get_keyboard())
    bot.register_next_step_handler(message, my_stat_by_season_pt1)

def my_stat_season_2022(message):
    tg_id=message.chat.id
    player_info=[]
    player_info.append(tg_id)
    
    button_list=['Вернуться']
    season_2022_keyboard=Keyboard(button_list)
    text=db_player_season_2023_stat(db_session,player_info)
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
    buttons_list = ['Турнирные таблицы', 'Список игроков','Статистика команды', 'Статистика игроков', 'Вернуться']
    team_keyboard = Keyboard(buttons_list)
    bot.send_message(chat_id=message.chat.id, text='Команда', reply_markup=team_keyboard.get_keyboard())
    bot.register_next_step_handler(message, team_menu)

def team_menu(message):
    if message.text=='Турнирные таблицы':
        tournament_table(message)
    if message.text=='Список игроков':
        players_list(message)
    if message.text=='Статистика команды':
        team_stat(message)
    if message.text=='Статистика игроков':
        players_stat(message)
    if message.text=='Вернуться':
        if message.chat.id in PLAYERS_ID_LIST:
            MAIN(message)
        else:
            MAIN_ADMIN(message)

def tournament_table(message):
    bot.send_message(chat_id=message.chat.id, text='http://oflm.ru/league/vtoraya23/')
    TEAM(message)

def players_list(message):
    text=db_players_list(db_session)
    bot.send_message(chat_id=message.chat.id, text=text)
    TEAM(message)

def team_stat(message):
    buttons_list = ['Статистика команды по сезонам', 'Статистика команды за всё время','Вернуться']
    team_stat_keyboard = Keyboard(buttons_list)
    bot.send_message(chat_id=message.chat.id, text='Выберите период', reply_markup=team_stat_keyboard.get_keyboard())
    bot.register_next_step_handler(message, team_stat_menu)

def players_stat(message):
    pass

def team_stat_menu(message):
    if message.text=='Статистика команды по сезонам':
        team_stat_by_season(message)
    if message.text=='Статистика команды за всё время':
        text=db_team_all_time_stat(db_session)
        bot.send_message(chat_id=message.chat.id, text=text)
        team_stat(message)
    if message.text=='Вернуться':
        TEAM(message)

def team_stat_by_season(message):
    buttons_list = ['Статистика команды за сезон 2022', 'Статистика команды за текущий сезон', 'Вернуться']
    team_stat_by_season_keyboard = Keyboard(buttons_list)

    bot.send_message(chat_id=message.chat.id, text='Выберите сезон' , reply_markup=team_stat_by_season_keyboard.get_keyboard())
    bot.register_next_step_handler(message,team_stat_by_season_menu)

def team_stat_by_season_menu(message):
    if message.text=='Статистика команды за текущий сезон':
        team_stat_current_season(message)
    if message.text=='Статистика команды за сезон 2022':
        team_stat_season_2022(message)
    if message.text=='Вернуться':
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
------------------------------------------УПРАВЛЕНИЕ КОМАНДОЙ---------------------------------
"""
def TEAM_MANAGEMENT(message):
    buttons_list = ['Результат матча','Подготовить рассылку','Изменить состав команды', 'Редактировать профиль игрока', 'Вернуться']
    team_management_keyboard = Keyboard(buttons_list)
    bot.send_message(chat_id=message.chat.id, text='Меню управления командой',reply_markup=team_management_keyboard.get_keyboard())
    bot.register_next_step_handler(message, team_management_menu)

def team_management_menu(message):
    if message.text=='Результат матча':
        game_result(message)
    if message.text=='Подготовить рассылку':
        pass
    if message.text=='Изменить состав команды':
        pass
    if message.text=='Редактировать профиль игрока':
        pass
    if message.text=='Вернуться':
        MAIN_ADMIN(message)

def game_result(message):
    game_info=[]
    bot.send_message(chat_id=message.chat.id, text='Счёт игры (забито : пропущено):')
    bot.register_next_step_handler(message, team_stat_pt1 ,game_info)

def team_stat_pt1(message,game_info):
    string=message.text
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
    for i in range(y):
        pass
        #проверка построчно на валидность данных, потом на существование игроков, потом соранение одной строкой в game_info и перелача в sql запрос
"""
def team_stat_pt3(message, game_info):
    if game_info[0]=="поражение":
        text=f"Поражение\nЗабито: {game_info[4]}\nПропущено: {game_info[5]}\nЖёлтые карточки: {game_info[6]}\nКрасные карточки: {game_info[7]}"
    if game_info[0]=="победа":
        text=f"Победа\nЗабито: {game_info[4]}\nПропущено: {game_info[5]}\nЖёлтые карточки: {game_info[6]}\nКрасные карточки: {game_info[7]}"
    if game_info[0]=="ничья":
        text=f"Ничья\nЗабито: {game_info[4]}\nПропущено: {game_info[5]}\nЖёлтые карточки: {game_info[6]}\nКрасные карточки: {game_info[7]}"

    buttons_list = ['Подтвердить', 'Отменить']
    keyboard = Keyboard(buttons_list)
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard.get_keyboard())
    bot.register_next_step_handler(message, team_stat_pt4 ,game_info)
"""
def team_stat_pt4(message,game_info):
    command=message.text
    if command =="Подтвердить":
        insert_game_result(db_session, game_info)
        bot.send_message(chat_id=message.chat.id, text="Статистика изменена")
        TEAM_MANAGEMENT(message)
    if command =="Отменить":
        TEAM_MANAGEMENT(message)