from conn import *
from engine.botError import *



"""
-------------------------------------Запрос для инициализации--------------------------------
"""
def get_player_name(conn,tg_id) -> int:
    sql = f'select name from players where tg_id={tg_id}'
    conn.execute(sql)
    player_name = conn.fetch_next()
    return player_name[0].split(' ')[1]

def get_player_number(conn,tg_id):#нигде не используется
    sql = f'select number from players where tg_id={tg_id}'
    conn.execute(sql)
    number =''
    result=conn.fetch_next()
    for row in result:
        number=row
    return(number)

"""

"""

def get_player_tg(conn, player_info):
    name=player_info[0]
    sql = f'select tg_id from players where name="{name}"'
    conn.execute(sql)
    tg_id =''
    result=conn.fetch_next()
    if not result:
        tg_id=False
    else:
        for row in result:
            tg_id=row
        return(tg_id)

def get_names_and_numbers(conn):
    sql='select number, name from players where tg_id is not null'
    conn.execute(sql)
    result=conn.fetch_all()
    list=[]
    for row in result:
        list.append(row)
    return(list)

def db_players_list(conn):
    sql="select number, name, vk_id from players"
    conn.execute(sql)
    list=[]
    output=""
    result=conn.fetch_all()
    for row in result:
        list.append(row)
    for i in range(0,len(list)):
        output+= f'{list[i][1]}\nНомер: {list[i][0]}\n{list[i][2]}\n\n'  
    return(output)

"""
---------------------------------------------------------Запрос статистики--------------------------------------------------------
"""

def db_player_all_time_stat(conn,player_info):
    tg_id=player_info[0]
    sql=f"select games, goals, assists, yellow_cards, red_cards from players_stat_all_time psat join players p on p.number=psat.number where tg_id={tg_id}"
    conn.execute(sql)
    stat=[]
    result=conn.fetch_all()
    for row in result:
        stat.append(row)
    if not stat:
        output=DBdataError.process()
    else:
        output= f'Игры: {stat[0][0]}\nГолы: {stat[0][1]}\nГолевые передачи: {stat[0][2]}\nЖёлтые карточки: {stat[0][3]}\nКрасные карточки: {stat[0][4]}'
    
    return(output)

def db_player_season_2023_stat(conn,player_info):
    tg_id=player_info[0]
    sql=f"select games, goals, assists, yellow_cards, red_cards from players_stat_season_2023 pss23 join players p on p.number=pss23.number where tg_id={tg_id}"    
    conn.execute(sql)
    stat=[]
    result=conn.fetch_all()
    for row in result:
        stat.append(row)
    if not stat:
        output=DBdataError.process()
    else:
        output= f'Игры: {stat[0][0]}\nГолы: {stat[0][1]}\nГолевые передачи: {stat[0][2]}\nЖёлтые карточки: {stat[0][3]}\nКрасные карточки: {stat[0][4]}'

    return(output)

def db_player_season_2022_stat(conn,player_info):
    tg_id=player_info[0]
    sql=f"select games, goals, assists, yellow_cards, red_cards from players_stat_season_2022 pss22 join players p on p.number=pss22.number where tg_id={tg_id}"
    conn.execute(sql)
    stat=[]
    result=conn.fetch_all()
    for row in result:
        stat.append(row)
    if not stat:
        output=DBdataError.process()
    else:
        output= f'Игры: {stat[0][0]}\nГолы: {stat[0][1]}\nГолевые передачи: {stat[0][2]}\nЖёлтые карточки: {stat[0][3]}\nКрасные карточки: {stat[0][4]}'

    return(output)

def db_team_all_time_stat(conn):
    sql="select * from team_stat_all_time"
    conn.execute(sql)
    team_stat=[]
    result=conn.fetch_all()
    for row in result:
        team_stat.append(row)
    if not team_stat:
        output=DBdataError.process()
    else:
        output= f'Игры:{team_stat[0][0]}\nПобеды:{team_stat[0][1]}\nПоражения:{team_stat[0][2]}\nНичьи:{team_stat[0][3]}\nГолов забито:{team_stat[0][4]}\nГолов пропущено:{team_stat[0][5]}\nЖёлтые карточки:{team_stat[0][6]}\nКрасные карточки:{team_stat[0][7]}'

    return(output)

def db_team_season_2022_stat(conn):
    sql="select * from team_stat_season_2022"
    conn.execute(sql)
    team_stat=[]
    result=conn.fetch_all()
    for row in result:
        team_stat.append(row)
    if not team_stat:
        output=DBdataError.process()
    else:
        output= f'Игры:{team_stat[0][0]}\nПобеды:{team_stat[0][1]}\nПоражения:{team_stat[0][2]}\nНичьи:{team_stat[0][3]}\nГолов забито:{team_stat[0][4]}\nГолов пропущено:{team_stat[0][5]}\nЖёлтые карточки:{team_stat[0][6]}\nКрасные карточки:{team_stat[0][7]}'

    return(output)

def db_team_season_2023_stat(conn):
    sql="select * from team_stat_season_2023"
    conn.execute(sql)
    team_stat=[]
    result=conn.fetch_all()
    for row in result:
        team_stat.append(row)
    if not team_stat:
        output=DBdataError.process()
    else:
        output= f'Игры:{team_stat[0][0]}\nПобеды:{team_stat[0][1]}\nПоражения:{team_stat[0][2]}\nНичьи:{team_stat[0][3]}\nГолов забито:{team_stat[0][4]}\nГолов пропущено:{team_stat[0][5]}\nЖёлтые карточки:{team_stat[0][6]}\nКрасные карточки:{team_stat[0][7]}'

    return(output)


"""
--------------------------------------------------Проверка наличия информации-----------------------------------------------------------
(есть - True, нет - False)
"""
def check_number(conn,player_info):
    number=player_info[0]
    sql=f"select number from players where number={number}"
    conn.execute(sql)
    list=[]
    result=conn.fetch_all()
    for row in result:
        list.append(row)
    if not list:
        return False
    else:
        return True
    
def check_name(conn,player_info):
    name=player_info[1]
    sql=f"select number from players where name='{name}'"
    conn.execute(sql)
    list=[]
    result=conn.fetch_all()
    for row in result:
        list.append(row)
    if not list:
        return False
    else:
        return True
        
def check_tg_id(conn,player_info):
    tg_id=player_info[2]
    sql=f"select number from players where tg_id='{tg_id}'"
    conn.execute(sql)
    list=[]
    result=conn.fetch_all()
    for row in result:
        list.append(row)
    if not list:
        return False
    else:
        return True

def check_vk_id(conn, player_info):
    number= player_info[0]
    sql=f"select vk_id from players where number={number}"
    conn.execute(sql)
    list=[]
    result=conn.fetch_all()
    for row in result:
        list.append(row)
    if not list:
        return False
    else:
        return True


"""
----------------------------------------------------Изменения в БД----------------------------------------------
"""
def insert_game_result_player(conn, game_info):
    player_info=game_info[8]
    sql_arr=[]
    for i in range(0,len(player_info)):
        name=player_info[i].split(":")[0]
        goals=player_info[i].split(":")[1]
        assists=player_info[i].split(":")[2]
        yc=player_info[i].split(":")[3]
        rc=player_info[i].split(":")[4]
        sql=f"update players_stat_all_time set games=games+1, goals=goals+{goals}, assists=assists+{assists}, yellow_cards=yellow_cards+{yc}, red_cards=red_cards+{rc} where number=(select number from players where name='{name}')"
        sql_arr.append(sql)
    for i in range(0,len(sql_arr)):
        sql=sql_arr[i]
        conn.execute(sql)

def insert_game_result_team(conn, game_info):
    wins= game_info[1]
    loses = game_info[2]
    draws = game_info[3]
    gs=game_info[4]
    gc=game_info[5]
    yc=game_info[6]
    rc=game_info[7]
    sql=f"update team_stat_all_time set games = games + 1, wins=wins +{wins}, loses= loses+ {loses}, draws = draws+{draws}, goals_scored= goals_scored+ {gs}, goals_conceded=goals_conceded + {gc}, yellow_cards= yellow_cards + {yc}, red_cards= red_cards+ {rc}"
    sql1=f"update team_stat_season_2023 set games = games + 1, wins=wins +{wins}, loses= loses+ {loses}, draws = draws+{draws}, goals_scored= goals_scored+ {gs}, goals_conceded=goals_conceded + {gc}, yellow_cards= yellow_cards + {yc}, red_cards= red_cards+ {rc}"
    conn.execute(sql)
    conn.execute(sql1)

def db_insert_player(conn,player_info):
    number=player_info[0]
    name= player_info[1]
    tg_id=player_info[2]
    vk_id=player_info[3]
    sql=f"insert into players (number, name, tg_id, vk_id) values({number}, '{name}', {tg_id}, '{vk_id}') "
    sql1=f"insert into players_stat_all_time (number) values({number})"
    sql2=f"insert into players_stat_season_2022 (number) values({number})"
    sql3=f"insert into players_stat_season_2023 (number) values({number})"
    conn.execute(sql)
    conn.execute(sql1)
    conn.execute(sql2)
    conn.execute(sql3)

def db_delete_player(conn, player_info):
    number=player_info[0]
    sql=f"delete from players where number={number}"
    conn.execute(sql)

def db_insert_vk_id(conn,player_info):
    number= player_info[0]
    vk_id= player_info[1]
    sql=f"update players set vk_id='{vk_id}' where number={number}"
    conn.execute(sql)
    result=conn.fetch_all()
    return (result)

"""
---------------------------------------------
"""
def get_name_by_number(conn,player_info):
    number=player_info[0]
    sql=f"select name from players where number={number}"
    conn.execute(sql)
    result=conn.fetch_next()
    return (result)
