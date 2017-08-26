"""
Class Parse_game:

Takes a base URL, e.g. 
        http://gd2.mlb.com/components/game/mlb/year_2015/month_08/day_23
    
    Completes the URL with the various xml files:
        game.xml
        linescore.xml
        inning/inning/xml
        players.xml
        rawboxscore.xml
        
    Parses each to yield dataframes for 
        game
        boxscore
        action
        runner
        player
        coach
        po
        umpire
        hip
        atbat
        pitch 
    
    Saves dataframes to SQL, making new tables or columns if necessary
    
    Functions:
    
    parse_game(self):
        General game information.  
        Linescore.xml provides most of the info; game.xml provides the rest
        Even for a rainout/cancelled game, there should be some game info
        Sometimes a gameday_link goes nowhere = no game info at all.  In this case,
        return False and don't try to collect any pitch, atbat, player, etc info 
        
            
    parse_boxscore(self):
        The inning-by-inning boxscore
        PITCHr/x does not download this, but it might be useful
        
    parse_player_coach_umpires(self):
        Contains player, coach, and umpire information for the game
        Generate 3 separate dataframes from the xml file
        Each dataframe parsed separately (parse_player, parse_coach, parse_umpire)
        
        
    parse_player_id_to_name(self):
        Takes the "player" subsection from the parsed "player.xml" file
                
    parse_player(self, player):
        
    parse_coach(self, coach): 
        Takes the "coach" subsection from the parsed "player.xml" file
            
    parse_umpire(self, umpire): 
        Takes the "umpire" subsection from the parsed "player.xml" file
            
    parse_hip(self):
        Hits
        
    parse_ab_pitch_runner_action_po(self):
        The inning/inning_all.xml files is broken into 5 dataframes:
            atbat
            pitch
            runner
            po
            action
        Each one is parsed separately from the original xml
                        
    parse_atbat(self, ab): 
        Parses the "atbat" subsection from the parsed "inning/inning_all.xml" file

    parse_pitch(self, ab):
        Parses the "pitch" subsection from the parsed "inning/inning_all.xml" file
        
    parse_runner(self, ab):
        Parses the "runner" subsection from the parsed "inning/inning_all.xml" file
                
    parse_action(self, act):
        Parses the "action" subsection from the parsed "inning/inning_all.xml" file
                
    parse_po(self, ab):
        Parses the "po" subsection from the parsed "inning/inning_all.xml" file
        This could be empty/non-existent if there were no pitchouts in the game
                
    get_gameDF(self):
        Return gameDF to check for minimal success 
    
"""

import lxml
import requests
from lxml import etree
from bs4 import BeautifulSoup as Soup

import pandas as pd
import numpy as np
import os.path 

dbFolder = "/Users/iayork/Documents/Baseball/"

class Parse_game():
    """ Class Parse_game takes a base URL, e.g. 
        http://gd2.mlb.com/components/game/mlb/year_2015/month_08/day_23
    
    Completes the URL with the various xml files:
        game.xml
        linescore.xml
        inning/inning/xml
        players.xml
        rawboxscore.xml
        
    Parses each to yield dataframes for 
        game
        boxscore
        action
        runner
        player
        coach
        po
        umpire
        hip
        atbat
        pitch 
        
    Usage:
    
    parser = Parse_game(gdl) 
    if parser.parse_game():  # parse_game returned True, therefore game exists 
        try:
            parser.parse_boxscore()                     # boxscoreDF
            parser.parse_player_coach_umpires()         # playerDF, 
                                                          coachDF, 
                                                          umpireDF
            parser.parse_ab_pitch_runner_action_po()    # atbatDF, 
                                                          pitchDF, 
                                                          runnerDF, 
                                                          poDF, 
                                                          actionDF 
            parser.parse_hip()                          # hipDF
    
    """
    
    # pitchRx starts with miniscoreboard.xml per date, which lists all the 
    # game information in one xml file. This seems to be where they get the 
    # gameday_link information (also media, which I don't collect)
    
    def __init__(self, gdl):
        self.gameday_url = gdl
        self.gdl = gdl.split('/')[-2:-1][0].strip('/')


    # ------------------- Parsing functions -------------------------
    def parse_game(self):
        """ General game information.  
            Linescore.xml provides most of the info; game.xml provides the rest
            Even for a rainout/cancelled game, there should be some game info
            Sometimes a gameday_link goes nowhere = no game info at all.  In this case,
            return False and don't try to collect any pitch, atbat, player, etc info 
        """
        # Start with linescore.xml and generate a dictionary of values gameD
        try:
            tree = etree.parse('%s%s' % (self.gameday_url, 'linescore.xml'))
            game = tree.getroot() 
            gameD = dict(game.attrib) 
        except:
            #raise
            #print (self.gdl, '%s%s' % (self.gameday_url, 'linescore.xml'))
            return False 
        
        # Then update gameD with extra information in game.xml
        try:
            tree = etree.parse('%s%s' % (self.gameday_url, 'game.xml'))
            game_gm = tree.getroot() 
            game_gmD = dict(game_gm.attrib) 
            gameD.update(game_gmD)
        except OSError: 
            pass   # Rainouts - "game" file can be empty even though "linescore" exists  
        
        # Convert dict to df self.gameDF
        try:
            self.gameDF = self.gameDF.append(pd.DataFrame(gameD, index=(0,)))
        except AttributeError: 
            # If no gameDF has been made, make one from gameD
            self.gameDF = pd.DataFrame(gameD, index=(0,))
        
        # Set up all the other dataframes as blanks 
        self.blank_dataframes()
        return True 
        
    def blank_dataframes(self):
        """Set up default dataframes with minimal information 
           (gameday_link) 
           Overwrite these if there is actual information
        """
        self.boxscoreDF = pd.DataFrame({'gameday_link':self.gdl}, index=(0,))
        self.pitchDF    = pd.DataFrame({'gameday_link':self.gdl}, index=(0,))
        self.runnerDF   = pd.DataFrame({'gameday_link':self.gdl}, index=(0,))
        self.poDF       = pd.DataFrame({'gameday_link':self.gdl}, index=(0,))
        self.actionDF   = pd.DataFrame({'gameday_link':self.gdl}, index=(0,))
        self.playerDF   = pd.DataFrame({'gameday_link':self.gdl}, index=(0,))
        self.coachDF    = pd.DataFrame({'gameday_link':self.gdl}, index=(0,))
        self.umpireDF   = pd.DataFrame({'gameday_link':self.gdl}, index=(0,))
        
        self.atbatDF    = pd.DataFrame()
        self.hipDF      = pd.DataFrame()
            
            
    def parse_boxscore(self):
        """ The inning-by-inning boxscore
            PitchRx does not download this, but it might be useful 
        """
        try:
            tree = etree.parse('%s%s' % (self.gameday_url,'rawboxscore.xml'))
            for boxscore in tree.iterfind('linescore'):
                boxscoreD = dict(boxscore.attrib)
                boxscoreD['gameday_link'] = self.gdl
                for inning in boxscore.iterfind('inning_line_score'):
                    inningD = dict(inning.attrib)
                    for side in ['home','away']:
                        try:
                            boxscoreD['%s_%s' % (side, inningD['inning']) ] = inningD[side]
                        except KeyError:  # No info for home or away?
                            boxscoreD['%s_%s' % (side, inningD['inning']) ] = np.nan
            
            self.boxscoreDF = pd.DataFrame(boxscoreD, index=(0,))
        except OSError: # No file found
            pass
        
    def parse_player_coach_umpires(self):
        """ Contains player, coach, and umpire information for the game
            Generate 3 separate dataframes from the xml file
            Each dataframe parsed separately (parse_player, parse_coach, parse_umpire)
            Indirectly yields playerDF, coachDF, umpireDF
        """
        try:
            tree = etree.parse('%s%s' % (self.gameday_url, 'players.xml'))
            for team in tree.iterfind('team'):
                for player in team.iterfind('player'):
                    self.parse_player(player)
                for coach in team.iterfind('coach'):
                    self.parse_coach(coach)
            for umpires in tree.iterfind('umpires'):
                for umpire in umpires.iterfind('umpire'):
                    self.parse_umpire(umpire)
                
            self.parse_player_id_to_name(self.playerDF)
        except OSError: # No file found
            pass
        
    def parse_player_id_to_name(self, df): 
        # TODO - Fix name lookups
        self.id_to_nameD = {x[0]:'%s %s' % (x[1], x[2])
                            for x in df[['id','first','last']].values}
                
    def parse_player(self, player):
        """ Called by parse_player_coach_umpires and yields playerDF""" 
        try:
            playerD = dict(player.attrib) 
            playerD['gameday_link'] = self.gdl
            self.playerDF = self.playerDF.append(pd.DataFrame(playerD, index=(0,)))
        except OSError: # No file found
            pass
        
    def parse_coach(self, coach): 
        """ Called by parse_player_coach_umpires and yields coachDF
            Takes the "coach" subsection from the parsed "player.xml" file
        """ 
        try:
            coachD = dict(coach.attrib) 
            coachD['gameday_link'] = self.gdl 
            self.coachDF = self.coachDF.append(pd.DataFrame(coachD, index=(0,)))
        except OSError: # No file found
            pass
            
    def parse_umpire(self, umpire): 
        """ Called by parse_player_coach_umpires and yields umpireDF
            Takes the "umpire" subsection from the parsed "player.xml" file
        """ 
        try:
            umpireD = dict(umpire.attrib) 
            umpireD['gameday_link'] = self.gdl 
            self.umpireDF = self.umpireDF.append(pd.DataFrame(umpireD, index=(0,)))
        except OSError: 
            pass
            
    def parse_hip(self):
        """ Hits
        """ 
        try:
            tree = etree.parse('%s%s' % (self.gameday_url,'inning/inning_hit.xml')) 
            if len(tree.findall('hip')) == 0:  #no-hitter?
                self.hipDF = pd.DataFrame({'gameday_link': self.gdl}, index=(0,))
            for hip in tree.iterfind('hip'):
                hipD = dict(hip.attrib) 
                self.hipDF = self.hipDF.append(pd.DataFrame(hipD, index=(0,)))
        except OSError: # No file found
            self.hipDF = pd.DataFrame({'gameday_link': self.gdl}, index=(0,))
        
    def parse_ab_pitch_runner_action_po(self):
        """ The inning/inning_all.xml files is broken into 5 dataframes:
            atbat
            pitch
            runner
            po
            action
            Each one is parsed separately out of the original xml
        """
        try:
            tree = etree.parse('%s%s' % (self.gameday_url,'inning/inning_all.xml'))  
            for inning in tree.iterfind('inning'): 
                inning_number = inning.attrib['num']
                for side in ('top','bottom'):
                    for inning_side in inning.iterfind(side):
                        for ab in inning_side.iterfind('atbat'):  
                            self.parse_atbat(ab, inning_number, side) 
                            self.parse_pitch(ab)
                            self.parse_runner(ab)
                            self.parse_po(ab)
                        
                        for act in inning_side.iterfind('action'):  
                            self.parse_action(act)
        except OSError: # No file found
            pass
                        
    def parse_atbat(self, ab, inning_number, side): 
        """ Parses the "atbat" subsection from the parsed "inning/inning_all.xml" file
        """
        num = ab.attrib['num'] 
        abD = dict(ab.attrib) 
        abD['Inning'] = inning_number
        abD['inning_side'] = side
        abD['gameday_link'] = self.gdl
        try:
            abD['pitcher_name'] = self.id_to_nameD[abD['pitcher']]
        except KeyError: # Name not known, search later
            abD['pitcher_name'] = np.nan
        try:
            abD['batter_name'] = self.id_to_nameD[abD['batter']]
        except KeyError: # Name not known, search later
            abD['batter_name'] = np.nan
        self.atbatDF = self.atbatDF.append(pd.DataFrame(abD, index=(0,)))

    def parse_pitch(self, ab):
        """ Parses the "pitch" subsection from the parsed "inning/inning_all.xml" file
        """
        num = ab.attrib['num']  
        for pt in ab.iterfind('pitch'):  
            pitchD = dict(pt.attrib)
            pitchD['num'] = num
            pitchD['gameday_link'] = self.gdl 
            if 'nasty' not in pitchD.keys():
                pitchD['nasty'] = np.nan
            self.pitchDF = self.pitchDF.append(pd.DataFrame(pitchD, index=(0,)))

    def parse_runner(self, ab):
        """ Parses the "runner" subsection from the parsed "inning/inning_all.xml" file
        """
        num = ab.attrib['num'] 
        for rn in ab.iterfind('runner'): 
            rnD = dict(rn.attrib) 
            rnD['num'] = num
            rnD['gameday_link'] = self.gdl
            self.runnerDF = self.runnerDF.append(pd.DataFrame(rnD, index=(0,))) 
                
    def parse_action(self, act):
        """ Parses the "action" subsection from the parsed "inning/inning_all.xml" file"""
        actD = dict(act.attrib) 
        actD['gameday_link'] = self.gdl
        self.actionDF = pd.DataFrame(actD, index=(0,))
                
    def parse_po(self, ab):
        """ Parses the "po" subsection from the parsed "inning/inning_all.xml" file
            This could be empty/non-existent if there were no pitchouts in the game
        """ 
        num = ab.attrib['num'] 
        if len(ab.findall('po')) == 0:  #no-hitter?
            self.poDF = pd.DataFrame({'num':num,'gameday_link':self.gdl}, index=(0,))
        else: 
            for po in ab.iterfind('po'):  
                poD = dict(po.attrib)
                poD['num'] = num
                poD['gameday_link'] = self.gdl 
                self.poDF = self.poDF.append(pd.DataFrame(poD, index=(0,)))
                

    def get_gameDF(self):
        """ Return gameDF to check for minimal success 
        """
        try:
            return self.gameDF
        except AttributeError:
            return False
        
    def get_dataframes(self): 
        return {'game':     self.gameDF, 
                'boxscore': self.boxscoreDF, 
                'player':   self.playerDF, 
                'coach':    self.coachDF, 
                'umpire':   self.umpireDF, 
                'atbat':    self.atbatDF, 
                'pitch':    self.pitchDF, 
                'runner':   self.runnerDF, 
                'po':       self.poDF, 
                'action':   self.actionDF, 
                'hip':      self.hipDF}
                

    # --------------End of Parse_game class ----------------