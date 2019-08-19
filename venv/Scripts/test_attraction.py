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

def get_links_attraction(id):
    print("link..........")

    r = requests.get("https://www.tripadvisor.com/Attractions-"+id+"-Activities-a_allAttractions.true")
    soup = BeautifulSoup(r.text, "html.parser")


    # id parsing
    pattern = "data-locationid=\"[^\"]+"
    r = re.compile(pattern)
    pid_list = []
    pids = r.findall(str(soup))
    for pid in pids:
        pid_list.append(id + '-' + 'd' + pid[17:])
    pid_list = pid_list[:10]

    if len(pid_list)== 0:
        pattern = "\"id\":[0-9]+,\"name\""
        r = re.compile(pattern)
        pid_list = []
        pids = r.findall(str(soup))
        print(pids)
        for pid in pids:
            pid_list.append(id + '-' + 'd' + pid[5:-7])
        pid_list = pid_list[4:14]

    return pid_list

def get_content_attraction(link):
    url = "https://www.tripadvisor.com/Attraction_Review-" + link
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    string = ""
    for item in soup:
        string = string + str(item)

    # main line parsing
    pattern = "\"LocalBusiness\",\"name\":\".*?\",\"aggregateRating"
    r = re.compile(pattern)
    results = r.findall(string)
    line = results[0]
    line = line[16:]
    line = line.encode('utf-8')
    line = line.decode('unicode_escape')

    # name parsing
    pattern = "\"name\":\"[^\"]+"
    r = re.compile(pattern)
    results = r.findall(line)
    pname = results[0]
    pname = pname[8:]

    # url parsing
    pattern = ",\"url\":\".*?\",\"image"
    r = re.compile(pattern)
    results = r.findall(line)
    url = results[0]
    url = url[8:-8]

    # image url parsing
    pattern = ",\"image\":\".*?\",\"aggregateRating"
    r = re.compile(pattern)
    results = r.findall(line)
    img_url = results[0]
    img_url = img_url[10:-18]

    dic = {
        'name':pname,
        'url':'https://www.tripadvisor.com'+url,
        'img_url':img_url
    }
    print(dic)
    return dic


if __name__=='__main__':
    #link = input("link : ")
    link = 'https://www.tripadvisor.com/Home-g293913'
    patten = "Home-.*"
    r = re.compile(patten)
    results = r.findall(link)
    id = results[0]
    id = id[5:12]
    print(id)

    url = 'https://www.tripadvisor.com/Home-'
    string = ""
    r = requests.get(url + id)
    soup = BeautifulSoup(r.text, "html.parser")
    for item in soup.find_all('script'):
        string = string + str(item.find_all(text=True))
    patten = "\"EntryGeo\",\"value\":\".*?-"
    r = re.compile(patten)
    results = r.findall(string)
    location = results[0]
    location = location[20:-1]

    print(location)

    start_time = time.time()
    pool = Pool(processes=16)
    attractions = pool.map(get_content_attraction, get_links_attraction(id))
    #hotels = pool.map(get_content_hotel, get_links_hotel(id))
    #shopping = pool.map(get_content_shopping, get_links_shopping(id))
    #restaurants = pool.map(get_content_restaurant, get_links_restaurant(id))

