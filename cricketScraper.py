#%%
'''
Download Cricket Data
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import csv
import sys
import time
import os
import unicodedata
# from urlparse import urlparse
from bs4 import BeautifulSoup, SoupStrainer

BASE_URL = 'http://www.espncricinfo.com'

if not os.path.exists('./espncricinfo-fc'):
    os.mkdir('./espncricinfo-fc')

url = 'http://search.espncricinfo.com/ci/content/match/search.html?search=odi;all=1;page='

# for i in range(0, 6019):
    # odi: 
soupy = BeautifulSoup(urllib.request.urlopen(url + str(1)).read())

#%%
time.sleep(1)
for new_host in soupy.findAll('a', {'class' : 'srchPlyrNmTxt'}):
    try:
        new_host = new_host['href']
    except:
        continue
    odiurl = BASE_URL + urllib.parse.urlparse(new_host).geturl()
    new_host = unicodedata.normalize('NFKD', new_host).encode('ascii','ignore')
    print (new_host)
    #print(type(str.split(new_host)[3]))
    print (str.split(new_host, "/")[4])
    html = urllib.request.urlopen(odiurl).read()
    if html:
        with open('espncricinfo-fc/{0!s}'.format(str.split(new_host, "/")[4]), "wb") as f:
            f.write(html)

