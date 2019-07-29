from bs4 import BeautifulSoup
import requests
import re
import shutil
import json
import os
from collections import OrderedDict
from pprint import pprint
import pathlib
import time
from multiprocessing import Pool
from urllib.request import urlopen

url = 'https://www.tripadvisor.com/Attraction_Review-g189158-d195318-Reviews-Mosteiro_dos_Jeronimos-Lisbon_Lisbon_District_Central_Portugal.html'
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")
string = ""
for item in soup.find_all('script'):
    string = string + str(item.find_all(text=True))
patten = "\"EntryGeo\",\"value\":\".*?-"
r = re.compile(patten)
results = r.findall(string)
location = results[0]
location = location[20:-1]

patten = "\"truncatedDescription\":{\"text\":\".*?\",\""
r = re.compile(patten)
results = r.findall(string)
if (len(results) == 0):
    patten = "\"description\":{\"text\":\".*?\",\""
    r = re.compile(patten)
    results = r.findall(string)
    if (len(results) == 0):
        description=""
    else:
        description = results[0]
        description = description[23:-3]
else:
    description = results[0]
    description = description[23:-3]

print(description)