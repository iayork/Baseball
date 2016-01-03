# Baseball
Miscellaneous baseball scripts

**Baseball**: Package containing miscellaneous baseball utilities, mainly for handling PITCHf/x data

* Minimally documented and written for my own use, with my own paths etc hard-coded into the scripts.
* Contents: 
  * baseball.py - Calculate WHIP, ERIP, get info on called/swinging strikes, balls, hits, babip
  * batting.py  - get SLG, OBP, babip, strikes, hits, swings for a sub-region within the batter's strike zone
  * pitch.py - Calculate pitch flight (position of the pitch at 1/100-second intervals based on starting position and accelerations)
  * plotting.py - Draw circles, set up charts for 1, 2, or multiple pitch visualizations, utilities including fonts, cmaps, colors
  * strikezone.py - Polygons representing 50-percent strike zones from 2008-2015; official strike zone; StrikeZone and Zone classes
  * utilities.py - Connect to SQL pitchF/X database; connect to baseball-reference.com; produce pandas dataframe from pitchF/X data

**Download_MLB.py**: Download PITCHf/x and related data from MLB

**Download_MLB_threaded.py**: Download PITCHf/x and related data from MLB

* Conceptually based off PITCHr/x but written from scratch in Python
* Multiprocessed in an attempt to make downloading and parsing go faster
