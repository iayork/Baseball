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

import sqlite3 as sql
from sqlite3 import OperationalError
import pandas.io.sql as pdsql 
from pandas.io.sql import DatabaseError

from multiprocessing import Pool

from Parse_game import Parse_game



dbFolder = "/Users/iayork/Documents/Baseball/"

# ------------------- SQL functions -------------------------           
def update_sql(df, df_name, con):
    """Update SQLite database; alter table to add new columns if needed"""
    try:
        df.to_sql(df_name, if_exists='append', con=con, index=False)  
    except OperationalError as oe: # No column exists?
        error_info = oe.args[0]
        if 'has no column named ' in error_info:
            # Add the missing column to the table 
            table = error_info.split()[1]
            column_to_add = error_info.split()[-1]
            alter_table = 'ALTER TABLE %s ADD COLUMN "%s" TEXT;' % (table, column_to_add) 
            c = con.cursor()
            c.execute(alter_table)
            con.commit()
            # Having updated the table, start updating again
            update_sql(df, df_name, con) 
        else:    
            try:
                # "index=False" seems problematic some times - Why?
                # TODO - eliminate index that comes from dataframe?
                df.to_sql(name, if_exists='append', con=con)  
            except:
                raise 

def write_info_to_sql(dict_of_dataframes):  
    con = sql.connect(os.path.join(dbFolder, 'PitchFX', 'MBL_Scrape_test_threaded.db'))
    for df_name in dict_of_dataframes.keys(): 
        df = dict_of_dataframes[df_name]
        try:
            update_sql(df, df_name, con)
        except Exception as exc:  
            # If game is broken, don't try to save any more data
            # TODO: Depending on exception, just add the game to list of bad games
            # and continue.  There are legit reasons for empty games
            raise  
         
            if saved != True:
                bad_gdls[parser.gdl] = saved
                #print (saved)
    con.commit()
    con.close()  

       
def remove_duplicate_rows():
    
    con = sql.connect(os.path.join(dbFolder, 'PitchFX', 'MBL_Scrape_test_threaded.db'))
    for table in ('action', 'coach', 'hip', 'pitch', 'po', 'umpire', 
                  'atbat', 'game', 'boxscore', 'player', 'runner'):
        try:
            df = pd.read_sql("select * from %s" % table, con)
            print ('Table %s before removing duplicates is %i rows' % (table, len(df)))
            df.drop_duplicates(inplace=True)
            print ('Table %s after removing duplicates is %i rows' % (table, len(df)))
            df.to_sql(name=table, if_exists='replace', con=con)
        except (OperationalError, DatabaseError):
            pass

def check_all_games_written(gameday_links):
    con = sql.connect(os.path.join(dbFolder, 'PitchFX', 'MBL_Scrape_test_threaded.db'))
    c = con.cursor()
    try:
        c.execute("""Select distinct gameday_link from game""")
        sql_gdls = [x[0] for x in c.fetchall()]
        con.close()
        if set([x.strip('/').split('/')[-1].strip('gid_') for x in gameday_links]).issubset(set(sql_gdls)):
            print ("Saved %i games for month %s, %s" % ( len(gameday_links), m, year_start))
        else:
            print ("Not saved to SQL: ")
            print (set([x.strip('/').split('/')[-1].strip('gid_') for x in gameday_links]) - (set(sql_gdls)))
    
    except OperationalError:
        pass

# ------------User input for start/end --------------                
def get_ymd_from_input():
    """Ask for input on year, day/month to start with"""
    try:
        year_start = int(input('Year: '))
    except:
        year_start = 2015
    try:
        month_start = int(input('Start month: '))
    except:
        month_start = 1
    try:
        day_start = int(input('Start day : '))
    except:
        day_start = 1
    try:
        month_end = int(input('End month: '))
    except:
        month_end = 12
    try:
        day_end = int(input('End day : '))
    except:
        day_end = 31
    return (year_start, month_start, month_end, day_start, day_end)
    

def get_month_urls(year_url, month_start, month_end):  

    # ------------------- Get URLs for all months in a year ------
    r = requests.get(year_url)
    year = Soup(r.text, 'lxml')
    month_urls = [a.attrs['href'] for a in year.findAll('a') if 'month' in a.text] 
    # Only keep months between month_start and month_end
    month_urls = [x for x in month_urls if int(x.replace('month_','').replace('/','')) >= int(month_start)]
    month_urls = [x for x in month_urls if int(x.replace('month_','').replace('/','')) <= int(month_end)]
    return month_urls
    
def get_day_urls(year_url, month_url, month_start, month_end, day_start, day_end):
    # TODO - Check if I should have put day_end instead of day_start in the month_end check
    m = month_url.replace('month_', '').strip('/')
    r = requests.get('%s%s' % (year_url, month_url))
    month = Soup(r.text, 'lxml')
    day_links = [a.attrs['href'] for a in month.findAll('a') if 'day' in a.text] 
    day_urls = ['%s%s%s' % (year_url, month_url, day_link) for day_link in day_links]
    
    # only keep days between start and end
    if int(m) == int(month_start):
        day_urls = ['%s%s%s' % (year_url, month_url, day_link) for day_link in day_links 
                    if int(day_link.replace('day_','').strip('/')) >= int(day_start)]
    if int(m) == int(month_end): 
        day_urls = ['%s%s%s' % (year_url, month_url, day_link) for day_link in day_links 
                    if int(day_link.replace('day_','').strip('/')) >= int(day_start)] # day_end???
    
    print ('Month %s: Collected %i day URLs; now collecting gameday_link URLs' % (m, len(day_urls)))
    
    return day_urls 
    
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
            pass
            #bad_gdls.append(': '.join([gdl, exc.args[0]])) 
    else:
        pass
        #bad_gdls.append(': '.join([gdl, 'Failed to parse Game properly'])) 
        
    return parser.get_dataframes() # Returns a dictionary of df names : df
    

def collect_gameday_urls(day_url): 
    """Collect gameday_links and pass them on for parsing"""
    r = requests.get(day_url)
    day = Soup(r.text, 'lxml')
    return ['%s%s' % (day_url, a.attrs['href']) for a in day.findAll('a') if 'gid_' in a.text]


    

# ======================= Main script ============================================
def main():    
    (year_start, month_start, month_end, day_start, day_end) = get_ymd_from_input() 
    assert month_end >= month_start, "End month can't be earlier than start month"
    assert day_end >= day_start, "End day can't be earlier than start day" 
    
    print ("Collecting games from %s-%s-%s to %s-%s-%s" % (month_start, day_start, year_start,
                                                          month_end, day_end, year_start))

            
    # Set the base URL for the year 
    year_url = 'http://gd2.mlb.com/components/game/mlb/year_%s/' % year_start

    # Get URLs for all months in a year
    month_urls = get_month_urls(year_url, month_start, month_end)

    # loop through months, get URLs for each day

    for month_url in month_urls: 
        bad_gdls = {}    # Collect a month's worth of bad gameday_links to print
        day_urls = get_day_urls(year_url, month_url, month_start, month_end, day_start, day_end) 

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
                    write_info_to_sql(result)
                
                # Are we done?  Give feedback
                if (i+50) > len(gameday_links):
                    print ('Parsed and saved %i of %i games' % (len(gameday_links), len(gameday_links)))
                else:   
                   print ('Parsed and saved %i of %i games' % ((i+50), len(gameday_links)))
    
            # Check if all games are written to SQLite
            check_all_games_written(gameday_links)

            if len(bad_gdls) > 0:
                print ('Bad GDLs: %s' % ('\n'.join(['%s (%s)' % (x[0], x[1]) for x in bad_gdls.items()] )))
            
        # ------ Remove duplicate rows via pandas ------------
        
        remove_duplicate_rows()
        
            
if __name__ == "__main__":
    main()