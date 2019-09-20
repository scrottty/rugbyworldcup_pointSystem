#%%
import urllib.request
import requests
from bs4 import BeautifulSoup
import json
import re
#%%
# URL to get all of the matches at the world cup
url = "http://stats.espnscrum.com/statsguru/rugby/stats/index.html?class=1;page=3;spanmax1=31+dec+2015;spanmin1=1+jan+2015;spanval1=span;template=results;trophy=17;type=team;view=results"

# get the webpage data
webpage = BeautifulSoup(urllib.request.urlopen(url).read())

# find all of the links relating to matches
matches = webpage.findAll(href=re.compile("/statsguru/rugby/match/"))


#%%
matchURL = 'http://stats.espnscrum.com/statsguru/rugby/match/181970.html?view=scorecard'
# matchURL = 'http://www.espncricinfo.com/ci/engine/match/1199228.html'
matchWebpage = BeautifulSoup(urllib.request.urlopen(matchURL).read())



#%%
pattern = ">(\d+).*\n{1}.*Tackling.*\n{1}.*>(\d+)"
x = re.findall(pattern, str(matchWebpage))

#%%
f = open('match.txt', 'w')
print(matchWebpage,file=f)
f.close()

# "Match stats.*\n.*\n.*\n.*\">(\S*)<.*\n.*\n.*\">(\S*)<"
#%%
f = open('output.txt', 'w')
print(results,file=f)
f.close()

#%%
statName = 'ddd'
pattern = ">(\d+).*\n{1}.*" + statName +".*\n{1}.*>(\d+)"

#%%
import pandas as pd

df = pd.DataFrame(columns=['a', 'b', 'c'])

#%%

ff = matches.findAll(href=re.compile("/statsguru/rugby/match/"))
f = open('output2.txt', 'w')
for game in ff:
    print(game,file=f)
f.close()

#%%
dd = "ddflk{0}"
print(dd.format(3))

#%%
'''
- Get webpage of all the games at the world cup
- Find the URL of each match page
- Load the page
- Search through the page for the stats
- Do this twice for each team


- Output table will be 

Team Name | Match ID | Opponent | Points For | Points Against | Tackles % | No. Tackles | Passes | Meters Gained | Clean Breaks | Drop Goals | 

'''