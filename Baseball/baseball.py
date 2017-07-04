"""
Functions for calculating pitching and batting stats and outcomes 
    
def get_whip_from_bbref(df): 
def get_erip_from_bbref(df): 

def pitch_pcts_per_game(df, ptypes):
    #Pitch mix usage as percentages per game
    
def get_gb_from_pfx(df):
    # Ground Ball Percentage (GB%) = Ground Balls / Balls in Play 
    
#------Balls, strikes, fouls, swinging strikes, called strikes from PITCHf/x df----------   

def get_strikes_all(df):
    # swinging misses, fouls, hits, called strikes 
    
def get_balls(df):  
                             
def get_called_strikes(df): 
    
def get_hits(df):  
                               
def get_swings_all(df):
    # No called strikes or balls; swinging misses, fouls, hits 
    
def get_fouls(df): 
                               
def get_swinging_strikes(df):  
                               
def get_swinging_strikes_fouls(df):
    # Any swing that isn't in play, including swinging misses and fouls 
                               
def get_outs_in_play(df):
    # Any in-play event that isn't a hit (includes errors and sacrifices as outs) 
                    
def get_contact(df)
    
#----Get location of pitches that results in various events--------

def get_balls_px_pz(df, ptype=None):
def get_outs_px_pz(df, ptype=None): 
def get_called_strikes_px_pz(df, ptype=None):
def get_swinging_px_pz(df, ptype=None):
def get_fouls_px_pz(df, ptype=None):
def get_hits_px_pz(df, ptype=None):
    
#----Misc -------------

def get_bases_per_pitch(df, ptype=None):

def get_babip(df, ptype=None)



"""

import pandas as pd
import sqlite3 as sql
import os.path

def get_whip_from_bbref(df):
    return ((df['H']) + (df['BB']))/(df['IP'])
    
def get_erip_from_bbref(df):
    return df['ER']/df['IP']

def pitch_pcts_per_game(df, ptypes):
    """ Pitch mix usage as percentages per game"""
    usageD = {}
    for gdl in df['gameday_link'].unique():
        usageD[gdl] = {}
        gm = df[df['gameday_link']==gdl] 

        for ptype in ptypes:
            usageD[gdl][ptype] = len(gm[gm['pitch_type']==ptype])/len(gm)*100
    usageDF = pd.DataFrame(usageD).T
    usageDF['Dates'] = ['%s-%s-%s' % (x.split('_')[2], 
                       x.split('_')[3], 
                       x.split('_')[1][-2:]) for x in usageDF.index] 
    return usageDF

def get_gb_from_pfx(df):
    """Ground Ball Percentage (GB%) = Ground Balls / Balls in Play"""
    inplay = df[df['des'].str.contains('In play')]
    gb = inplay[(inplay['atbat_des'].str.contains('ground ball')) | 
                (inplay['atbat_des'].str.contains('grounds'))]
    return len(gb)/len(inplay) * 100.0


#------Balls, strikes, fouls, swinging strikes, called strikes from PITCHf/x df----------   

def get_strikes_all(df):
    # swinging misses, fouls, hits, called strikes
    balls = ('Ball', 'Hit By Pitch', 'Ball In Dirt', 'Pitchout',
             'Intent Ball', 'Automatic Ball')
    return df[~(df['des'].isin(balls))] 
    
def get_balls(df): 
    balls = ('Ball', 'Hit By Pitch', 'Ball In Dirt', 'Pitchout',
             'Intent Ball', 'Automatic Ball')
    return df[df['des'].isin(balls)]  
                             
def get_called_strikes(df):
    return df[df['des']=='Called Strike']  
    
def get_hits(df): 
    return df[(df['des'].str.contains('In play') ) & 
              (df['event'].isin(['Single','Double','Triple','Home Run']))]  
                               
def get_swings_all(df):
    # No called strikes or balls; swinging misses, fouls, hits
    return df[~(df['des'].isin(['Ball', 'Hit By Pitch', 'Ball In Dirt', 'Pitchout',
                                'Intent Ball', 'Automatic Ball', 'Called Strike']))] 
    
def get_fouls(df):
    fouls = ('Foul', 'Foul (Runner Going)', 'Foul Tip','Foul Bunt')
    fouls_in_des = df[(df['des'].isin(fouls))]
    return fouls_in_des
    # fouls in play 
    df[ (df['des']=='In play, out(s)') & 
        (df['atbat_des'].str.contains('foul'))][['des','atbat_des']]
                               
def get_swinging_strikes(df):
    swinging = ('Swinging Strike','Swinging Strike (Blocked)','Missed Bunt')
    return df[(df['des'].isin(swinging))] 
                               
def get_swinging_strikes_fouls(df):
    # Any swing that isn't in play, including swinging misses and fouls
    swings = Baseball.get_swinging_strikes(df)
    fouls = Baseball.get_fouls(df) 
    return swings.append(fouls)
    return contact
                               
def get_outs_in_play(df):
    # Any in-play event that isn't a hit (includes errors and sacrifices as outs)
    return df[ (df['des'].str.contains('In play') ) & 
               (~(df['event'].isin(['Single','Double','Triple','Home Run'])))] 
                    
def get_contact(df):
    # Any contact: Hits, fouls, in-play outs
    hits = Baseball.get_hits(df)
    fouls = Baseball.get_fouls(df)
    outs = Baseball.get_outs_in_play(df)
    contact = hits.append(fouls)
    contact = contact.append(outs)
    
    
#----Get location of pitches that results in various events--------

def get_balls_px_pz(df, ptype=None):
    df2 = Baseball.get_balls(df)
    if ptype:
        df2 = df2[df2['pitch_type']==ptype]
    return (df2['px'].values, df2['pz'].values) 

def get_outs_px_pz(df, ptype=None): 
    df2 = Baseball.get_outs_in_play(df)
    if ptype:
        df2 = df2[df2['pitch_type']==ptype]
    return (df2['px'].values, df2['pz'].values)

def get_called_strikes_px_pz(df, ptype=None):
    df2 = Baseball.get_called_strikes(df)
    if ptype:
        df2 = df2[df2['pitch_type']==ptype]
    return (df2['px'].values, df2['pz'].values)
    
def get_swinging_px_pz(df, ptype=None):
    df2 = Baseball.get_swinging_strikes(df)
    if ptype:
        df2 = df2[df2['pitch_type']==ptype]
    return (df2['px'].values, df2['pz'].values)

def get_fouls_px_pz(df, ptype=None):
    df2 = Baseball.get_fouls(df)
    if ptype:
        df2 = df2[df2['pitch_type']==ptype]
    return (df2['px'].values, df2['pz'].values)

def get_hits_px_pz(df, ptype=None): 
    df2 = Baseball.get_hits(df)
    if ptype:
        df2 = df2[df2['pitch_type']==ptype]
    return (df2['px'].values, df2['pz'].values)
    
#----Misc -------------

def get_bases_per_pitch(df, ptype=None): 
    if ptype is None: 
        p = df.copy()
    else:
        p = df[df['pitch_type']==ptype]
    if len(p) > 0:
        p2 = p[p['des'].str.contains('In play')]
        bases = (len(p2[p2['event']=='Single']) + 
                (2*len(p2[p2['event']=='Double'])) +
                (3*len(p2[p2['event']=='Triple'])) +
                (4*len(p2[p2['event']=='Home Run'])))
        bases_per_pitch = bases/len(p)
    else:
        bases_per_pitch = 0
    return (bases_per_pitch)

def get_babip(df, ptype=None):
    # BABIP = (H – HR)/(AB – K – HR + SF)
    # BABIP = (H-HR)/(BIP-HR)  

    if ptype is None:
        p = df.copy()
    else:
        p = df[df['pitch_type']==ptype]
    bip = len( p[(p['des'].str.contains('In play')) & (~p['event'].str.contains('Error'))])
    hits = len(Baseball.get_hits(p))  
    hr = len(p[(p['des'].str.contains('In play')) & 
               (p['event']=='Home Run')])
    sf = len( p[(p['des'].str.contains('In play')) & (p['event'].str.contains('Sac Fly'))])
    #print (bip, hits, hr)

    return (hits-hr)/(bip-hr+sf)