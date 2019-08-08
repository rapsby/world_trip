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


url ='https://www.tripadvisor.com/Hotels-g187147'
#url = "https://www.tripadvisor.com/Hotel_Review-g187147-d274978"
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")
string = ""
for item in soup:
    string = string +"\n"+str(item)

pattern = "locIds.*?}"
r = re.compile(pattern)
results = r.findall(string)
line = results[0]
line = line[11:-3]
id_list = str.split(line, ',')
print(id_list)
print(len(id_list))
'''
pattern = "onclick=\"return false;\" target=\"_blank\">.*?>"
r = re.compile(pattern)
results = r.findall(line)
pname = results[0]
pname = pname[8:]
print(pname)

pattern = "href=\".*?\""
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


