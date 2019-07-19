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
starttime = time.time()
loc = input("위치 : ")
upHpAreaId = 2
hpAreaId = input("AreaId : ")


file = 'C:/Users/k/Desktop/json/TempPlace.json'
basefile = 'C:/Users/k/Desktop/json/hhhppp/hotplace.json'
kofile = 'C:/Users/k/Desktop/json/ko.xlf'
kobasefile = 'C:/Users/k/Desktop/json/hhhppp/ko.xlf'
shutil.copy(basefile, file)

r = requests.get("https://www.siksinhot.com/taste?upHpAreaId=" + str(upHpAreaId) + "&hpAreaId="+str(hpAreaId)+"&isBestOrd=N")
soup = BeautifulSoup(r.text, "html.parser")

# 상호명 parsing
mr = soup.find_all("script")
pattern = "\"pname\":\"[^\"]+"
r = re.compile(pattern)
results = r.findall(str(mr))

# 추천 맛집 string 정리
it = iter(results)
list = []
str = "";
while True:
    try:


        pname = next(it)
        pname = pname[9:]
        list.append(pname)
        if(len(results) == len(list)):
            str +="\""+loc+"의 $hotplace-kind 맛집은 "+pname+" 입니다. 다른 음식 추천을 원하시면 다시 음식 종류를 말해주시고 종료를 원하시면 취소를 말씀해주세요.\""
        else:
            str +="\""+loc+"의 $hotplace-kind 맛집은 "+pname+" 입니다. 다른 음식 추천을 원하시면 다시 음식 종류를 말해주시고 종료를 원하시면 취소를 말씀해주세요.\",\n"



    except StopIteration:
        break

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
fileObj = codecs.open(kobasefile, "r", "utf-8" )
u = fileObj.readlines()
text = ""
for i in u :
    i = i.replace("목동", loc)
    text += i+'\n'

fw = codecs.open(kofile, 'w', 'utf8')
fw.write(text)
fw.close()

# 압축
os.chdir("C:/Users/k/Desktop/json")
import zipfile
with zipfile.ZipFile('namespace.zip', mode='w') as f:
    f.write('ko.xlf', compress_type=zipfile.ZIP_DEFLATED)

print("성공")
print(time.time()-starttime)