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
    print("attraction link..........")

    r = requests.get("https://www.tripadvisor.com/Attractions-"+id+"-Activities-a_allAttractions.true")
    soup = BeautifulSoup(r.text, "html.parser")


    # id parsing
    pattern = "data-locationid=\"[^\"]+"
    r = re.compile(pattern)
    pid_list = []
    pids = r.findall(str(soup))
    for pid in pids:
        pid_list.append(id + '-' + 'd' + pid[17:])

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

def get_links_hotel(id):
    print("hotel link..........")

    r = requests.get("https://www.tripadvisor.com/Hotels-" + id)
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
        concated_list.append(id + '-' + 'd' + pid)

    print(concated_list)
    return concated_list

def get_content_hotel(link):
    url = "https://www.tripadvisor.com/Hotel_Review-" + link
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    string = ""
    for item in soup:
        string = string + "\n" + str(item)

    pattern = "<h1 class=\"ui_header h1\" id=\"HEADING\">.*?</h1>"
    r = re.compile(pattern)
    results = r.findall(string)
    pname = results[0]
    pname = pname[38:-5]

    pattern = ";background-image:url.*?\".*?\""
    r = re.compile(pattern)
    results = r.findall(string)
    img_url = None
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
        else:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            pattern = ";background-image:url.*?\".*?\""
            r = re.compile(pattern)
            results = r.findall(string)
            img_url = None
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

    dic = {
        'name': pname,
        'url': url,
        'img_url': img_url
    }
    print(dic)
    return dic

def get_links_shopping(id):
    print("link..........")
    url = "https://www.tripadvisor.com/Attractions-"+id+"-Activities-c26"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    string = ""
    for item in soup:
        string = string + str(item)

    # id parsing
    pattern = '<!--trkL:.*?-->'
    r = re.compile(pattern)
    results = r.findall(string)

    results =results[:10]

    # id list return
    concated_list = []
    for i in range(10):
        pid = results[i]
        pid = pid[9:-3]
        concated_list.append(id + '-' + 'd' + pid)


    print(concated_list)
    return concated_list

def get_content_shopping(link):
    url = "https://www.tripadvisor.com/Attraction_Review-" + link
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
    img_url = results[0]
    img_url = img_url[14:]

    dic = {
        'name':pname,
        'url':url,
        'img_url':img_url
    }
    print(dic)
    return dic

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