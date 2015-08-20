#! /usr/bin/env python

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

from multiprocessing import Pool

dbFolder = "/Users/iayork/Documents/Baseball/"

class Parse_game():
    def __init__(self, gdl):
        self.gameday_url = gdl
        self.gdl = gdl.split('/')[-2:-1][0].strip('/')
        
    def parse_game(self):
        try:
            tree = etree.parse('%s%s' % (self.gameday_url, 'linescore.xml'))
            game = tree.getroot() 
            gameD = dict(game.attrib) 
        except:
            raise
            print (self.gdl, '%s%s' % (self.gameday_url, 'linescore.xml'))
            return False 
            
        try:
            tree = etree.parse('%s%s' % (self.gameday_url, 'game.xml'))
            game_gm = tree.getroot() 
            game_gmD = dict(game_gm.attrib) 
            gameD.update(game_gmD)
        except OSError: 
            pass   # Rainouts - "game" file be empty even though "linescore" exists  
        
        try:
            self.gameDF = self.gameDF.append(pd.DataFrame(gameD, index=(0,)))
        except AttributeError: 
            self.gameDF = pd.DataFrame(gameD, index=(0,))
            
        return True
            
    def parse_linescore(self):
        tree = etree.parse('%s%s' % (self.gameday_url,'rawboxscore.xml'))
        game = tree.getroot() 
        gameD = dict(game.attrib) 
        for linescore in tree.iterfind('linescore'):
            linescoreD = dict(linescore.attrib)
    
            for inning in linescore.iterfind('inning_line_score'):
                inningD = dict(inning.attrib)
                for side in ['home','away']:
                    try:
                        linescoreD['%s_%s' % (side, inningD['inning']) ] = inningD[side]
                    except KeyError:  # No info for home or away?
                        linescoreD['%s_%s' % (side, inningD['inning']) ] = np.nan
                        
        linescoreD['Gameday_link'] = self.gdl  
        try:
            self.linescoreDF = self.linescoreDF.append(pd.DataFrame(linescoreD, index=(0,)))
        except AttributeError: 
            self.linescoreDF = pd.DataFrame(linescoreD, index=(0,))
                        
        
    def parse_player_coach_umpires(self):
        tree = etree.parse('%s%s' % (self.gameday_url, 'players.xml'))
        for team in tree.iterfind('team'):
            for player in team.iterfind('player'):
                self.parse_player(player)
            for coach in team.iterfind('coach'):
                self.parse_coach(coach)
        for umpires in tree.iterfind('umpires'):
            for umpire in umpires.iterfind('umpire'):
                self.parse_umpire(umpire)
                
        self.parse_player_id_to_name()
        
    def parse_player_id_to_name(self):
        self.id_to_nameD = {x[0]:'%s %s' % (x[1], x[2])
                            for x in self.playerDF[['id','first','last']].values}
                
    def parse_player(self, player):
        playerD = dict(player.attrib) 
        playerD['Gameday_link'] = self.gdl
        try:
            self.playerDF = self.playerDF.append(pd.DataFrame(playerD, index=(0,)))
        except AttributeError: 
            self.playerDF = pd.DataFrame(playerD, index=(0,))
        
    def parse_coach(self, coach): 
        coachD = dict(coach.attrib) 
        coachD['Gameday_link'] = self.gdl
        try:
            self.coachDF = self.coachDF.append(pd.DataFrame(coachD, index=(0,)))
        except AttributeError: 
            self.coachDF = pd.DataFrame(coachD, index=(0,))
            
    def parse_umpire(self, umpire): 
        umpireD = dict(umpire.attrib) 
        umpireD['Gameday_link'] = self.gdl
        try:
            self.umpireDF = self.umpireDF.append(pd.DataFrame(umpireD, index=(0,)))
        except AttributeError: 
            self.umpireDF = pd.DataFrame(umpireD, index=(0,))
            
    def parse_hip(self):
        tree = etree.parse('%s%s' % (self.gameday_url,'inning/inning_hit.xml'))
        for hip in tree.iterfind('hip'):
            hipD = dict(hip.attrib) 
            hipD['Gameday_link'] = self.gdl
        try:
            self.hipDF = self.hipDF.append(pd.DataFrame(hipD, index=(0,)))
        except AttributeError: 
            try:
                self.hipDF = pd.DataFrame(hipD, index=(0,))
            except UnboundLocalError:  # No hits, return empty DF
                self.hipDF = pd.DataFrame()
        
    def parse_ab_pitch_runner_action_po(self):
        tree = etree.parse('%s%s' % (self.gameday_url,'inning/inning_all.xml'))  
        for inning in tree.iterfind('inning'): 
            self.inning_number = inning.attrib['num']
            for self.side in ('top','bottom'):
                for inning_side in inning.iterfind(self.side):
                    for ab in inning_side.iterfind('atbat'): 
                        self.parse_atbat(ab) 
                        self.parse_pitch(ab)
                        self.parse_runner(ab)
                        self.parse_po(ab)
                        
                    for act in inning_side.iterfind('action'):  
                        self.parse_action(act)
                        

    def parse_atbat(self, ab): 
        num = ab.attrib['num'] 
        abD = dict(ab.attrib) 
        abD['Inning'] = self.inning_number
        abD['inning_side'] = self.side
        abD['Gameday_link'] = self.gdl
        try:
            abD['pitcher_name'] = self.id_to_nameD[abD['pitcher']]
        except KeyError: # Name not known, search later
            abD['pitcher_name'] = np.nan
        try:
            abD['batter_name'] = self.id_to_nameD[abD['batter']]
        except KeyError: # Name not known, search later
            abD['batter_name'] = np.nan
        try:
            self.atbatDF = self.atbatDF.append(pd.DataFrame(abD, index=(0,)))
        except AttributeError: 
            self.atbatDF = pd.DataFrame(abD, index=(0,))

    def parse_pitch(self, ab):
        num = ab.attrib['num'] 
        for pt in ab.iterfind('pitch'):  
            pitchD = dict(pt.attrib)
            pitchD['num'] = num
            pitchD['Gameday_link'] = self.gdl
            if 'nasty' not in pitchD.keys():
                pitchD['nasty'] = np.nan
            try:
                self.pitchDF = self.pitchDF.append(pd.DataFrame(pitchD, index=(0,)))
            except AttributeError: 
                self.pitchDF = pd.DataFrame(pitchD, index=(0,)) 

    def parse_runner(self, ab):
        num = ab.attrib['num'] 
        for rn in ab.iterfind('runner'): 
            rnD = dict(rn.attrib) 
            rnD['num'] = num
            rnD['Gameday_link'] = self.gdl
            try:
                self.runnerDF = self.runnerDF.append(pd.DataFrame(rnD, index=(0,))) 
            except AttributeError: 
                self.runnerDF = pd.DataFrame(rnD, index=(0,))
                
    def parse_action(self, act):
            actD = dict(act.attrib) 
            actD['Gameday_link'] = self.gdl
            try:
                self.actionDF = self.actionDF.append(pd.DataFrame(actD, index=(0,))) 
            except AttributeError:
                self.actionDF = pd.DataFrame(actD, index=(0,))
                
    def parse_po(self, ab):
        num = ab.attrib['num'] 
        for po in ab.iterfind('po'):  
            poD = dict(po.attrib)
            poD['num'] = num
            poD['Gameday_link'] = self.gdl
            try:
                self.poDF = self.poDF.append(pd.DataFrame(poD, index=(0,)))
            except AttributeError: 
                self.poDF = pd.DataFrame(poD, index=(0,))
                
               
    def update_sql(self, df, name, con):
        """Update SQLite database; alter table to add new columns if needed"""
        try:
            df.to_sql(name, if_exists='append', con=con, index=False)  
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
                self.update_sql(df, name, con) 
            else:    
                try:
                    # "index=False" seems problematic some times - Why?
                    df.to_sql(name, if_exists='append', con=con)  
                except:
                    raise 
                    
    def get_gameDF(self):
        return self.gameDF
    
    def save_all(self, con):
        saved = True
        try:
            self.update_sql(self.gameDF, 'game', con)
        except Exception as exc:  
            # If game is broken, don't try to save remainder
            return exc.args[0]
        try:
            self.update_sql(self.linescoreDF, 'linescore', con)
        except Exception as exc:  
            saved = exc.args[0]
        try:
            self.update_sql(self.atbatDF, 'atbat', con)
        except Exception as exc:  
            saved = exc.args[0]
        try:
            self.update_sql(self.pitchDF, 'pitch', con)
        except Exception as exc:  
            saved = exc.args[0]
        try:
            self.update_sql(self.actionDF, 'action', con)
        except Exception as exc:  
            saved = exc.args[0]
        try:
            self.update_sql(self.runnerDF, 'runner', con)
        except Exception as exc:  
            saved = exc.args[0]
        try:
            self.update_sql(self.playerDF, 'player', con)
        except Exception as exc:  
            saved = exc.args[0]
        try:
            self.update_sql(self.coachDF, 'coach', con)
        except Exception as exc:  
            saved = exc.args[0]
        try:
            self.update_sql(self.hipDF, 'hip', con)
        except Exception as exc:  
            ssaved = exc.args[0]
        try:
            self.update_sql(self.umpireDF, 'umpire', con)
        except Exception as exc:  
            saved = exc.args[0]
        try:
            self.update_sql(self.poDF, 'po', con)
        except Exception as exc:  
            saved = exc.args[0]
            
        return saved

                
def parse_gdls(gdl):  
    """Download and parse game information"""
    parser = Parse_game(gdl)
    if parser.parse_game():
        #print(parser.get_gameDF()['gameday_link'].values[0] )
        try:
            parser.parse_linescore()
            parser.parse_player_coach_umpires()
            parser.parse_ab_pitch_runner_action_po()
            parser.parse_hip()
        except Exception as exc: 
            pass
            #bad_gdls.append(': '.join([gdl, exc.args[0]])) 
    else:
        pass
        #bad_gdls.append(': '.join([gdl, 'Failed to parse Game properly'])) 
        
    return parser 

def collect_gameday_urls(day_url): 
    """Collect gameday_links and pass them on for parsing"""
    r = requests.get(day_url)
    day = Soup(r.text)
    return ['%s%s' % (day_url, a.attrs['href']) for a in day.findAll('a') if 'gid_' in a.text]
                
            
def write_to_sqlite(results): 
    """Collect scraping/parsing results and write to SQLite"""
    
    con = sql.connect(os.path.join(dbFolder, 'PitchFX', 'MBL_Scrape_test_threaded.db'))
    for parser in results: 
        if parser.parse_game():
            saved = parser.save_gameDF()
            if saved:
                parser.save_all()
            
        else:
                bad_gdls[parser.gdl] = "Failed to parse correctly"

    con.commit()
    con.close() 

                
def get_ymd():
    """Ask for input on year, day/month to start with"""
    year_start = input('Year: ')
    try:
        month_start = input('Month: ')
    except:
        month_start = 1
    try:
        day_start = input('Day : ')
    except:
        day_start = 1
    return (year_start, month_start, day_start)

# ------------------- Start the main script ------------------------------------------
    
(year_start, month_start, day_start) = get_ymd() 

            
# ------------------- Set the base URL for the year ------

year_url = 'http://gd2.mlb.com/components/game/mlb/year_%s/' % year_start

# ------------------- Get URLs for all months in a year ------
r = requests.get(year_url)
year = Soup(r.text)
month_urls = [a.attrs['href'] for a in year.findAll('a') if 'month' in a.text] 
try:
    month_urls =[x for x in month_urls if int(x.replace('month_','').replace('/','')) >= int(month_start)]
except:
    pass

# ------------------- loop through months, get URLs for each day --
gameday_links = []

for month_url in month_urls: 
    bad_gdls = {}    # Collect a month's worth of bad gameday_links to print

    m = month_url.replace('month_', '').strip('/')
    r = requests.get('%s%s' % (year_url, month_url))
    month = Soup(r.text)
    day_links = [a.attrs['href'] for a in month.findAll('a') if 'day' in a.text] 

    if int(m) == int(month_start):
        day_urls = ['%s%s%s' % (year_url, month_url, day_link) for day_link in day_links 
                    if int(day_link.replace('day_','').strip('/')) >= int(day_start)] 
    else:
        day_urls = ['%s%s%s' % (year_url, month_url, day_link) for day_link in day_links]
    
    print ('Month %s: Collected %i day URLs; now collecting gameday_link URLs' % (m, len(day_urls)))

    # ------------------- Multiprocess - Collect gameday_links from days -------

    pool = Pool() 
    results = pool.map(collect_gameday_urls, day_urls) 
    pool.close() 
    for gdls in results:
        gameday_links.extend(gdls) 
    print('Collected %i gameday_link URLs; now parsing games' % len(gameday_links))
 
    # ------------------- Multiprocess - download & parse gamedays in groups of 50 -----
    for i in range(0,len(gameday_links),50):
        pool = Pool() 
        results = pool.map(parse_gdls, gameday_links[i:i+50]) 
        pool.close() 
        
        # ------------------- Multiprocess - write to SQL -----
    
        con = sql.connect(os.path.join(dbFolder, 'PitchFX', 'MBL_Scrape_test_threaded.db'))
        for parser in results: 
            saved = parser.save_all(con) 
            if saved != True:
                bad_gdls[parser.gdl] = saved
                #print (saved)
            

        con.commit()
        con.close() 
        
        
        if (i+50) > len(gameday_links):
            print ('Parsed and saved %i of %i games' % (len(gameday_links), len(gameday_links)))
        else:   
           print ('Parsed and saved %i of %i games' % ((i+50), len(gameday_links)))
    
    # ------------------- Check if all games are written to SQLite -------------

    con = sql.connect(os.path.join(dbFolder, 'PitchFX', 'MBL_Scrape_test_threaded.db'))
    c = con.cursor()
    c.execute("""Select distinct gameday_link from game""")
    sql_gdls = [x[0] for x in c.fetchall()]
    con.close()
    if set([x.strip('/').split('/')[-1].strip('gid_') for x in gameday_links]).issubset(set(sql_gdls)):
        print ("Saved %i games for month %s, %s" % ( len(gameday_links), m, year_start))
    else:
        print ("Not saved to SQL: ")
        print (set([x.strip('/').split('/')[-1].strip('gid_') for x in gameday_links]) - (set(sql_gdls)))
        

    if len(bad_gdls) > 0:
        print ('Bad GDLs: %s' % ('\n'.join(['%s (%s)' % (x[0], x[1]) for x in bad_gdls.items()] )))