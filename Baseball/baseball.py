"""
Functions for calculating pitching and batting stats and outcomes

pitch_pcts_per_game(df, ptypes):
    Pitch mix usage as percentages per game
    
get_whip(df):

get_erip(df):

get_gb(df):

get_balls(df, ptype):

get_outs(df, ptype):

get_called(df, ptype):

get_swinging(df, ptype):

get_fouls(df, ptype):

get_hits_pxpz(df, ptype=None): 

get_hits_DF(df, ptype=None):

def get_bases_per_pitch(df, ptype=None): 

"""

import pandas as pd
import sqlite3 as sql
import os.path

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

def get_whip(df):
    return ((df['H']) + (df['BB']))/(df['IP'])
    
def get_erip(df):
    return df['ER']/df['IP']

def get_gb(df):
    """Ground Ball Percentage (GB%) = Ground Balls / Balls in Play"""
    inplay = df[df['des'].str.contains('In play')]
    gb = inplay[(inplay['atbat_des'].str.contains('ground')) | (inplay['atbat_des'].str.contains('Ground'))]
    return len(gb)/len(inplay) * 100.0


def get_balls(df, ptype):
    df2 = df[((df['des'].str.contains('Ball')) |
              (df['des'].str.contains('Hit By Pitch')) |
              (df['des']=='Pitchout')) & (df['pitch_type']==ptype)]
    return (df2['px'].values, df2['pz'].values) 

def get_outs(df, ptype):
    p = df[df['pitch_type']==ptype]
    df2 = p[(p['des'].str.contains('In play, out')) |
            ((p['des'].str.contains('In play, no out')) & (p['event'].str.contains('out'))) | 
            ((p['des'].str.contains('In play, no out')) & (p['event'].str.contains('Pop Out'))) | 
            ((p['des'].str.contains('In play, no out')) & (p['event'].str.contains('Fielders Choice'))) | 
            ((p['des'].str.contains('In play, no out')) & (p['event'].str.contains('Error'))) | 
            ((p['des'].str.contains('In play, no out')) & (p['event'].str.contains('Sac Fly'))) |
            ((p['des'].str.contains('In play, no out')) & (p['event'].str.contains('Sac Bunt'))) |
            ((p['des'].str.contains('In play, no out')) & (p['event'].str.contains('nterference'))) |
            ((p['des'].str.contains('In play, no out')) & (p['event'].str.contains('Double Play'))) |
            ((p['des'].str.contains('In play, run')) & (p['event'].str.contains('out'))) | 
            ((p['des'].str.contains('In play, run')) & (p['event'].str.contains('Pop Out'))) | 
            ((p['des'].str.contains('In play, run')) & (p['event'].str.contains('Fielders Choice'))) | 
            ((p['des'].str.contains('In play, run')) & (p['event'].str.contains('Error'))) | 
            ((p['des'].str.contains('In play, run')) & (p['event'].str.contains('Sac Fly'))) |
            ((p['des'].str.contains('In play, run')) & (p['event'].str.contains('Sac Bunt'))) |
            ((p['des'].str.contains('In play, run')) & (p['event'].str.contains('nterference'))) |
            ((p['des'].str.contains('In play, run')) & (p['event'].str.contains('Double Play'))) ]
    return (df2['px'].values, df2['pz'].values)

def get_called(df, ptype):
    df2 = df[(df['des'].str.contains('Called Strike')) & (df['pitch_type']==ptype)]
    return (df2['px'].values, df2['pz'].values)

def get_swinging(df, ptype):
    df2 = df[((df['des'].str.contains('Swinging Strike')) |
              (df['des'].str.contains('Missed Bunt'))) & (df['pitch_type']==ptype)]
    return (df2['px'].values, df2['pz'].values)

def get_fouls(df, ptype):
    df2 = df[(df['des'].str.contains('Foul')) & (df['pitch_type']==ptype)]
    return (df2['px'].values, df2['pz'].values)

def get_hits_pxpz(df, ptype=None): 
    if ptype is None: 
        p = df.copy()
    else:
        p = df[df['pitch_type']==ptype]
    p2 = p[p['des'].str.contains('In play')]
    df2 = p2[(~p2['des'].str.contains('In play, out')) &
             (~p2['event'].str.contains('Grounded Into DP')) & 
             (~p2['event'].str.contains('out')) & 
             (~p2['event'].str.contains('Pop Out')) & 
             (~p2['event'].str.contains('Fielders Choice')) & 
             (~p2['event'].str.contains('Error')) & 
             (~p2['event'].str.contains('Sac Fly')) &
             (~p2['event'].str.contains('Sac Bunt')) &
             (~p2['event'].str.contains('Interference')) &
             (~p2['event'].str.contains('Double Play')) ] 
    df3 = p2[(p2['event']=='Single') | 
             (p2['event']=='Double') | 
             (p2['event']=='Triple') | 
             (p2['event']=='Home Run') ]

    #print(df3[['des','event']])
    return (df3['px'].values, df3['pz'].values)

def get_hits_DF(df, ptype=None): 
    if ptype is None: 
        p = df.copy()
    else:
        p = df[df['pitch_type']==ptype]
    p2 = p[p['des'].str.contains('In play')]
    hitsDF = p2[(p2['event']=='Single') | 
                (p2['event']=='Double') | 
                (p2['event']=='Triple') | 
                (p2['event']=='Home Run') ]

    return (hitsDF)

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
    hits = len(get_hits(p)[0])  
    hr = len(p[(p['des'].str.contains('In play')) & 
               (p['event']=='Home Run')])
    sf = len( p[(p['des'].str.contains('In play')) & (p['event'].str.contains('Sac Fly'))])
    #print (bip, hits, hr)

    return (hits-hr)/(bip-hr+sf)