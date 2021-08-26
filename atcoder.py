import requests
import bs4
import os
import pickle

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
    
