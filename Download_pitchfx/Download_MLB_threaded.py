"""
Download pitchF/X files from MLB.com, save to SQLite
                
# ------------------- SQL functions -------------------------           
def update_sql(df, df_name, con):
    Update SQLite database; alter table to add new columns if needed
    

def write_info_to_sql(dict_of_dataframes):  
       
def remove_duplicate_rows()

def check_all_games_written(gameday_links):
        
# ------------User input for start/end --------------                
def get_ymd_from_input():
    Ask for input on year, day/month to start with
    

def get_month_urls(year_url, month_start, month_end): 
    
def get_day_urls(year_url, month_url, month_start, month_end, day_start, day_end):
    # TODO - Check if I should have put day_end instead of day_start in the month_end check
    
# -------------- Other functions-------------------------
    
def parse_gdls(gdl):  
    Download and parse game information
    

def collect_gameday_urls(day_url):  
    

# ======================= Main script ============================================
def main():   
    
main()
    Set the base URL for the year
    Get URLs for all months in a year
    loop through months, get URLs for each day
        Multiprocess - Collect gameday_links from days
        Multiprocess - download & parse gamedays in groups of 50
            Multiprocess - write to SQL
        Check if all games are written to SQLite
    Remove duplicate rows via pandas
    Save to SQLite
    
"""

import lxml
import requests
from lxml import etree
from bs4 import BeautifulSoup as Soup

import pandas as pd
import numpy as np
import os.path
from datetime import datetime
import sys

import sqlite3 as sql
from sqlite3 import OperationalError
import pandas.io.sql as pdsql 
from pandas.io.sql import DatabaseError

from multiprocessing import Pool

from Parse_game import Parse_game



dbFolder = "/Users/iayork/Documents/Baseball/"

# ------------------- SQL functions -------------------------           
def write_info_to_sql(dict_of_dataframes, sql_db):  
    con = sql.connect(os.path.join(dbFolder, 'PitchFX', sql_db))
    for df_name, df in dict_of_dataframes.items():  
        ### XXX CHECK - does df_name, df work properly from .items()
        try:
            update_sql(df, df_name, con)
        except Exception as exc:  
            # If game is broken, don't try to save any more data
            # TODO: Depending on exception, just add the game to list of bad games
            # and continue.  There are legit reasons for empty games
            raise  
         
            #if saved != True:
            #    bad_gdls[parser.gdl] = saved
            #    print (saved)
    con.commit()
    con.close()  

       
def update_sql(df, df_name, con):
    """Update SQLite database; alter table to add new columns if needed""" 
    # If table already exists, check for columns in df not in sql
    check_table = """SELECT name FROM sqlite_master WHERE type='table' AND name='%s' """
    c = con.cursor()
    c.execute(check_table % df_name)
    if c.fetchone() is not None:
        c.execute('select * from %s' % df_name)
        sql_cols = [x[0] for x in c.description]
        if len(set(df.columns) - set(sql_cols)) > 0:
            # Add missing columns if necessary
            for new_col in set(df.columns) - set(sql_cols):  
                alter_table = 'ALTER TABLE %s ADD COLUMN "%s" TEXT;' % (df_name, new_col) 
                c.execute(alter_table)  
        
    try:
        df.to_sql(df_name, if_exists='append', con=con, index=False) 
        con.commit() 
    except sql.OperationalError as oe: 
        con.commit()
        raise
    

def check_all_games_written(gameday_links, sql_db):
    # TODO: Save reason for failed games along with the failures
    con = sql.connect(os.path.join(dbFolder, 'PitchFX', sql_db))
    c = con.cursor()
    try:
        c.execute("""Select distinct gameday_link from game""")
        sql_gdls = [x[0] for x in c.fetchall()]
        con.close()
        if set([x.strip('/').split('/')[-1].strip('gid_') for x in gameday_links]).issubset(set(sql_gdls)):
            print ("Saved %i games" % ( len(gameday_links)))
        else:
            print ("Not saved to SQL: ")
            print (set([x.strip('/').split('/')[-1].strip('gid_') for x in gameday_links]) - 
                   (set(sql_gdls)))
    
    except sql.OperationalError:
        #print("CAUGHT OE")
        #sys.exit()
        pass
        #raise


def remove_duplicate_rows(sql_db):
    con = sql.connect(os.path.join(dbFolder, 'PitchFX', sql_db))
    for table in ('action', 'coach', 'hip', 'pitch', 'po', 'umpire', 
                  'atbat', 'game', 'boxscore', 'player', 'runner'):
        try:
            df = pd.read_sql("select * from %s" % table, con)
            df.drop_duplicates(inplace=True)
            df.to_sql(name=table, if_exists='replace', con=con)
        except (sql.OperationalError, DatabaseError):
            pass

# ------------User input for start/end --------------                
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
    day_links = [x for x in day_links if start_date <= convert_ymd_to_datetime(year, m, x.split('_')[-1].strip('/')) <= end_date]
    day_urls = ['%s%s%s' % (year_url, month_url, day_link) for day_link in day_links]
    
    print ('Month %s: Collected %i day URLs; now collecting gameday_link URLs' % (m, len(day_urls)))
    
    return day_urls 
    
def convert_ymd_to_datetime(y,m,d):
    return datetime.strptime('%s-%s-%s' % (y, m, d), '%Y-%m-%d')
    
# -------------- Other functions-------------------------
    
def parse_gdls(gdl):  
    """Download and parse game information"""
    parser = Parse_game(gdl) 
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
        return {} # Empty dict 
        #pass
        #bad_gdls.append(': '.join([gdl, 'Failed to parse Game properly'])) 
    

def collect_gameday_urls(day_url): 
    """Collect gameday_links and pass them on for parsing"""
    r = requests.get(day_url)
    day = Soup(r.text, 'lxml')
    return ['%s%s' % (day_url, a.attrs['href']) for a in day.findAll('a') if 'gid_' in a.text]


    

# ======================= Main script ============================================
def main():    
    (year, month_start, month_end, day_start, day_end, sql_db) = get_ymd_from_input() 
    start_date = convert_ymd_to_datetime(year, month_start, day_start)
    end_date = convert_ymd_to_datetime(year, month_end, day_end)
    
    assert end_date >= start_date, "End date can't be earlier than start date" 
    
    print ("Collecting games from %s-%s-%s to %s-%s-%s" % (month_start, day_start, year,
                                                          month_end, day_end, year))
            
    # Set the base URL for the year 
    year_url = 'http://gd2.mlb.com/components/game/mlb/year_%s/' % year

    # Get URLs for all months in a year
    month_urls = get_month_urls(year_url, month_start, month_end)

    # loop through months, get URLs for each day

    for month_url in month_urls: 
        bad_gdls = {}    # Collect a month's worth of bad gameday_links to print
        day_urls = get_day_urls(year_url, month_url, year, start_date, end_date) 

        # ------------------- Multiprocess - Collect gameday_links from days -------

        pool = Pool() 
        results = pool.map(collect_gameday_urls, day_urls) 
        pool.close() 
        
        gameday_links = []
        for gdls in results:
            gameday_links.extend(gdls) 
        print('Collected %i gameday_link URLs; now parsing games' % len(gameday_links))
 
        # ------------------- Multiprocess - Download & parse gamedays in groups of 50 -----
        if len(gameday_links) >= 0:
            for i in range(0,len(gameday_links),50):
                pool = Pool() 
                results = pool.map(parse_gdls, gameday_links[i:i+50]) 
                pool.close()  
                
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
                for result in results:
                    write_info_to_sql(result, sql_db)
                
                # Are we done?  Give feedback
                if (i+50) > len(gameday_links):
                    print ('Parsed and saved %i of %i games' % (len(gameday_links), len(gameday_links)))
                else:   
                   print ('Parsed and saved %i of %i games' % ((i+50), len(gameday_links)))
    
            # Check if all games are written to SQLite
            check_all_games_written(gameday_links, sql_db)

            if len(bad_gdls) > 0:
                print ('Bad GDLs: %s' % ('\n'.join(['%s (%s)' % (x[0], x[1]) for x in bad_gdls.items()] )))
            
        # ------ Remove duplicate rows via pandas ------------
        
        remove_duplicate_rows(sql_db)
        
            
if __name__ == "__main__":
    main()