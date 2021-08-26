import requests
import bs4
import os
import pickle
fileid=["1zXrLq7ZN8bwtcvn0nLig0ed4gn0lQjMc"]
path="atcoder/rematc"
remdict={}

async def check_atcoder():
    result=[[],[],[],[]]
    link=[]
    url="https://atcoder.jp/contests/"
    r=requests.get(url)
    soup=bs4.BeautifulSoup(r.content, "html.parser")
    elem=soup.select("#contest-table-upcoming")
    for i in elem[0].findAll("time"):
        result[0].append(i.text)
    for i in elem[0].select("a[href*=contest]"):
        link.append("https://atcoder.jp"+i.get("href"))
        result[1].append(i.text)
    for i in link:
        result[2].append(i)
    for  i in elem[0].select(".text-center"):
        if " - " in i.text or "All" in i.text or "-"==i.text:
            result[3].append("Rated:"+i.text)
    return result

def rematc_init(Drive):
    global remdict
    gf = Drive.CreateFile({'id': fileid[0]})
    gf.GetContentFile(path)
    f = open(path)
    if os.stat(path).st_size == 0:
        pickle.dump(remdict,f)
    else:
        remdict=pickle.load(f)
    return

def rematc_save(Drive):
    global remdict
    f = open(path,mode="f")
    f.write(remdict)
    f.close()
    gf = Drive.CreateFile({"id": fileid[0], "title": "rematc"})
    gf.SetContentFile(path)
    gf.Upload()
    return 
def rematc_check(discordid):
    global remdict
    if discordid in remdict:
        return remdict[discordid]
    else:
        return -1

def rematc_change(Drive,atcid,discordid):
    global remdict
    changeid=0
    if atcid==None and discordid in remdict:#通知停止
        changeid=1
        remdict.pop(discordid) 
    elif not atcid=="":#通知追加と変更
        changeid=1
        atcid=check_rate(atcid)
        if atcid != -1:
            remidict[discordid]=atcid
    if changeid==1:
        rematc_save(Drive)
    return 

def check_rate(id):
    #print("test")
    rate=100000
    url="https://atcoder.jp/users/"+id
    r=requests.get(url)
    if r.status_code==404:
        return -1
    else:
        soup=bs4.BeautifulSoup(r.content, "html.parser")
        elem=soup.find("div",class_="col-md-9 col-sm-12")
        #print(elem)
        for i in elem:
            #print(type(i))
            if "dl-table" in str(i):
                d=i.find_all('span', {"class":{lambda value: value and value.startswith('user')}})
                #print("d")
                for c in d:
                    rate=min(rate,int(c.string))
        pass  
    if not rate==100000:  
        return rate
    else:
        return -1
    
#print(check_rate("blackpit9"))