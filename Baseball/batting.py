import pandas as pd 
import numpy as np
import Baseball

def get_center_point(x, y, x_step, y_step):
    """
    Finds the centerpoint of a sub-region, for plotting purposes
    """
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
    
    
#------In/out of strike zone-------------------------------

def zone_as_polygon(year):
    """
    Converts a strike zone (as a series of points) into a matplotlib polygon path
    Allows use of path.contains_points to test if pitches are inside a strike zone 
    
    """
    import matplotlib.patches as patches 
    zone_dict = Baseball.get_50pct_zone(2016) 
    xy_r = np.array([np.array(xy) for xy in zip(np.array(zone_dict['xRs'][:-1]), 
                     np.array(zone_dict['yRs'][:-1]))])
    zone_polygon_r = patches.Polygon(xy_r,closed=True, 
                                     facecolor='grey', alpha=0.1)
    zone_path_r = zone_polygon_r.get_path()
    
    xy_l = np.array([np.array(xy) for xy in zip(np.array(zone_dict['xLs'][:-1]), 
                     np.array(zone_dict['yLs'][:-1]))])
    zone_polygon_l = patches.Polygon(xy_l,closed=True, 
                                     facecolor='grey', alpha=0.1)
    zone_path_l = zone_polygon_l.get_path()
    return {'R':zone_path_r, 'L':zone_path_l}
    
    
def get_o_zone_pitches(df, year, stand, radius=-0.25):
    """
    Given a strike zone and a pitchab dataframe, 
    labels pitches as "inside" or "outside" the zone
    Uses a radius of -0.25 by default to ignore pitches that are touching the 
    "edge" of the zone (i.e. in the region of 50% ball/strike calls)
    Returns the dataframe with a new column "Inside_zone_for_o-zone" 
    "False" = pitches outside the strike zone
    """

    zone_path = zone_as_polygon(year)[stand]
    df2 = df.copy()
    df2.loc[:,'Inside_zone_for_o-zone'] = zone_path.contains_points(df2[['px','pz']].values, 
                                                         radius = radius)
    return(df2[(df2['Inside_zone_for_o-zone']==False)])
    
def get_o_zone_swings(df, year, stand):
    """
    Given a pitchab dataframe, returns a dataframe containing 
    pitches outside the strike zone (= 0.25 radius) that were swung at
    """
    o_zone_pitches = get_o_zone_pitches(df, year,stand)
    o_zone_swings = o_zone_pitches[~(o_zone_pitches['des'].isin(Baseball.balls)) & 
                                    (o_zone_pitches['des']!='Called Strike')]
    return o_zone_swings
    
def get_o_zone_swing_pct(df, stand, year=2016):
    """
    Given a pitchab dataframe, returns the percent of pitches 
    outside the strike zone (+ 0.25 radius) that were swung at
    """
    o_zone_pitches = get_o_zone_pitches(df,year,stand)
    o_zone_swings = get_o_zone_swings(df, year, stand)
    o_swing_pct = len(o_zone_swings)/len(o_zone_pitches)*100
    return o_swing_pct

    
def get_in_zone_pitches(df, year, stand, radius=0.25):
    """
    Given a strike zone and a pitchab dataframe, 
    labels pitches as "inside" or "outside" the zone
    Uses a radius of 0.25 by default to ignore pitches that are touching the 
    "edge" of the zone (i.e. in the region of 50% ball/strike calls)
    Returns the dataframe with a new column "Inside_zone_for_o-zone" 
    "True" = pitches outside the strike zone
    """
    zone_path = zone_as_polygon(year)[stand]
    df2 = df.copy()
    df2.loc[:,'Inside_zone_for_in-zone'] = zone_path.contains_points(df2[['px','pz']].values, 
                                                         radius = radius)
    return(df2[(df2['Inside_zone_for_in-zone']==True)])
    
def get_in_zone_swings(df, year, stand):
    """
    Given a pitchab dataframe, returns a dataframe containing 
    pitches inside the strike zone (+ 0.25 radius) that were swung at
    """
    in_zone_pitches = get_in_zone_pitches(df, year,stand)
    in_zone_swings = in_zone_pitches[~(in_zone_pitches['des'].isin(Baseball.balls)) & 
                                      (in_zone_pitches['des']!='Called Strike')]
    return in_zone_swings
    
def get_in_zone_swing_pct(df, stand, year=2016):
    """
    Given a strike zone and a pitchab dataframe, 
    labels pitches as "inside" or "outside" the zone
    Uses a radius of 0.25 by default to ignore pitches that are touching the 
    "edge" of the zone (i.e. in the region of 50% ball/strike calls)
    Returns the dataframe with a new column "Inside_zone_for_o-zone" 
    "True" = pitches outside the strike zone
    """
    in_zone_pitches = get_in_zone_pitches(df,year,stand)
    in_zone_swings = get_in_zone_swings(df, year, stand)
    in_swing_pct = len(in_zone_swings)/len(in_zone_pitches)*100
    return in_swing_pct
             

    
#------Get OBP, SLG, OPS from a PITCHf/x dataframe----------

def get_atbats_df_pfx(df):
    """
    Given a pitchab dataframe return a dataframe containing 
    pitches from official at-bats only
    """

    no_atbat = ['Walk', 'Intent Walk', 'Sac Bunt', 'Hit By Pitch', 
                'Sac Fly', 'Catcher Interference', 'Fan interference',
                'Batter Interference', 'Sac Fly DP', 'Sacrifice Bunt DP',
                'Runner Out']
    return df[~df['event'].isin(no_atbat)]

def get_atbats_count_pfx(df):
    """
    Given a pitchab dataframe return the number of official at-bats
    """
    ab = Baseball.get_atbats_df_pfx(df)
    return len(ab.groupby(['gameday_link','num']).first())

def get_pa_count_pfx(df):

    """
    Given a pitchab dataframe return the number of official plate appearances
    PA = AB + BB + HBP + SH + SF + Times Reached on Defensive Interference
    -> Calculate by first counting at-bats and then counting additional events 
    that count toward a plate appearance
    """ 
    pa_extras = ['Walk', 'Sac Fly', 'Hit By Pitch', 'Intent Walk', 'Sac Bunt', 
                'Sac Fly', 'Catcher Interference', 'Fan interference',
                'Batter Interference', 'Sac Fly DP', 'Sacrifice Bunt DP'] 
    pa = (Baseball.get_atbats_count_pfx(df) + 
          len(df[df['event'].isin(pa_extras)].groupby(['gameday_link','num']).first()))
    return pa

def get_obp_pfx(df):
    """
    Calculate on-base percentage from a pitchab dataframe
    OBP = (Hits + Walks + Hit by Pitch) / (At Bats + Walks + Hit by Pitch + Sacrifice Flies)
    """
    ob_events = ['Single', 'Double', 'Triple', 'Home Run', 'Walk', 
                 'Intent Walk', 'Hit By Pitch'] 
    on_base = len(df[df['event'].isin(ob_events)].groupby(['gameday_link','num']).first())
    obp_pa = Baseball.get_pa_count_pfx(df)
    return on_base/obp_pa
     
     
def get_slg_pfx(df):
    """
    Calculate slugging from a pitchab dataframe
    SLG = (Total bases) / (At Bats)
    """
    tb = Baseball.get_tb(df)
    ab = Baseball.get_atbats_count_pfx(df)
    return(tb/ab) 

def get_slg_per_atbat_pfx(df): 
    """Calculate Total bases per ATBAT """ 
    ab = len(Baseball.get_atbats_df_pfx(df))
    tb = Baseball.get_tb(df)
    return tb/len(events)
    
def get_hits(df):
    """
    Given a pitchab dataframe, return a datafrom containing only pitches 
    that were successfully hit
    """
    hit_des = ['In play, no out','In play, run(s)']
    hit_event = ['Single','Double','Triple','Home Run']
    hits = df[(df['event'].isin(hit_event)) & 
              (df['des'].isin(hit_des))]
    return hits
    
def get_tb(df):
    """
    From a pitchab dataframe calculate total bases 
    """
    hits = get_hits(df)

    b1 = len(hits[hits['event']=='Single'])
    b2 = len(hits[hits['event']=='Double']) * 2
    b3 = len(hits[hits['event']=='Triple']) * 3
    b4 = len(hits[hits['event']=='Home Run']) * 4
    tb = (b1 + b2 + b3 + b4)
    return tb
    
def hits_tb_per_pitch(df):
    """
    From a pitchab dataframe return a dict containing
        Pitches
        Hits
        Total Bases
        Total Bases per pitch'
    """
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

def get_ops_pfx(df):
    """
    From a pitchab dataframe calculate OPS
    OPS = SLG + OBP
    """
    slg = Baseball.get_slg_pfx(df)
    obp = Baseball.get_obp_pfx(df)
    return(slg + obp)
    
