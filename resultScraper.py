'''
This script scraps ESPN statsguru to get all stats and creates a table for the point to be calculated upon

Steps:
- Get webpage of all the games at the world cup
- Find the URL of each match page
- Load the page
- Search through the page for the stats
- Do this twice for each team


- Output table will be 

Team Name | Match ID | Opponent | Points For | Points Against | Tackles % | No. Tackles | Passes | Meters Gained | Clean Breaks | Drop Goals | Yellows | Reds

'''
#%%

# Import Libraries
import urllib.request
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import json

# Get all of the match URLs
matchListURL = "https://www.rugbyworldcup.com/matches"
matchesPage = str(BeautifulSoup(urllib.request.urlopen(matchListURL).read(), 'html.parser'))

pattern = '"url": "https:\/\/www\.rugbyworldcup\.com\/match\/(\d*)"'
matches = re.findall(pattern, matchesPage)

pattern = 'eventStatus": "(.*)",'
matchStatus = re.findall(pattern, matchesPage)

#%%
# Download each game stats and create table
statURL = 'https://cmsapi.pulselive.com/rugby/match/{0}/stats?language=en'

df = pd.DataFrame(columns = ['TeamName', 'MatchID', 'Opponent', 'PointsFor', 'PointsAgainst', 'Tackle%', 'NumTackles', 'Passes', 'Meters', 'Breaks', 'DropGoals', 'Yellows', 'Reds'])

for match, matchRun in zip(matches, matchStatus):
    if matchRun == 'Upcoming':
        continue

    print('Downloading match: ' + match)
    
    webpage = urllib.request.urlopen(statURL.format(match)).read()
    data = json.loads(webpage.decode())

    # Do for each team
    for i in range(2):
        df = df.append({'TeamName': data['match']['teams'][i]['name'], 
                        'MatchID' : data['match']['matchId'],
                        'Opponent': data['match']['teams'][1]['name'] if i==0 else data['match']['teams'][0]['name'],
                        'PointsFor': data['match']['scores'][i],
                        'PointsAgainst': data['match']['scores'][1] if i==0 else data['match']['scores'][0],
                        'Tackle%': data['teamStats'][i]['stats']['TackleSuccess'],
                        'NumTackles': data['teamStats'][i]['stats']['Tackles'],
                        'Passes': data['teamStats'][i]['stats']['Passes'],
                        'Meters': data['teamStats'][i]['stats']['Metres'],
                        'Breaks': data['teamStats'][i]['stats']['clean_breaks'],
                        'DropGoals': sum([x['stats']['DropGoals'] for x in data['teamStats'][i]['playerStats'] if 'DropGoals' in x['stats']]),
                        'Yellows': sum([x['stats']['YellowCards'] for x in data['teamStats'][i]['playerStats'] if 'YellowCards' in x['stats']]),
                        'Reds': sum([x['stats']['RedCards'] for x in data['teamStats'][i]['playerStats'] if 'RedCards' in x['stats']])},
                        ignore_index=True)

df.set_index("TeamName", inplace=True)

df.to_csv('Matches.csv')