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

# Get all of the match URLs
# matchListURL = "http://stats.espnscrum.com/statsguru/rugby/stats/index.html?class=1;page={0};spanmax1=31+dec+2015;spanmin1=1+jan+2015;spanval1=span;template=results;trophy=17;type=team;view=results"
matchListURL = "http://stats.espnscrum.com/statsguru/rugby/stats/index.html?class=1;page={0};orderby=date;spanmax1=31+dec+2019;spanmin1=1+jan+2019;spanval1=span;template=results;trophy=17;type=team;view=match"

# Guessing that there wont be more than 10 pages
matches = []
for i in range(10):
    # get the webpage data
    webpage = BeautifulSoup(urllib.request.urlopen(matchListURL.format(i+1)).read())

    # find all of the links relating to matche
    temp = webpage.findAll(href=re.compile("/statsguru/rugby/match/"))
    if len(temp) > 0:
        matches.extend(list(temp))
    else:
        break

# Get the unique pages
matches = list(set(matches))

#%%


def GetStat(statName, text):
    pattern = ">(\d+).*\n{1}.*" + statName + ".*\n{1}.*>(\d+)"
    return re.findall(pattern, text)[0]

def GetStatSlash(statName, text):
    pattern = ">(\d+/\d+).*\n{1}.*" + statName + ".*\n{1}.*>(\d+/\d+)"
    return [x.split("/") for x in re.findall(pattern, text)[0]]

def GetTeamNames(text):
    pattern = "Match stats.*\n.*\n.*\n.*\">(.*)<.*\n.*\n.*\">(.*)<"
    return re.findall(pattern, text)[0]

def GetMatchID(text):
    pattern = "match/(\d*).html"
    return re.findall(pattern, text)[0]

def GetResult(text):
    pattern = "</span> (\d*) - (\d*) <span"
    return re.findall(pattern, text)[0]


df = pd.DataFrame(columns = ['TeamName', 'MatchID', 'Opponent', 'PointsFor', 'PointsAgainst', 'Tackle%', 'NumTackles', 'Passes', 'Meters', 'Breaks', 'DropGoals', 'Yellows', 'Reds'])

# Pull the stats from each page
baseURL = "http://stats.espnscrum.com"
for match in matches:
    matchURL = baseURL + match['href'] + "?view=scorecard"
    print(matchURL)
    matchWebpage = str(BeautifulSoup(urllib.request.urlopen(matchURL).read()))

    # These are games not yet played
    if len(matchWebpage) < 6000:
        continue

    teams = GetTeamNames(matchWebpage)
    matchID = GetMatchID(matchURL)
    points = GetResult(matchWebpage)
    tackles = GetStatSlash("Tackles", matchWebpage)
    passes = GetStat("Passes", matchWebpage)
    meters = GetStat("Metres", matchWebpage)
    breaks = GetStat("breaks", matchWebpage)
    dropgoals = GetStat("Dropped", matchWebpage)
    cards = GetStatSlash("Yellow", matchWebpage)

    # For each team, log the results
    for i in range(2):
        df = df.append({'TeamName': teams[i], 
                        'MatchID' : int(matchID),
                        'Opponent': teams[1] if i==0 else teams[0],
                        'PointsFor': float(points[i]),
                        'PointsAgainst': points[1] if i==0 else points[0],
                        'Tackle%': float(tackles[i][0])/(float(tackles[i][0])+float(tackles[i][1])),
                        'NumTackles': int(tackles[i][0]),
                        'Passes': int(passes[i]),
                        'Meters': int(meters[i]),
                        'Breaks': int(breaks[i]),
                        'DropGoals': int(dropgoals[i]),
                        'Yellows': int(cards[i][0]),
                        'Reds': int(cards[i][1])}, ignore_index=True)
    
    time.sleep(2)

df.set_index("TeamName", inplace=True)

df.to_csv('Matches.csv')

#%%
url = "https://www.rugbyworldcup.com/matches"

webpage = BeautifulSoup(urllib.request.urlopen(url).read())

f = open('output.txt', 'w')
print(webpage, file=f)
f.close()

# https://cmsapi.pulselive.com/rugby/match/25294/stats?language=en
# https://www.rugbyworldcup.com/matches

#%%
matchesPageURL = "https://www.rugbyworldcup.com/matches"
matchesPage = str(BeautifulSoup(urllib.request.urlopen(url).read()))

pattern = '"url": "https:\/\/www\.rugbyworldcup\.com\/match\/(\d*)"'
matches = re.findall(pattern, matchesPage)



#%%
import json
statURL = 'https://cmsapi.pulselive.com/rugby/match/{0}/stats?language=en'

webpage = urllib.request.urlopen(statURL.format(matches[0]))
data = json.loads(webpage.read().decode())
f = open('output.txt', 'w')
print(json.dumps(data, indent=4), file=f)
f.close()

#%%
data['match']['teams'][0]['name']
data['teamStats'][0]['stats']['BallWonZoneA']