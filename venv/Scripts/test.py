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

url = 'https://www.tripadvisor.com/Attraction_Review-g187870-d194251'
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")
string = ""
for item in soup.find_all('script'):
    string = string + str(item.find_all(text=True))

print(string)