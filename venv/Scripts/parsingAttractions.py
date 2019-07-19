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

start = time.time()

text = ""

loc ="default"# = "1" #input("위치 : ")
upHpAreaId = 2
hpAreaId = ""# = 1026 #input("AreaId : ")

intent_file = 'C:/Users/k/Desktop/trip_json/Attractions.json'
baseintent_file = 'C:/Users/k/Desktop/trip_json/original/Attractions.json'
deploy_file = 'C:/Users/k/Desktop/trip_json/en.xlf'
basedeploy_file = 'C:/Users/k/Desktop/trip_json/original/en.xlf'
shutil.copy(baseintent_file, intent_file)



def get_links(id):
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
    patten = "\"description\":{\"text\":\"[^\"]+"
    r = re.compile(patten)
    results = r.findall(string)

    if(len(results) == 0):
        description = ""
    else:
        description = results[0]
        description = description[23:]

    sentence = pname +".\t"+ description

    # removing unicode in sentence
    
    print(sentence)
    return sentence

if __name__=='__main__':
    id = 'g187870' #input("id : ")
    start_time = time.time()
    pool = Pool(processes=16) # 4개의 프로세스를 사용합니다.
    result = pool.map(get_content, get_links(id))
    print(result)
    print("--- %s seconds ---" % (time.time() - start_time))

'''
# 기본 파일에 위치, 추천 맛집 텍스트 넣기
import codecs
fileObj = codecs.open(basefile, "r", "utf-8" )
u = fileObj.readlines()
text = ""
for i in u :
    i = i.replace("ㅁㅈㅇㅊ", loc)
    i = i.replace("ㄹㅋㅇㅅ", str)
    text += i+'\n'

fw = codecs.open(file, 'w', 'utf8')
fw.write(text)
fw.close()



# ko.xlf 파일 수정해서 압축파일 만들기
fileObj = codecs.open(basedeploy_file, "r", "utf-8" )
u = fileObj.readlines()
text = ""
for i in u :
    i = i.replace("_destination_", loc)
    text += i+'\n'

fw = codecs.open(deploy_file, 'w', 'utf8')
fw.write(text)
fw.close()

# 압축
os.chdir("C:/Users/k/Desktop/trip_json")
import zipfile
with zipfile.ZipFile('namespace.zip', mode='w') as f:
    f.write('en.xlf', compress_type=zipfile.ZIP_DEFLATED)
'''
