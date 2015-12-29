"""
Functions for calculating and analyzing pitches

def pitch_flight(df_row): 
    Take a single row of a pitchfx dataframe (i.e. a Series)
    Calculate the x, y, z positions for each timepoint t
    Return a dictionary containing lists of each parameter
"""

import pandas as pd 
import numpy as np
from math import sqrt
    
def pitch_flight(df_row): 
    """
    Calculate the x, y, z positions for each timepoint t
    Return a dictionary containing lists of each parameter
    
    """ 
    assert isinstance(df_row, pd.Series), "Must pass a Series (one dataframe row)"
    
    y0 = 50  
    az_noair = -32.174 
    ax_noair = 0 
    
    vy0 = df_row['vy0']
    vx0 = df_row['vx0']  
    vz0 = df_row['vz0']  
    ay = df_row['ay'] 
    az = df_row['az']
    ax = df_row['ax']
    z0 = df_row['z0']
    x0 = df_row['x0']

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