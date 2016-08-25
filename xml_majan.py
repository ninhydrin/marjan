# coding:utf-8
import xml.etree.ElementTree as ET
import numpy as np
import urllib.request
import requests
import gzip
import bs4
import os, sys,time
from train import TrainData

xml_save_dir = "xml_dir"
gz_save_dir = "gz_dir"

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
        filename = os.path.join(gz_save_dir,url.split('/')[-1])
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

def get_xml(url, save=None):
    """urlを渡すとデータを持ってくる
    """
    #response = urllib.request.urlopen(url)
    response = requests.get(url)
    #data = response.read()
    data = response.content
    data = ET.fromstring(data)
    if not save is None:
        name = os.path.join(xml_save_dir,url.split("/")[-1][1:])
        name+=".xml"
        tree = ET.ElementTree(data)
        tree.write(name)
    return data

def test ():
    a = get_haihu_name()
    a = download_file(a[-8])
    a = gz_extract(a)
    a = haihu_d_list(a)
    a = get_xml(a[0],True)
    a = match_parse(a)
    a = a[1]
    players = init_player(a["INIT"])
    train = make_data(a["SUTE"],players)
    return (a,players,train)


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
    datas = TrainData()
    tsumo_moji = ["T","U","V","W"]
    sute_moji = ["D","E","F","G"]

    for i in haihu:
        if "REACH" in i.tag:
            for j in i.items():
                if j[0]=="who":
                    players[int(j[1])].reach=1
            if i.get("step")=="2":
                print ("REACH")

        elif "N" in i.tag[0]:
            item =  {j[0]:j[1]for j in i.items()}
            naki_info =naki(int(item["m"]))
            print(naki_info[0])
            players[int(item["who"])].add_naki_info(naki_info)
            players[int(item["who"])].tsumo(sute)
        else:
            for j, k in enumerate(tsumo_moji):
                if k == i.tag[0]:
                    players[j].tsumo(int(i.tag[1:]))
            for j, k in enumerate(sute_moji):
                if k == i.tag[0]:
                    players[j].throw(int(i.tag[1:]))
                    datas.make_vec(players, j)
        if i.tag[0] != "N" and  i.tag !="REACH":
            sute = int(i.tag[1:])
    return datas


def naki(num):
    bit = bin(num)
    who = int(bit[-2: ],2)
    if int(bit[-3]):
        hai_min = int(bit[-5:-3],2)
        hai_mid = int(bit[-7:-5],2)
        hai_max = int(bit[-9:-7],2)
        type_six = int(bit[2:8],2)
        min_pai = type_six // 3
        naki_pai = type_six % 3
        return ("qi", who, hai_min, hai_mid, hai_max, min_pai, naki_pai)
    else:
        if int(bit[-4]):#ぽん
            type_seven = int(bit[2:9],2)
            pon_pai = type_seven // 3
            naki_pai = type_seven % 3
            amari_pai = int(bit[-7:-5],2)
            return ("pon", who, pon_pai, naki_pai, amari_pai)
        elif int(bit[-5]):#加槓
            type_seven = int(bit[2:9],2)
            pon_pai = type_seven // 3
            naki_pai = type_seven % 3
            ka_pai = int(bit[-7:-5],2)
            return ("ka", who, pon_pai, naki_pai, amari_pai)
        else:
            assert bit[-2:-6]=="0000"
            kan = int(bit[2:10],2) // 4
            kind = "min" if who else "an"
            return (kind, who, kan)

def get_all():
    h = "html"
    dir_list = [i for i in os.listdir(h) if i[0]!="."]
    for i in dir_list:
        html_list = [i for i in os.listdir(os.path.join(h, i)) if i[0]!="."]
        for j in html_list:
            haihu_list = haihu_d_list(open(os.path.join(h, i, j)).read())
            for k in haihu_list:
                print(i,j,k)
                try:
                    a = get_xml(k,True)
                    #time.sleep(10)
                except urllib.error.URLError as e:
                    print(e.reason)
                    #time.sleep(5)
