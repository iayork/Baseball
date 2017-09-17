import pandas as pd 
import numpy as np
from math import sqrt
import Baseball

#---------Functions for calculating position of a pitch in flight----------
def pitch_flight(df_row): 
    """
    Calculate the x, y, z positions for each timepoint t
    Return a dictionary containing lists of each parameter
    
    """ 
    assert isinstance(df_row, pd.DataFrame), "Must pass one dataframe row"
    assert len(df_row)==1, "Must pass one dataframe row"
    
    y0 = 50  
    az_noair = -32.174 
    ax_noair = 0 
    
    vy0 = df_row.iloc[0]['vy0']
    vx0 = df_row.iloc[0]['vx0']  
    vz0 = df_row.iloc[0]['vz0']  
    ay = df_row.iloc[0]['ay'] 
    az = df_row.iloc[0]['az']
    ax = df_row.iloc[0]['ax']
    z0 = df_row.iloc[0]['z0']
    x0 = df_row.iloc[0]['x0']

    z_time = [] 
    y_time = []
    x_time = [] 
    t_time = [] 
    z_noair_time = []
    x_noair_time = []

    
    # Calculate t for y=55
    # Start with that time, and pass an adjustment to set it to 0
     
    t55 = (-vy0 - sqrt(vy0*vy0 - 2*ay * (y0 - 55)))/ay   
    vy55 = -(sqrt(vy0*vy0 + 2*ay * (55 - y0))) 
    vyend = -(sqrt(vy0*vy0 + 2*ay * (1.417 - y0)))
    
    mph = -(vy0 * 60 *60)/5280.0 
    mph55 = -(vy55 * 60 *60)/5280.0 
    mphend = -(vyend * 60 *60)/5280.0 

    for ty in np.arange(0.00, 2 , 0.01):
        adj_ty = ty + t55
        
        y = ((((vy0 + ay * adj_ty) * (vy0 + ay * adj_ty)) - (vy0*vy0))/(2*ay)) + y0 

        z = z0 + vz0 * adj_ty + 1/2 * az * adj_ty*adj_ty 
        z_noair = z0 + vz0 * adj_ty + 1/2 * az_noair * adj_ty*adj_ty  

        x = x0 + vx0 * adj_ty + 1/2 * ax * adj_ty*adj_ty
        x_noair = x0 + vx0 * adj_ty + 1/2 * ax_noair * adj_ty*adj_ty

        z_time.append(z)
        y_time.append(y)
        x_time.append(x) 
        t_time.append(ty)
        z_noair_time.append(z_noair)
        x_noair_time.append(x_noair)

        if y <= 1.417:
            break 
            
    return {'z_time':z_time, 
            'x_time':x_time, 
            't_time':t_time,
            'y_time':y_time,
            'z_noair_time':z_noair_time, 
            'x_noair_time':x_noair_time, 
            'mph':mph,
            'mph55':mph55,
            'mphend':mphend,
            'ptype':df_row['pitch_type'],
            'stand':df_row['stand']}
            
    
def speed_at_feet(df, feet=55):
    """
    Calculate pitch speed at any distance from the plate (default = 55 feet)
    Usage: For a PITCHf/x dataframe df
    df['Speed55'] = df.apply(speed_at_feet, axis=1)
    or
    df['Speed15'] = speed_at_feet(df, feet=15)
    """
    y0 = 50  
    vy_feet = -(np.sqrt(df['vy0']*df['vy0'] + 2*df['ay'] * (feet - y0)))
    mph_feet = -(vy_feet * 60*60)/5280.0 
            
    return mph_feet
    
#---------Pitch usage----------
    
def pitch_usage_games(df):
    # Turn a PITCHf/x dataframe into per-game pitch usage percents 
    
    usage = pd.DataFrame(df.groupby(['gameday_link','pitch_type']).count()['count'])
    usage = usage.reset_index()
    usage.rename(columns={'pitch_type':'Pitch type'}, inplace=True)
    
    usage['Date'] = usage['gameday_link'].apply(Baseball.gdl_to_date)
    usage2 = usage.pivot(index='Date',columns='Pitch type',values='count').fillna(0)
    usage2['Total'] = usage2.sum(axis=1)

    for ptype in usage2.columns[:-1]:
        usage2['%s_pct' % ptype] = usage2[ptype]/usage2['Total']*100
    usage_pct = usage2[[x for x in usage2.columns if 'pct' in x]].copy()
    usage_pct.rename(columns={x:x.replace('_pct','') for x in usage_pct.columns}, inplace=True)
    return usage_pct
    
def pitch_usage_year(df):
    # Turn a PITCHf/x dataframe into per-year pitch usage percents 
    usage_yr = df[['pitch_type','count']].groupby('pitch_type').count() 
    usage_yr['Percent'] = usage_yr.apply(lambda x:x/usage_yr['count'].sum(axis=0)*100)
    usage_yr = usage_yr.drop(['count'],axis=1)
    return usage_yr
    
#------Situational pitch usage--------

def get_usage_all_counts(df, ptypes=None):
    # Show pitch usage in each count
    if ptypes is None:
        ptypes = df['pitch_type'].unique()
    countD = {}
    for count in ['0-0', '0-1', '0-2', 
                  '1-0', '1-1', '1-2',
                  '2-0', '2-1', '2-2',
                  '3-0', '3-1', '3-2']:
        c = df[df['count']==count]
        countD[count] = {}
        countD[count]['Total'] = len(c)
        for ptype in ptypes:
            countD[count]['%s%%' % ptype] = '%.1f' % ((len(c[c['pitch_type']==ptype]))/len(c) * 100)
    return pd.DataFrame(countD)

def get_countD(df, ptypes):
    countD = {}
    for count_type in ['Ahead', 'Behind']:
        c = df[df['count'].isin(Baseball.counts[count_type])]
        countD[count_type] = {}
        countD[count_type]['Total'] = len(c)
        for ptype in ptypes:
            countD[count_type][ptype] = (len(c[c['pitch_type']==ptype]))/len(c) * 100

    return pd.DataFrame(countD)

def get_usage(df):
    # takes the full dataframe
    usage_conditions = df[['count','pitch_type']].groupby('pitch_type').count()/len(df) * 100
    usage_conditions.rename(columns={'count':'All'},inplace=True)
    
    for stand in ['L','R']:
        total = len(df[df['stand']==stand])
        tmp = df[df['stand']==stand][['count','pitch_type']].groupby('pitch_type').count()/total * 100
        tmp.rename(columns={'count':stand},inplace=True)
        usage_conditions = usage_conditions.merge(tmp, left_index=True, right_index=True, how='outer') 
        usage_conditions.rename(columns={'L':'LHB', 'R':'RHB'}, inplace=True)
    return usage_conditions
    
def pitch_usage_situational(df, ptypes=None):
    # Turn a PITCHf/x dataframe into pitch usage percents 
    # including situations (vs RHB and LHB, ahead and behind)
    if ptypes is None:
        ptypes = df['pitch_type'].unique()
    countDF = get_countD(df, ptypes)
    usage_conditions = get_usage(df)
    usage_conditions = usage_conditions.merge(countDF, 
                                              left_index=True, 
                                              right_index=True)
    return usage_conditions
    
    
#------- Pitch values - Total bases/100 pitches, balls/100 pitches -------

def get_b100(df, ptype=None):
    # Balls per 100 pitches 
    # If no pitch type is given, give results for the whole dataframe
    
    if ptype is None:
        pt = df
    else:
        pt = df[df['pitch_type']==ptype] 
    b = pt[pt['des'].isin(Baseball.balls)] 
    
    b100 = len(b)/len(pt)*100
    return b100

def get_b100_tb100_per_ptype(df, ptypes=None):
    if ptypes is None:
        ptypes = df['pitch_type'].unique()
    tb100sD = {}
    b100sD = {}
    for ptype in ptypes: 
        try: 
            ptype_df = df[df['pitch_type']==ptype]
            tb100sD[ptype] = Baseball.hits_tb_per_pitch(ptype_df)['TB_per_pitch']*100
            b100sD[ptype] = get_b100(ptype_df)
        except ZeroDivisionError:
            tb100sD[ptype]  = np.nan
            b100sD[ptype] = np.nan
    
    return(tb100sD, b100sD)


