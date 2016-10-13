"""
Functions for calculating and analyzing pitches

def pitch_flight(df_row): 
    Take a single row of a pitchfx dataframe (i.e. a Series)
    Calculate the x, y, z positions for each timepoint t
    Return a dictionary containing lists of each parameter
    
    
def speed_at_feet(df, feet=55): 
    PITCHf/x start_speed is at 50 feet from home plate
    Calculate pitch speed at any distance from the plate 
    Default = 55 feet (Brooks Baseball style)
    Usage: For a PITCHf/x dataframe df
    df['Speed55'] = df.apply(speed_at_feet, axis=1)
    or
    df['Speed15'] = speed_at_feet(df, feet=15) 
    
def pitch_usage(df):
    # Turn a PITCHf/x dataframe into pitch usage percents 
"""

import pandas as pd 
import numpy as np
from math import sqrt


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
    
def gdl_to_date(x):
    return '%s-%s-%s' % (x.split('_')[2], x.split('_')[3], x.split('_')[1])
    
def pitch_usage(df):
    # Turn a PITCHf/x dataframe into per-game pitch usage percents 
    u1 = pd.DataFrame(df.groupby(['gameday_link','pitch_type']).count()['count'])
    u1 = u1.reset_index()
    u1.rename(columns={'pitch_type':'Pitch type'}, inplace=True)
    u1['Date'] = u1['gameday_link'].apply(gdl_to_date)
    u2 = u1.pivot(index='Date',columns='Pitch type',values='count').fillna(0)
    u2['Total'] = u2.sum(axis=1)
    for ptype in u2.columns[:-1]:
        u2['%s_pct' % ptype] = u2[ptype]/u2['Total']*100
    u_pct = u2[[x for x in u2.columns if 'pct' in x]]
    u_pct.rename(columns={x:x.replace('_pct','') for x in u_pct.columns}, inplace=True)
    return u_pct
    
def pitch_usage_year(df):
    # Turn a PITCHf/x dataframe into per-year pitch usage percents 
    usage_yr = df[['pitch_type','count']].groupby('pitch_type').count() 
    usage_yr['Percent'] = usage_yr.apply(lambda x:x/usage_yr['count'].sum(axis=0)*100)
    usage_yr = usage_yr.drop(['count'],axis=1)
    return usage_yr