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
    
get_2D_pxpz_hist(df, rot=True, bins=10): 
    Get a 2D histogram of px/pz values from a dataframe 
    
    For imshow and seaborn heatmaps at least, the hists need to be rotated 90 degrees
                
smooth_2D_hist(x,y,values):
    Smooth 2D histogram using interpolation

circle(x, y, s, ax, fc='white', ec='dimgray', vmin=None, vmax=None, **kwargs)
    For drawing the circles in Batter's Strike Zones by SLG
    Takes either a single facecolor or a list of colors
    
circles(x, y, s, ax, ec, fc='white', lw=2.5, a=0.2, **kwargs):
    For drawing the pitch indicators in the game characterization
      
half_circle(x, y, s, c, ax, a=0.5, **kwargs):
    For drawing the pitch indicators in the game characterization

basic_layout_pitcher_2(year=2016): 
    Visualize the strike zone from the umpire's view for a pitcher
    Two charts, one for LHB, one for RHB (one pitch type only)
    Plot the de facto strike zone for the year on each plot 
    
basic_layout_pitcher_4(year=2016)
basic_layout_pitcher_6(year=2016)
basic_layout_pitcher_8(year=2016)
basic_layout_pitcher_10(year=2016)


def show_batter(ax, stand, xyl=[1.35, 2], xyr=[-1.35, 2],
                img_path_l="/Users/iayork/Documents/Baseball/Batter_Silhouette_LHB_2.png",
                img_path_r="/Users/iayork/Documents/Baseball/Batter_Silhouette_RHB_2.png"):
    Batter silouhettes
    
basic_plot_batter(stand, year=2016): 
    Visualize the strike zone from the umpire's view for a batter
    Two charts, one for LHP, one for RHP
    Plot the de facto strike zone for the year on each plot 
    
plot_3D(df, ptypes=None, output_dir='/Users/iayork/Downloads', output_folder='ptch3D'):
    3D scatter plot of pitches, colored by pitch type
    Generates a series of plots, rotating 5 o each time (convert to GIF using ImageMacgick)
    
    Input: Dataframe containing PITCHf/x data
    Optional:
        ptypes: If only want to plot a subset of the pitch types in the dataframe
        output_dir, output_folder - Where to save the output charts 
    
    
scatter_with_hover(df, x, y,
                       fig=None, cols=None, name=None, marker='x',
                       fig_width=500, fig_height=500, **kwargs):
                       
    http://blog.rtwilson.com/bokeh-plots-with-dataframe-based-tooltips/
    Plots an interactive scatter plot of `x` vs `y` using bokeh, with automatic
    tooltips showing columns from `df`.
    
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
import numpy as np
import matplotlib as mpl
import seaborn as sb
from matplotlib import pyplot as plt


"""A dict of seaborn colors suitable for plotting various pitch types """
muted = sb.color_palette('muted') 
set2 = sb.color_palette('Set2')    
ptype_clrs = {  'FF':muted[2], 
                'FT':muted[0], 
                'CU':muted[1],  
                'KC':muted[1],
                'CH':set2[1], 
                'SL':muted[3], 
                'FC':muted[4], 
                'FO':set2[1],
                'SI':muted[0],
                'FS':set2[1],  
                'KN':muted[5],  
                'EP':'grey'}
    

def get_2D_pxpz_hist(df, rot=True, smooth=True, bins=10):
    """
    Get a 2D histogram of px/pz values from a dataframe 
    
    For imshow and seaborn heatmaps at least, the hists need to be rotated 90 degrees
    """ 
    
    import numpy as np
    from scipy import ndimage 
    
    hmap, xedges, yedges = np.histogram2d(x=df['px'].values, 
                                          y=df['pz'].values,
                                          range=[[-2.5, 2.5], [0, 5]],
                                          bins=bins)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    
    if smooth:
        (xnew, ynew, hmap) = Baseball.smooth_2D_hist(xedges, yedges, hmap) 
        extent = [xnew[0], xnew[-1], ynew[0], ynew[-1]] 
    
    if rot:
        return (extent, ndimage.rotate(hmap, 90, reshape=False))
    else: 
        return (extent, hmap)   
                

def smooth_2D_hist(x,y,values):
    """ Smooth 2D histogram using interpolation"""
    
    from scipy import interpolate
    import numpy as np
    
    f = interpolate.interp2d(x[:-1], y[:-1], values)
    xnew = np.arange(min(x), max(x), 0.03)
    ynew = np.arange(min(y), max(y), 0.03)
    knew = f(xnew, ynew)
    return (xnew, ynew, knew)
    
                

def animation_3_views():  
    fig = plt.figure(figsize=(25,12.5))
    
    gs = gridspec.GridSpec(3, 3,
                       width_ratios=[12,12,4],
                       height_ratios=[1,1,4]
                       )
    gs.update(hspace=0.05, wspace=0.05)
    
    ax1 = plt.subplot(gs[0, 1])
    ax2 = plt.subplot(gs[1, 1])
    ax3 = plt.subplot(gs[0:2, 2]) 
    
    zone_dict = utilities.get_50pct_zone(year)
    ax3.plot(zone_dict['xRs'], zone_dict['yRs'], linestyle='-', linewidth=1, color=dark[0])  

    ax1.set_ylim(-3.2,1.8)  # -2.5, 2.5
    ax1.set_xlim(65,0)  
    ax1.set_xlabel('') 
    ax1.set_xticklabels([])
    ax1.set_ylabel("Feet from center of plate", fontsize=10) 
    ax1.tick_params(axis='both', which='major', labelsize=10)
    ax1.set_title('Top view', fontsize=12)
    
    ax2.set_ylim(0,7.0) 
    ax2.set_xlim(65,0)  
    ax2.set_xlabel("Feet from home plate", fontsize=10)
    ax2.tick_params(axis='both', which='major', labelsize=10)
    ax2.set_ylabel("Feet above plate", fontsize=10)  
    ax2.text(34.7, 6.1, "Side view", fontsize=12) 
    ax2.text(59, 0.4, "@soshbaseball", fontsize=10, alpha=0.8)
    
    ax3.set_ylim(0, 7.0) 
    ax3.set_xlim(-3.2,1.8)  # -2.5, 2.5  
    ax3.yaxis.tick_right()
    ax3.set_xlabel("Feet from center of plate", fontsize=10) 
    ax3.set_ylabel('Feet above plate', fontsize=10)
    ax3.yaxis.set_label_position("right")
    ax3.tick_params(axis='both', which='major', labelsize=10)
    ax3.set_title("Umpire's view", fontsize=12)
    
    return (fig, ax1, ax2, ax3)
    
    
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
    
    
def circle(x, y, s, ax, fc='white', ec='dimgray', vmin=None, vmax=None, **kwargs):
    from matplotlib.patches import Circle
    from matplotlib.collections import PatchCollection 

    #http://stackoverflow.com/questions/9081553/python-scatter-plot-size-and-style-of-the-marker 
    patches = [Circle((x_,y_), s_) for x_,y_,s_ in zip(x,y,s)]
    
    if type(fc) == list:
        kwargs.update(edgecolor=ec, linestyle='-', antialiased=True) 
        collection = PatchCollection(patches, **kwargs)
        collection.set_array(np.asarray(fc))
        collection.set_clim(vmin, vmax) 
    else:
        kwargs.update(edgecolor=ec, facecolor=fc, linestyle='-', antialiased=True)  
        collection = PatchCollection(patches, **kwargs)

    ax.add_collection(collection)
    return collection 
    
    
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
    
    
def basic_layout_pitcher_2(year=2016):
    """
    Visualize the strike zone from the umpire's view for a pitcher
    Two charts, one for LHB, one for RHB (one pitch type only)
    Plot the de facto strike zone for the year on each plot """

    from Baseball import strikezone 
    zone_dict = strikezone.get_50pct_zone(year) 

    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(11.5,6), facecolor='white')
    
    ax1.plot(zone_dict['xLs'], zone_dict['yLs'], linestyle='-', linewidth=1, color='dimgrey') 
    ax2.plot(zone_dict['xRs'], zone_dict['yRs'], linestyle='-', linewidth=1, color='dimgrey')  
    
    ax1.set_ylim(0, 5.0) 
    ax1.set_xlim(-2.5,2.5) 
    ax2.set_ylim(0, 5.0) 
    ax2.set_xlim(-2.5,2.5)   
    ax1.set_xlabel("Feet from center of plate", fontsize=14) 
    ax2.set_xlabel("Feet from center of plate", fontsize=14) 
    ax1.set_ylabel('Feet above plate', fontsize=14)
    ax1.set_title('LHB')
    ax2.set_title('RHB')
    ax2.set_yticklabels([])
    ax2.set_ylabel('')   
    
    #ax1.text(-2.3, 0.2, '@soshbaseball', fontsize=12, alpha=0.8)
    
    plt.tight_layout()
    
    return (fig, (ax1, ax2))  

  
    
    
def basic_layout_pitcher_4(year=2016):
    """
    Visualize the strike zone from the umpire's view for a pitcher
    Four charts, two for LHB, two for RHB 
    Plot the de facto strike zone for the year on each plot """

    from Baseball import strikezone 
    zone_dict = strikezone.get_50pct_zone(year) 

    fig, ((ax1, ax2),(ax3,ax4)) = plt.subplots(2,2,figsize=(11.5,12), facecolor='white') 
    
    ax1.set_title('LHB')
    ax2.set_title('RHB')
    for ax in (ax1,ax2,ax3,ax4):
        ax.set_ylim(0, 5.0) 
        ax.set_xlim(-2.5,2.5) 
    for ax in (ax1,ax2):
        ax.set_xticklabels([])
        ax.set_xlabel('')
    for ax in (ax2,ax4):
        ax.plot(zone_dict['xRs'], zone_dict['yRs'], linestyle='-', linewidth=1, color='dimgrey') 
        ax.set_yticklabels([])
        ax.set_ylabel('')
    for ax in (ax3,ax4):
        ax.set_xlabel("Feet from center of plate", fontsize=14) 
    for ax in (ax1,ax3): 
        ax.plot(zone_dict['xLs'], zone_dict['yLs'], linestyle='-', linewidth=1, color='dimgrey') 
        ax.set_ylabel('Feet above plate', fontsize=14)
    
    ax1.text(-2.3, 0.2, '@soshbaseball', fontsize=12, alpha=0.8)
    
    plt.tight_layout()
    
    return (fig, ((ax1,ax2),(ax3,ax4)))
    
    
def basic_layout_pitcher_6(year=2016):
    """
    Visualize the strike zone from the umpire's view for a pitcher
    Six charts, three for LHB, three for RHB 
    Plot the de facto strike zone for the year on each plot """

    from Baseball import strikezone 
    zone_dict = strikezone.get_50pct_zone(year) 

    fig, ((ax1, ax2),(ax3,ax4),(ax5,ax6)) = plt.subplots(3,2,figsize=(11.5,16), facecolor='white')
    
    for ax in (ax1,ax3,ax5):
        ax.plot(zone_dict['xLs'], zone_dict['yLs'], linestyle='-', linewidth=1, color='dimgrey') 
        ax.set_ylim(0, 7.0) 
        ax.set_xlim(-2.5,2.5)
        ax.set_ylabel('Feet above plate', fontsize=14)
    for ax in (ax2,ax4,ax6):
        ax.plot(zone_dict['xRs'], zone_dict['yRs'], linestyle='-', linewidth=1, color='dimgrey')  
        ax.set_ylim(0, 7.0) 
        ax.set_xlim(-2.5,2.5)
        ax2.set_yticklabels([])
        ax2.set_ylabel('')   
    for ax in (ax1,ax2,ax3,ax4):
        ax.set_xlabel('')
        ax.set_xticklabels([])
     
    ax5.set_xlabel("Feet from center of plate", fontsize=14) 
    ax6.set_xlabel("Feet from center of plate", fontsize=14) 
    ax1.set_title('LHB')
    ax2.set_title('RHB')
    
    ax1.text(-2.3, 0.2, '@soshbaseball', fontsize=12, alpha=0.8)
    
    plt.tight_layout()
    
    return (fig,((ax1,ax2),(ax3,ax4),(ax5,ax6)))  
    
    
    
def basic_layout_pitcher_8(year=2016): 
    """
    Visualize the strike zone from the umpire's view for a pitcher
    Four rows of 2 charts, one for LHB, one for RHB
    Plot the de facto strike zone for the year on each plot """
    
    from Baseball import strikezone 
    zone_dict = strikezone.get_50pct_zone(year) 
    
    fig, ((ax1, ax2),(ax3,ax4),
          (ax5,ax6),(ax7,ax8)) = plt.subplots(4,2,figsize=(8,16), facecolor='white')
    # Plot the strike zone on each plot
    for ax in (ax1,ax3,ax5,ax7):
        ax.plot(zone_dict['xLs'], zone_dict['yLs'], linewidth=2, color='grey') 
        ax.set_ylabel('Height (feet)')
    for ax in (ax2,ax4,ax6,ax8):
        ax.plot(zone_dict['xRs'], zone_dict['yRs'], linewidth=2, color='grey')  
        ax.set_ylabel('')
        ax.set_yticklabels([])
    
    for ax in (ax1, ax2, ax3,ax4,ax5,ax6,ax7,ax8):
        ax.set_ylim(0,5) 
        ax.set_xlim(-2.5,2.5) 
    for ax in (ax1, ax2, ax3,ax4,ax5,ax6):
        ax.set_xticklabels([]) 
    for ax in (ax7,ax8):
        ax.set_xlabel('Distance from center of plate (feet)') 
    
    ax1.text(-2.3, 0.2, '@soshbaseball', fontsize=12, alpha=0.8)

    plt.tight_layout()
    return (fig,((ax1,ax2),(ax3,ax4),(ax5,ax6),(ax7,ax8)))

    
    
def basic_layout_pitcher_10(year=2016): 
    """
    Visualize the strike zone from the umpire's view for a pitcher
    Five rows of 2 charts, one for LHB, one for RHB
    Plot the de facto strike zone for the year on each plot """
    
    from Baseball import strikezone 
    zone_dict = strikezone.get_50pct_zone(year) 
    
    fig, ((ax1, ax2),(ax3,ax4),
          (ax5,ax6),(ax7,ax8),(ax9,ax10)) = plt.subplots(5,2,figsize=(8,20), facecolor='white')
    # Plot the strike zone on each plot
    for ax in (ax1,ax3,ax5,ax7,ax9):
        ax.plot(zone_dict['xLs'], zone_dict['yLs'], linewidth=2, color='grey') 
        ax.set_ylabel('Height (feet)')
    for ax in (ax2,ax4,ax6,ax8,ax10):
        ax.plot(zone_dict['xRs'], zone_dict['yRs'], linewidth=2, color='grey')  
        ax.set_ylabel('')
        ax.set_yticklabels([])
    
    for ax in (ax1, ax2, ax3,ax4,ax5,ax6,ax7,ax8,ax9,ax10):
        ax.set_ylim(0,5) 
        ax.set_xlim(-2.5,2.5) 
    for ax in (ax2, ax4, ax6, ax8, ax10):
        ax.set_yticklabels([])
        ax.set_ylabel('')
    for ax in (ax1, ax2, ax3,ax4,ax5,ax6,ax7,ax8):
        ax.set_xticklabels([])
        ax.set_xlabel('')
    for ax in (ax9,ax10):
        ax.set_xlabel('Distance from center of plate (feet)') 
    
    ax1.text(-2.3, 0.2, '@soshbaseball', fontsize=12, alpha=0.8)

    plt.tight_layout()
    return (fig,((ax1,ax2),(ax3,ax4),(ax5,ax6),(ax7,ax8),(ax9,ax10)))
    
    
def basic_layout_pitcher_12(year=2016): 
    """
    Visualize the strike zone from the umpire's view for a pitcher
    Six rows of 2 charts, one for LHB, one for RHB
    Plot the de facto strike zone for the year on each plot """
    
    from Baseball import strikezone 
    zone_dict = strikezone.get_50pct_zone(year) 
    
    fig, ((ax1, ax2),(ax3,ax4),(ax5,ax6),
          (ax7,ax8),(ax9,ax10),(ax11,ax12)) = plt.subplots(6,2,figsize=(8,20), facecolor='white')
    # Plot the strike zone on each plot
    for ax in (ax1,ax3,ax5,ax7,ax9,ax11):
        ax.plot(zone_dict['xLs'], zone_dict['yLs'], linewidth=2, color='grey') 
        ax.set_ylabel('Height (feet)')
    for ax in (ax2,ax4,ax6,ax8,ax10,ax12):
        ax.plot(zone_dict['xRs'], zone_dict['yRs'], linewidth=2, color='grey')  
        ax.set_ylabel('')
        ax.set_yticklabels([])
    
    for ax in (ax1, ax2, ax3,ax4,ax5,ax6,ax7,ax8,ax9,ax10,ax11,ax12):
        ax.set_ylim(0,5) 
        ax.set_xlim(-2.5,2.5) 
    for ax in (ax11,ax12):
        ax.set_xlabel('Distance from center of plate (feet)') 
    
    ax1.text(-2.3, 0.2, '@soshbaseball', fontsize=12, alpha=0.8)

    plt.tight_layout()
    return (fig,((ax1,ax2),(ax3,ax4),(ax5,ax6),(ax7,ax8),(ax9,ax10),(ax11,ax12)))
    
    
def show_batter(ax, stand, xyl=[1.35, 2], xyr=[-1.35, 2], zoom=0.17,
                img_folder_l='/Users/iayork/Downloads',
                img_file_l='lefty_trace_d.png',
                img_folder_r='/Users/iayork/Downloads',
                img_file_r='righty_trace_d.png') :

    # img_folder_l="/Users/iayork/Documents/Baseball",
    # img_file_l="Batter_Silhouette_LHB_2.png",
    # img_folder_r="/Users/iayork/Documents/Baseball",
    # img_file_r="Batter_Silhouette_RHB_2.png")
    
    from matplotlib.offsetbox import OffsetImage, AnnotationBbox
    from matplotlib._png import read_png
    import os.path
     
    if stand=='L':
        img = read_png(os.path.join(img_folder_l, img_file_l))
        xy = xyl
    elif stand=='R':
        img = read_png(os.path.join(img_folder_r, img_file_r))
        xy = xyr
    imgbox = OffsetImage(img,  zoom=zoom, alpha=0.2)
    ab = AnnotationBbox(imgbox, xy=xy, xycoords='data', frameon=False)
    ax.add_artist(ab)


def basic_plot_batter(stand, year=2016):
    """
    Visualize the strike zone from the umpire's view for a batter
    Two charts, one for LHP, one for RHP
    Plot the de facto strike zone for the year on each plot """

    from Baseball import strikezone 
    zone_dict = strikezone.get_50pct_zone(year) 
    
    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(11.5,6), facecolor='white')

    if stand == 'L':
        ax1.plot(zone_dict['xLs'], zone_dict['yLs'], linestyle='-', linewidth=2, color='grey') 
        ax2.plot(zone_dict['xLs'], zone_dict['yLs'], linestyle='-', linewidth=2, color='grey') 
    elif stand == 'S':
        ax1.plot(zone_dict['xRs'], zone_dict['yRs'], linestyle='-', linewidth=2, color='grey') 
        ax2.plot(zone_dict['xLs'], zone_dict['yLs'], linestyle='-', linewidth=2, color='grey') 
    else: 
        ax1.plot(zone_dict['xRs'], zone_dict['yRs'], linestyle='-', linewidth=2, color='grey')
        ax2.plot(zone_dict['xRs'], zone_dict['yRs'], linestyle='-', linewidth=2, color='grey')

    ax1.set_xlim(-2.5,2.5)
    ax1.set_ylim(0,5)
    ax1.set_ylabel('Strike zone height')
    ax1.set_xlabel('Distance from center of home plate')

    ax2.set_xlim(-2.5,2.5)
    ax2.set_ylim(0, 5)
    ax2.set_ylabel('')
    ax2.set_yticklabels([])
    ax2.set_xlabel('Distance from center of home plate')
    
    plt.tight_layout()
    
    return (fig, ax1,ax2)


def plot_3D(df, ptypes=None, output_dir='/Users/iayork/Downloads', output_folder='ptch3D'):
    """
    3D scatter plot of pitches, colored by pitch type
    Generates a series of plots, rotating 5 o each time (convert to GIF using ImageMacgick)
    
    Input: Dataframe containing PITCHf/x data
    Optional:
        ptypes: If only want to plot a subset of the pitch types in the dataframe
        output_dir, output_folder - Where to save the output charts 
    
    """
    from math import floor, ceil
    import os
    import Baseball
    ptype_clrs = Baseball.ptype_clrs
    
    try:
        folder = os.path.join(output_dir, output_folder)
        os.mkdir(folder)
    except OSError:
        pass  
        
    min_speed = floor(df['start_speed'].min()/10)*10
    max_speed = ceil(df['start_speed'].max()/10)*10
    
    if ptypes == None:
        ptypes = df['pitch_type'].unique()

    ax1 = plt.subplot(111, projection='3d', axisbg='white')
    #ax1.set_zlim(min_speed, max_speed)
    f = 0
    az = 0
    label = True
    pos = True
    
    while True:
        i = 0
        for ptype in ptypes:
            if label:
                ax1.scatter(xs=df[df['pitch_type']==ptype]['pfx_x'],
                            ys=df[df['pitch_type']==ptype]['pfx_z'], 
                            zs=df[df['pitch_type']==ptype]['start_speed'],
                            c=ptype_clrs[ptype], alpha=0.6, s=50, 
                            label=ptype)
            else:
                ax1.scatter(xs=df[df['pitch_type']==ptype]['pfx_x'],
                            ys=df[df['pitch_type']==ptype]['pfx_z'], 
                            zs=df[df['pitch_type']==ptype]['start_speed'],
                            c=ptype_clrs[ptype], alpha=0.6, s=50)
            i += 1
        label = False

        ax1.set_xlabel('\nHorizontal movement')
        ax1.set_ylabel('\nVertical movement')
        ax1.set_zlabel('\nSpeed')

        ax1.view_init(elev=20, azim=az)
        if pos:
            az += 5
            if az >= 90:
                pos = False
        else:
            az -= 5
            if az < 0:
                break
    
        ax1.legend(bbox_to_anchor=(1,1)) ; 
        f += 1 
        plt.savefig(os.path.join(output_dir, output_folder, '3D_chars%02d.png' % f), 
                    bbox_inches='tight', 
                    pad_inches=0.2, 
                    dpi=200)


    

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
    
def cmapBlRd(median):
    """Diverging cmap blue->red centered on "median" value"""

    cdictBlRdDvg = {'red': ((0.0, 0.15, 0.15),
                         (median, 0.865, 0.865),
                         (1.0, 0.706, 0.706)),
                'blue': ((0.0, 0.706, 0.706),
                          (median, 0.865, 0.865),
                          (1.0, 0.016, 0.016)),
                'green': ((0.0, 0.16, 0.16),
                         (median, 0.865, 0.865),
                         (1.0, 0.150, 0.150))}

    cmBlRdDvg = mpl.colors.LinearSegmentedColormap('Bl_Rd_Diverging_CMAP', cdictBlRdDvg)
    return cmBlRdDvg
    
    
def cmapBlRd_bright(median):
    """Diverging cmap blue->red centered on "median" value
       Using the same brighter colors as the matplotlib bwr cmap"""

    cdictBlRdDvg = {'red': ((0.0, 0.0, 0.0),
                         (median, 0.996, 0.996),
                         (1.0, 1, 1)),
                'blue': ((0.0, 1, 1),
                          (median, 0.996, 0.996),
                          (1.0, 0.008, 0.008)),
                'green': ((0.0, 0.0, 0.0),
                         (median, 0.996, 0.996),
                         (1.0, 0.008, 0.008))}

    cmBlRdDvg = mpl.colors.LinearSegmentedColormap('Bl_Rd_Diverging_CMAP', cdictBlRdDvg)
    return cmBlRdDvg
    
    
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool


def scatter_with_hover(df, x, y,
                       fig=None, cols=None, name=None, marker='x',
                       fig_width=500, fig_height=500, **kwargs):
    """
    http://blog.rtwilson.com/bokeh-plots-with-dataframe-based-tooltips/
    Plots an interactive scatter plot of `x` vs `y` using bokeh, with automatic
    tooltips showing columns from `df`.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing the data to be plotted
    x : str
        Name of the column to use for the x-axis values
    y : str
        Name of the column to use for the y-axis values
    fig : bokeh.plotting.Figure, optional
        Figure on which to plot (if not given then a new figure will be created)
    cols : list of str
        Columns to show in the hover tooltip (default is to show all)
    name : str
        Bokeh series name to give to the scattered data
    marker : str
        Name of marker to use for scatter plot
    **kwargs
        Any further arguments to be passed to fig.scatter

    Returns
    -------
    bokeh.plotting.Figure
        Figure (the same as given, or the newly created figure)

    Example
    -------
    fig = scatter_with_hover(df, 'A', 'B')
    show(fig)

    fig = scatter_with_hover(df, 'A', 'B', cols=['C', 'D', 'E'], marker='x', color='red')
    show(fig)

    Author
    ------
    Robin Wilson <robin@rtwilson.com>
    with thanks to Max Albert for original code example
    """

    # If we haven't been given a Figure obj then create it with default
    # size etc.
    if fig is None:
        fig = figure(width=fig_width, height=fig_height, tools=['box_zoom', 'reset'])

    # We're getting data from the given dataframe
    source = ColumnDataSource(data=df)

    # We need a name so that we can restrict hover tools to just this
    # particular 'series' on the plot. You can specify it (in case it
    # needs to be something specific for other reasons), otherwise
    # we just use 'main'
    if name is None:
        name = 'main'

    # Actually do the scatter plot - the easy bit
    # (other keyword arguments will be passed to this function)
    fig.scatter(df[x], df[y], source=source, name=name, marker=marker, **kwargs)

    # Now we create the hover tool, and make sure it is only active with
    # the series we plotted in the previous line
    hover = HoverTool(names=[name])

    if cols is None:
        # Display *all* columns in the tooltips
        hover.tooltips = [(c, '@' + c) for c in df.columns]
    else:
        # Display just the given columns in the tooltips
        hover.tooltips = [(c, '@' + c) for c in cols]

    hover.tooltips.append(('index', '$index'))

    # Finally add/enable the tool
    fig.add_tools(hover)

    return fig