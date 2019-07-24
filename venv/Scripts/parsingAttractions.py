# -*- coding: utf-8 -*-
from unidecode import unidecode
from unicodedata import *
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
import plistlib
import codecs


start = time.time()

def get_links(link):
    print("link")

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
    while True:
        try:
            pid = next(it)
            pid = pid[24:]
            list.append(id+'-'+'d'+pid)

        except StopIteration:
            break

    return list

def get_content(link):
    r = requests.get("https://www.tripadvisor.com/Attraction_Review-" + link)
    soup = BeautifulSoup(r.text, "html.parser")
    string = ""
    for item in soup.find_all('script'):
        string = string + str(item.find_all(text=True))

    string = unidecode(string)


    # name parsing
    patten = "{\"data\":{\"name\":\"[^\"]+"
    r = re.compile(patten)
    results = r.findall(string)
    pname = results[0]
    pname = pname[17:]

    # description parsing
    patten = "\"description\":{\"text\":\".*?\",\""
    r = re.compile(patten)
    results = r.findall(string)

    if(len(results) == 0):
        description = ""
    else:
        description = results[0]
        description = description[23:-3]


    #print(description)
    sentence = pname + "  " + description

    suffix = " Say \'Attractions\' If you want more attractions or Say cancel.";
    sentence = pname + ". " + description + suffix
    return sentence

if __name__=='__main__':

    intent_file = 'C:/Users/k/Desktop/trip_json/Attractions.json'
    baseintent_file = 'C:/Users/k/Desktop/trip_json/original/Attractions.json'
    deploy_file = 'C:/Users/k/Desktop/trip_json/en.xlf'
    basedeploy_file = 'C:/Users/k/Desktop/trip_json/original/en.xlf'
    shutil.copy(baseintent_file, intent_file)

    attractions = ""
    link = input("link : ")
    patten = "Attractions-.*?-"
    r = re.compile(patten)
    results = r.findall(link)
    id = results[0]
    id = id[12:-1]
    print(id)
    patten = "true-.*?_"
    r = re.compile(patten)
    results = r.findall(link)
    location = results[0]
    location = location[5:-1]
    print(location)

    start_time = time.time()
    pool = Pool(processes=16)
    result = pool.map(get_content, get_links(id))

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

