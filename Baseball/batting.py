"""
Functions related to batting 

get_slg_in_box(strikes_in_box)
    Get slugging percent in a sub-region of the strike zone
    
    Input: dataframe containing strikes within a specific sub-region
    output: (total_bases, number_of_hits)

get_box_info(df)
    Takes a full pitchFX dataframe
    
    Breaks strike zone into sub-regions
    Finds the pitches in each subregion, calculates slg and hits in each
    Returns a dict containing 
            {'xs': (center of each box)
             'ys': (center of each box)
             'pitches_in_zone_pct': (Percent of all pitches that are in each box) 
             'slgs': (total bases per hit in box)
             'hits': (total hits in box)
             'hits_per_ptch': hits in box/pitches in box * percent of pitches in box 
             
    
def get_strikes(df) 

def get_hits(df)

def get_swings_all(df) 
                               
def get_swinging_strikes_fouls(df)
                               
def get_swinging_strikes(df)

#------Get OBP, SLG, OPS from a PITCHf/x dataframe----------
def get_atbats_pfx(df)

def get_slg_pfx(df) 

def get_obp_pfx(df)

def get_ops_pfx(df)

"""

import pandas as pd 
import numpy as np
import Baseball


ptype_sets = {'Fastballs':['FT', 'FF','SI', 'FC','FA', 'FS','SI','FO'],
              'Breaking':['SL', 'CB', 'CU', 'KC','SC'],
              'Knuckleballs':['KN',], 
              'Offspeed':['CH','SF','EP']}

def get_center_point(x, y, x_step, y_step):
    """Finds the centerpoint of each sub-region, for plotting purposes"""
    x_point = x + (x_step/2.0)
    y_point = y + (y_step/2.0)
    return(x_point, y_point) 
    

def get_slg_in_box(strikes_in_box): 
    """
    Get slugging percent in a sub-region of the strike zone
    
    Input: dataframe containing strikes (pitches) within a specific sub-region
    output: (total_bases, number_of_hits) 
    """
    
    if len(strikes_in_box) == 0:
        return (0, 0)
    else:
        singles = strikes_in_box[(strikes_in_box['des'].str.contains('In play')) & 
                                (strikes_in_box['event']=='Single')]
        doubles = strikes_in_box[(strikes_in_box['des'].str.contains('In play')) & 
                                (strikes_in_box['event']=='Double')] 
        triples = strikes_in_box[(strikes_in_box['des'].str.contains('In play')) & 
                                (strikes_in_box['event']=='Triple')] 
        homers = strikes_in_box[(strikes_in_box['des'].str.contains('In play')) & 
                                (strikes_in_box['event']=='Home Run')]
        tb_in_box = len(singles) + len(doubles) * 2 + len(triples) * 3 + len(homers) * 4 
        hits_in_box = len(singles) + len(doubles) + len(triples) + len(homers)
        return (tb_in_box, hits_in_box ) 
    

def get_box_info(df):
    """
    Takes a pitchFX dataframe
    
    Breaks into sub-regions
    Finds the pitches in each subregion, calculates slg and hits in each
    Returns a dict box_infoD[(ctr_x, ctr_y)] containing 
             'pitch_pct': (Percent of all pitches that are in each box) 
             'slgs': (total bases per hit in box)
             'hits': (total hits in box)
             'hits_per_ptch': hits in box/pitches in box * percent of pitches in box
    """
    (top, bottom,left,right, x_step, y_step) = Baseball.official_zone_25_boxes()
    
    assert len(df) > 0, 'Empty dataframe' 

    box_infoD = {}
    
    for x in np.linspace(left, right, 6):
        for y in np.linspace(bottom, top, 6):
            ctr_x, ctr_y = get_center_point(x, y, x_step, y_step)  
            box_infoD[(ctr_x, ctr_y)] = {}
            
            box = df[(df['px'] >= x) & (df['px'] < x + x_step) &
                     (df['pz'] >= y) & (df['pz'] < y + y_step)]
            
            if len(box) == 0:
                box_infoD[(ctr_x, ctr_y)]['slgs'] = 0
                box_infoD[(ctr_x, ctr_y)]['hits'] = 0
                box_infoD[(ctr_x, ctr_y)]['hits_per_pitch'] = 0
                box_infoD[(ctr_x, ctr_y)]['pitch_pct'] = 0
            else: 
                (tb_in_box, hits_in_box) = get_slg_in_box(box) 
                
                box_infoD[(ctr_x, ctr_y)]['hits_per_pitch'] = hits_in_box/len(box)
                box_infoD[(ctr_x, ctr_y)]['pitch_pct'] = len(box)/len(df)*100
            
                if hits_in_box == 0:
                    box_infoD[(ctr_x, ctr_y)]['slgs'] = 0
                    box_infoD[(ctr_x, ctr_y)]['hits'] = 0
                else:
                    box_infoD[(ctr_x, ctr_y)]['slgs'] = tb_in_box/hits_in_box
                    box_infoD[(ctr_x, ctr_y)]['hits'] = hits_in_box 
                
    return (box_infoD)
             
    
def get_strikes(df):
    return df[~(df['des'].isin(['Ball', 'Hit By Pitch', 'Ball In Dirt', 'Pitchout',
                               'Intent Ball', 'Automatic Ball']))] 

def get_hits(df): 
    return df[(df['des'].str.contains('In play') ) & 
              (df['event'].isin(['Single','Double','Triple','Home Run']))]  
                               
def get_swings_all(df):
    return df[~(df['des'].isin(['Ball', 'Hit By Pitch', 'Ball In Dirt', 'Pitchout',
                                'Intent Ball', 'Automatic Ball', 'Called Strike']))] 
                               
def get_swinging_strikes_fouls(df):
    return df[(df['des'].isin(['Foul', 'Swinging Strike', 'Foul (Runner Going)',
                               'Swinging Strike (Blocked)', 'Foul Tip']))]
                               
def get_swinging_strikes(df):
    return df[(df['des'].isin(['Swinging Strike', 'Swinging Strike (Blocked)']))] 
    
    
#------Get OBP, SLG, OPS from a PITCHf/x dataframe----------
def get_atbats_df_pfx(df):
    no_atbat = ['Walk', 'Intent Walk', 'Sac Bunt', 'Hit By Pitch', 
                'Sac Fly', 'Catcher Interference', 'Fan interference',
                'Batter Interference', 'Sac Fly DP', 'Sacrifice Bunt DP',
                'Runner Out']
    return df[~df['event'].isin(no_atbat)]

def get_atbats_count_pfx(df):
    ab = Baseball.get_atbats_df_pfx(df)
    return len(ab.groupby(['gameday_link','num']).first())

def get_pa_count_pfx(df):
    # PA = AB + BB + HBP + SH + SF + Times Reached on Defensive Interference
    pa_extras = ['Walk', 'Sac Fly', 'Hit By Pitch', 'Intent Walk', 'Sac Bunt', 
                'Sac Fly', 'Catcher Interference', 'Fan interference',
                'Batter Interference', 'Sac Fly DP', 'Sacrifice Bunt DP'] 
    pa = (Baseball.get_atbats_count_pfx(df) + 
          len(df[df['event'].isin(pa_extras)].groupby(['gameday_link','num']).first()))
    return pa

def get_pa_for_obp(df):
    # At Bats + Walks + Hit by Pitch + Sacrifice Flies
    obp_pa_extras = ['Walk', 'Sac Fly', 'Hit By Pitch', 'Intent Walk',  
                'Sac Fly', 'Catcher Interference', 'Fan interference',
                'Batter Interference', 'Sac Fly DP', 'Sacrifice Bunt DP'] 
    obp_pa = (Baseball.get_atbats_count_pfx(df) + 
          len(df[df['event'].isin(obp_pa_extras)].groupby(['gameday_link','num']).first()))
    return obp_pa

def get_obp_pfx(df):
    # (Hits + Walks + Hit by Pitch) / (At Bats + Walks + Hit by Pitch + Sacrifice Flies)
    ob_events = ['Single', 'Double', 'Triple', 'Home Run', 'Walk', 
                 'Intent Walk', 'Hit By Pitch'] 
    on_base = len(df[df['event'].isin(ob_events)].groupby(['gameday_link','num']).first())
    obp_pa = Baseball.get_pa_for_obp(df)
    return on_base/obp_pa

def get_slg_pfx(df):  
    ab = Baseball.get_atbats_df_pfx(df)
    events = list(ab.groupby(['gameday_link','num']).first()['event'].values)
    b1 = events.count('Single')
    b2 = events.count('Double') * 2
    b3 = events.count('Triple') * 3
    b4 = events.count('Home Run') * 4
    return (b1 + b2 + b3 + b4)/len(events)

def get_ops_pfx(df):
    slg = Baseball.get_slg_pfx(df)
    obp = Baseball.get_obp_pfx(df)
    return(slg + obp)
    
