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
url ='https://www.tripadvisor.com/Attractions-g187147-Activities-c26-Paris_Ile_de_France.html'
url ='https://www.tripadvisor.com/Hotels-g187147-Paris_Ile_de_France-Hotels.html'
url = 'https://www.tripadvisor.com/Attraction_Review-g187147-d188150-Reviews-Musee_d_Orsay-Paris_Ile_de_France.html'
url = "https://www.tripadvisor.com/Attractions-" + "g187147" + "-Activities-c26"

r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")
string = ""
for item in soup.find_all('script'):
    string = string + str(item.find_all(text=True))
print(string)


img = soup.find_all(class_="ui_column is-12")
for a in img:
    print(a)
    print("\n\n")
#img = img[3]
#print(img.get("data-lazyurl"))
'''
pattern = "\"LocationInformation\",\"locationId\":[^}]+"
r = re.compile(pattern)
results = r.findall(string)
location = results[0]
location = location[35:]
results =results[:4]
id_list = []
for id in results:
    id_list.append(id[35:])

print(id_list)
'''
'''
pattern = "\"truncatedDescription\":{\"text\":\".*?\",\""
r = re.compile(pattern)
results = r.findall(string)
if (len(results) == 0):
    pattern = "\"description\":{\"text\":\".*?\",\""
    r = re.compile(pattern)
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
'''