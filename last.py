import requests
from bs4 import BeautifulSoup
import json
import re



#歌曲:种类字典
dictSong={}

#用户字典
dictUin={}
#所有用户id
listUin=[]
#去除重复id
setUin=[]
#去除重复disstid
t=0
#获取晴天歌曲下评论用户的uid
def getUin(pagnerNum):
    x=0
    header  = {'Referer':'https://y.qq.com/portal/profile.html?uin=1152921504613031000#sub=song&tab=like&','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    url = "https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg"
    paramter = {
        'g_tk': '550934167',
        'jsonpCallback' : 'jsoncallback0726551257273067',
        'loginUin': '331161787',
        'hostUin':'0',
        'format': 'jsonp',
        'inCharset': 'utf8',
        'outCharset': 'GB2312',
        'notice': '0',
        'platform': 'yqq',
        'needNewCode': '0',
        'cid': '205360772',
        'reqtype': '2',
        'biztype': '1',
        'topid' : '97773',
        'cmd':'8',
        'needmusiccrit': '0',
        'pagenum': pagnerNum ,
        'pagesize': '25',
        'lasthotcommentid': '',
        'callback': 'jsoncallback0726551257273067',#可能会变
        'domain': 'qq.com',
        'ct': '24',
        'cv': '101010'
        }
    rawList = requests.get(url,params=paramter, headers = header )
    stringList = rawList.text[29:-4]#call的变化可能导致此处长度的变化，可以考虑此处用正则表达式再用split函数获取值=
    jsonList = json.loads(stringList)
    CommentList = jsonList.get("comment").get("commentlist")
    while x<len(CommentList):
        listUin.append(CommentList[x].get("uin"))
        x=x+1



#获取distid用以拼装歌曲id从而得到歌曲类型
def getDisstid(uin):
    global dictUin
    result=""
    header = {'Referer': 'https://y.qq.com/portal/profile.html?uin=1152921504613031000#sub=song&tab=like&',
              'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    url = "https://c.y.qq.com/rsc/fcgi-bin/fcg_get_profile_homepage.fcg"#发表评论的用户的主页
    paramter = {
        'g_tk': '550934167',
        'jsonpCallback': 'MusicJsonCallback6903964246446181',
        'loginUin': '331161787',
        'hostUin': '0',
        'format': 'jsonp',
        'inCharset': 'utf8',
        'outCharset':'utf-8',
        'notice': '0',
        'platform': 'yqq',
        'needNewCode': '0',
        'cid': '205360838',
        'ct': '20',
        'userid': uin,
        'reqfrom':'1',
        'reqtype':'0'
    }
    rawList = requests.get(url,params=paramter, headers = header )
    stringList = rawList.text[36:-5]
    jsonList = re.findall(r'"id":"\d{5,20}"',stringList)[0]
    nameList = re.findall(r'"nick":".{1,30}?"',stringList)[0]
    if jsonList:
        result = jsonList.split(":")[-1][1:-1]
        resultName = nameList.split(":")[-1][1:-1]
        dictUin[uin]=resultName               #uin和其对应的昵称
    if result:
        return result                   #去除外部引号的disstid



#获取评论用户的喜欢的歌单里的歌曲songmid并将list返回
def getListInfo(disstid):
    x=0
    result=[]
    header = {'Referer': 'https://y.qq.com/portal/profile.html?uin=1152921504613031000#sub=song&tab=like&',
              'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    url = "https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg"#发表评论的用户的我喜欢歌单内容
    paramter = {
        'type': '1',
        'json': '1',
        'utf8': '1',
        'onlysong': '1',
        'nosign': '1',
        'song_begin': '0',
        'song_num': '150',#歌曲数目
        'disstid': disstid,
        '_': '1526962637884',
        'g_tk' : '550934167',
        'jsonpCallback' : 'MusicJsonCallback007932978135133384',
        'loginUin' : '331161787',
        'hostUin': '0',
        'format': 'jsonp',
        'inCharset': 'utf8',
        'outCharset': 'utf-8',
        'notice': '0',
        'platform': 'yqq',
        'needNewCode': '0',
    }
    rawList = requests.get(url,params=paramter, headers = header )
    stringList = rawList.text
    rawresult = re.findall(r'"songmid":".{14}"',stringList)

    while x<len(rawresult):
        result.append(rawresult[x][-15:-1])
        x+=1
    print("此用户包含的歌曲数目")
    print(len(result))
    if result:
        return result

def getSongDetail(songmid):
    global dictSong
    header = {
              'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    url = "https://c.y.qq.com/v8/fcg-bin/fcg_play_single_song.fcg"  # 歌曲信息
    paramter = {
        'songmid': songmid ,
        'tpl':'yqq_song_detail',
        'callback': 'etOneSongInfoCallback',
        'g_tk': '550934167',
        'jsonpCallback': 'getOneSongInfoCallback',
        'loginUin': '', # 你的QQ数目
        'hostUin': '0',
        'format':'jsonp',
        'inCharset': 'utf8',
        'outCharset': 'utf-8',
        'notice': '0',
        'platform': 'yqq',
        'needNewCode': '0',
    }
    rawList = requests.get(url, params=paramter, headers=header)
    stringList = rawList.text
    rawResult = re.findall(r'"name":".{1,40}?"',stringList)[2].split(":")[-1][1:-1]
    rawResultGener = re.findall(r'"genre":\d',stringList)[0].split(":")[-1]
    print(rawResult)
    print(rawResultGener)
    dictSong[rawResult]=rawResultGener#需要注意的是这个字典放到outPut字典之后需要清零
    if rawResult:
        return rawResult









if __name__ == "__main__":
    dictOutput={}
    fpath="D:\\QQMusicResult\\result2.txt"
    while t<100:#页数
        getUin(t)
        t=t+1
    setUin=set(listUin)
    print("去除重复用户之后的用户数目")
    print(len(setUin))
    temp=list(setUin)#去重之后保持原有顺序
    temp.sort(key=listUin.index)
    print(len(temp))
    for uin in temp:
        try:
            print("this is uin")
            print(uin)
            listAlbummid= getListInfo(getDisstid(uin))#此处得到了歌单的songmid
            if listAlbummid:
                for song in listAlbummid:#b遍历albummid从而将歌曲信息与风格加入到dictsong中
                    try:
                        getSongDetail(song)
                    except:
                        print("inner except")
                        continue
                nickName = dictUin.get(uin)
                print(nickName)
                dictOutput[nickName]=dictSong
                dictSong={}
        except:
            print("outer except")
            continue
    print(dictOutput)
    with open(fpath,'a',encoding='utf-8') as f:
        for out in dictOutput:
            f.write('{'+'\''+str(out)+ '\'' + ':'+str(dictOutput.get(out))+'}' +'\n')





