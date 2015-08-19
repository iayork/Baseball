#! /usr/bin/env python

import lxml
import requests
from lxml import etree
from bs4 import BeautifulSoup as Soup

import pandas as pd
import numpy as np
import os.path
import sys

import sqlite3 as sql
from sqlite3 import OperationalError
import pandas.io.sql as pdsql 


class Parse_game():
    def __init__(self, gdl):
        self.gdl = gdl 
        
    def parse_game(self):
        try:
            tree = etree.parse('%s%s%s%s%s' % (year_url, month_url, day_url, gdl, 
                                               'game.xml'))
            game = tree.getroot() 
            gameD = dict(game.attrib) 
        except:
            return False
            
        try:
            tree = etree.parse('%s%s%s%s%s' % (year_url, month_url, day_url, gdl,
                                               'linescore.xml'))
            game_ls = tree.getroot() 
            game_lsD = dict(game_ls.attrib) 
        except:
            return False 
        gameD.update(game_lsD) 
        
        try:
            self.gameDF = self.gameDF.append(pd.DataFrame(gameD, index=(0,)))
        except AttributeError: 
            self.gameDF = pd.DataFrame(gameD, index=(0,))
            
        return True
            
    def parse_linescore(self):
        tree = etree.parse('%s%s%s%s%s' % (year_url, month_url, day_url, gdl, 
                                           'rawboxscore.xml'))
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
                        
        linescoreD['Gameday_link'] = self.gdl.strip('/')     
        try:
            self.linescoreDF = self.linescoreDF.append(pd.DataFrame(linescoreD, index=(0,)))
        except AttributeError: 
            self.linescoreDF = pd.DataFrame(linescoreD, index=(0,))
                        
        
    def parse_player_coach_umpires(self):
        tree = etree.parse('%s%s%s%s%s' % (year_url, month_url, day_url, gdl, 
                                           'players.xml'))
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
        playerD['Gameday_link'] = self.gdl.strip('/')
        try:
            self.playerDF = self.playerDF.append(pd.DataFrame(playerD, index=(0,)))
        except AttributeError: 
            self.playerDF = pd.DataFrame(playerD, index=(0,))
        
    def parse_coach(self, coach): 
        coachD = dict(coach.attrib) 
        coachD['Gameday_link'] = self.gdl.strip('/')
        try:
            self.coachDF = self.coachDF.append(pd.DataFrame(coachD, index=(0,)))
        except AttributeError: 
            self.coachDF = pd.DataFrame(coachD, index=(0,))
            
    def parse_umpire(self, umpire): 
        umpireD = dict(umpire.attrib) 
        umpireD['Gameday_link'] = self.gdl.strip('/')
        try:
            self.umpireDF = self.umpireDF.append(pd.DataFrame(umpireD, index=(0,)))
        except AttributeError: 
            self.umpireDF = pd.DataFrame(umpireD, index=(0,))
            
    def parse_hip(self):
        tree = etree.parse('%s%s%s%s%s' % (year_url, month_url, day_url, gdl, 
                                               'inning/inning_hit.xml'))
        for hip in tree.iterfind('hip'):
            hipD = dict(hip.attrib) 
            hipD['Gameday_link'] = self.gdl.strip('/')
        try:
            self.hipDF = self.hipDF.append(pd.DataFrame(hipD, index=(0,)))
        except AttributeError: 
            try:
                self.hipDF = pd.DataFrame(hipD, index=(0,))
            except UnboundLocalError:  # No hits, return empty DF
                self.hipDF = pd.DataFrame()
        
    def parse_ab_pitch_runner_action_po(self):
        tree = etree.parse('%s%s%s%s%s' % (year_url, month_url, day_url, gdl,
                                           'inning/inning_all.xml')) 
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
        abD['Side'] = self.side
        abD['Gameday_link'] = self.gdl.strip('/')
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
            pitchD['Gameday_link'] = self.gdl.strip('/')
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
            rnD['Gameday_link'] = self.gdl.strip('/')
            try:
                self.runnerDF = self.runnerDF.append(pd.DataFrame(rnD, index=(0,))) 
            except AttributeError: 
                self.runnerDF = pd.DataFrame(rnD, index=(0,))
                
    def parse_action(self, act):
            actD = dict(act.attrib) 
            actD['Gameday_link'] = self.gdl.strip('/')
            try:
                self.actionDF = self.actionDF.append(pd.DataFrame(actD, index=(0,))) 
            except AttributeError:
                self.actionDF = pd.DataFrame(actD, index=(0,))
                
    def parse_po(self, ab):
        num = ab.attrib['num'] 
        for po in ab.iterfind('po'):  
            poD = dict(po.attrib)
            poD['num'] = num
            poD['Gameday_link'] = self.gdl.strip('/')
            try:
                self.poDF = self.poDF.append(pd.DataFrame(poD, index=(0,)))
            except AttributeError: 
                self.poDF = pd.DataFrame(poD, index=(0,))
                
    def get_gameDF(self):
        return self.gameDF
    
    def get_linescoreDF(self):
        return self.linescoreDF
    
    def get_atbatDF(self):
        return self.atbatDF
                
    def get_pitchDF(self):
        return self.pitchDF
                
    def  get_actionDF(self):
        try:
            return self.actionDF
        except AttributeError: # No actions in the game, return an empty dataframe
            return pd.DataFrame()
                
    def get_runnerDF(self):
        return self.runnerDF
                
    def get_playerDF(self):
        return self.playerDF
                
    def  get_coachDF(self):
        return self.coachDF
    
    def get_hipDF(self):
        return self.hipDF
    
    def get_umpireDF(self):
        return self.umpireDF
    
    def get_poDF(self):
        try:
            return self.poDF
        except AttributeError: # No pitchouts in the game, return an empty dataframe
            return pd.DataFrame()
            
def update_sql(df, name, con):
    try:
        df.to_sql(name, if_exists='append', con=con, index=False)  
    except OperationalError as oe: # No column exists?
        error_info = oe.args[0]
        if 'has no column named ' in error_info:
            table = error_info.split()[1]
            column_to_add = error_info.split()[-1]
            alter_table = 'ALTER TABLE %s ADD COLUMN "%s" TEXT;' % (table, column_to_add) 
            c = con.cursor()
            c.execute(alter_table)
            con.commit()
            update_sql(df, name, con)
        else:   
            #print ('Exception (not missing column)', error_info, flush=True)
            try:
                df.to_sql(name, if_exists='append', con=con)  
            except:
                raise 
                
def get_ymd():
    year = input('Year: ')
    month = input('Start month: ')
    day = input('Start day: ')
    return (year, month, day)
    
(year, month, day) = get_ymd()

                
# ------------------- Set the base URL for the year ------
dbFolder = "/Users/iayork/Documents/Baseball/"

year_url = 'http://gd2.mlb.com/components/game/mlb/year_%s/' % year

# ------------------- Get URLs for all months in a year ------
r = requests.get(year_url)
year = Soup(r.text)
month_urls = [a.attrs['href'] for a in year.findAll('a') if 'month' in a.text] 
try:
    month_urls =[x for x in month_urls 
                 if int(x.replace('month_','').replace('/','')) >= int(month)]
except:
    pass
    

# ------------------- loop through months, get URLs for each day --
for month_url in month_urls: 
    bad_gdls = []    # Collect a month's worth of bad gameday_links to print
    print(month_url.replace('month_', '').strip('/'), end = ': ', flush=True)
    r = requests.get('%s%s' % (year_url, month_url))
    month = Soup(r.text)
    day_urls = [a.attrs['href'] for a in month.findAll('a') if 'day' in a.text] 
    try:
        day_urls =[x for x in day_urls 
                     if int(x.replace('day_','').replace('/','')) >= int(day)]
    except:
        pass 

    # ------------------- loop through days -------------------
    for day_url in day_urls:
        print(day_url.replace('day_', '').strip('/'), end = ' ', flush=True)
        r = requests.get('%s%s%s' % (year_url, month_url, day_url))
        day = Soup(r.text)
        gameDF = pd.DataFrame()
    
        # ------------------- Initialize blank dataframes -------------------
        linescoreDF = pd.DataFrame()

        atbatDF = pd.DataFrame()
        pitchDF = pd.DataFrame()
        actionDF = pd.DataFrame()
        runnerDF = pd.DataFrame()
        poDF = pd.DataFrame()

        playerDF = pd.DataFrame()
        coachDF = pd.DataFrame()

        hipDF = pd.DataFrame()
        umpireDF = pd.DataFrame()

        # 'gamecenter.xml' has media info if we want to collect that at some point
        # 'miniscoreboard.xml' has some game/post-game info but most is covered in 'game.xml' 
    
        # ------------------- Get gameday_links -------------------

        gameday_links = [a.attrs['href'] for a in day.findAll('a') if 'gid_' in a.text]

        # ------------------- loop through Gamedays, parse out game data ----
        for gdl in gameday_links:
            parser = Parse_game(gdl)
            if parser.parse_game():
                gameDF = gameDF.append(parser.get_gameDF())
                try:
                    parser.parse_linescore()

                    parser.parse_player_coach_umpires()
                    parser.parse_ab_pitch_runner_action_po()
                    parser.parse_hip()
                
                    linescoreDF = linescoreDF.append(parser.get_linescoreDF())
                    atbatDF = atbatDF.append(parser.get_atbatDF())
                    pitchDF = pitchDF.append(parser.get_pitchDF())
                    actionDF = actionDF.append(parser.get_actionDF())
                    runnerDF = runnerDF.append(parser.get_runnerDF())

                    playerDF = playerDF.append(parser.get_playerDF())
                    coachDF = coachDF.append(parser.get_coachDF())
                    umpireDF = umpireDF.append(parser.get_umpireDF())
                    hipDF = hipDF.append(parser.get_hipDF())
                    poDF = poDF.append(parser.get_poDF())
                except Exception as exc: 
                    bad_gdls.append(': '.join([gdl, exc.args[0]])) 
            else:
                bad_gdls.append(': '.join([gdl, 'Failed to parse Game properly']))

    
        # ------------------- Write each day's info to SQLite -------------------

        con = sql.connect(os.path.join(dbFolder, 'PitchFX', 'MBL_Scrape_test.db'))
        for df, name in zip([atbatDF, pitchDF, actionDF, runnerDF, linescoreDF, 
                             playerDF, coachDF, umpireDF, hipDF, gameDF],
                            ['atbat', 'pitch', 'action', 'runner', 'linescore',
                             'player', 'coach', 'umpire', 'hip', 'game']):
            try:
                update_sql(df, name, con)
            except:
                raise
            
        con.commit()
        con.close()
        
    print('\nCompleted month %s' % month_url.replace('month_', '').strip('/'), flush=True)
    if len(bad_gdls) > 0:
        print ('Bad GDLs: %s' % '\n'.join(bad_gdls))