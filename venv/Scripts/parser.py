# -*- coding: utf-8 -*-
from unidecode import unidecode
from unicodedata import *
from bs4 import BeautifulSoup
import requests
import re
import shutil
import json
import os
import pathlib
import time
from multiprocessing import Pool
import codecs



start = time.time()

def get_links_attraction(id):
    print("link..........")

    r = requests.get("https://www.tripadvisor.com/Attractions-"+id)
    soup = BeautifulSoup(r.text, "html.parser")
    string = ""
    for item in soup.find_all('script'):
        string = string + str(item.find_all(text=True))

    # id parsing
    pattern = "distanceToGeo\":0},{\"id\":[^,]+"
    r = re.compile(pattern)
    results = r.findall(string)


    # id list return
    it = iter(results)
    list = []
    for i in range(4):
        pid = next(it)
        pid = pid[24:]
        list.append(id+'-'+'d'+pid)


    return list

def get_content_attraction(link):
    url = "https://www.tripadvisor.com/Attraction_Review-" + link
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    string = ""
    for item in soup.find_all('script'):
        string = string + str(item.find_all(text=True))

    # name parsing
    patten = "{\"data\":{\"name\":\"[^\"]+"
    r = re.compile(patten)
    results = r.findall(string)
    pname = results[0]
    pname = pname[17:]

    # img url
    img = soup.find_all("img")
    img = img[3]
    img_url = img.get("data-lazyurl")

    dic = {
        'name':pname,
        'url':url,
        'img_url':img_url
    }
    return dic

def get_links_hotel(id):
    print("link..........")

    r = requests.get("https://www.tripadvisor.com/Attractions-"+id)
    soup = BeautifulSoup(r.text, "html.parser")
    string = ""
    for item in soup.find_all('script'):
        string = string + str(item.find_all(text=True))

    # id parsing
    pattern = "distanceToGeo\":0},{\"id\":[^,]+"
    r = re.compile(pattern)
    results = r.findall(string)


    # id list return
    it = iter(results)
    list = []
    for i in range(4):
        pid = next(it)
        pid = pid[24:]
        list.append(id+'-'+'d'+pid)


    return list

def get_content_hotel(link):
    url = "https://www.tripadvisor.com/Attraction_Review-" + link
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    string = ""
    for item in soup.find_all('script'):
        string = string + str(item.find_all(text=True))

    # name parsing
    patten = "{\"data\":{\"name\":\"[^\"]+"
    r = re.compile(patten)
    results = r.findall(string)
    pname = results[0]
    pname = pname[17:]

    # img url
    img = soup.find_all("img")
    img = img[3]
    img_url = img.get("data-lazyurl")

    dic = {
        'name':pname,
        'url':url,
        'img_url':img_url
    }
    return dic

def get_links_shopping(id):
    print("link..........")
    url = "https://www.tripadvisor.com/Attractions-"+id+"-Activities-c26"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    string = ""
    for item in soup.find_all('script'):
        string = string + str(item.find_all(text=True))

    # id parsing
    pattern = "distanceToGeo\":0},{\"id\":[^,]+"
    r = re.compile(pattern)
    results = r.findall(string)


    # id list return
    it = iter(results)
    list = []
    for i in range(4):
        pid = next(it)
        pid = pid[24:]
        list.append(id+'-'+'d'+pid)


    return list

def get_content_shopping(link):
    url = "https://www.tripadvisor.com/Attraction_Review-" + link
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    string = ""
    for item in soup.find_all('script'):
        string = string + str(item.find_all(text=True))

    # name parsing
    patten = "{\"data\":{\"name\":\"[^\"]+"
    r = re.compile(patten)
    results = r.findall(string)
    pname = results[0]
    pname = pname[17:]

    # img url
    img = soup.find_all("img")
    img = img[3]
    img_url = img.get("data-lazyurl")

    dic = {
        'name':pname,
        'url':url,
        'img_url':img_url
    }
    return dic

def get_links_restaurant(id):
    print("link..........")

    r = requests.get("https://www.tripadvisor.com/Attractions-"+id)
    soup = BeautifulSoup(r.text, "html.parser")
    string = ""
    for item in soup.find_all('script'):
        string = string + str(item.find_all(text=True))

    # id parsing
    pattern = "distanceToGeo\":0},{\"id\":[^,]+"
    r = re.compile(pattern)
    results = r.findall(string)


    # id list return
    it = iter(results)
    list = []
    for i in range(4):
        pid = next(it)
        pid = pid[24:]
        list.append(id+'-'+'d'+pid)


    return list

def get_content_restaurant(link):
    url = "https://www.tripadvisor.com/Attraction_Review-" + id
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    string = ""
    for item in soup.find_all('script'):
        string = string + str(item.find_all(text=True))

    # name parsing
    patten = "{\"data\":{\"name\":\"[^\"]+"
    r = re.compile(patten)
    results = r.findall(string)
    pname = results[0]
    pname = pname[17:]

    # img url
    img = soup.find_all("img")
    img = img[3]
    img_url = img.get("data-lazyurl")

    dic = {
        'name':pname,
        'url':url,
        'img_url':img_url
    }
    return dic

if __name__=='__main__':

    intent_file = 'C:/Users/k/Desktop/trip_json/Attractions.json'
    baseintent_file = 'C:/Users/k/Desktop/trip_json/original/Attractions.json'
    deploy_file = 'C:/Users/k/Desktop/trip_json/en.xlf'
    basedeploy_file = 'C:/Users/k/Desktop/trip_json/original/en.xlf'
    shutil.copy(baseintent_file, intent_file)

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
    attractions = pool.map(get_content_attraction, get_links_attraction(id))
    #hotels = pool.map(get_content_hotel, get_links_hotel(id))
    #shopping = pool.map(get_content_shopping, get_links_shopping(id))
    #restaurants = pool.map(get_content_restaurant, get_links_restaurant(id))

'''
    # removing unicode in result sentence
    for i in range(0,len(result)):
        data = result[i]

        data = data.encode('utf-8')
        data = data.decode('unicode_escape')
        data = data.encode('utf-8')
        data = data.decode('unicode_escape')
        data = str.replace(data, "\"", "\\\"")
        attractions += "\"" + data + "\"" + "\n"
        if i != len(result) - 1:
            attractions += ","

        #print(attractions)

    # intent 파일에 텍스트 넣기
    fileObj = codecs.open(baseintent_file, "r", "utf-8")
    u = fileObj.readlines()
    text = ""
    for i in u:
        i = i.replace("$location$", location)
        i = i.replace("$attraction$", attractions)
        text += i + '\n'

    fw = codecs.open(intent_file, 'w', 'utf8')
    fw.write(text)
    fw.close()

    # en.xlf 파일 수정해서 압축파일 만들기
    fileObj = codecs.open(basedeploy_file, "r", "utf-8")
    u = fileObj.readlines()
    text = ""
    for i in u:
        i = i.replace("$location$", location)
        text += i + '\n'

    fw = codecs.open(deploy_file, 'w', 'utf8')
    fw.write(text)
    fw.close()

    # 압축
    os.chdir("C:/Users/k/Desktop/trip_json")
    import zipfile

    with zipfile.ZipFile('namespace.zip', mode='w') as f:
        f.write('en.xlf', compress_type=zipfile.ZIP_DEFLATED)



    print("--- %s seconds ---" % (time.time() - start_time))

'''