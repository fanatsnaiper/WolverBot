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

        buttons_list = ['Моя статистика','Команда','Управление командой']
        menu_keyboard = Keyboard(buttons_list)

        #bot.send_photo(chat_id=message.chat.id,photo=InputFile(MAIN_PHOTO))
        bot.send_message(chat_id=message.chat.id, text='Главное меню', reply_markup=menu_keyboard.get_keyboard())
    else:
        user = User(message)
        if initial == True:

            bot.send_message(chat_id=message.chat.id,text=f'Привет, {user.name}!')

        buttons_list = ['Моя статистика','Команда', 'Обратная связь']
        menu_keyboard = Keyboard(buttons_list)

        bot.send_message(chat_id=message.chat.id,text='Главное меню',reply_markup=menu_keyboard.get_keyboard())

@bot.message_handler(func=lambda message: message.text == 'Вернуться')
def cancel(message):
    print(TREE)
    try:
        TREE.pop(-1)
    except:
        send_start(message,initial=False)
    if not TREE.__len__():
        send_start(message,initial=False)
    else:
        parent = TREE[-1]
        if parent == 'Моя статистика':
            send_my_stat(message)
        if parent == 'Моя статистика по сезонам':
            send_my_by_season_stat(message)
        if parent == 'Команда':
            send_team(message)
        if parent == 'Турнирные таблицы':
            send_tables(message)
        if parent == 'Статистика команды':
            send_team_stat(message)
        if parent == 'Статистика команды по сезонам':
            send_team_all_time_stat(message)
        if parent == 'Игра':
            prepair_game_mailing(message)
        if parent == 'Тренировка':
            prepair_training_mailing(message)
        if parent == 'Управление командой':
            team_management(message)


"""
---------------------------------------------------БЛОК ОБРАТНАЯ СВЯЗЬ------------------------------------------------
"""
@bot.message_handler(func=lambda message: message.text=='Обратная связь')
def send_feedback(message):
    if message.text !='Вернуться':
        TREE.append(message.text)

    buttons_list = ['Вернуться']
    my_stat_keyboard = Keyboard(buttons_list)
    bot.send_message(chat_id=message.chat.id, text='Введите сообщение', reply_markup=my_stat_keyboard.get_keyboard())

    info=[]
    tg_id=message.chat.id
    tg_id=int(tg_id)
    info.append(tg_id)
    bot.register_next_step_handler(message, type_feedback,info )

def type_feedback(message,info):
    feedback=message.text
    info.append(feedback)
    db_feedback_insert(db_session,info)

    bot.send_message(chat_id=message.chat.id, text='Сообщение отправлено')
    for user_number in range(len(TEST_ID)):
        chat_id = TEST_ID[user_number]
        bot.send_message (text = 'Получено сообщение', chat_id = chat_id)

# @bot.message_handler(func=lambda message: message.text=="Проверка feedback'а")
# def send_feedback(message):
#     if message.text !='Вернуться':
#         TREE.append(message.text)
#
#     buttons_list = ['Вернуться']
#     my_stat_keyboard = Keyboard(buttons_list)
#
#     sql=db_feedback_check(db_session)
#     bot.send_message(chat_id=message.chat.id, text=f'__Имя пользователя:__\n{sql[0][0]}\n\n__Текст:__\n"{sql[0][1]}"',
#                      parse_mode='MarkdownV2', reply_markup=my_stat_keyboard.get_keyboard())
"""
--------------------------------------------------БЛОК МОЯ СТАТИСТИКА--------------------------------------------------
"""
@bot.message_handler(func=lambda message: message.text=='Моя статистика')
def send_my_stat(message):
    if message.text !='Вернуться':
        TREE.append(message.text)

    buttons_list = ['Моя статистика по сезонам', 'Моя статистика за всё время','Вернуться']
    my_stat_keyboard = Keyboard(buttons_list)
    bot.send_message(chat_id=message.chat.id, text='Выберите период', reply_markup=my_stat_keyboard.get_keyboard())

@bot.message_handler(func=lambda message: message.text =='Моя статистика за всё время')
def send_my_all_time_stat(message):
    tg_id=message.chat.id
    player_info=[]
    player_info.append(tg_id)
    
    text = db_player_all_time_stat(db_session,player_info)
    bot.send_message(chat_id=message.chat.id, text=text)


@bot.message_handler(func=lambda message: message.text=='Моя статистика по сезонам')
def send_my_by_season_stat(message):
    if message.text !='Вернуться':
        TREE.append(message.text)

    buttons_list = ['Моя статистика за сезон 2022', 'Моя статистика за текущий сезон','Вернуться']
    my_by_season_stat_keyboard = Keyboard(buttons_list)
    bot.send_message(chat_id=message.chat.id, text='Выберите сезон',reply_markup=my_by_season_stat_keyboard.get_keyboard())

@bot.message_handler(func=lambda message: message.text=='Моя статистика за текущий сезон')
def send_my_season_2023_stat(message):
    tg_id=message.chat.id
    player_info=[]
    player_info.append(tg_id)
    
    text=db_player_season_2023_stat(db_session,player_info)
    bot.send_message(chat_id=message.chat.id, text=text)
    

@bot.message_handler(func=lambda message: message.text=='Моя статистика за сезон 2022')
def send_my_season_2022_stat(message):
    tg_id=message.chat.id
    player_info=[]
    player_info.append(tg_id)
    
    text=db_player_season_2022_stat(db_session,player_info)
    bot.send_message(chat_id=message.chat.id, text=text)
"""
--------------------------------------------------БЛОК КОМАНДА--------------------------------------------------
"""

@bot.message_handler(func=lambda message: message.text=='Команда')
def send_team(message):
    if message.text !='Вернуться':
        TREE.append(message.text)

    buttons_list = ['Турнирные таблицы', 'Список игроков','Статистика команды', 'Статистика игроков', 'Вернуться']
    stat_keyboard = Keyboard(buttons_list)
    bot.send_message(chat_id=message.chat.id, text='Команда', reply_markup=stat_keyboard.get_keyboard())

@bot.message_handler(func=lambda message: message.text=='Турнирные таблицы')
def send_tables(message):

    bot.send_message(chat_id=message.chat.id, text='http://oflm.ru/league/vtoraya23/')



@bot.message_handler(func=lambda message: message.text=='Список игроков')
def send_players_list(message):
    """
    player_list=db_players_list(db_session)
    msg=""
    for i in range (0,len(player_list)):
        msg+=f'{player_list[i][1]}\nНомер: {player_list[i][0]}\n{player_list[i][2]}\n\n'

    bot.send_message(chat_id=message.chat.id, text=msg)
    """
    text=db_players_list(db_session)
    bot.send_message(chat_id=message.chat.id, text=text)

@bot.message_handler(func=lambda message: message.text=='Статистика команды')
def send_team_stat(message):
    if message.text !='Вернуться':
        TREE.append(message.text) 

    buttons_list = ['Статистика команды по сезонам', 'Статистика команды за всё время','Вернуться']
    stat_keyboard = Keyboard(buttons_list)
    bot.send_message(chat_id=message.chat.id, text='Выберите сезон', reply_markup=stat_keyboard.get_keyboard())

@bot.message_handler(func=lambda message: message.text=='Статистика команды за всё время')
def send_team_all_time_stat(message):

    text=db_team_all_time_stat(db_session)
    bot.send_message(chat_id=message.chat.id, text=text)

@bot.message_handler(func=lambda message: message.text=='Статистика команды по сезонам')
def send_team_by_season_stat(message):
    if message.text !='Вернуться':
        TREE.append(message.text)

    buttons_list = ['Статистика команды за сезон 2022', 'Статистика команды за текущий сезон', 'Вернуться']
    team_by_season_keyboard = Keyboard(buttons_list)

    bot.send_message(chat_id=message.chat.id, text='Выберите сезон' , reply_markup=team_by_season_keyboard.get_keyboard())

@bot.message_handler(func=lambda message: message.text=='Статистика команды за сезон 2022')
def send_team_season_2022_stat(message):

    text=db_team_season_2022_stat(db_session)
    bot.send_message(chat_id=message.chat.id, text=text)

@bot.message_handler(func=lambda message: message.text=='Статистика команды за текущий сезон')
def send_team_season_2023_stat(message):

    text=db_team_season_2023_stat(db_session)
    bot.send_message(chat_id=message.chat.id, text=text)

@bot.message_handler(func=lambda message: message.text=='Статистика игроков')
def send_players_list(message):
    if message.text !='Вернуться':
        TREE.append(message.text)

    markup = types.InlineKeyboardMarkup()
    btn1=types.InlineKeyboardButton(text="Павловичев Кирилл", callback_data="1")
    btn2=types.InlineKeyboardButton(text="Серов Егор", callback_data="2")
    btn3=types.InlineKeyboardButton(text="Мельников Глеб", callback_data="3")
    btn4=types.InlineKeyboardButton(text="Светлаков Лев", callback_data="4")
    btn5=types.InlineKeyboardButton(text="Амирбеков Садам", callback_data="5")
    btn6=types.InlineKeyboardButton(text="Белый Иван", callback_data="6")
    btn7=types.InlineKeyboardButton(text="Яковлев Михаил", callback_data="7")
    btn8=types.InlineKeyboardButton(text="Кожемякин Игнат", callback_data="8")
    btn9=types.InlineKeyboardButton(text="Каплин Андрей", callback_data="9")
    btn10=types.InlineKeyboardButton(text="Куренинов Вадим", callback_data="10")
    btn11=types.InlineKeyboardButton(text="Чуканов Кирилл", callback_data="11")
    btn12=types.InlineKeyboardButton(text="Таболин Михаил", callback_data="12")
    btn13=types.InlineKeyboardButton(text="Низамов Алексей", callback_data="13")
    btn14=types.InlineKeyboardButton(text="Рой Игорь", callback_data="14")
    btn15=types.InlineKeyboardButton(text="Порвал Резинкин", callback_data="15")
    btn16=types.InlineKeyboardButton(text="Кожемякин Захар", callback_data="16")
    btn17=types.InlineKeyboardButton(text="Мальцев Константин", callback_data="17")
    btn18=types.InlineKeyboardButton(text="Рожков Руслан", callback_data="18")

    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12, btn13, btn14, btn15, btn16, btn17, btn18)
    bot.send_message(chat_id=message.chat.id, text="Выберите игрока",reply_markup=markup)      

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        player_info=[]
        if call.data == "1":
            name="Павловичев Кирилл"
            player_info.append(name)
            tg_id=get_player_tg(db_session,player_info)
            player_info=[]
            player_info.append(tg_id)
            output= db_player_all_time_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За всё время:\n"+output)
            output= db_player_season_2022_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2022:\n"+output)
            output= db_player_season_2023_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2023:\n"+output)
        if call.data == "2":
            name="Серов Егор"
            player_info.append(name)
            tg_id=get_player_tg(db_session,player_info)
            player_info=[]
            player_info.append(tg_id)
            output= db_player_all_time_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За всё время:\n"+output)
            output= db_player_season_2022_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2022:\n"+output)
            output= db_player_season_2023_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2023:\n"+output)
        if call.data == "3":
            name="Мельников Глеб"
            player_info.append(name)
            tg_id=get_player_tg(db_session,player_info)
            player_info=[]
            player_info.append(tg_id)
            output= db_player_all_time_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За всё время:\n"+output)
            output= db_player_season_2022_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2022:\n"+output)
            output= db_player_season_2023_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2023:\n"+output)
        if call.data == "4":
            name="Светлаков Лев"
            player_info.append(name)
            tg_id=get_player_tg(db_session,player_info)
            player_info=[]
            player_info.append(tg_id)
            output= db_player_all_time_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За всё время:\n"+output)
            output= db_player_season_2022_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2022:\n"+output)
            output= db_player_season_2023_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2023:\n"+output)
        if call.data == "5":
            name="Амирбеков Садам"
            player_info.append(name)
            tg_id=get_player_tg(db_session,player_info)
            player_info=[]
            player_info.append(tg_id)
            output= db_player_all_time_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За всё время:\n"+output)
            output= db_player_season_2022_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2022:\n"+output)
            output= db_player_season_2023_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2023:\n"+output)
        if call.data == "6":
            name="Белый Иван"
            player_info.append(name)
            tg_id=get_player_tg(db_session,player_info)
            player_info=[]
            player_info.append(tg_id)
            output= db_player_all_time_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За всё время:\n"+output)
            output= db_player_season_2022_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2022:\n"+output)
            output= db_player_season_2023_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2023:\n"+output)
        if call.data == "7":
            name="Яковлев Михаил"
            player_info.append(name)
            tg_id=get_player_tg(db_session,player_info)
            player_info=[]
            player_info.append(tg_id)
            output= db_player_all_time_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За всё время:\n"+output)
            output= db_player_season_2022_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2022:\n"+output)
            output= db_player_season_2023_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2023:\n"+output)
        if call.data == "8":
            name="Кожемякин Игнат"
            player_info.append(name)
            tg_id=get_player_tg(db_session,player_info)
            player_info=[]
            player_info.append(tg_id)
            output= db_player_all_time_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За всё время:\n"+output)
            output= db_player_season_2022_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2022:\n"+output)
            output= db_player_season_2023_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2023:\n"+output)
        if call.data == "9":
            name="Каплин Андрей"
            player_info.append(name)
            tg_id=get_player_tg(db_session,player_info)
            player_info=[]
            player_info.append(tg_id)
            output= db_player_all_time_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За всё время:\n"+output)
            output= db_player_season_2022_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2022:\n"+output)
            output= db_player_season_2023_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2023:\n"+output)
        if call.data == "10":
            name="Куренинов Вадим"
            player_info.append(name)
            tg_id=get_player_tg(db_session,player_info)
            player_info=[]
            player_info.append(tg_id)
            output= db_player_all_time_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За всё время:\n"+output)
            output= db_player_season_2022_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2022:\n"+output)
            output= db_player_season_2023_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2023:\n"+output)
        if call.data == "11":
            name="Чуканов Кирилл"
            player_info.append(name)
            tg_id=get_player_tg(db_session,player_info)
            player_info=[]
            player_info.append(tg_id)
            output= db_player_all_time_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За всё время:\n"+output)
            output= db_player_season_2022_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2022:\n"+output)
            output= db_player_season_2023_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2023:\n"+output)
        if call.data == "12":
            name="Таболин Михаил"
            player_info.append(name)
            tg_id=get_player_tg(db_session,player_info)
            player_info=[]
            player_info.append(tg_id)
            output= db_player_all_time_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За всё время:\n"+output)
            output= db_player_season_2022_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2022:\n"+output)
            output= db_player_season_2023_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2023:\n"+output)
        if call.data == "13":
            name="Низамов Алексей"
            player_info.append(name)
            tg_id=get_player_tg(db_session,player_info)
            player_info=[]
            player_info.append(tg_id)
            output= db_player_all_time_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За всё время:\n"+output)
            output= db_player_season_2022_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2022:\n"+output)
            output= db_player_season_2023_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2023:\n"+output)
        if call.data == "14":
            name="Рой Игорь"
            player_info.append(name)
            tg_id=get_player_tg(db_session,player_info)
            player_info=[]
            player_info.append(tg_id)
            output= db_player_all_time_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За всё время:\n"+output)
            output= db_player_season_2022_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2022:\n"+output)
            output= db_player_season_2023_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2023:\n"+output)
        if call.data == "15":
            name="Порвал Резинкин"
            player_info.append(name)
            tg_id=get_player_tg(db_session,player_info)
            player_info=[]
            player_info.append(tg_id)
            output= db_player_all_time_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За всё время:\n"+output)
            output= db_player_season_2022_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2022:\n"+output)
            output= db_player_season_2023_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2023:\n"+output)
        if call.data == "16":
            name="Кожемякин Захар"
            player_info.append(name)
            tg_id=get_player_tg(db_session,player_info)
            player_info=[]
            player_info.append(tg_id)
            output= db_player_all_time_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За всё время:\n"+output)
            output= db_player_season_2022_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2022:\n"+output)
            output= db_player_season_2023_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2023:\n"+output)
        if call.data == "17":
            name="Мальцев Константин"
            player_info.append(name)
            tg_id=get_player_tg(db_session,player_info)
            player_info=[]
            player_info.append(tg_id)
            output= db_player_all_time_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За всё время:\n"+output)
            output= db_player_season_2022_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2022:\n"+output)
            output= db_player_season_2023_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2023:\n"+output)
        if call.data == "18":
            name="Рожков Руслан"
            player_info.append(name)
            tg_id=get_player_tg(db_session,player_info)
            player_info=[]
            player_info.append(tg_id)
            output= db_player_all_time_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За всё время:\n"+output)
            output= db_player_season_2022_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2022:\n"+output)
            output= db_player_season_2023_stat(db_session, player_info)
            bot.send_message(chat_id=call.message.chat.id, text=f"За сезон 2023:\n"+output)




"""
-------------------------------------------------   БЛОК ВАЖНАЯ ИНФОРМАЦИЯ  ---------------------------------------------------
"""





"""
--------------------------------------------------  БЛОК УПРАВЛЕНИЕ КОМАНДОЙ    --------------------------------------------------
"""


@bot.message_handler(func=lambda message: message.text=='Управление командой')
def team_management(message):
    if message.text !='Вернуться':
        TREE.append(message.text) # добавляем родительский раздел, чтобы понять, какую статистику выдать

    buttons_list = ['Результат матча','Подготовить рассылку','Изменить состав команды', 'Редактировать профиль игрока', 'Вернуться']
    team_management_keyboard = Keyboard(buttons_list)
    bot.send_message(chat_id=message.chat.id, text='Меню управления командой',reply_markup=team_management_keyboard.get_keyboard())

@bot.message_handler(func=lambda message: message.text=='Результат матча')
def game_result(message):
    if message.text !='Вернуться':
        TREE.append(message.text)

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

def team_stat_pt2(message, game_info):
    string=message.text
    yellow=string.split(":")[0]
    red=string.split(":")[1]
    if IntValidator.validateValue(yellow) == True:
        if IntValidator.validateValue(red) == True:
            game_info.append(yellow)
            game_info.append(red)

            bot.send_message(chat_id=message.chat.id, text='Проверьте данные:')
            bot.register_next_step_handler(message, team_stat_pt3 ,game_info)
    else:
        output=BotValueError.process()
        bot.send_message(chat_id=message.chat.id, text=output)

def team_stat_pt3(message, game_info):
    if game_info[0]=="поражение":
        text=f"Поражение\nЗабито: {game_info[4]}\nПропущено: {game_info[5]}\nЖёлтые карточки: {game_info[6]}\nКрасные карточки: {game_info[7]}"
    if game_info[0]=="победа":
        text=f"Победа\nЗабито: {game_info[4]}\nПропущено: {game_info[5]}\nЖёлтые карточки: {game_info[6]}\nКрасные карточки: {game_info[7]}"
    if game_info[0]=="ничья":
        text=f"Ничья\nЗабито: {game_info[4]}\nПропущено: {game_info[5]}\nЖёлтые карточки: {game_info[6]}\nКрасные карточки: {game_info[7]}"

    bot.send_message(chat_id=message.chat.id, text=text)
    bot.register_next_step_handler(message, team_stat_pt4 ,game_info)

def team_stat_pt4(message,game_info):
    change_stat_team_alltime(db_session, game_info)
    bot.send_message(chat_id=message.chat.id, text="Статистика изменена")


"""
----------------------------------------------- добавить\удалить игрока ---------------------------------------------------
"""


@bot.message_handler(func=lambda message: message.text=='Изменить состав команды')
def add_delete_player(message):
    if message.text !='Вернуться':
        TREE.append(message.text) # добавляем родительский раздел, чтобы понять, какую статистику выдать

    buttons_list = ['Добавить игрока', 'Удалить игрока', 'Вернуться']
    add_new_player_keyboard = Keyboard(buttons_list)
    bot.send_message(chat_id=message.chat.id, text='Выберите нужное',reply_markup=add_new_player_keyboard.get_keyboard())

@bot.message_handler(func=lambda message: message.text=='Добавить игрока')
def add_player_pt1(message):
    player_info = []
    bot.send_message(chat_id=message.chat.id,text='Введите фамилию и имя игрока')
    bot.register_next_step_handler(message, type_player_name,player_info)

def type_player_name(message,player_info):
    name = message.text
    if TextValidator.validatePlayerName(name) == True:
        name=str(name)
        player_info.append(name)
        if check_name(db_session,player_info)==False:
            bot.send_message(chat_id=message.chat.id,text='Введите номер игрока')
            bot.register_next_step_handler(message, type_player_number, player_info)
        else:
            bot.send_message(chat_id=message.chat.id, text='Игрок с таким именем уже существует')

    else:
        output=BotValueError.process()
        bot.send_message(chat_id=message.chat.id, text=output)

def type_player_number(message, player_info):
    number=message.text
    if IntValidator.validateValue(number) == True:
        number=int(number)
        player_info.append(number)
        if check_number(db_session,player_info)==False:
            bot.send_message(chat_id=message.chat.id,text='Введите tg_id игрока')
            bot.register_next_step_handler(message, type_tg_id, player_info)
        else:
            bot.send_message(chat_id=message.chat.id,text='Данный номер занят')
    else:
        output=BotValueError.process()
        bot.send_message(chat_id=message.chat.id, text=output)

def type_tg_id(message,player_info):
    tg_id = message.text
    if IntValidator.validateValue(tg_id) == True:
        tg_id=str(tg_id)
        player_info.append(tg_id)
        if check_tg_id(db_session,player_info)==False:
            bot.send_message(chat_id=message.chat.id, text='Игрок добавлен')
            db_insert_player(db_session,player_info)
        else:
            bot.send_message(chat_id=message.chat.id, text='Данный tg_id уже принадлежит другому игроку')
    else:
        output=BotValueError.process()
        bot.send_message(chat_id=message.chat.id, text=output)

@bot.message_handler(func=lambda message: message.text=='Удалить игрока')
def delete_player_pt1(message):
    
    bot.send_message(chat_id=message.chat.id, text='Введите номер игрока')
    bot.register_next_step_handler(message, delete_player_pt2)

def delete_player_pt2(message):
    number=message.text
    if IntValidator.validateValue(number) == True:
        number=int(number)
        player_info=[]
        player_info.append(number)
        if check_number(db_session,player_info)==False:
            bot.send_message(chat_id=message.chat.id, text='Игрока с таким номером не существует')
            bot.register_next_step_handler(message, delete_player_pt1)

        else:
            name=check_number(db_session,player_info)
            markup = ReplyKeyboardMarkup
            button_list = ['Подтвердить', 'Отменить']
            markup=Keyboard(button_list)
            bot.send_message(chat_id=message.chat.id, text=f'Подтвердите удаление игрока\t{name}',reply_markup=markup.get_keyboard())          
    else:
        output=BotValueError.process()
        bot.send_message(chat_id=message.chat.id, text=output)


@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Подтвердить"):
        #db_delete_player(db_session,player_info)
        bot.send_message(message.chat.id, text=f"Игрок удалён")
    elif(message.text == "Отменить"):
        bot.send_message(message.chat.id, text="Удаление отменено")


"""
--------------------------------------------------  рассылка    ------------------------------------------------------
"""
@bot.message_handler(func=lambda message: message.text=='Подготовить рассылку')
def mailing_variants(message):
    if message.text !='Вернуться':
        TREE.append(message.text)

    buttons_list = ['Игра','Тренировка', 'Объявление', 'Вернуться']
    add_new_player_keyboard = Keyboard(buttons_list)

    bot.send_message(chat_id=message.chat.id, text='Выберите мероприятие',reply_markup=add_new_player_keyboard.get_keyboard())

@bot.message_handler(func=lambda message: message.text=='Игра')
def prepair_game_mailing(message):

    bot.send_message(chat_id=message.chat.id, text='Введите день')

    info=[]
    bot.register_next_step_handler(message,type_game_day, info)

def type_game_day(message, info):
    date=message.text
    info.append(date)

    bot.send_message(chat_id=message.chat.id,text='Введите время в формате HH:MM')
    bot.register_next_step_handler(message, type_game_time, info)

def type_game_time(message, info):
    time=message.text
    info.append(time)

    bot.send_message(chat_id=message.chat.id,text='Вставьте адрес')
    bot.register_next_step_handler(message, type_game_address, info)
#сделать заготовленный список адресов 
def type_game_address(message, info):
    address=message.text
    info.append(address)

    bot.send_message(chat_id=message.chat.id, text='Вставьте ссылку на опрос')
    bot.register_next_step_handler(message, type_game_link, info)

def type_game_link(message,info):

    link = message.text
    info.append(link)

    str_game=f'Время игры:{info[0]} {info[1]}\nАдрес:{info[2]}\nОпрос:{info[3]}'

    for user_number in range(len(TEST_ID)):
        chat_id = TEST_ID[user_number]
        bot.send_message (text = str_game, chat_id = chat_id)

@bot.message_handler(func=lambda message: message.text=='Тренировка')
def prepair_training_mailing(message):

    bot.send_message(chat_id=message.chat.id, text='Введите день')

    info=[]
    bot.register_next_step_handler(message,type_training_day, info)

def type_training_day(message, info):
    date=message.text
    info.append(date)

    bot.send_message(chat_id=message.chat.id,text='Введите время в формате HH:MM')
    bot.register_next_step_handler(message, type_training_time, info)

def type_training_time(message, info):
    time=message.text
    info.append(time)

    bot.send_message(chat_id=message.chat.id,text='Вставьте адрес')
    bot.register_next_step_handler(message, type_training_address, info)
#сделать заготовленный список адресов 
def type_training_address(message, info):
    address=message.text
    info.append(address)

    bot.send_message(chat_id=message.chat.id, text='Вставьте ссылку на опрос')
    bot.register_next_step_handler(message, type_training_link, info)

def type_training_link(message,info):

    link = message.text
    info.append(link)

    str_training=f'Время тренировки:{info[0]} {info[1]}\nАдрес:{info[2]}\nОпрос:{info[3]}'

    for user_number in range(len(TEST_ID)):
        chat_id = TEST_ID[user_number]
        bot.send_message (text = str_training, chat_id = chat_id)

#сразу выполняется
"""
Заготовка под рассылку по времени

def type_link(message,info):

    link = message.text
    info.append(link)
    buttons_list = ['Вернуться']
    work_keyboard = Keyboard(buttons_list)

    text, link = info[0],info[1]
    str = f'Проверьте данные:\nТекст:"{text}"\nСсылка:"{link}"'


    bot.send_message(chat_id=message.chat.id, text=str)
    bot.send_message(chat_id=message.chat.id, text='Введите время рассылки')
    bot.register_next_step_handler(message, type_date, info, str)
def type_date(message,info,chat_id):
    #считать время из сообщения, проверить на адекватность (если сегодня раньше текущего момента- идёт нахуй, ночное тоже исключим: 00:00-6:00)
    date=message.text
    time=f"{date}"
    date=datetime.datetime.strptime(message.text, '%H:%M').time()

    info.append(date)
    date=info[2]
    print(date)

    str=f'{info[0]}\n{info[1]}'

    for user_number in range(len(PLAYERS_ID_LIST)):
        chat_id = PLAYERS_ID_LIST[user_number]
        #bot.send_message (text = str, chat_id = chat_id)
        schedule.every().day.at(time).do(bot.send_message (text = str, chat_id = chat_id))

"""

"""
    #добавить меню с вариантами: свой вариант, сейчас, через полчаса, через час, утром(8:00), днём(14:00), вечером(18:00), завтра утром(8:00), завтра днём(14:00), завтра вечером(18:00)
"""

@bot.message_handler(func=lambda message: message.text=='Объявление')
def prepair_advertisement(message):
    if message.text !='Вернуться':
        TREE.append(message.text)

    buttons_list = ['Вернуться']
    keyboard = Keyboard(buttons_list)

    bot.send_message(chat_id=message.chat.id, text='Введите текст', reply_markup=keyboard.get_keyboard())
    bot.register_next_step_handler(message,type_advertisement)

def type_advertisement(message):
    text=message.text

    for user_number in range(len(TEST_ID)):
        chat_id = TEST_ID[user_number]
        bot.send_message (text = text, chat_id = chat_id)


"""
-------------------------------------------------   редактировать профиль игрока(вставляет ссылку на вк)    ---------------------------------------
"""
@bot.message_handler(func=lambda message: message.text=='Редактировать профиль игрока')
def choose_player(message):
    if message.text !='Вернуться':
        TREE.append(message.text)

    buttons_list = ['Вернуться']
    keyboard = Keyboard(buttons_list)

    bot.send_message(chat_id=message.chat.id, text='Введите номер игрока', reply_markup=keyboard.get_keyboard())
    bot.register_next_step_handler(message,type_number)

def type_number(message):
    number=message.text

    if IntValidator.validateValue(number) == True:

        number=int(number)
        player_info=[]
        player_info.append(number)

        bot.send_message(chat_id=message.chat.id, text='Введите ссылку на профиль в Вконтакте')
        bot.register_next_step_handler(message, type_vk_id,player_info)
    else:
        output=BotValueError.process()
        return(output)

def type_vk_id(message, player_info):
    vk_id=message.text

    if TextValidator.validateValue(vk_id) == True:

        player_info.append(vk_id)

        bot.send_message(chat_id=message.chat.id, text='Профиль изменён')
        db_insert_vk_id(db_session,player_info)
    else:
        output=BotValueError.process()
        return(output)