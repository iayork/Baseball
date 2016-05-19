"""Various utility functions for baseball: SQL connections, SQL database calls

get_con(year, dbFolder="/Users/iayork/Documents/Baseball/PitchFX", db=False):
    dbFolder default="/Users/iayork/Documents/Baseball/PitchFX"
    
get_pitchab(con, reg): 
    Get everything from pitch and atbat, merge on gameday_link + num
    usage: get_pitchab(con, reg=True)
    set "reg=False" to get spring training, all-star, post-season games
    
get_pitchab_for_pitcher(pitcher_name, con, reg):  
    Get everything from pitch and atbat for a specific pitcher, 
    merge on gameday_link + num
    usage: get_pitchab_for_pitcher(pitcher_name, con, reg=True)
    set "reg=False" to get spring training, all-star, post-season games
    
get_bbref_pitch(url): 
    returns a pandas dataframe containing bbref gameday info 
    usage get_bbref(url)
    
bbref_date_to_gdl_date(bbref_date, year):
    take date in format "Apr 8" or "Jul 7(1)" and convert to "04-08-15" format
    usage: bbref_date_to_gdl_date(bbref_date, year)
    year default = 2015
    
convert_bbref_ip(s):
    convert series containing innings pitched in ".1", ".2" format 
    to ".33", ".67" format 
    
pitch_abbrs():
    A dict of standard abbreviations for pitch types 
"""

import pandas as pd
import sqlite3 as sql
import os.path
 
    
def get_con(year, dbFolder="/Users/iayork/Documents/Baseball/PitchFX", db=False):
    """ dbFolder default="/Users/iayork/Documents/Baseball/PitchFX" """
    if not db:
        db = 'pitchfx%s.db' % year
    
    print(os.path.join(dbFolder, db))
    return  sql.connect(os.path.join(dbFolder, db))   
    
        
def get_pitchab(con, reg=True):
    """ 
    Get everything from pitch and atbat, merge on gameday_link + num
    usage: get_pitchab(con, reg=True)
    set "reg=False" to get spring training, all-star, post-season games
    """
    atbat = pd.read_sql("select * from atbat ", con)
    pitch = pd.read_sql("select * from pitch ", con)
    pitchab = pitch.merge(atbat, on=['gameday_link','num'], suffixes=('', '_duplicate_delete'))

    if reg:
        game_sql = """select gameday_link from game where game_type="R" """
        reg_gdls_df = pd.read_sql(game_sql, con) 
        reg_gdls = ['gid_%s' % x for x in reg_gdls_df['gameday_link'].values]
        pitchab = pitchab[pitchab['gameday_link'].isin(reg_gdls)]
        
    drop_cols = [x for x in pitchab.columns if '_duplicate_delete' in x]
    for param in ('break_angle', 'break_length','break_y'):
        pitchab[param] = pd.to_numeric(pitchab[param]) 
    return pitchab.drop(drop_cols, axis=1)
    
    
def get_pitchab_for_pitcher(pitcher_name, con, reg=True): 
    """
    Get everything from pitch and atbat for a specific pitcher, 
    merge on gameday_link + num
    usage: get_pitchab_for_pitcher(pitcher_name, con, reg=True)
    set "reg=False" to get spring training, all-star, post-season games
    """

    atbat_sql = """select * from atbat where pitcher_name = "%s" """ % pitcher_name

    pitch_sql = """select * from pitch where gameday_link in 
    (select gameday_link from atbat where pitcher_name = "%s") """ % pitcher_name

    atbat = pd.read_sql(atbat_sql, con)
    pitch = pd.read_sql(pitch_sql, con)

    pitchab = pitch.merge(atbat, on=['gameday_link','num']) 
    pitchab.dropna(subset=['px',], inplace=True)

    if reg:
        game_sql = """select gameday_link from game where game_type="R" """
        reg_gdls_df = pd.read_sql(game_sql, con) 
        reg_gdls = ['gid_%s' % x for x in reg_gdls_df['gameday_link'].values]
        pitchab = pitchab[pitchab['gameday_link'].isin(reg_gdls)]
    for param in ('break_angle', 'break_length','break_y'):
        pitchab[param] = pd.to_numeric(pitchab[param]) 
    return pitchab  

    
def bbref_date_to_gdl_date(bbref_date, year):
    """ 
    take date in format "Apr 8" or "Jul 7(1)" and convert to "04-08-15" format
    usage: bbref_date_to_gdl_date(bbref_date, year)
    year default = 2015
    """
    dateD = {'Mar':3, 
             'Apr':4,
             'May':5,
             'Jun':6,
             'Jul':7,
             'Aug':8,
             'Sep':9,
             'Oct':10,
             'Nov':11}
    if len(str(year)) == 4:
        year = str(year)[-2:]
             
    new_date = '%02d-%02d-%s' % (dateD[bbref_date.split()[0]],
                                 int(bbref_date.split()[-1].split('(')[0]),
                                 year)
    return new_date
    
    
def get_bbref_pitch(url, year=2015):
    """ 
    returns a pandas dataframe containing bbref info (not all numeric?)
    usage get_bbref(url)
    """
    
    import Baseball
    import requests
    from bs4 import BeautifulSoup 
    
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    tbl = soup.find('table', id='pitching_gamelogs')
    bbref = pd.read_html(str(tbl))[0] 
    # Drop the last row = summary row
    bbref = bbref.iloc[:-1] 
    try:
        bbref = bbref[bbref['Gcar'] != 'Tm']
    except TypeError:
        pass 
    bbref = bbref.dropna(subset=['Gcar',], axis=0)
    for param in bbref.columns:
        bbref[param] = pd.to_numeric(bbref[param], errors='ignore')
    
    bbref['GDL_Date'] = bbref['Date'].apply(lambda x:bbref_date_to_gdl_date(x, year))
    bbref['IP'] = bbref['IP'].apply(convert_bbref_ip)
    
    bbref['WHIP'] = Baseball.get_whip(bbref)
    bbref['ERIP'] = Baseball.get_erip(bbref)
    
        
    return bbref 
    
def get_bbref_bat(url, year=2015):
    from bs4 import BeautifulSoup
    import requests 
    
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'lxml') 
    tbl = soup.find('table', id='batting_gamelogs')
    bbref = pd.read_html(str(tbl))[0] 
    # Drop the last row = summary row
    bbref = bbref.iloc[:-1] 
    try:
        bbref = bbref[~((bbref['Gcar'].str.contains('Tm')) |
                       (bbref['Gcar'].str.contains('Gcar')))]
    except TypeError:
        pass 
    bbref = bbref.dropna(subset=['Gcar',], axis=0)
    for param in bbref.columns:
        bbref[param] = pd.to_numeric(bbref[param], errors='ignore')
    
    bbref['GDL_Date'] = bbref['Date'].apply(lambda x:Baseball.bbref_date_to_gdl_date(x, year)) 
    return (bbref) 


def gdl_to_date(gdl): 
    # Takes gameday_link and returns a date as a string like 05-01-16
    y, m, d = (gdl.split('_')[1], gdl.split('_')[2], gdl.split('_')[3])
    return ('%s-%s-%s' % (m, d, y[-2:]))
    
def gdl_to_datetime(x):
    # Takes a gameday_link and returns a date as a datetime
    return pd.to_datetime(gdl_to_date(x), format='%m-%d-%y')
                             
    
def convert_bbref_ip(x):
    """ 
    convert series containing innings pitched in ".1", ".2" format 
    to ".33", ".67" format
    """  
    return round(int(x)) + (x-round(int(x)))/0.3

    
def pitch_abbrs():
    """A dict of standard abbreviations for pitch types """
    pitch_abbrs = {'FT':'Two-seam fastball',
                    'CH':'Changeup',
                    'SL':'Slider',
                    'FF':'Four-seam fastball',
                    'CU':'Curve',
                    'SI':'Sinker',
                    'FC':'Cut fastball',
                    'FS':'Split-finger fastball',
                    'FA':'Fastball',
                    'KC':'Knuckle curve',
                    'PO':'Pitchout',
                    'EP':'Eephus',
                    'IN':'Intentional ball',
                    'SC':'Screwball',
                    'FO':'Forkball',
                    'KN':'Knuckleball',
                    'UN':'Unknown',
                    'AB':'Automatic ball'}
    return pitch_abbrs
