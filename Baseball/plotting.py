"""
Various functions frequently used in plotting

ptype_colors  
    Not a function 
    A dict of seaborn colors suitable for plotting various pitch types 
    
pitch_char_3panel(df): 
    Set up a 3-panel plot for pitch characteristics:
    break_length vs speed
    break_angle vs speed
    break_length vs break_length 
    
circles(x, y, s, c, ax, vmin, vmax, **kwargs):

circle(x, y, s, ax, c, fc='white', ec='dimgray', **kwargs):
      
half_circle(x, y, s, c, ax, a=0.5, **kwargs):

basic_layout_2(year=2015)
    Basic side-by-side set of square plots with strike zone shown
    
large_font():   
    16pt dimgray sans normal 

medium_font(): 
    12pt dimgray sans normal 
    
small_font(): 
    10pt dimgray sans normal 

cmapGnRd(): 
    Green-to-red colormap

cmapGyRd(): 
    Grey-to-red colormap

cmapGyGn(): 
    Grey-to-green colormap 

""" 

import pandas as pd
import matplotlib as mpl
import seaborn as sb
from matplotlib import pyplot as plt

"""A dict of seaborn colors suitable for plotting various pitch types """

muted = sb.color_palette('muted') 
set2 = sb.color_palette('muted')    
ptype_clrs = {  'FF':muted[2], 
                'FT':muted[0], 
                'CU':muted[1],  
                'KC':muted[1],
                'CH':set2[1], 
                'SL':muted[3], 
                'FC':muted[4], 
                'FO':set2[1],
                'SI':muted[4]}
    
    
def pitch_char_3panel(df):
    """
    Set up a 3-panel plot for pitch characteristics:
    break_length vs speed
    break_angle vs speed
    break_length vs break_length
    """
     
    fig, (ax1,ax2,ax3) = plt.subplots(1,3,figsize=(15,5))
    
    i = 0
    for ptype in df['pitch_type'].unique():
        clr = ptype_clrs[ptype]
        df[df['pitch_type']==ptype].plot(x='break_length',
                                         y='start_speed', 
                                         kind='scatter', 
                                         ax=ax1, 
                                         color=clr) 
        df[df['pitch_type']==ptype].plot(x='break_angle',
                                         y='start_speed', 
                                         kind='scatter', 
                                         ax=ax2, 
                                         color=clr)
        df[df['pitch_type']==ptype].plot(x='break_angle',
                                         y='break_length', 
                                         kind='scatter', 
                                         ax=ax3,  
                                         color=clr, 
                                         label=ptype)
        i += 1
 
    ax1.set_xlim(0,20)
    ax1.set_ylim(70,100) 
    ax2.set_xlim(-60,20)
    ax2.set_ylim(70,100) 
    ax3.set_xlim(-60,20)
    ax3.set_ylim(0,20)

    ax3.legend(bbox_to_anchor=(1.12,1)) ;

    for ax in (ax1,ax2):
        ax.set_ylabel('Speed')
    for ax in (ax3,):
        ax.set_ylabel('Break length') 
    for ax in (ax2, ax3):
        ax.set_xlabel('Break angle')
    ax1.set_xlabel('Break length')

    plt.tight_layout()
    return(fig, ax1,ax2,ax3)
    
    
def circles(x, y, s, ax, ec, fc='white', lw=2.5, a=0.2, **kwargs):
    from matplotlib.patches import Circle
    from matplotlib.collections import PatchCollection 

    #http://stackoverflow.com/questions/9081553/python-scatter-plot-size-and-style-of-the-marker 
    
    kwargs.update(facecolor=fc, linewidth=lw, edgecolor=ec, linestyle='-', 
                  alpha=a, antialiased=True) 

    patches = [Circle((x_,y_), s) for x_,y_ in zip(x,y)] 
    collection = PatchCollection(patches, **kwargs)

    ax.add_collection(collection)
    return collection
    
def circle(x, y, s, ax, c, fc='white', ec='dimgray', **kwargs):
    from matplotlib.patches import Circle
    from matplotlib.collections import PatchCollection 

    #http://stackoverflow.com/questions/9081553/python-scatter-plot-size-and-style-of-the-marker 

    kwargs.update(facecolor=fc,linewidth=0.25, 
                  edgecolor=ec, linestyle='-', antialiased=True) 

    patches = [Circle((x_,y_), s_) for x_,y_,s_ in zip(x,y,s)] 
    collection = PatchCollection(patches, **kwargs)

    ax.add_collection(collection)
    return collection 
    
      
def half_circle(x, y, s, c, ax, a=0.5, **kwargs):
    """
    http://stackoverflow.com/questions/15326069/matplotlib-half-black-and-half-white-circle
    Add two half circles to the axes *ax* (or the current axes) with the 
    specified facecolors *colors* rotated at *angle* (in degrees).
    """ 
    from matplotlib.patches import Circle
    from matplotlib.collections import PatchCollection 

    kwargs.update(color=c, antialiased=True, alpha=a) 
    patches = [Wedge((x_,y_), s, 0, 180) for x_,y_ in zip(x,y)] 
    collection = PatchCollection(patches, **kwargs)

    ax.add_collection(collection)
    return collection     
    
    
def basic_layout_2(year=2015):
    """ Basic side-by-side set of square plots with strike zone shown """ 

    from Baseball import strikezone 
    zone_dict = strikezone.get_50pct_zone(year) 

    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(12,7))
    
    ax1.plot(zone_dict['xLs'], zone_dict['yLs'], linestyle='-', linewidth=1, color='dimgrey') 
    ax2.plot(zone_dict['xRs'], zone_dict['yRs'], linestyle='-', linewidth=1, color='dimgrey')  
    
    ax1.set_ylim(0, 7.0) 
    ax1.set_xlim(-2.5,2.5) 
    ax2.set_ylim(0, 7.0) 
    ax2.set_xlim(-2.5,2.5)   
    ax1.set_xlabel("Feet from center of plate", fontsize=14) 
    ax2.set_xlabel("Feet from center of plate", fontsize=14) 
    ax1.set_ylabel('Feet above plate', fontsize=14)
    ax1.set_title('LHB')
    ax2.set_title('RHB')
    ax2.set_yticklabels([])
    ax2.set_ylabel('')   
    
    plt.tight_layout()
    
    return (fig, ax1, ax2)
    

def large_font():  
    """ 16pt dimgray sans normal """ 
    
    font = {'family' : 'sans',
            'color'  : 'dimgray',
            'weight' : 'normal',
            'size'   : 16,
            }
    return font

def medium_font():  
    """ 12pt dimgray sans normal """ 
    
    font = {'family' : 'sans',
            'color'  : 'dimgray',
            'weight' : 'normal',
            'size'   : 12,
            }
    return font
    
def small_font():
    """ 10pt dimgray sans normal """ 
    
    font = {'family' : 'sans',
            'color'  : 'dimgray',
            'weight' : 'normal',
            'size'   : 10,
                  }
    return font
    
def cmapGnRd(): 
    
    cdictGnRd = {'red': ((0.0, 0.4, 0.4),
                         (1.0, 0.9, 0.9)),
                'green': ((0.0, 0.9, 0.9),
                          (1.0, 0.2, 0.2)),
                'blue': ((0.0, 0.2, 0.2),
                         (1.0, 0.2, 0.2))}

    cmapGnRd = mpl.colors.LinearSegmentedColormap('my_colormap', cdictGnRd)
    return cmapGnRd
    
def cmapGyRd():  
    cdictGyRd = {'red': ((0.0, 0.93, 0.93),
                         (0.05, 0.93, 0.93),
                         (0.8, 0.8, 0.8),
                         (1.0, 0.3, 0.3)),
                 'green': ((0.0, 0.93, 0.93),
                           (0.05, 0.93, 0.93),
                           (0.8, 0.2, 0.2),
                           (1.0, 0.1, 0.1)),
                 'blue': ((0.0, 0.96, 0.96),
                          (0.05, 0.96, 0.96),
                          (0.8, 0.2, 0.2),
                          (1.0, 0.1, 0.1))}
    cmapGyRd = mpl.colors.LinearSegmentedColormap('my_colormap', cdictGyRd) 
    return cmapGyRd  
    
def cmapGyGn():  
    cdictGyGn = {'red': ((0.0, 0.93, 0.93),
                         (0.05, 0.93, 0.93),
                         (0.8, 0.2, 0.2),
                         (1.0, 0.1, 0.1)),
                 'green': ((0.0, 0.93, 0.93),
                           (0.05, 0.93, 0.93),
                           (0.8, 0.8, 0.8),
                           (1.0, 0.3, 0.3)),
                 'blue': ((0.0, 0.96, 0.96),
                          (0.05, 0.96, 0.96),
                          (0.8, 0.2, 0.2),
                          (1.0, 0.1, 0.1))}
    cmapGyGn = mpl.colors.LinearSegmentedColormap('my_colormap', cdictGyGn) 
    return cmapGyGn