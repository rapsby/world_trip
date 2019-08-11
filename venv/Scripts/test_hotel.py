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
import html



def get_links_hotel(id):
    print("link..........")

    r = requests.get("https://www.tripadvisor.com/Hotels-"+id)
    soup = BeautifulSoup(r.text, "html.parser")
    string = ""
    for item in soup:
        string = string + "\n" + str(item)

    pattern = "locIds.*?}"
    r = re.compile(pattern)
    results = r.findall(string)
    line = results[0]
    line = line[11:-3]
    id_list = str.split(line, ',')

    # id list return
    it = iter(id_list)
    concated_list = []
    for i in range(10):
        pid = next(it)
        concated_list.append(id+'-'+'d'+pid)

    return concated_list

def get_content_hotel(link):
    url = "https://www.tripadvisor.com/Hotel_Review-" + link
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    string = ""
    for item in soup:
        string = string +"\n"+ str(item)

    pattern = "<h1 class=\"ui_header h1\" id=\"HEADING\">.*?</h1>"
    r = re.compile(pattern)
    results = r.findall(string)
    pname = results[0]
    pname = pname[38:-5]
    pname = pname.encode('utf-8')
    pname = pname.decode('unicode_escape')
    pname = pname.encode('utf-8')
    pname = pname.decode('unicode_escape')
    pname = str(html.unescape(pname))
    img_url = None
    count = 0
    while True:
        count += 1
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        string = ""
        for item in soup:
            string = string + "\n" + str(item)
        pattern = ";background-image:url.*?\".*?\""
        r = re.compile(pattern)
        results = r.findall(string)
        if (len(results)) != 0:
            img_url = results[0]
            img_url = img_url[23:-1]
        else:
            pattern = "\"width\":[0-9]{4,4},\"height\":[0-9]{3,3},\"url\":\".*?jpg"
            r = re.compile(pattern)
            results = r.findall(string)
            if (len(results)) != 0:
                img_url = results[0]
                img_url = img_url[33:]
        if img_url != None:
            break
        else:
            print("error count " + str(count))

    dic = {
        'name':pname,
        'url':url,
        'img_url':img_url
    }
    print(dic)
    return dic


if __name__=='__main__':
    link = input("link : ")
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
    hotels = pool.map(get_content_hotel, get_links_hotel(id))
    #shopping = pool.map(get_content_shopping, get_links_shopping(id))
    #restaurants = pool.map(get_content_restaurant, get_links_restaurant(id))

