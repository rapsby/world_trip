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
url = "https://www.tripadvisor.com/Attractions-g187147-Activities-a_allAttractions.true"
url = "https://www.tripadvisor.com/Attraction_Review-g187147-d188757"
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

string = ""
for item in soup.find_all('script'):
    string = string +"\n" +str(item.find_all(text=True))


pattern = "\"LocalBusiness\",\"name\":\".*?\",\"aggregateRating"
r = re.compile(pattern)
results = r.findall(string)
line = results[0]
line = line[16:]
line = line.encode('utf-8')
line = line.decode('unicode_escape')
print(line)

pattern = "\"name\":\"[^\"]+"
r = re.compile(pattern)
results = r.findall(line)
pname = results[0]
pname = pname[8:]
print(pname)

pattern = ",\"url\":\".*?\",\"image"
r = re.compile(pattern)
results = r.findall(line)
url = results[0]
url = url[8:-8]
print(url)

pattern = ",\"image\":\".*?\",\"aggregateRating"
r = re.compile(pattern)
results = r.findall(line)
img_url = results[0]
img_url = img_url[10:-18]
print(img_url)


'''
pattern = "data-locationid=\"[^\"]+"
r = re.compile(pattern)
id_list = []
ids = r.findall(str(soup))
for id in ids:
    id_list.append(id+'-'+'d'+id[17:])
print(id_list)
'''
'''
string = ""

for item in soup.find_all('script'):
    string = string +"\n" +str(item.find_all(text=True))
#print(string)
print(soup)
data-locationid="188150"
'''
'''
img = soup.find_all('script')
for a in img:
    print(a)
'''


#src = img link , href poiName
'''
box = soup.find_all(class_="ui_column is-12")
box = box[1:11]
box_list = list()
for cl in box:
    dic = {
        'name': pname,
        'url': url,
        'img_url': img_url
    }
    
    
#img = img[3]
#print(img.get("data-lazyurl"))
'''
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