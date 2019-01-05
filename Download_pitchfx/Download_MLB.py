"""
Scrape MLB for pitchfx data

Usage:
python "/Users/iayork/Documents/Baseball/Baseball scripts/Download_pitchfx/Download_MLB.py"

"""

import lxml
import requests
from lxml import etree
from bs4 import BeautifulSoup as Soup

import pandas as pd
import numpy as np
import os, os.path
from datetime import datetime
import sys

from sqlalchemy import create_engine, inspect, select
from sqlalchemy.exc import OperationalError, InvalidRequestError
import sqlite3 as sql
#from sqlite3 import OperationalError
import pandas.io.sql as pdsql 
from pandas.io.sql import DatabaseError
from sqlalchemy import exc

from multiprocessing import Pool

from Parse_game import Parse_game
from Remove_duplicates import *

dbFolder = "/Users/iayork/Documents/Baseball/"

# ------------------- SQL functions ------------------------- 

def write_info_to_sql(dict_of_dataframes, sql_db, engine):  
    con = engine.connect()
    inspector = inspect(engine)
    try:
        for df_name, df in dict_of_dataframes.items(): 
            try:
                if df_name in inspector.get_table_names():
                    check_columns(df, df_name, sql_db, inspector)
                df.to_sql(df_name, if_exists='append', con=con, index=False)
            except AttributeError as exc:  # no df in dict 
                print('AttributeError: \t\t %s' % exc.args[0]) 
                #raise
                pass
            except OperationalError as exc: #exc.OperationalError as exc: 
                print('Operational error: \t\t %s' % exc.args[0]) 
                pass
            
                    # TODO: Depending on exception, add the game to list of bad games
                    # and continue.  There may be legit reasons for empty games
    except AttributeError:
        pass
    con.close() 
        
def check_columns(df, df_name, sql_db, inspector): 
    sql_cols = [x['name'] for x in inspector.get_columns(df_name)] 
    if len(set(df.columns) - set(sql_cols)) > 0:
        # Add missing columns if necessary  
        # TODO Re-use the sqlalchemy con if possible 
        con_sql = sql.connect(os.path.join(dbFolder, 'PitchFX', sql_db)) 
        for new_col in set(df.columns) - set(sql_cols):  
            alter_table = 'ALTER TABLE %s ADD COLUMN "%s" TEXT;' % (df_name, new_col) 
            con_sql.execute(alter_table)   
        con_sql.commit()
        con_sql.close()
    
def check_all_games_written(gameday_links, engine):
    # TODO: Save reason for failed games along with the failures
    gdls_to_write = [x.split('gid_')[-1].strip('/') for x in gameday_links]
    gdls_in_sb = set([r[0] for r in engine.execute('SELECT gameday_link FROM game')])
    if set(gdls_to_write).issubset(gdls_in_sb):
        print("All %i games in gameday links written to SQLite" % len(gameday_links))
    else:
        not_written = set(gdls_to_write) - gdls_in_sb
        print('Not written to SQLite:', '\n'.join(not_written))
        
def convert_cols_to_numeric(engine):
    print('Converting atbat columns to numeric')
    # TODO - Don't quit on non-existent tables
    con = engine.connect()
    try:
        atbat = pd.read_sql_table('atbat', con)
        for col in ('Inning', 'away_team_runs', 'home_team_runs', 'event_num', 'num','o', 's', 'b'):
            atbat[col] = pd.to_numeric(atbat[col])
        atbat.to_sql('atbat', if_exists='replace', con=con, index=False)
    except ValueError as exc:
        print('\t\tValueError:  %s' % exc.args[0]) 
        pass
    try:
        print('Converting pitch columns to numeric')
        pitch = pd.read_sql_table('pitch', con)
        for col in ('event_num', 'id', 'num', 
                    'sz_bot', 'sz_top','x', 'y', 
                    'pz', 'x0','ax', 'vy0', 'ay', 'z0','az','y0', 'px','vx0', 'vz0',
                    'pfx_x', 'pfx_z', 'break_angle', 'break_length', 'break_y', 
                    'spin_rate',  'spin_dir',
                    'end_speed', 'start_speed'):
            pitch[col] = pd.to_numeric(pitch[col])
        pitch.to_sql('pitch', if_exists='replace', con=con, index=False)
    except ValueError as exc:
        print('\t\tValueError:  %s' % exc.args[0]) 
        pass
    
    except InvalidRequestError as exc:  
        print('InvalidRequestError: \t\t %s' % exc.args[0]) 
        pass
    print('Finished converting columns to numeric')
    con.close()

# ------------User input for start/end --------------     
def get_gameday_links():
    (year, month_start, month_end, day_start, day_end, sql_db) = get_ymd_from_input() 
    start_date = convert_ymd_to_datetime(year, month_start, day_start)
    end_date = convert_ymd_to_datetime(year, month_end, day_end) 
    # Set the base URL for the year 
    year_url = 'http://gd2.mlb.com/components/game/mlb/year_%s/' % year

    # Get URLs for all months in a year
    month_urls = get_month_urls(year_url, month_start, month_end)

    assert end_date >= start_date, "End date can't be earlier than start date" 

    print ("Collecting games from %s-%s-%s to %s-%s-%s" % (month_start, day_start, year,
                                                          month_end, day_end, year))  

    # loop through months, get URLs for each day
    gameday_links = []
    bad_gdls = {}    # Collect a month's worth of bad gameday_links to print
    for month_url in month_urls: 
        day_urls = get_day_urls(year_url, month_url, year, start_date, end_date)  
        # ------------------- Multiprocess - Collect gameday_links from days -------
        with Pool() as pool:
            results = pool.map(collect_gameday_urls, day_urls)  
        
        for gdls in results: 
            gameday_links.extend(gdls)  
    return (sql_db, gameday_links) 
           
def get_ymd_from_input():
    """Ask for input on year, day/month to start with"""
    try:
        mdy = input("Start date in mm-dd-yyyy format: ")
        (m,d,y) = mdy.split('-')
        year = int(y)
        month_start = int(m)
        day_start = int(d)
    except:
        raise 
    try:
        today = pd.to_datetime('today').strftime("%m-%d-%Y")
        mdy = input("End date in mm-dd-yyyy format: ")
        (m,d,y) = mdy.split('-')
        year_end = int(y)
        month_end = int(m)
        day_end = int(d)
    except:
        raise 
    try:
        sql_db = input("SQL database: ")
    except:
        raise 
    assert year == year_end, "Can't collect more than one year at a time (%s, %s)" % (year, year_end)
    return (year, month_start, month_end, day_start, day_end, sql_db)
    

def get_month_urls(year_url, month_start, month_end):  
    # ------------------- Get URLs for all months in a year ------
    r = requests.get(year_url)
    year = Soup(r.text, 'lxml')
    month_urls = [a.attrs['href'] for a in year.findAll('a') if 'month' in a.text] 
    # Only keep months between month_start and month_end
    month_urls = [x for x in month_urls if int(x.replace('month_','').replace('/','')) >= int(month_start)]
    month_urls = [x for x in month_urls if int(x.replace('month_','').replace('/','')) <= int(month_end)]
    return month_urls
    
def get_day_urls(year_url, month_url, year, start_date, end_date): 
    m = month_url.replace('month_', '').strip('/')
    r = requests.get('%s%s' % (year_url, month_url))
    month = Soup(r.text, 'lxml')
    day_links = [a.attrs['href'] for a in month.findAll('a') if 'day' in a.text] 
    
    # Only keep dates that are between the start and end date
    day_links = [x.strip('/') for x in day_links if date_in_range(year, m, x, start_date, end_date) ] 
    day_urls = ['%s%s%s' % (year_url, month_url, day_link) for day_link in day_links]
    print ('Month %s: Collected %i day URLs; now collecting gameday_link URLs' % (m, len(day_urls)))
    
    return day_urls 
    
def convert_ymd_to_datetime(y,m,d):
    try:
        return datetime.strptime('%s-%s-%s' % (y, m, d), '%Y-%m-%d')
    except:
        print('Gameday url shows non-existent date %s-%s-%s; skip' % (m, d, y))
        return None
        
def date_in_range(year, m, x, start_date, end_date):
    date = convert_ymd_to_datetime(year, m, x.split('_')[-1].strip('/'))
    if date is not None:
        return (start_date <= date <= end_date)
    
# -------------- Other functions-------------------------
    
def parse_gdls(gdl):  
    """Download and parse game information""" 
    with Parse_game(gdl) as parser:   
        if parser.parse_game():  # parse_game returned True, therefore game exists  
            try:
                parser.parse_boxscore()  # Yields boxscoreDF
                parser.parse_player_coach_umpires()  # Yields playerDF, coachDF, umpireDF
                parser.parse_ab_pitch_runner_action_po() 
                # Yields atbatDF, pitchDF, runnerDF, poDF, actionDF
                parser.parse_hip() # Yields hipDF
            except Exception as exc: 
                raise 
                #bad_gdls.append(': '.join([gdl, exc.args[0]])) 
            return parser.get_dataframes() # Returns a dictionary of df names : df
     
        else:
            print('\t\t(No data)', gdl)
            return {} # Empty dict 
            #pass
            #bad_gdls.append(': '.join([gdl, 'Failed to parse Game properly'])) 
    
def collect_gameday_urls(day_url): 
    """Collect gameday_links and pass them on for parsing"""
    r = requests.get(day_url)
    day = Soup(r.text, 'lxml')
    return ['%s/%s/' % (day_url, a.attrs['href'].strip('/').split('/')[-1]) for a in day.findAll('a') if 'gid_' in a.text]

def download_parse_unpooled(gameday_links):
    # SHOULD BE ABLE TO DELETE THIS 
    print('Saving %i games' % len(gameday_links), end=' ... ')            
    for i in range(len(gameday_links)):
        gdl = gameday_links[i]
        result = parse_gdls(gdl)
        write_info_to_sql(result, sql_db)
        print(len(gameday_links)-1-i, end=' ... ')
    print ('Done parsing and saving games')
    
def download_parse_pooled(gameday_links, sql_db, engine, STEP = 8):
    # results are a list of dictionary of dataframes 
    #   {'game':    self.gameDF, 
    #   'boxscore': self.boxscoreDF, 
    #   'player':   self.playerDF, 
    #   'coach':    self.coachDF, 
    #   'umpire':   self.umpireDF, 
    #   'atbat':    self.atbatDF, 
    #   'pitch'     self.pitchDF, 
    #   'runner':   self.runnerDF, 
    #   'po':       self.poDF, 
    #   'action':   self.actionDF, 
    #   'hip':      self.hipDF} 
    
    with Pool(STEP) as pool:
        for i in range(0, len(gameday_links), 50): 
            gameday_links_slice = gameday_links[i:i+50]
            results = pool.map(parse_gdls, gameday_links_slice) 
            print('Saving games ... ', end='')  
            for result in results:  
                write_info_to_sql(result, sql_db, engine)
                del(result) 
            if i+50 > len(gameday_links):
                c = len(gameday_links)
            else:
                c = i+50
            print ('Parsed and saved %i of %i games' % (c, len(gameday_links)))
        
    print ('Finished parsing and saving %i games' % (len(gameday_links)))
    

# ======================= Main script ============================================
def main():    
    sql_db, gameday_links = get_gameday_links()
 
    # ------------------- Multiprocess - Download & parse gamedays in groups of 50 -----
    print('Collected %i gameday_link URLs; now parsing games' % len(gameday_links))
    
    engine = create_engine('sqlite:///%s' % os.path.join(dbFolder, 'PitchFX', sql_db)) 
    if len(gameday_links) >= 0: 
        #download_parse_unpooled(gameday_links)
        download_parse_pooled(gameday_links, sql_db, engine)
        
    # Convert to numeric
    convert_cols_to_numeric(engine)
        
    # Check if all games are written to SQLite
    check_all_games_written(gameday_links,engine)

    #if len(bad_gdls) > 0:
    #    print ('Bad GDLs: %s' % ('\n'.join(['%s (%s)' % (x[0], x[1]) for x in bad_gdls.items()] )))
            
        # ------ Remove duplicate rows via pandas ------------
        
    # remove_duplicate_rows(os.path.join(dbFolder, 'PitchFX', sql_db))
    
    engine.dispose()
        
            
if __name__ == "__main__":
    main()