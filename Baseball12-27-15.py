"""
        
        
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
class Baseball(object):
    """ Parent class and misc. functions for baseball
    
    pitch_pcts_per_game 
    
    get_whip
    	usage get_whip(df)
    	WHIP given walks, hits, and inning count
    
    get_erip
    	usage get_erip(df)
    	earned runs per inning given ER and inning count
    	
    get_gb
    
    get_balls
    
    get_outs
    
    get_called
    
    get_swinging
    
    get_fouls

    def get_hits_pxpz

    def get_hits_DF
    
    get_bases_per_pitch

    def get_babip
    
    
    """
    
    def pitch_pcts_per_game(self, df, ptypes):
        usageD = {}
        for gdl in df['gameday_link'].unique():
            usageD[gdl] = {}
            gm = df[df['gameday_link']==gdl] 

            for ptype in ptypes:
                usageD[gdl][ptype] = len(gm[gm['pitch_type']==ptype])/len(gm)*100
        usageDF = self.pd.DataFrame(usageD).T
        usageDF['Dates'] = ['%s-%s-%s' % (x.split('_')[2], 
                           x.split('_')[3], 
                           x.split('_')[1][-2:]) for x in usageDF.index]
        return usageDF

    def __init__(self):
        from importlib import import_module
        self.pd = import_module('pandas')
        self.sql = import_module('sqlite3')
        self.path = import_module('os.path') 
    
                
    def get_whip(self, df):
        return ((df['H']) + (df['BB']))/(df['IP'])
        
    def get_erip(self, df):
    	return df['ER']/df['IP']

    def get_gb(self, df):
        # Ground Ball Percentage (GB%) = Ground Balls / Balls in Play
        inplay = df[df['des'].str.contains('In play')]
        gb = inplay[(inplay['atbat_des'].str.contains('ground')) | (inplay['atbat_des'].str.contains('Ground'))]
        return len(gb)/len(inplay) * 100.0
    
    
    def get_balls(self, df, ptype):
        df2 = df[((df['des'].str.contains('Ball')) |
                  (df['des'].str.contains('Hit By Pitch')) |
                  (df['des']=='Pitchout')) & (df['pitch_type']==ptype)]
        return (df2['px'].values, df2['pz'].values) 

    def get_outs(self, df, ptype):
        p = df[df['pitch_type']==ptype]
        df2 = p[(p['des'].str.contains('In play, out')) |
                ((p['des'].str.contains('In play, no out')) & (p['event'].str.contains('out'))) | 
                ((p['des'].str.contains('In play, no out')) & (p['event'].str.contains('Pop Out'))) | 
                ((p['des'].str.contains('In play, no out')) & (p['event'].str.contains('Fielders Choice'))) | 
                ((p['des'].str.contains('In play, no out')) & (p['event'].str.contains('Error'))) | 
                ((p['des'].str.contains('In play, no out')) & (p['event'].str.contains('Sac Fly'))) |
                ((p['des'].str.contains('In play, no out')) & (p['event'].str.contains('Sac Bunt'))) |
                ((p['des'].str.contains('In play, no out')) & (p['event'].str.contains('nterference'))) |
                ((p['des'].str.contains('In play, no out')) & (p['event'].str.contains('Double Play'))) |
                ((p['des'].str.contains('In play, run')) & (p['event'].str.contains('out'))) | 
                ((p['des'].str.contains('In play, run')) & (p['event'].str.contains('Pop Out'))) | 
                ((p['des'].str.contains('In play, run')) & (p['event'].str.contains('Fielders Choice'))) | 
                ((p['des'].str.contains('In play, run')) & (p['event'].str.contains('Error'))) | 
                ((p['des'].str.contains('In play, run')) & (p['event'].str.contains('Sac Fly'))) |
                ((p['des'].str.contains('In play, run')) & (p['event'].str.contains('Sac Bunt'))) |
                ((p['des'].str.contains('In play, run')) & (p['event'].str.contains('nterference'))) |
                ((p['des'].str.contains('In play, run')) & (p['event'].str.contains('Double Play'))) ]
        return (df2['px'].values, df2['pz'].values)

    def get_called(self, df, ptype):
        df2 = df[(df['des'].str.contains('Called Strike')) & (df['pitch_type']==ptype)]
        return (df2['px'].values, df2['pz'].values)

    def get_swinging(self, df, ptype):
        df2 = df[((df['des'].str.contains('Swinging Strike')) |
                  (df['des'].str.contains('Missed Bunt'))) & (df['pitch_type']==ptype)]
        return (df2['px'].values, df2['pz'].values)

    def get_fouls(self, df, ptype):
        df2 = df[(df['des'].str.contains('Foul')) & (df['pitch_type']==ptype)]
        return (df2['px'].values, df2['pz'].values)

    def get_hits_pxpz(self, df, ptype=None): 
        if ptype is None: 
            p = df.copy()
        else:
            p = df[df['pitch_type']==ptype]
        p2 = p[p['des'].str.contains('In play')]
        df2 = p2[(~p2['des'].str.contains('In play, out')) &
                 (~p2['event'].str.contains('Grounded Into DP')) & 
                 (~p2['event'].str.contains('out')) & 
                 (~p2['event'].str.contains('Pop Out')) & 
                 (~p2['event'].str.contains('Fielders Choice')) & 
                 (~p2['event'].str.contains('Error')) & 
                 (~p2['event'].str.contains('Sac Fly')) &
                 (~p2['event'].str.contains('Sac Bunt')) &
                 (~p2['event'].str.contains('Interference')) &
                 (~p2['event'].str.contains('Double Play')) ] 
        df3 = p2[(p2['event']=='Single') | 
                 (p2['event']=='Double') | 
                 (p2['event']=='Triple') | 
                 (p2['event']=='Home Run') ]
    
        #print(df3[['des','event']])
        return (df3['px'].values, df3['pz'].values)

    def get_hits_DF(self, df, ptype=None): 
        if ptype is None: 
            p = df.copy()
        else:
            p = df[df['pitch_type']==ptype]
        p2 = p[p['des'].str.contains('In play')]
        hitsDF = p2[(p2['event']=='Single') | 
                    (p2['event']=='Double') | 
                    (p2['event']=='Triple') | 
                    (p2['event']=='Home Run') ]
    
        return (hitsDF)

    def get_bases_per_pitch(self, df, ptype=None): 
        if ptype is None: 
            p = df.copy()
        else:
            p = df[df['pitch_type']==ptype]
        if len(p) > 0:
            p2 = p[p['des'].str.contains('In play')]
            bases = (len(p2[p2['event']=='Single']) + 
                    (2*len(p2[p2['event']=='Double'])) +
                    (3*len(p2[p2['event']=='Triple'])) +
                    (4*len(p2[p2['event']=='Home Run'])))
            bases_per_pitch = bases/len(p)
        else:
            bases_per_pitch = 0
        return (bases_per_pitch)

    def get_babip(self, df, ptype=None):
        # BABIP = (H – HR)/(AB – K – HR + SF)
        # BABIP = (H-HR)/(BIP-HR)  
    
        if ptype is None:
            p = df.copy()
        else:
            p = df[df['pitch_type']==ptype]
        bip = len( p[(p['des'].str.contains('In play')) & (~p['event'].str.contains('Error'))])
        hits = len(get_hits(p)[0])  
        hr = len(p[(p['des'].str.contains('In play')) & 
                   (p['event']=='Home Run')])
        sf = len( p[(p['des'].str.contains('In play')) & (p['event'].str.contains('Sac Fly'))])
        #print (bip, hits, hr)
    
        return (hits-hr)/(bip-hr+sf)


class Utilities(Baseball):
    """
    Various utility functions for baseball: SQL connections, SQL database calls
    
    Inherits functions from Baseball class
    
    get_con()
        usage: get_con(dbFolder, db)
        dbFolder default="/Users/iayork/Documents/Baseball/PitchFX"
        db default = 'pitchFX2015.db'
    get_pitchab(): 
        usage: get_pitchab(con, reg=True)
        set "reg=False" to get spring training, all-star, post-season games
        Get everything from pitch and atbat, merge on gameday_link + num
    get_pitchab_for_pitcher()
        usage: get_pitchab_for_pitcher(pitcher_name, con, reg=True)
        set "reg=False" to get spring training, all-star, post-season games
        Get everything from pitch and atbat for a specific pitcher, 
        merge on gameday_link + num
    get_bbref(): 
        usage get_bbref(url)
        returns a pandas dataframe containing bbref info (not all numeric?)
    bbref_date_to_gdl_date()
        usage: bbref_date_to_gdl_date(bbref_date, year)
        year default = 2015
        take date in format "Apr 8" or "Jul 7(1)" and convert to "04-08-15" format
    def get_ip(s):
        convert series containing innings pitched in ".1", ".2" format to ".33", ".67" format
    def pitch_abbrs():
        A dict of standard abbreviations for pitch types
    """


    def __init__(self): 
        
        Baseball.__init__(self)
        from importlib import import_module
        self.pd = import_module('pandas')
        self.sql = import_module('sqlite3')
        self.path = import_module('os.path')

        
    def get_con(self, dbFolder="/Users/iayork/Documents/Baseball/PitchFX", db='pitchFX2015.db'):
        """
        usage: get_con(dbFolder, db)
        dbFolder default="/Users/iayork/Documents/Baseball/PitchFX"
        db default = 'pitchFX2015.db'
        """
        return  self.sql.connect(self.path.join(dbFolder, db))   
        
            
    def get_pitchab(self, con, reg=True):
        """
        usage: get_pitchab(con)
        Get everything from pitch and atbat, merge on gameday_link + num
        """
        atbat = self.pd.read_sql("select * from atbat ", con)
        pitch = self.pd.read_sql("select * from pitch ", con)
        pitchab = pitch.merge(atbat, on=['gameday_link','num'], suffixes=('', '_duplicate_delete'))
    
        if reg:
            game_sql = """select gameday_link from game where game_type="R" """
            reg_gdls_df = self.pd.read_sql(game_sql, con) 
            reg_gdls = ['gid_%s' % x for x in reg_gdls_df['gameday_link'].values]
            pitchab = pitchab[pitchab['gameday_link'].isin(reg_gdls)]
            
        drop_cols = [x for x in pitchab.columns if '_duplicate_delete' in x]
        for param in ('break_angle', 'break_length','break_y', 'event_num'):
            pitchab[param] = self.pd.to_numeric(pitchab[param]) 
        return pitchab.drop(drop_cols, axis=1)
        
        
    def get_pitchab_for_pitcher(self, pitcher_name, con, reg=True): 
    
        atbat_sql = """select * from atbat where pitcher_name = "%s" """ % pitcher_name

        pitch_sql = """select * from pitch where gameday_link in 
        (select gameday_link from atbat where pitcher_name = "%s") """ % pitcher_name

        atbat = self.pd.read_sql(atbat_sql, con)
        pitch = self.pd.read_sql(pitch_sql, con)
    
        pitchab = pitch.merge(atbat, on=['gameday_link','num']) 
        pitchab.dropna(subset=['px',], inplace=True)
    
        if reg:
            game_sql = """select gameday_link from game where game_type="R" """
            reg_gdls_df = self.pd.read_sql(game_sql, con) 
            reg_gdls = ['gid_%s' % x for x in reg_gdls_df['gameday_link'].values]
            pitchab = pitchab[pitchab['gameday_link'].isin(reg_gdls)]
        return pitchab 
        
    def get_bbref(self, url):
        import requests
        from bs4 import BeautifulSoup 
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, 'lxml')
        tbl = soup.find('table', id='pitching_gamelogs')
        bbref = self.pd.read_html(str(tbl))[0]
        
        bbref2 = bbref[bbref['Gcar']!='Tm']
        bbref2 = bbref2.dropna(subset=['Gcar',], axis=0)
        for param in bbref2.columns:
            bbref2[param] = self.pd.to_numeric(bbref2[param], errors='ignore')
        return bbref2 
        
    def bbref_date_to_gdl_date(self, bbref_date, year=2015):
        dateD = {'Mar':3, 
                 'Apr':4,
                 'May':5,
                 'Jun':6,
                 'Jul':7,
                 'Aug':8,
                 'Sep':9,
                 'Oct':10,
                 'Nov':11}
        if len(str(year)) == 4:
            year = str(year)[-2:]
                 
        new_date = '%02d-%02d-%s' % (dateD[bbref_date.split()[0]],
                                     int(bbref_date.split()[-1].split('(')[0]),
                                     year)
        return new_date
                                 
        
    def get_ip(s):
        # convert series containing innings pitched in ".1", ".2" format to ".33", ".67" format
        return [(round(int(x)) + (x-round(int(x)))/0.3) for x in s]

        
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


class Plotting(object):
    """
    Various functions frequently used in plotting:
        
    
        def circles(self, x, y, s, c, ax, vmin, vmax, **kwargs):
        def setup_basic_plot(self, pitches, pytpe):
        
        def annot_font(self):
        def small_font(self):
        def cmapGnRd(self): 
        def cmapGyRd(self): 
        def cmapGyGn(self):  
        
    ptype_colors()
        A dict of seaborn colors suitable for plotting various pitch types 
    """

    def __init__(self): 
        from importlib import import_module
        self.pd = import_module('pandas') 
        self.mpl = import_module('matplotlib')
        self.sb = import_module('seaborn')
        from matplotlib import pyplot as plt
        self.plt = plt 
        
        self.muted = self.sb.color_palette('muted')  
        
    
    def ptype_clrs(self):
        return {'FF':self.muted[2], 
                'FT':self.muted[0], 
                'CU':self.muted[1],  
                'KC':self.muted[1],
                'CH':self.set2[1], 
                'SL':self.muted[3], 
                'FC':self.muted[4], 
                'FO':self.set2[1]}
        
        
    def pitch_char_3panel(self, df):
        fig, (ax1,ax2,ax3) = self.plt.subplots(1,3,figsize=(15,5))
        
        i = 0
        for ptype in df['pitch_type'].unique():
            df[df['pitch_type']==ptype].plot(x='break_length',
                                             y='start_speed', 
                                             kind='scatter', 
                                             ax=ax1, 
                                             color=self.muted[i]) 
            df[df['pitch_type']==ptype].plot(x='break_angle',
                                             y='start_speed', 
                                             kind='scatter', 
                                             ax=ax2, 
                                             color=self.muted[i])
            df[df['pitch_type']==ptype].plot(x='break_angle',
                                             y='break_length', 
                                             kind='scatter', 
                                             ax=ax3,  
                                             color=self.muted[i], 
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

        self.plt.tight_layout()
        return(fig, ax1,ax2,ax3)
        
    def circles(self, x, y, s, ax, ec, fc='white', lw=2.5, a=0.2, **kwargs):
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
        
        
    def setup_basic_plot(self, pitches, pytpe):
        
        if pitch14ab2['p_throws'].values[0] == 'R':
            xlims = (-3,2)
        else:
            xlims = (-2,3)  
    
        fig, (ax1, ax2) = self.plt.subplots(1,2,figsize=(13,6))
    
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

        self.plt.tight_layout()
        return (fig,ax1, ax2)
        

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
        
        cdictGnRd = {'red': ((0.0, 0.4, 0.4),
                             (1.0, 0.9, 0.9)),
                    'green': ((0.0, 0.9, 0.9),
                              (1.0, 0.2, 0.2)),
                    'blue': ((0.0, 0.2, 0.2),
                             (1.0, 0.2, 0.2))}

        cmapGnRd = self.mpl.colors.LinearSegmentedColormap('my_colormap', cdictGnRd)
        return cmapGnRd
        
    def cmapGyRd(self):  
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
        cmapGyRd = self.mpl.colors.LinearSegmentedColormap('my_colormap', cdictGyRd) 
        return cmapGyRd  
        
    def cmapGyGn(self):  
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
        cmapGyGn = self.mpl.colors.LinearSegmentedColormap('my_colormap', cdictGyGn) 
        return cmapGyGn


class Strikezone(object):
    """
    class Strikezone(object):
        def __init__(self):
        def official_zone(self):
        def get_x_list(self):
        def get_y_list(self):
        def get_std_zone(self): 
        def get_new_zone(self):
        def get_50pct_zone(self, year=2015):

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
                        (0.6, 1.5), (-0.375, 1.5)]

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
        
    def pitch_flight(self, params=None): 
        """
        params is a dictionary containing info for a single pitch
        Dec 2015 changed to 'params=None' instead of just 'params' and 
        set params = self.param_dict instead of defining in the call
        
        """
        params = self.param_dict
    
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