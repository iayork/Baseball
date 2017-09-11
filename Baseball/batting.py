"""
Functions related to batting 

def tb_per_pitch_subzone(df): 
    Get total bases in a sub-region of the strike zone
    
    Input: dataframe containing pitches within a specific sub-region
    output: dataframe with 
        rows = vertical position, 
        columns = horizontal position, 
        values = TB per pitch in that subzone
        
def hits_per_pitch_subzone(df): 
    Get hits per pitch in a sub-region of the strike zone
    
    Input: dataframe containing pitches within a specific sub-region
    output: dataframe with 
        rows = vertical position, 
        columns = horizontal position, 
        values = Hits per pitch in that subzone
    
def hits_per_subzone(df):  
    Get hit count (not per pitch) in a sub-region of the strike zone
    
    Input: dataframe containing pitches within a specific sub-region
    output: dataframe with 
        rows = vertical position, 
        columns = horizontal position, 
        values = Hit count in that subzone 

get_batter_location_success(df)
    DEPRECATED, use tb_per_pitch_subzone instead 
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
             
    


#------Get OBP, SLG, OPS from a PITCHf/x dataframe----------
def get_atbats_pfx(df)

def get_slg_pfx(df) 

def get_obp_pfx(df)

def get_ops_pfx(df)

"""

import pandas as pd 
import numpy as np
import Baseball

def get_center_point(x, y, x_step, y_step):
    """Finds the centerpoint of each sub-region, for plotting purposes"""
    x_point = x + (x_step/2.0)
    y_point = y + (y_step/2.0)
    return(x_point, y_point) 
    

def hits_per_pitch_subzone(df): 
    """
    Get hits per pitch in a sub-region of the strike zone
    
    Input: dataframe containing pitches within a specific sub-region
    output: dataframe with 
        rows = vertical position, 
        columns = horizontal position, 
        values = Hits per pitch in that subzone
    """
    
    hits_subzoneD = {} 
    for row in  np.arange(-1.5, 1.5, 0.6): 
        for col in np.arange(1, 4, 0.6):
            subzone = df[(df['px']>=row) & 
                         (df['px']<row+0.6) & 
                         (df['pz']>=col) & 
                         (df['pz']<col+0.6)] 
                         
            hitsD = Baseball.tb_per_pitch(subzone)
            hits = hitsD['Hits']
            pitches = hitsD['Pitches']
            try:
                hits_per_pitch = hits/pitch
            except ZeroDivisionError:
                hits_per_pitch = 0 
            
            try:
                hits_subzoneD[row].append( hits_per_pitch ) 
            except KeyError:
                hits_subzoneD[row] =  [hits_per_pitch, ] 
    return pd.DataFrame(hits_subzoneD, index=np.arange(1, 4, 0.6))     
    
    
    
def hits_per_subzone(df): 
    """
    Get hit count (not per pitch) in a sub-region of the strike zone
    
    Input: dataframe containing pitches within a specific sub-region
    output: dataframe with 
        rows = vertical position, 
        columns = horizontal position, 
        values = Hit count in that subzone
    """
    
    hits_subzoneD = {} 
    for row in  np.arange(-1.5, 1.5, 0.6): 
        for col in np.arange(1, 4, 0.6):
            subzone = df[(df['px']>=row) & 
                         (df['px']<row+0.6) & 
                         (df['pz']>=col) & 
                         (df['pz']<col+0.6)] 
            hitsD = Baseball.tb_per_pitch(subzone)
            try:
                hits_subzoneD[row].append( hitsD['Hits']) 
            except KeyError:
                hits_subzoneD[row] =  [hitsD['Hits'], ] 
    return pd.DataFrame(hits_subzoneD, index=np.arange(1, 4, 0.6))     
    
def tb_per_pitch_subzone(df): 
    """
    Get total bases in a sub-region of the strike zone
    
    Input: dataframe containing pitches within a specific sub-region
    output: dataframe with 
        rows = vertical position, 
        columns = horizontal position, 
        values = TB per pitch in that subzone
    """
    
    tb_subzoneD = {} 
    for row in  np.arange(-1.5, 1.5, 0.6): 
        for col in np.arange(1, 4, 0.6):
            subzone = df[(df['px']>=row) & 
                         (df['px']<row+0.6) & 
                         (df['pz']>=col) & 
                         (df['pz']<col+0.6)] 
            tbD = Baseball.tb_per_pitch(subzone)
            try:
                tb_subzoneD[row].append( tbD['TB_per_pitch']) 
            except KeyError:
                tb_subzoneD[row] =  [tbD['TB_per_pitch'], ] 
    return pd.DataFrame(tb_subzoneD, index=np.arange(1, 4, 0.6)) 
    

def get_batter_location_success(df):
    """
    Takes a pitchFX dataframe
    
    Breaks into sub-regions
    Finds the pitches in each subregion, calculates slg and hits in each
    Returns a dict box_infoD[(ctr_x, ctr_y)] containing 
             'pitch_pct': (Percent of all pitches that are in each box) 
             'TB': (total bases in box)
             'TB_per_pitch'
             'hits': (total hits in box)
             'hits_per_ptch': hits in box/pitches in box
    """
    print("""This function is deprecated and probably doesn't work correctly anyway
             Use tb_per_pitch_subzone instead""")
    
    (top, bottom,left,right, x_step, y_step) = Baseball.official_zone_25_boxes()
    
    assert len(df) > 0, 'Empty dataframe' 
    # Only include pitches that are inside the "official strike zone 25 boxes"
    total_pitches = len(df[(df['px']>=left) & (df['px']<=right) & 
                           (df['pz']>=bottom) & (df['pz']<=top)])

    box_infoD = {}
    
    for x in np.linspace(left, right, 6):
        for y in np.linspace(bottom, top, 6):
            ctr_x, ctr_y = get_center_point(x, y, x_step, y_step)  
            box_infoD[(ctr_x, ctr_y)] = {}
            
            box = df[(df['px'] >= x) & (df['px'] < x + x_step) &
                     (df['pz'] >= y) & (df['pz'] < y + y_step)]
            
            if len(box) == 0:
                box_infoD[(ctr_x, ctr_y)]['pitch_pct'] = 0
                box_infoD[(ctr_x, ctr_y)]['TB'] = 0
                box_infoD[(ctr_x, ctr_y)]['hits'] = 0
                box_infoD[(ctr_x, ctr_y)]['hits_per_pitch'] = 0
                box_infoD[(ctr_x, ctr_y)]['TB_per_pitch'] = 0
            else: 
                (tb_in_box, hits_in_box) = get_TB_in_box(box) 
                
                box_infoD[(ctr_x, ctr_y)]['pitch_pct'] = len(box)/total_pitches
                box_infoD[(ctr_x, ctr_y)]['TB'] = tb_in_box
                box_infoD[(ctr_x, ctr_y)]['TB_per_pitch'] = tb_in_box/len(box)
                box_infoD[(ctr_x, ctr_y)]['hits'] = hits_in_box
                box_infoD[(ctr_x, ctr_y)]['hits_per_pitch'] = hits_in_box/len(box)
                
    return (box_infoD)
             

    
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
    tb = Baseball.get_tb(df)
    ab = Baseball.get_atbats_count_pfx(df)
    return(tb/ab) 

def get_slg_per_atbat_pfx(df): 
    """Total bases per ATBAT """ 
    ab = len(Baseball.get_atbats_df_pfx(df))
    tb = Baseball.get_tb(df)
    return tb/len(events)
    
def get_hits(df):

    hit_des = ['In play, no out','In play, run(s)']
    hit_event = ['Single','Double','Triple','Home Run']
    hits = df[(df['event'].isin(hit_event)) & 
              (df['des'].isin(hit_des))]
    return hits
    
def get_tb(df):
    hits = get_hits(df)

    b1 = len(hits[hits['event']=='Single'])
    b2 = len(hits[hits['event']=='Double']) * 2
    b3 = len(hits[hits['event']=='Triple']) * 3
    b4 = len(hits[hits['event']=='Home Run']) * 4
    tb = (b1 + b2 + b3 + b4)
    return tb
    
def hits_tb_per_pitch(df):
    tb = Baseball.get_tb(df)
    hits = get_hits(df)
    if len(df) == 0:
        tb_per_pitch = 0
    else:
        tb_per_pitch = tb/len(df)
    return {'Pitches':len(df),
            'Hits':len(hits),
            'TB':tb,
            'TB_per_pitch':tb_per_pitch}    
    
def get_tb_per_pitch_pfx(df): 
    """Total bases per pitch, deprecated because tb_per_pitch is more useful """   
    return (Baseball.get_TB_in_box(df)[0])/len(df)

def get_ops_pfx(df):
    slg = Baseball.get_slg_pfx(df)
    obp = Baseball.get_obp_pfx(df)
    return(slg + obp)
    
