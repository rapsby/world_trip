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


def get_links_restaurant(id):
    print("link..........")
    url = "https://www.tripadvisor.com/Restaurants-"+id
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    string = ""
    for item in soup:
        string = string + str(item)

    # id parsing
    pattern = '\"LocationInformation\",\"locationId\":.*?,'
    r = re.compile(pattern)
    results = r.findall(string)
    results = results[:10]

    # id list return
    concated_list = []
    for i in range(10):
        pid = results[i]
        pid = pid[35:-2]
        concated_list.append(id + '-' + 'd' + pid)


    print(concated_list)
    return concated_list

def get_content_restaurant(link):
    url = "https://www.tripadvisor.com/Restaurant_Review-" + link
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    string = ""
    for item in soup:
        string = string + str(item)

    # name parsing
    patten = "{\"data\":{\"name\":\"[^\"]+"
    r = re.compile(patten)
    results = r.findall(string)
    pname = results[0]
    pname = pname[17:]

    # img url
    patten = "data-lazyurl=\".*?jpg"
    r = re.compile(patten)
    results = r.findall(string)
    img_url = None
    if len(results)!=0:
        img_url = results[0]
        img_url = img_url[14:]


    dic = {
        'name':pname,
        'url':url,
        'img_url':img_url
    }
    print(dic)
    return dic

if __name__=='__main__':
    #link = input("link : ")
    link = 'https://www.tripadvisor.com/Home-g187147'
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
    #attractions = pool.map(get_content_attraction, get_links_attraction(id))
    #hotels = pool.map(get_content_hotel, get_links_hotel(id))
    #shopping = pool.map(get_content_shopping, get_links_shopping(id))
    restaurants = pool.map(get_content_restaurant, get_links_restaurant(id))

