# coding:utf-8
import xml.etree.ElementTree as ET
import numpy as np
import urllib.request
import requests
import gzip
import bs4
import os, sys

xml_save_dir = "xml_dir"

def match_parse(xml):
    all_list = xml
    #all_list = xml.getroot()
    match_list = [all_list[0].items()]
    assert all_list[3].tag == "TAIKYOKU"
    match = None
    for i in all_list[4:]:
        if i.tag == "INIT":
            if match:
                match_list.append(match)
            match = {"SUTE":[],"INIT":i.items()}

        elif i.tag == "AGARI":
            match["AGARI"] = i.items()

        else:
            match["SUTE"].append(i)

    return match_list


def get_haihu_name():
    url="http://tenhou.net/sc/raw/list.cgi"
    response = urllib.request.urlopen(url)
    data = response.read()
    data_list={}
    exec("kari="+data.decode("utf-8").replace("file","'file'").replace("size","'size'"),locals(),data_list)
    distillation_data_list = ["http://tenhou.net/sc/raw/dat/"+i["file"] for i in data_list["kari"] if "scc" in i["file"]]
    return distillation_data_list

def download_file(url,filename=None):
    if not filename:
        filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
        return filename
    return False

def gz_extract(filename):
    with gzip.open(filename,"rb") as f:
        content = f.read()
    return content

def haihu_d_list(html):
    soup = bs4.BeautifulSoup(html,"lxml")
    return [i["href"].replace("/?log=","/log/?") for i in soup.p.find_all("a")]

def get_xml(url):
    response = urllib.request.urlopen(url)
    data = response.read()
    return ET.fromstring(data)

def test ():
    a = get_haihu_name()
    a = download_file(a[-8])
    a = gz_extract(a)
    a = haihu_d_list(a)
    a = get_xml(a[0])
    a = match_parse(a)
    a = a[1]
    players = init_player(a["INIT"])
    make_data(a["SUTE"],players)
    return a

from marjan import Player

def init_player(init):
    players = {}
    for i in init:
        if "hai" in i[0]:
            players[int(i[0][-1])]=Player(i[0][-1],i[1].rsplit(","))
        elif "oya" in i[0]:
            oya_num=int(i[1])
    players[oya_num].oya = 1
    return players

def make_data(haihu, players):
    datas=[]
    for i in haihu:
        print (i)
        if "REACH" in i.tag:
            for j in i.items():
                if j[0]=="who":
                    players[int(j[1])].reach=1

        elif "T" in i.tag[0]:
            players[0].tsumo(i.tag[1:])
        elif "U" in i.tag[0]:
            players[1].tsumo(i.tag[1:])
        elif "V" in i.tag[0]:
            players[2].tsumo(i.tag[1:])
        elif "W" in i.tag[0]:
            players[3].tsumo(i.tag[1:])
        elif "D" in i.tag[0]:
            players[0].throw(i.tag[1:])
        elif "E" in i.tag[0]:
            players[1].throw(i.tag[1:])
        elif "F" in i.tag[0]:
            players[2].throw(i.tag[1:])
        elif "G" in i.tag[0]:
            players[3].throw(i.tag[1:])
        elif "N" in i.tag[0]:
            for j in i.items():
                if j[0]=="who":
                    players[int(j[1])].tsumo(sute)
            pass

        if i.tag[0] != "N" and  i.tag !="REACH":
            sute = i.tag[1:]
        #datas.append(out_data())

def out_data(num,players):
    ans = players[num].tehai
    for i in players.keys():
        if i.my_num != num:
            ans+=players[i].sute
    return ans
