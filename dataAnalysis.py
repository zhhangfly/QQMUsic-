import io
import re
import json


#统计歌曲数目分布
num40 = 0
num80 = 0
num100 = 0
num110 = 0
num120 = 0
num130 = 0
num140 = 0
num150 = 0
num150 = 0


outputList = {}
fpath="D:\\QQMusicResult\\result2.txt"
with open(fpath,'r',encoding='utf8') as f:
    for line in f.readlines():
        try:
            print(line.strip())
            outputList.update(eval(line.strip()))

        except:
            print("except")
            continue
listName=outputList.keys
for ele in outputList:
    songNum = len(outputList.get(ele))
    if songNum>=40:
        num40+=1
    if songNum>=80:
        num80+=1
    if songNum>=100:
        num100+=1
    if songNum>=110:
        num110+=1
    if songNum>=120:
        num120+=1
    if songNum>=130:
        num130+=1
    if songNum>=140:
        num140+=1
    if songNum==150:
        num150+=1

#各个区间数目
print(num40)
print(num80)
print(num100)
print(num110)
print(num120)
print(num130)
print(num140)
print(num150)


print(len(outputList))