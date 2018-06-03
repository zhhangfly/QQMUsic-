import pandas as pd
import numpy as np
from pandas import Series,DataFrame
from scipy.cluster.vq import kmeans,vq,whiten

#导入wordcloud模块和matplotlib模块
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from scipy.misc import imread



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

#用户名称key
userList=[]

#歌曲数目大于100的userList
bigUserList = []

#用户：歌单字典
outputList = {}




fpath="D:\\QQMusicResult\\result2.txt"
with open(fpath,'r',encoding='utf8') as f:
    for line in f.readlines():
        try:
            outputList.update(eval(line.strip()))

        except:
            print("except")
            continue

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
print('歌单数目大于40的用户数目:'+str(num40))
print('歌单数目大于80的用户数目:'+str(num80))
print('歌单数目大于100的用户数目:'+str(num100))
print('歌单数目大于110的用户数目:'+str(num110))
print('歌单数目大于120的用户数目:'+str(num120))
print('歌单数目大于130的用户数目'+str(num130))
print('歌单数目大于140的用户数目'+str(num140))
print('歌单数目等于150的用户数目'+str(num150))

#取出歌单数量大于等于100的用户
for ele in outputList:
    if len(outputList.get(ele))<100:
        userList.append(ele)
for user in userList:
    del outputList[user]


#对这531个用户的歌单求交集(此时的outputList已经只有歌曲数目大于100的用户)
for ele in outputList:
    bigUserList.append(ele)

#显示歌单重复数目最多的两个人
def getBiggestRepeats():

    # 用户重复歌曲数目统计
    songsRepeats = []

    rawNum = -1
    bigOuter = -1
    bigInner = -1

    sum = 0
    repeats = 0
    for outer in range(0,531):
        for inner in range(outer,531):
            if outer!=inner:
                songsOuter = outputList.get(bigUserList[outer])
                songsInner = outputList.get(bigUserList[inner])
                setListOuter = set(songsOuter.keys())
                setListInner = set(songsInner.keys())
                repeatNumbers = len(setListOuter&setListInner)
                songsRepeats.append(repeatNumbers)
                if repeatNumbers > rawNum:
                    rawNum = repeatNumbers
                    bigOuter = outer
                    bigInner = inner
    print('第'+ str(bigOuter) +'个用户'+ '和第' + str(bigInner) + '个用户的歌曲重复数目最大为'+ str(rawNum))
    for num in songsRepeats:
        sum = sum +num

    averageNum = sum/len(songsRepeats)
    print(averageNum)
    for num in songsRepeats:
        if num >=averageNum:
            repeats+=1
    print(repeats)
    print(len(songsRepeats))



def getRecommandByContents():
    rawNum = -1
    bigOuter = -1

    num = int(input('输入你的下标:'))
    for outer in range(0, 531):
        if num!=outer:
            songsOuter = outputList.get(bigUserList[outer])
            songsInner = outputList.get(bigUserList[num])
            setListOuter = set(songsOuter.keys())
            setListInner = set(songsInner.keys())
            repeatNumbers = len(setListOuter & setListInner)
            print('第' + str(outer) + '个用户' + '和第' + str(num) + '个用户的歌曲重复数目为' + str(repeatNumbers))
            if repeatNumbers > rawNum:
                rawNum = repeatNumbers
                bigOuter = outer
    print('第' + str(bigOuter) + '个用户' + '和第' + str(num) + '个用户的歌曲重复数目最大,为' + str(rawNum))
    songsOuter = outputList.get(bigUserList[bigOuter])
    songsInner = outputList.get(bigUserList[num])
    setListOuter = set(songsOuter.keys())
    setListInner = set(songsInner.keys())
    print('重复歌曲为:'+ str(setListOuter & setListInner))
    print("推荐的歌曲为")
    for ele in setListOuter:
        if ele not in setListOuter&setListInner:
            print(str(ele))



def getRecommandByGeners():
    #gene:number字典
    gerneNumDict={}

    gerneNumList=[]

    #user:{gener:number}dict
    userGenerNumDict = {}




    tempNum = 0


    a=0
    b=0
    c=0
    e=0
    f=0
    for user in range(0,len(bigUserList)):
        for song in outputList.get(bigUserList[user]):
            gener = outputList.get(bigUserList[user]).get(song)
            if gener == '1':
                a+=1
            elif gener == '2':
                b+=1
            elif gener == '3':
                c+=1
            elif gener == '5':
                e+=1
            else:
                f+=1
        gerneNumDict['gener1'] = a
        gerneNumDict['gener2'] = b
        gerneNumDict['gener3'] = c
        gerneNumDict['gener5'] = e
        gerneNumDict['othergener'] = f
        gerneNumList.append(a)
        gerneNumList.append(b)
        gerneNumList.append(c)
        gerneNumList.append(e)
        gerneNumList.append(f)
        userGenerNumDict[bigUserList[user]] = gerneNumDict
        gerneNumDict={}
        gerneNumList=[]
        a = 0
        b = 0
        c = 0
        e = 0
        f = 0
    print(userGenerNumDict)
    rawdata = DataFrame(userGenerNumDict)
    data = rawdata.T#转置
    #data.to_excel('C:/Users/张博/Desktop/数据挖掘.xlsx',sheet_name='data')
    num = int(input('输入你的下标:'))
    user = np.array(data.iloc[num].values)
    for index in data.index:
        if index!=bigUserList[num]:
            direct = np.array(data.loc[index].values)
            cos = np.dot(user,direct)/(np.linalg.norm(direct)*np.linalg.norm(user))
            if cos>tempNum:
                tempNum = cos
                tempName = index
    print('最高的相似度为:'+str(tempNum))
    songs = outputList.get(tempName)
    setList = set(songs.keys())#重合度最高的用户的歌单信息
    songsInner = outputList.get(bigUserList[num])
    setListInner = set(songsInner.keys())#选中用户的歌单信息

    print('重复歌曲为:'+ str(setList & setListInner))
    print("推荐的歌曲为")
    for ele in setList:
        if ele not in setList&setListInner:
            print(str(ele))




#聚类分析推荐个歌曲
def getRecommandByCluster():
    #gene:number字典
    gerneNumDict={}

    gerneNumList=[]

    #user:{gener:number}dict
    userGenerNumDict = {}
    #点集
    points=[]

    #同簇数据点
    labellist=[]

    #同簇歌曲推荐信息
    setresults=set()

    tempNum = 0


    a=0.0
    b=0.0
    c=0.0
    e=0.0
    f=0.0
    for user in range(0,len(bigUserList)):
        for song in outputList.get(bigUserList[user]):
            gener = outputList.get(bigUserList[user]).get(song)
            if gener == '1':
                a+=1
            elif gener == '2':
                b+=1
            elif gener == '3':
                c+=1
            elif gener == '5':
                e+=1
            else:
                f+=1
        gerneNumDict['gener1'] = a
        gerneNumDict['gener2'] = b
        gerneNumDict['gener3'] = c
        gerneNumDict['gener5'] = e
        gerneNumDict['othergener'] = f
        gerneNumList.append(a)
        gerneNumList.append(b)
        gerneNumList.append(c)
        gerneNumList.append(e)
        gerneNumList.append(f)
        userGenerNumDict[bigUserList[user]] = gerneNumDict
        gerneNumDict={}
        gerneNumList=[]
        a = 0.0
        b = 0.0
        c = 0.0
        e = 0.0
        f = 0.0
    print(userGenerNumDict)
    rawdata = DataFrame(userGenerNumDict)
    data = rawdata.T                                #获得了DataFram格式的数据
    for index in data.index:
        direct = np.array(data.loc[index].values)
        points.append(direct)
    centroid = kmeans(points, 100)[0]
    label = vq(points, centroid)[0]
    print(label)
    num = int(input('输入你的下标:'))
    userlabel = label[num]
    for l in range(0,len(label)):
        if label[l-1]==userlabel:
            labellist.append(l)#此时labellist储存了同簇元素下标
    songsInner = outputList.get(bigUserList[num])
    setListInner = set(songsInner.keys())
    print('推荐的歌曲为：')
    print(len(labellist))
    for t in range(0,len(labellist)):
        songs = outputList.get(bigUserList[t])
        setsongs = set(songs.keys())
        for ele in setsongs:
            setresults.add(ele)
    print(len(setresults))
    for ele in setresults:
        if ele not in setListInner:
            print(str(ele))

def newUserWrite():
    #所有歌曲
    songsList = []
    fpath="D:\\QQMusicResult\\songsresult.txt"
    for user in bigUserList:
        songs = outputList.get(user).keys()
        for song in songs:
            songsList.append(song)
    with open(fpath,'a',encoding='utf-8') as f:
        for out in songsList:
            f.write(str(out)+' ')


def newUserRead():
    fpath = "D:\\QQMusicResult\\songsresult.txt"
    text = open(fpath,'r',encoding ='utf8').read()
    bg_pic = imread('jay.jpg')
    wc = WordCloud(background_color='white',  # 背景颜色
                   max_words=500,  # 最大词数
                   mask=bg_pic,  # 以该参数值作图绘制词云，这个参数不为空时，width和height会被忽略
                   max_font_size=100,  # 显示字体的最大值
                   font_path="C:/Windows/Fonts/STFANGSO.ttf",  # 解决显示口字型乱码问题，可进入C:/Windows/Fonts/目录更换字体
                   random_state=42,  # 为每个词返回一个PIL颜色
                   # width=1000,  # 图片的宽
                   # height=860  #图片的长
                   )

    # 显示词云图片

    wc.generate(text)
    # 基于彩色图像生成相应彩色
    image_colors = ImageColorGenerator(bg_pic)
    # 显示图片
    plt.imshow(wc)
    # 关闭坐标轴
    plt.axis('off')
    # 绘制词云
    plt.figure()
    plt.imshow(wc.recolor(color_func=image_colors))
    plt.axis('off')
    # 保存图片
    wc.to_file('biggerUser.png')
















if __name__ == "__main__":
    newUserRead()