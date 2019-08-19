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
import html

url ='https://www.tripadvisor.com/Hotels-g187147'
url = "https://www.tripadvisor.com/Hotel_Review-g187147-d274978"
url = "https://www.tripadvisor.com/Hotel_Review-g187147-d233805"
url = "https://www.tripadvisor.com/Hotel_Review-g187147-d4340356"
url = 'https://www.tripadvisor.com/Hotel_Review-g187147-d228694'
url = 'https://www.tripadvisor.com/Hotel_Review-g187147-d313072-Reviews-Le_Regent_Montmartre_by_HipHopHostels-Paris_Ile_de_France.html'
url = 'https://www.tripadvisor.com/Hotel_Review-g187147-d599275-Reviews-Hotel_Oceania_Paris_Porte_de_Versailles-Paris_Ile_de_France.html'
url = 'https://www.tripadvisor.com/Hotel_Review-g187147-d274978'
url = 'https://www.tripadvisor.com/Hotel_Review-g187147-d583986-Reviews-Hotel_Longchamp_Elysees-Paris_Ile_de_France.html'
url = 'https://www.tripadvisor.com/Attractions-g187147-Activities-c26'
#url = 'https://www.tripadvisor.com/Attraction_Review-g187147-d246225-Reviews-Forum_des_Halles-Paris_Ile_de_France.html'
url = 'https://www.tripadvisor.com/Attraction_Review-g196586-d4749809-Reviews'
url = 'https://www.tripadvisor.com/Restaurants-g187147-Paris_Ile_de_France.html'
#url = 'https://www.tripadvisor.com/Restaurant_Review-g187147-d14215380'
url = 'https://www.tripadvisor.com/Hotel_Review-g294217-d652907'
url = 'https://www.tripadvisor.com/Attractions-g297415-Activities-c26'
url = 'https://www.tripadvisor.com/Attraction_Review-g297415-d3362245'
url = 'https://www.tripadvisor.com/Attraction_Review-g293913'
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")
string = ""
for item in soup:
    string = string +"\n"+str(item)

pattern = 'locIds\\\\\":\\\\\".*?\"'
r = re.compile(pattern)
results = r.findall(string)

print(string)
'''
pattern = ";background-image:url.*?\".*?\""
r = re.compile(pattern)
results = r.findall(string)
if(len(results))!= 0:
    img_url = results[0]
    img_url = img_url[23:-1]

else:
    print('hi')
    print(soup)
    pattern = "\"width\":[0-9]{4,4},\"height\":[0-9]{3,3},\"url\":\".*?jpg"
    r = re.compile(pattern)
    results = r.findall(string)
    img_url = results[0]
    img_url = img_url[33:]

print(img_url)

'''
