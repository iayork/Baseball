"""
class Strikezone(object):
    def __init__(self):
    def official_zone(self):
    def get_x_list(self):
    def get_y_list(self):
    def get_std_zone(self): 
    def get_new_zone(self):
    def get_50pct_zone(self, year=2014):
        

class Utilities(Strikezone):
    def __init__(self): 
    def circles(self, x, y, s, c, ax, vmin, vmax, **kwargs):
    def setup_basic_plot(self, pitches, pytpe):
    def con(self, dbpath):  
    def query(self, sql_query, con):
    def annot_font(self):
    def small_font(self):
    def cmapGnRd(self): 
    def cmapGyRd(self): 
    def cmapGyGn(self):  
    def pitch_abbrs(self):
    
    plus all Strikezone via inheritance
        
        
class Zone(Strikezone):
    def __init__(self, df, x_num, y_num): 
    def getxy(self, x_num, y_num):
    def get_pitches(self, df): 
    def get_hits_in_zone(self, df):
    def get_center_point(self):
    def get_color(self, clrs): 
    def get_annot(self): 
    
    plus all Strikezone via inheritance


class Pitch(object):
    def __init__(self, df_row):
    def calculate_pitch(self, vy0, vx0, vz0, ay, az, ax, z0, x0, y0 ):

"""


class Strikezone(object):
    """
    class Strikezone(object):
        def __init__(self):
        def official_zone(self):
        def get_x_list(self):
        def get_y_list(self):
        def get_std_zone(self): 
        def get_new_zone(self):
        def get_50pct_zone(self, year=2014):

    """
    def __init__(self):
        pass
        
    def official_zone(self):
        self.sz_left = -1.66/2
        self.sz_right = 1.66/2
        self.x_step = (self.sz_right - self.sz_left)/3.0
        self.leftmost = (self.sz_left - self.x_step)
        self.rightmost = (self.sz_right + self.x_step)
        
        self.sz_bottom = 1.58
        self.sz_top = 3.4
        self.y_step = (self.sz_top - self.sz_bottom)/3.0
        self.bottommost = (self.sz_bottom - self.y_step)
        self.topmost = (self.sz_top + self.y_step)
    
    def get_x_list(self):
        return [self.leftmost + (i * self.x_step) for i in range(5)]
    
    def get_y_list(self):
        return [self.bottommost + (i * self.y_step) for i in range(5)]
    
    def get_std_zone(self): 
        self.official_zone()    
        szx = [self.sz_left, self.sz_left, self.sz_right, self.sz_right, self.sz_left]
        szy = [3.4, 1.75, 1.75, 3.4, 3.4]
        return {'szx':szx, 'szy':szy}
    
    def get_new_zone(self):
        szy2 = [self.sz_top, self.sz_bottom, self.sz_bottom, self.sz_top, self.sz_top]
        return {'szx':self.szx, 'szy':szy2}
        
    def get_50pct_zone(self, year=2015):
        # Outside the points the chance of a ball vs. a called strike is > 50%
        
        # 50% strike zone (zone outside of which there is >50% chance a pitch will be called a ball vs. a strike)
        # From "Strike zone quartiles league-wide.ipynb"

        k_zoneL_2008 = [(-1.0, 1.75), (-1.125, 1.875), (-1.125, 2.0), (-1.25, 2.125), (-1.25, 2.25), (-1.25, 2.375), (-1.25, 2.5), 
                        (-1.25, 2.625), (-1.25, 2.75), (-1.125, 2.875), (-1.125, 3.0), (-1.0, 3.125), (-0.75, 3.25), (0.5, 3.25), 
                        (0.625, 3.125), (0.75, 3.0), (0.75, 2.875), (0.875, 2.75), (0.875, 2.625), (0.875, 2.5), (0.875, 2.375), 
                        (0.875, 2.25), (0.75, 2.125), (0.75, 2.0), (0.625, 1.875), (0.375, 1.75), (-1.0, 1.75)]
        k_zoneR_2008 = [(-0.625, 1.75), (-0.875, 1.875), (-1.0, 2.0), (-1.0, 2.125), (-1.0, 2.25), (-1.0, 2.375), (-1.0, 2.5), 
                        (-1.0, 2.625), (-1.0, 2.75), (-1.0, 2.875), (-1.0, 3.0), (-0.875, 3.125), (-0.75, 3.25), (-0.5, 3.375), 
                        (0.625, 3.25), (0.875, 3.125), (0.875, 3.0), (1.0, 2.875), (1.0, 2.75), (1.0, 2.625), (1.0, 2.5), 
                        (1.0, 2.375), (1.0, 2.25), (1.0, 2.125), (1.0, 2.0), (0.875, 1.875), (0.75, 1.75), (-0.625, 1.75)]


        k_zoneL_2009 = [(-1.0, 1.75), (-1.125, 1.875), (-1.25, 2.0), (-1.25, 2.125), (-1.25, 2.25), (-1.25, 2.375), (-1.25, 2.5), 
                        (-1.25, 2.625), (-1.25, 2.75), (-1.125, 2.875), (-1.125, 3.0), (-1.0, 3.125), (-0.875, 3.25), (0.5, 3.25), 
                        (0.625, 3.125), (0.75, 3.0), (0.75, 2.875), (0.875, 2.75), (0.875, 2.625), (0.875, 2.5), (0.75, 2.375), 
                        (0.75, 2.25), (0.75, 2.125), (0.625, 2.0), (0.625, 1.875), (0.375, 1.75), (-1.0, 1.75)]

        k_zoneR_2009 = [(-0.625, 1.75), (-0.875, 1.875), (-1.0, 2.0), (-1.0, 2.125), (-1.0, 2.25), (-1.0, 2.375), (-1.0, 2.5), 
                        (-1.0, 2.625), (-1.0, 2.75), (-1.0, 2.875), (-1.0, 3.0), (-0.875, 3.125), (-0.75, 3.25), (-0.25, 3.375), 
                        (0.625, 3.25), (0.75, 3.125), (0.875, 3.0), (1.0, 2.875), (1.0, 2.75), (1.0, 2.625), (1.0, 2.5), 
                        (1.0, 2.375), (1.0, 2.25), (1.0, 2.125), (0.875, 2.0), (0.875, 1.875), (0.625, 1.75), (-0.625, 1.75)]

        k_zoneL_2010 = [(-1.0, 1.75), (-1.125, 1.875), (-1.125, 2.0), (-1.25, 2.125), (-1.25, 2.25), (-1.25, 2.375), (-1.25, 2.5), 
                        (-1.25, 2.625), (-1.125, 2.75), (-1.125, 2.875), (-1.0, 3.0), (-1.0, 3.125), (-0.75, 3.25), (-0.125, 3.375), 
                        (0.5, 3.25), (0.625, 3.125), (0.75, 3.0), (0.75, 2.875), (0.75, 2.75), (0.75, 2.625), (0.75, 2.5), 
                        (0.75, 2.375), (0.75, 2.25), (0.75, 2.125), (0.75, 2.0), (0.625, 1.875), (0.375, 1.75), (-1.0, 1.75)]

        k_zoneR_2010 = [(-0.625, 1.75), (-0.875, 1.875), (-1.0, 2.0), (-1.0, 2.125), (-1.0, 2.25), (-1.0, 2.375), (-1.0, 2.5), 
                        (-1.0, 2.625), (-1.0, 2.75), (-1.0, 2.875), (-0.875, 3.0), (-0.875, 3.125), (-0.625, 3.25), (0.625, 3.25), 
                        (0.875, 3.125), (0.875, 3.0), (1.0, 2.875), (1.0, 2.75), (1.0, 2.625), (1.0, 2.5), (1.0, 2.375), 
                        (1.0, 2.25), (1.0, 2.125), (1.0, 2.0), (0.875, 1.875), (0.75, 1.75), (-0.625, 1.75)]


        k_zoneL_2011 = [(-0.875, 1.625), (-1.0, 1.75), (-1.125, 1.875), (-1.125, 2.0), (-1.125, 2.125), (-1.25, 2.25), 
                        (-1.25, 2.375), (-1.125, 2.5), (-1.125, 2.625), (-1.125, 2.75), (-1.125, 2.875), (-1.125, 3.0), 
                        (-1.0, 3.125), (-0.875, 3.25), (-0.5, 3.375), (0.25, 3.375), (0.625, 3.25), (0.625, 3.125), (0.75, 3.0), 
                        (0.75, 2.875), (0.75, 2.75), (0.875, 2.625), (0.875, 2.5), (0.875, 2.375), (0.875, 2.25), (0.75, 2.125), 
                        (0.75, 2.0), (0.625, 1.875), (0.5, 1.75), (-0.875, 1.625)]

        k_zoneR_2011 = [(-0.25, 1.625), (-0.75, 1.75), (-0.875, 1.875), (-1.0, 2.0), (-1.0, 2.125), (-1.0, 2.25), (-1.0, 2.375), 
                        (-1.0, 2.5), (-1.0, 2.625), (-1.0, 2.75), (-1.0, 2.875), (-1.0, 3.0), (-0.875, 3.125), (-0.75, 3.25), 
                        (-0.5, 3.375), (0.25, 3.375), (0.625, 3.25), (0.75, 3.125), (0.875, 3.0), (1.0, 2.875), (1.0, 2.75), 
                        (1.0, 2.625), (1.0, 2.5), (1.0, 2.375), (1.0, 2.25), (1.0, 2.125), (0.875, 2.0), (0.875, 1.875), 
                        (0.75, 1.75), (0.5, 1.625), (-0.25, 1.625)]

        k_zoneL_2012 = [(-1.0, 1.625), (-1.125, 1.75), (-1.125, 1.875), (-1.125, 2.0), (-1.25, 2.125), (-1.25, 2.25), 
                        (-1.25, 2.375), (-1.125, 2.5), (-1.125, 2.625), (-1.125, 2.75), (-1.125, 2.875), (-1.0, 3.0), 
                        (-0.875, 3.125), (-0.75, 3.25), (0.125, 3.375), (0.5, 3.25), (0.625, 3.125), (0.75, 3.0), 
                        (0.75, 2.875), (0.75, 2.75), (0.75, 2.625), (0.875, 2.5), (0.875, 2.375), (0.75, 2.25), (0.75, 2.125), 
                        (0.75, 2.0), (0.75, 1.875), (0.625, 1.75), (0.25, 1.625), (-1.0, 1.625)]

        k_zoneR_2012 = [(-0.625, 1.625), (-0.875, 1.75), (-1.0, 1.875), (-1.0, 2.0), (-1.0, 2.125), (-1.0, 2.25), (-1.0, 2.375), 
                        (-1.0, 2.5), (-1.0, 2.625), (-1.0, 2.75), (-1.0, 2.875), (-0.875, 3.0), (-0.875, 3.125), (-0.75, 3.25), 
                        (-0.375, 3.375), (0.625, 3.25), (0.75, 3.125), (0.875, 3.0), (0.875, 2.875), (1.0, 2.75), (1.0, 2.625), 
                        (1.0, 2.5), (1.0, 2.375), (1.0, 2.25), (1.0, 2.125), (1.0, 2.0), (0.875, 1.875), (0.875, 1.75), 
                        (0.625, 1.625), (-0.625, 1.625)]

        k_zoneL_2013 = [(-0.375, 1.5), (-1.0, 1.625), (-1.125, 1.75), (-1.125, 1.875), (-1.125, 2.0), (-1.125, 2.125), 
                        (-1.125, 2.25), (-1.125, 2.375), (-1.125, 2.5), (-1.125, 2.625), (-1.0, 2.75), (-1.0, 2.875), 
                        (-1.0, 3.0), (-0.875, 3.125), (-0.75, 3.25), (-0.25, 3.375), (0.125, 3.375), (0.5, 3.25), 
                        (0.75, 3.125), (0.75, 3.0), (0.75, 2.875), (0.75, 2.75), (0.75, 2.625), (0.875, 2.5), (0.875, 2.375), (0.875, 2.25), (0.75, 2.125), (0.75, 2.0), (0.75, 1.875), (0.625, 1.75), (0.375, 1.625), (-0.375, 1.5)]

        k_zoneR_2013 = [(-0.625, 1.625), (-0.875, 1.75), (-1.0, 1.875), (-1.0, 2.0), (-1.0, 2.125), (-1.0, 2.25), 
                        (-1.0, 2.375), (-1.0, 2.5), (-1.0, 2.625), (-1.0, 2.75), (-1.0, 2.875), (-1.0, 3.0), (-0.875, 3.125), 
                        (-0.75, 3.25), (-0.375, 3.375), (0.625, 3.25), (0.75, 3.125), (0.875, 3.0), (0.875, 2.875), (1.0, 2.75), 
                        (1.0, 2.625), (1.0, 2.5), (1.0, 2.375), (1.0, 2.25), (1.0, 2.125), (1.0, 2.0), (0.875, 1.875), 
                        (0.875, 1.75), (0.75, 1.625), (-0.625, 1.625)]

        k_zoneL_2014 = [(-0.875, 1.5), (-1.0, 1.625), (-1.0, 1.75), (-1.125, 1.875), (-1.125, 2.0), (-1.125, 2.125), 
                       (-1.125, 2.25), (-1.125, 2.375), (-1.125, 2.5), (-1.125, 2.625), (-1.125, 2.75), (-1.0, 2.875), 
                       (-1.0, 3.0), (-0.875, 3.125), (-0.75, 3.25), (-0.125, 3.375), (0.5, 3.25), (0.625, 3.125), 
                       (0.75, 3.0), (0.75, 2.875), (0.75, 2.75), (0.75, 2.625), (0.75, 2.5), (0.75, 2.375), (0.75, 2.25), 
                       (0.75, 2.125), (0.75, 2.0), (0.75, 1.875), (0.625, 1.75), (0.5, 1.625), (0.25, 1.5), (-0.875, 1.5), 
                       (-0.875, 1.5), (-0.875, 1.5)]

        k_zoneR_2014 = [(-0.375, 1.5), (-0.875, 1.625), (-0.875, 1.75), (-1.0, 1.875), (-1.0, 2.0), (-1.0, 2.125), 
                       (-1.0, 2.25), (-1.0, 2.375), (-1.0, 2.5), (-1.0, 2.625), (-1.0, 2.75), (-1.0, 2.875), (-0.875, 3.0), 
                       (-0.875, 3.125), (-0.75, 3.25), (-0.375, 3.375), (0.5, 3.25), (0.75, 3.125), (0.875, 3.0), 
                       (0.875, 2.875), (0.875, 2.75), (1.0, 2.625), (1.0, 2.5), (1.0, 2.375), (1.0, 2.25), (1.0, 2.125), 
                       (1.0, 2.0), (0.875, 1.875), (0.875, 1.75), (0.75, 1.625), (0.625, 1.5), (-0.375, 1.5)]
                       
        k_zoneL_2015 = [(-0.875,1.5), (-1.0,  1.6), (-1.1, 1.875), (-1.05, 2.75), (-1.0,   3.0), (-0.86, 3.28), 
                        (-0.115,3.45), (0.55,3.3), (0.75,3.0),  (0.8,2.875), (0.8,2.125), (0.75,2.0), (0.625,1.75), 
                        (0.5,1.625), (0.25,1.5), (-0.25,1.45), (-0.875, 1.5)]
 
		k_zoneR_2015 = [(-0.375,1.5), (-0.875, 1.625), (-.975, 1.875), (-1.0, 2.175), (-.975, 2.875), (-0.87, 3.125), 
		                (-0.75, 3.325), (-0.375,3.45), (0.5, 3.375), (0.825, 3.175), (.97, 2.875), (.97, 2.75), 
		                (.97, 2.625), (.97, 2.5), (.97, 2.375), (.97, 2.25), (.97, 2.125), (.97, 2.0), (0.9, 1.75), 
		                (0.6, 1.5), -0.375, 1.5)]

        zoneD = {2008:(k_zoneL_2008, k_zoneR_2008),
                 2009:(k_zoneL_2009, k_zoneR_2009),
                 2010:(k_zoneL_2010, k_zoneR_2010),
                 2011:(k_zoneL_2011, k_zoneR_2011),
                 2012:(k_zoneL_2012, k_zoneR_2012),
                 2013:(k_zoneL_2013, k_zoneR_2013),
                 2014:(k_zoneL_2014, k_zoneR_2014), 
                 2015:(k_zoneL_2015, k_zoneR_2015)}
        
        (k_zoneL, k_zoneR) = zoneD[year]
        return {'xLs': [x[0] for x in k_zoneL],
                'yLs': [x[1] for x in k_zoneL],
                'xRs': [x[0] for x in k_zoneR],
                'yRs': [x[1] for x in k_zoneR]} 
        

class Utilities(Strikezone):
    """ 
    class Utilities(Strikezone):
        def __init__(self): 
        def circles(self, x, y, s, c, ax, vmin, vmax, **kwargs):
        def setup_basic_plot(self, pitches, pytpe):
        def con(self, dbpath):  
        def query(self, sql_query, con):
        def annot_font(self):
        def small_font(self):
        def cmapGnRd(self): 
        def cmapGyRd(self): 
        def cmapGyGn(self):  
        def pitch_abbrs(self):
        
        
    class Zone(Strikezone):
        def __init__(self, df, x_num, y_num): 
        def getxy(self, x_num, y_num):
        def get_pitches(self, df): 
        def get_hits_in_zone(self, df):
        def get_center_point(self):
        def get_color(self, clrs): 
        def get_annot(self): 


    class Pitch(object):
        def __init__(self, df_row):
        def calculate_pitch(self, vy0, vx0, vz0, ay, az, ax, z0, x0, y0 ):

    """


    def __init__(self): 
        
        Strikezone.__init__(self) 
        
        self.y_plate = 1.417  
        self.az_noair = -32.174 
        self.ax_noair = 0  
        
    def pitchab_for_pitcher(pitcher_name, con):
        atbat_sql = """select pitcher_name, batter_name, gameday_link, num, stand, inning, 
        inning_side from atbat where pitcher_name = "%s" """ % pitcher_name

        pitch_sql = """select gameday_link, num, id, vy0,  vx0,  vz0, ax,  ay,  az,  
        x0,  y0,  z0, px,  pz, break_length, pitch_type, des from pitch where gameday_link in 
        (select gameday_link from atbat where pitcher_name = "%s") """ % pitcher_name

        atbat = pdsql.read_sql(atbat_sql, con)
        pitch = pdsql.read_sql(pitch_sql, con)
    
        pitchab = pitch.merge(atbat, on=['gameday_link','num'])
    
        #pitchab = pitchab.dropna(how='any')
    
        return pitchab
        
        
    def circles(self, x, y, s, c, ax, vmin, vmax, **kwargs):
        from matplotlib.patches import Circle
        from matplotlib.collections import PatchCollection 
        import numpy as np

        #http://stackoverflow.com/questions/9081553/python-scatter-plot-size-and-style-of-the-marker 
    
        patches = [Circle((x_,y_), s_) for x_,y_,s_ in zip(x,y,s)]
        collection = PatchCollection(patches, **kwargs)
 
        collection.set_array(np.asarray(c))
        collection.set_clim(vmin, vmax)

        ax.add_collection(collection)
        return collection 
        
    def circle(x, y, s, ax, c, fc='white', ec='dimgray', **kwargs):

        #http://stackoverflow.com/questions/9081553/python-scatter-plot-size-and-style-of-the-marker 
 
        kwargs.update(facecolor=fc,linewidth=0.25, 
                      edgecolor=ec, linestyle='-', antialiased=True) 
    
        patches = [Circle((x_,y_), s_) for x_,y_,s_ in zip(x,y,s)] 
        collection = PatchCollection(patches, **kwargs)

        ax.add_collection(collection)
        return collection        
        
        
    def setup_basic_plot(self, pitches, pytpe):
        if pitch14ab2['p_throws'].values[0] == 'R':
            xlims = (-3,2)
        else:
            xlims = (-2,3)  
    
        fig, (ax1, ax2) = plt.subplots(1,2,figsize=(13,6))
    
        for ax in (ax1, ax2):
            ax.set_ylim(0,7.5) 
            ax.set_xlim(xlims)   
            ax.plot(szx, szy, linestyle='-', linewidth=1, color=dark[0])
            ax.plot(szx, szy2, linestyle='--', linewidth=1, color=dark[0]) 
            ax.set_xlabel('Distance from home plate center (feet)')
    
        avgmphR = np.array([x.mph for x in pitches if x.stand=='R']).mean()
        avgmphL = np.array([x.mph for x in pitches if x.stand=='L']).mean()
        countR = len([x for x in pitches if x.stand=='R'])
        countL = len([x for x in pitches if x.stand=='L'])
    
        ax1.text(-0.5, 6, '%s: %.1f mph avg\nLHB (%i thrown)' % (ptype, avgmphL, countL) , font) 
        ax1.set_ylabel('Height (feet)')   

        ax2.text(-0.5, 6, '%s: %.1f mph avg\nRHB (%i thrown)' % (ptype, avgmphR, countR) , font)
    

        ax2.set_ylabel('') 
        ax2.set_yticklabels([]) 

        plt.tight_layout()
        return (fig,ax1, ax2)
        
    def con(self, dbpath):
        import sqlite3 as sql
        import pandas.io.sql as pdsql 
        if type(dbpath) == list:
            cons = []
            for dbp in dbpath:
                cons.append(sql.connect(dbpath))
                return cons
        else:
            con = sql.connect(dbpath) 
            return con
            
    def query(self, sql_query, con):
        import sqlite3 as sql
        import pandas.io.sql as pdsql 
        return pdsql.read_sql(sql_query, con)

    def large_font(self):   
        font = {'family' : 'sans',
                'color'  : 'dimgray',
                'weight' : 'normal',
                'size'   : 16,
                }
        return font

    def medium_font(self):  
        font = {'family' : 'sans',
                'color'  : 'dimgray',
                'weight' : 'normal',
                'size'   : 12,
                }
        return font
        
    def small_font(self):
        font = {'family' : 'sans',
                'color'  : 'dimgray',
                'weight' : 'normal',
                'size'   : 10,
                      }
        return font
        
    def cmapGnRd(self): 
        import matplotlib as mpl
        cdictGnRd = {'red': ((0.0, 0.4, 0.4),
                             (1.0, 0.9, 0.9)),
                    'green': ((0.0, 0.9, 0.9),
                              (1.0, 0.2, 0.2)),
                    'blue': ((0.0, 0.2, 0.2),
                             (1.0, 0.2, 0.2))}

        cmapGnRd = mpl.colors.LinearSegmentedColormap('my_colormap', cdictGnRd)
        return cmapGnRd
        
    def cmapGyRd(self):  
        import matplotlib as mpl
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
        
    def cmapGyGn(self):  
        import matplotlib as mpl
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
        
    def pitch_abbrs(self):
        pitch_abbrs = {'FT':'Two-seam fastball',
                        'CH':'Changeup',
                        'SL':'Slider',
                        'FF':'Four-seam fastball',
                        'CU':'Curve',
                        'SI':'Sinker',
                        'FC':'Cut fastball',
                        'FS':'Split-finger fastball',
                        'FA':'Fastball',
                        'KC':'Knuckle curve',
                        'PO':'Pitchout',
                        'EP':'Eephus',
                        'IN':'Intentional ball',
                        'SC':'Screwball',
                        'FO':'Forkball',
                        'KN':'Knuckleball',
                        'UN':'Unknown',
                        'AB':'Automatic ball'}
        return pitch_abbrs
        
        
        
class Zone(Strikezone):
    """ 
    class Zone(Strikezone):
        def __init__(self, df, x_num, y_num): 
        def getxy(self, x_num, y_num):
        def get_pitches(self, df): 
        def get_hits_in_zone(self, df):
        def get_center_point(self):
        def get_color(self, clrs): 
        def get_annot(self): 


    class Pitch(object):
        def __init__(self, df_row):
        def calculate_pitch(self, vy0, vx0, vz0, ay, az, ax, z0, x0, y0 ):

    """
    def __init__(self, df, x_num, y_num): 
        
        Strikezone.__init__(self)
        self.getxy(x_num, y_num) 
        self.get_hits_in_zone(df)
        
        self.x_list = self.get_x_list()
        self.y_list = self.get_y_list()
        
    def getxy(self, x_num, y_num):
        self.x = self.x_list[x_num]
        self.y = self.y_list[y_num]
        
    def get_pitches(self, df): 
        
        pitches_in_zoneDF = df[(df['px'] >= self.x) & 
                               (df['px'] < self.x + self.x_step) &
                               (df['pz'] >= self.y) &
                               (df['pz'] < self.y + self.y_step) ]
        
        self.pitches_in_zone_pct = len(pitches_in_zoneDF)/len(df) * 100.0
        return (pitches_in_zoneDF)
        
    def get_hits_in_zone(self, df):
        hit_des = ['In play, no out','In play, run(s)']
        pitches_in_zoneDF = self.get_pitches(df)
        hits_in_zoneDF = pitches_in_zoneDF[pitches_in_zoneDF['des'].isin(hit_des)]
        try:
            self.hits_pct = len(hits_in_zoneDF)/len(pitches_in_zoneDF) * 100.0 
        except ZeroDivisionError:
            self.hits_pct = 0
        
    def get_center_point(self):
        x_point = self.x + (self.x_step/2.0)
        y_point = self.y + (self.y_step/2.0)
        return(x_point, y_point)
        
    def get_color(self, clrs): 
        try:
            clr = clrs[floor(self.hits_pct/2)]
        except IndexError:
            clr = clrs[-1]
        return(clr) 
    
    def get_annot(self):
        txt = "%.1f%% (%.1f%%)" % (self.pitches_in_zone_pct, self.hits_pct) 
        txt_x = self.x + self.x_step * 0.2
        txt_y = self.y + self.y_step * 0.8
        return ((txt, txt_x, txt_y))



class Pitch(object):

    def __init__(self, df):
    
        self.az_noair = -32.174 
        self.ax_noair = 0  
        
        # Take arrays of values from dataframe
        
        import pandas as pd
        
        assert isinstance(df, pd.DataFrame), "Must pass a dataframe"
        
        self.pitch_params = ('vy0', 'vx0', 'vz0', 'ay','az', 'ax', 'z0', 'x0',
                             'stand', 'pitch_type')
        
        self.param_dict = {}
        for pitch_param in self.pitch_params:
            self.param_dict[pitch_param] = df[pitch_param].values  
        
        assert  max([len(self.param_dict[x]) for x in self.pitch_params]) == \
                min([len(self.param_dict[x]) for x in self.pitch_params]) , \
                "Not all the same counts for pitch params"
         
        
    def get_average_pitch(self):
        # Convert array of values to average, return as dict
        mean_param_dict = {}
        for pitch_param in self.pitch_params:
            mean_param_dict[pitch_param] = self.mean95(self.param_dict[pitch_param]) 
        
        return mean_param_dict
        
    def get_random_pitch(self, n_random=1):
        # n_random is number of random pitches to return
        import random
        random_pitch_list = []
        for i in range(n_random):
            # Take a pseudo-random pitch from an array of values, return as dict
            n = random.randint(1, len(self.param_dict['vy0'])-1)  
            random_param_dict = {}
            for pitch_param in self.pitch_params:
                random_param_dict[pitch_param] = self.param_dict[pitch_param][n]
            random_pitch_list.append(random_param_dict)
        
        if n_random == 1: 
            return random_param_dict
        else:
            return random_pitch_list
    
    def get_specific_pitch(self):
        # the dataframe passed was a single row. Convert it to a dict of parameters
        assert len(self.param_dict[self.pitch_params[0]]) == 1, "The info is not a single row of a dataframe"  
        
        specific_param_dict = {}
        for pitch_param in self.pitch_params:
            specific_param_dict[pitch_param] = self.param_dict[pitch_param][0]  
        
        return specific_param_dict
        
        
    def mean95(self, arr):
        # Calculate the mean of the center 95% of an array, discarding outliers
        arr_s = np.sort(arr)
        outer5 = floor(.025 * len(arr_s)) 
        if outer5 != 0:
            return arr_s[outer5:-outer5].mean()
        else:
            return arr_s.mean()
        
    def pitch_flight(self, params): 
        import numpy as np
        from math import sqrt
        
        y0 = 50  
        
        # params is a dictionary containing info for a single pitch
        vy0 = params['vy0']  
        vx0 = params['vx0']  
        vz0 = params['vz0']  
        ay = params['ay'] 
        az = params['az'] 
        ax = params['ax'] 
        z0 = params['z0'] 
        x0 = params['x0']  
    
        az_noair = self.az_noair
        ax_noair = self.ax_noair

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

            if y < 1.417:
                break 
                
        return {'z_time':z_time, 
                'x_time':x_time, 
                't_time':t_time,
                'y_time':y_time,
                'z_noair_time':z_noair_time, 
                'x_noair_time':x_noair_time, 
                'mph':mph,
                'mph55':mph55,
                'mphend':mphend}
                
    def get_list_of_params(self):
        # Convert param_dict into a list of specific parameters 
        
        list_of_params = []
        for i in range(len(self.param_dict['ax'])):
            pd = {}
            for pitch_param in self.pitch_params:
                pd[pitch_param] = self.param_dict[pitch_param][i] 
            list_of_params.append(pd)
        return list_of_params  

        
    def pitch_flight_many(self, list_of_params): 
        # Calculate pitch flight for multiple pitches at once; return a list of dicts
        import numpy as np
        from math import sqrt
        
        pitch_flight_list = []
        
        for params in list_of_params:
        
            y0 = 50  
        
            # params is a dictionary containing info for multiple pitches
            vy0 = params['vy0']  
            vx0 = params['vx0']  
            vz0 = params['vz0']  
            ay = params['ay'] 
            az = params['az'] 
            ax = params['ax'] 
            z0 = params['z0'] 
            x0 = params['x0'] 
            stand = params['stand'] 
            ptype = params['pitch_type']
    
            az_noair = self.az_noair
            ax_noair = self.ax_noair

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

                if y < 1.417:
                    break 
                
            pitch_flight_list.append( {'z_time':z_time,
                                       'x_time':x_time, 
                                       't_time':t_time,
                                       'y_time':y_time,
                                       'z_noair_time':z_noair_time, 
                                       'x_noair_time':x_noair_time, 
                                       'mph':mph,
                                       'mph55':mph55,
                                       'mphend':mphend,
                                       'stand':stand,
                                       'ptype':ptype
                                       } )

        return pitch_flight_list