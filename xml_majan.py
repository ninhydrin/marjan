# coding:utf-8
import sys
import xml.etree.ElementTree as ET
import numpy as np
import urllib.request
import requests
import gzip
import bs4
import os, sys,time

from train import TrainData
from mj2 import Pai


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

def get_xml(url, save_name=None):
    """urlを渡すとデータを持ってくる
    """
    response = requests.get(url)
    data = response.content
    data = ET.fromstring(data)
    if not save_name is None:
        tree = ET.ElementTree(data)
        tree.write(save_name)
    return data

def test ():
    #a = get_haihu_name()
    #a = download_file(a[-8])
    #a = gz_extract(a)
    #a = haihu_d_list(a)
    #a = get_xml(a[0],True)
    data = ET.fromstring(open("2015021823gm-00e1-0000-348e12c8.xml").read())
    data = match_parse(data)
    data = data[1]
    players = init_player(data["INIT"])
    train = make_data(data["SUTE"],players)
    return (data,players,train)


from marjan import TenhouPlayer

def replay (data):
    sute = data["SUTE"]
    init = data["INIT"]
    players = init_player(init)
    train = make_data(sute,players)
    if "AGARI" in data:
        agari(data["AGARI"])

def agari(data):
    data = {i[0]:i[1] for i in data}
    print("AGARI {}".format(data["who"]))
    print ("atari = {}".format(Pai.from_index(int(data["machi"]))))
    print ("hai ={}".format([Pai.from_index(int(i)) for i in data["hai"].rsplit(",")]))

def init_player(init):
    players = {}
    sorted(init)
    for i in init:
        if "hai" in i[0]:
            players[int(i[0][-1])]=TenhouPlayer(i[0][-1],i[1].rsplit(","))
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
            players[int(item["who"])].add_naki_info(naki_info)
            players[int(item["who"])].naki(sute)
        else:
            for j, k in enumerate(tsumo_moji):
                if k == i.tag[0]:
                    players[j].tsumo(int(i.tag[1:]))
            for j, k in enumerate(sute_moji):
                if k == i.tag[0]:
                    players[j].throw(int(i.tag[1:]))
                    #datas.make_vec(players, j)

        if i.tag[0] != "N" and  i.tag !="REACH" and i.tag!="RYUUKYOKU":
            sute = int(i.tag[1:])
        if i.tag == "RYUUKYOKU":
            print ("RYUUKYOKU")
    return datas


def naki(num):
    bit = "{0:016}".format(int(bin(num)[2:]))
    who = int(bit[-2:],2)
    if int(bit[-3]):#ちー
        hai_min = int(bit[-5:-3],2)
        hai_mid = int(bit[-7:-5],2)
        hai_max = int(bit[-9:-7],2)
        type_six = int(bit[:6],2)
        min_pai = type_six // 3
        naki_pai = type_six % 3
        return ("qi", who, hai_min, hai_mid, hai_max, min_pai, naki_pai)
    else:
        if int(bit[-4]):#ぽん
            type_seven = int(bit[:7],2)
            pon_pai = type_seven // 3
            naki_pai = type_seven % 3
            amari_pai = int(bit[-7:-5],2)
            return ("pon", who, pon_pai, naki_pai, amari_pai)
        elif int(bit[-5]):#加槓
            type_seven = int(bit[:7],2)
            pon_pai = type_seven // 3
            naki_pai = type_seven % 3
            ka_pai = int(bit[-7:-5],2)
            return ("ka", who, pon_pai, naki_pai, amari_pai)
        else:
            assert bit[-2:-6]=="0000"
            kan = int(bit[:8],2) // 4
            kind = "min" if who else "an"
            return (kind, who, kan)

def get_all():
    h = "html"
    dir_list = [i for i in os.listdir(h) if i[0]!="."]
    for year in dir_list[6:]:
        if not os.path.exists(os.path.join(xml_save_dir,year)):
            os.mkdir(os.path.join(xml_save_dir,year))
        html_list = [i for i in os.listdir(os.path.join(h, year)) if i[0]!="."]
        for html in html_list:
            haihu_list = open(os.path.join(h, year, html)).read()
            if haihu_list:
                haihu_list = haihu_d_list(haihu_list)
                for url in haihu_list:
                    sys.stderr.write("\ryear={}, html={}, url={}".format(year, html, url))
                    sys.stdout.flush()
                    save_name = os.path.join(xml_save_dir, year, url.split("/")[-1][1:])+".xml"
                    if os.path.exists(save_name):
                        continue
                    try:
                        a = get_xml(url, save_name)
                        #time.sleep(10)
                    except urllib.error.URLError as e:
                        print(e.reason)
                    except ET.ParseError as e:
                        print(e)
                        with open("error.log","a") as f:
                            f.write(url+"\n")
                        #time.sleep(5)
