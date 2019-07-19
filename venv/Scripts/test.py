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
"""
r = requests.get("https://www.tripadvisor.com/Attractions-" + 'g187870-d194251')
soup = BeautifulSoup(r.text, "html.parser")
"""
session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}
url = 'https://www.tripadvisor.com/Attractions-g187870-d194251'
html = session.get(url, headers=headers).content
soup = BeautifulSoup(html, "html.parser")

doc = urlopen(url).read()
print(doc)


string = ""
table = soup.find('div')
for item in soup.find_all('div'):
    string = string + str(item.find_all(text=True))

