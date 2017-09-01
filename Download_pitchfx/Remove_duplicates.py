"""
Use row_id to delete duplicate pitchfx rows


select rowid, gameday_link, num, batter_name, pitcher_name from atbat where rowid not in (select max(rowid) from atbat group by gameday_link, num,batter_name, pitcher_name);
delete from atbat where rowid not in (select max(rowid) from atbat group by gameday_link, num,batter_name, pitcher_name);
table_names = ['game', 'media', 'coach', 'player',  'umpire', 
               'hip', 'atbat', 'action', 'pitch', 'po', 'runner']
               
"""


import sqlite3 as sql
import os,os.path


def remove_duplicate_rows(path_to_db):

    con_sql = sql.connect(path_to_db) 
    c = con_sql.cursor()
            
    action_q = """delete from action where rowid not in 
              (select max(rowid) from action 
              group by gameday_link, num, event_num) """

    atbat_q = """delete from atbat where rowid not in 
                 (select max(rowid) from atbat 
                 group by gameday_link, num,batter_name, pitcher_name) """

    coach_q = """delete from coach where rowid not in 
                 (select max(rowid) from coach 
                 group by gameday_link, name, id) """

    game_q = """delete from game where rowid not in 
                (select max(rowid) from game 
                group by gameday_link, id) """

    hip_q = """delete from hip where rowid not in 
               (select max(rowid) from hip 
               group by gameday_link, batter, pitcher, inning, x) """

    media_q = """delete from media where rowid not in 
                (select max(rowid) from media 
                group by gameday_link, calendar_event_id, url) """

    pitch_q = """delete from pitch where rowid not in 
                (select max(rowid) from pitch 
                group by gameday_link, num, event_num) """

    player_q = """delete from player where rowid not in 
                  (select max(rowid) from player 
                  group by gameday_link, name, id, team_id) """

    po_q = """delete from po where rowid not in 
              (select max(rowid) from po 
              group by gameday_link, num, event_num) """

    runner_q = """delete from runner where rowid not in 
                  (select max(rowid) from runner 
                  group by gameday_link, num, event_num) """

    umpire_q = """delete from umpire where rowid not in 
                  (select max(rowid) from umpire 
                  group by gameday_link, id, name, position) """
                  
    count_q = """select count(rowid) from ?"""
    
    c.execute("""select count(rowid) from %s""" % 'game')
    rows = c.fetchall()[0][0]
    print('Rows in game before trimming: %i' % rows)
    
    for table, query in zip(('game', 'coach', 'player', 'umpire',
                             'hip', 'atbat', 'action', 'pitch', 'po', 'runner'),
                            (game_q, coach_q, player_q,  umpire_q, 
                             hip_q, atbat_q, action_q, pitch_q, po_q, runner_q)):
        c.execute("""select count(rowid) from %s""" % table)
        rows = c.fetchall()[0][0]
        print(table, rows, end=' ... ') 
        c.execute(query)
        con_sql.commit()
        c.execute("""select count(rowid) from %s""" % table)
        rows = c.fetchall()[0][0]
        print(rows) 
        
    con_sql.close()
    
    
    
    