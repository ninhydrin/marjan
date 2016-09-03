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

def get_haihu_name(old=False):
    url = "http://tenhou.net/sc/raw/list.cgi"
    if old:
        url = "http://tenhou.net/sc/raw/list.cgi?old"
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

def get_old():
    finished_list = os.listdir("html/2016")
    haihu_list = get_haihu_name(True)
    for haihu_gz_url in haihu_list:
        sys.stderr.write("\rurl={}".format(haihu_gz_url))
        sys.stdout.flush()
        if haihu_gz_url[-19:-3] not in finished_list:
            haihu_gz = download_file(haihu_gz_url)
            html_str = gz_extract(haihu_gz)
            with open("html/2016/"+haihu_gz[7:-3],"wb") as f:
                f.write(html_str)
