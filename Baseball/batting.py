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

"""

import pandas as pd 
import numpy as np
import Baseball


ptype_sets = {'Fastballs':['FT', 'FF','SI', 'FC','FA', 'FS','SI','FO'],
              'Breaking pitches':['SL', 'CB', 'CU', 'KC','SC'],
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
    
    Input: dataframe containing strikes within a specific sub-region
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
    return df[~(df['des'].isin(['Ball', 'Hit By Pitch', 'Ball In Dirt', 'Pitchout',
                               'Intent Ball', 'Automatic Ball']))] 
                               
def get_swings(df):
    return df[~(df['des'].isin(['Ball', 'Hit By Pitch', 'Ball In Dirt', 'Pitchout',
                                'Intent Ball', 'Automatic Ball', 'Called Strike']))] 