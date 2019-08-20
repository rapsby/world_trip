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
import html

start = time.time()

def replace_information(file, dicts):
    fileObj = codecs.open(file, "r", "utf-8")
    lines = fileObj.readlines()
    text = ""
    for i in lines:
        text += i

    count = 0
    for d in dicts:
        count += 1
        name = d['name']
        url = d['url']
        img_url = d['img_url']
        text = text.replace('$title' + str(count)+'$', name)
        text = text.replace('$url' + str(count)+'$', url)
        text = text.replace('$image' + str(count)+'$', img_url)

    fw = codecs.open(file, 'w', 'utf8')
    fw.write(text)
    fw.close()

def print_imgUrls(list_):
    ans ="------------\n"
    it = iter(list_)
    while True:
        try:
            ans += str(next(it))+"\n"

        except StopIteration:
            break
    print(ans)
    return ans


def get_links_attraction(id):
    print("link..........")

    r = requests.get("https://www.tripadvisor.com/Attractions-" + id + "-Activities-a_allAttractions.true")
    soup = BeautifulSoup(r.text, "html.parser")

    # id parsing
    pattern = "data-locationid=\"[^\"]+"
    r = re.compile(pattern)
    pid_list = []
    pids = r.findall(str(soup))
    for pid in pids:
        pid_list.append(id + '-' + 'd' + pid[17:])
    pid_list = pid_list[:10]

    if len(pid_list) == 0:
        pattern = "\"id\":[0-9]+,\"name\""
        r = re.compile(pattern)
        pid_list = []
        pids = r.findall(str(soup))
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
    pname = pname.encode('utf-8')
    pname = pname.decode('unicode_escape')
    pname = pname.encode('utf-8')
    pname = pname.decode('unicode_escape')
    pname = str(html.unescape(pname))


    # image url parsing
    pattern = ",\"image\":\".*?\",\"aggregateRating"
    r = re.compile(pattern)
    results = r.findall(line)
    img_url = results[0]
    img_url = img_url[10:-18]

    dic = {
        'name':pname,
        'url':url,
        'img_url':img_url
    }
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

    return concated_list

def get_content_hotel(link):
    url = "https://www.tripadvisor.com/Hotel_Review-" + link
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    string = ""
    for item in soup:
        string = string +"\n"+ str(item)

    #pattern = "<h1 class=\"ui_header h1\" id=\"HEADING\">.*?</h1>"
    pattern = "id=\"HEADING\">.*?</h1>"

    r = re.compile(pattern)
    results = r.findall(string)
    pname = results[0]
    pname = pname[13:-5]
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
    return dic

def get_links_shopping(id):
    print("shopping link..........")
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
    if len(results)==0:
        pattern = "locIds.*?}"
        r = re.compile(pattern)
        results = r.findall(string)
        line = results[0]
        line = line[11:-3]
        id_list = str.split(line, ',')
        it = iter(id_list)
        concated_list = []
        for i in id_list:
            pid = next(it)
            concated_list.append(id + '-' + 'd' + pid)


    else:
        results = results[:10]
        # id list return
        concated_list = []
        for i in range(10):
            pid = results[i]
            pid = pid[9:-3]
            concated_list.append(id + '-' + 'd' + pid)

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

    pname = pname.encode('utf-8')
    pname = pname.decode('unicode_escape')
    pname = pname.encode('utf-8')
    pname = pname.decode('unicode_escape')

    pname = str(html.unescape(pname))

    # img url
    patten = "data-lazyurl=\".*?\.jpg"
    r = re.compile(patten)
    results = r.findall(string)
    if len(results)==0:
        img_url ="https://us.123rf.com/450wm/kurita/kurita1507/kurita150700011/42167824-%ED%9D%B0-%EB%B0%94%ED%83%95.jpg?ver=6"
    else:
        img_url = results[0]
        img_url = img_url[14:]

    dic = {
        'name':pname,
        'url':url,
        'img_url':img_url
    }
    return dic

def get_links_restaurant(id):
    print("restaurant link..........")
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
    pname = pname.encode('utf-8')
    pname = pname.decode('unicode_escape')
    pname = pname.encode('utf-8')
    pname = pname.decode('unicode_escape')
    pname = str(html.unescape(pname))

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
    return dic

if __name__=='__main__':

    link = input("link : ")
    patten = "Home-g[0-9]*"
    r = re.compile(patten)
    results = r.findall(link)
    id = results[0]
    id = id[5:]
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
    hotels = pool.map(get_content_hotel, get_links_hotel(id))
    shopping = pool.map(get_content_shopping, get_links_shopping(id))
    restaurants = pool.map(get_content_restaurant, get_links_restaurant(id))
    #print_imgUrls(attractions)
    #print_imgUrls(hotels)
    #print_imgUrls(shopping)
    #print_imgUrls(restaurants)


    # intent 파일에 텍스트 넣기
    attractions_origin = 'C:/Users/k/Desktop/tour_json/tour_origin/intents/attractions.json'
    hotels_origin = 'C:/Users/k/Desktop/tour_json/tour_origin/intents/hotels.json'
    shopping_origin = 'C:/Users/k/Desktop/tour_json/tour_origin/intents/shopping.json'
    restaurants_origin = 'C:/Users/k/Desktop/tour_json/tour_origin/intents/restaurants.json'
    en_origin = 'C:/Users/k/Desktop/tour_json/tour_origin/en_origin.xlf'

    attractions_after = 'C:/Users/k/Desktop/tour_json/o_tour/intents/attractions.json'
    hotels_after = 'C:/Users/k/Desktop/tour_json/o_tour/intents/hotels.json'
    shopping_after = 'C:/Users/k/Desktop/tour_json/o_tour/intents/shopping.json'
    restaurants_after = 'C:/Users/k/Desktop/tour_json/o_tour/intents/restaurants.json'
    en = 'C:/Users/k/Desktop/tour_json/en.xlf'

    shutil.copy(attractions_origin, attractions_after)
    shutil.copy(hotels_origin, hotels_after)
    shutil.copy(shopping_origin, shopping_after)
    shutil.copy(restaurants_origin, restaurants_after)
    shutil.copy(en_origin, en)

    replace_information(attractions_after,attractions)
    replace_information(hotels_after, hotels)
    replace_information(shopping_after, shopping)
    replace_information(restaurants_after, restaurants)

# en 파일 수정, 압축파일 만들기
    fileObj = codecs.open(en_origin, "r", "utf-8")
    u = fileObj.readlines()
    text = ""
    for i in u:
        i = i.replace("$location$", location)
        text += i + '\n'

    fw = codecs.open(en, 'w', 'utf8')
    fw.write(text)
    fw.close()

    # deploy 내용 압축
    os.chdir("C:/Users/k/Desktop/tour_json")
    import zipfile
    with zipfile.ZipFile(location+'_namespace.zip', mode='w') as f:
        f.write('en.xlf', compress_type=zipfile.ZIP_DEFLATED)

    f = zipfile.ZipFile(location+'_tour.zip', 'w', zipfile.ZIP_DEFLATED)
    startdir = "./o_tour"
    for dirpath, dirnames, filenames in os.walk(startdir):
        for filename in filenames:
            f.write(os.path.join(dirpath, filename))
    f.close()



    print("--- %s seconds ---" % (time.time() - start_time))