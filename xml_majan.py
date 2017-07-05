#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
天鳳のスクレイピング
"""
import os, sys, time
import xml.etree.ElementTree as ET
import urllib.request
import gzip
import json

import requests
import bs4
from train import TrainData
from mj2 import Pai


class TenhoDownloader:
    xml_dir = "xml_dir"
    gz_dir = "gz_dir"
    if not os.path.isdir(xml_dir):
        os.mkdir(xml_dir)
        os.mkdir(gz_dir)

    @classmethod
    def get_haihu_name(cls, old=False):
        """gzファイルのリストを取得
        """
        url = "http://tenhou.net/sc/raw/list.cgi"
        if old:
            url = "http://tenhou.net/sc/raw/list.cgi?old"
        souce_url = "http://tenhou.net/sc/raw/dat/"
        response = urllib.request.urlopen(url)
        data = response.read()
        data_list = json.loads(data.decode("utf-8").replace("file",'"file"').replace("size",'"size"').replace("\r\n", "").replace("'", '"')[5:-2])
        distillation_data_list = [souce_url + i["file"] for i in data_list if "scc" in i["file"]]
        return distillation_data_list

    @classmethod
    def download_file(cls, url, filename=None):
        if not filename:
            filename = os.path.join(cls.gz_dir, url.split('/')[-1])
        r = requests.get(url, stream=True)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
            return filename
        return False

    @classmethod
    def gz_extract(cls, filename):
        with gzip.open(filename, "rb") as f:
            content = f.read()
        return content

    @classmethod
    def haihu_html_list(cls, html):
        soup = bs4.BeautifulSoup(html, "lxml")
        return [i["href"].replace("/?log=", "/log/?") for i in soup.p.find_all("a")]

    @classmethod
    def get_xml(cls, url, save_name=None):
        """urlを渡すとデータを持ってくる
        """
        response = requests.get(url)
        data = response.content
        data = ET.fromstring(data)
        if not save_name is None:
            tree = ET.ElementTree(data)
            tree.write(save_name)
        return data

    @classmethod
    def get_all(cls):
        h = "html"
        dir_list = [i for i in os.listdir(h) if i[0] != "."]
        for year in dir_list[6:]:
            if not os.path.exists(os.path.join(cls.xml_dir, year)):
                os.mkdir(os.path.join(cls.xml_dir, year))
            html_list = [i for i in os.listdir(os.path.join(h, year)) if i[0] != "."]
            for html in html_list:
                haihu_list = open(os.path.join(h, year, html)).read()
                if haihu_list:
                    haihu_list = cls.haihu_html_list(haihu_list)
                    for url in haihu_list:
                        sys.stderr.write("\ryear={}, html={}, url={}".format(year, html, url))
                        sys.stdout.flush()
                        save_name = os.path.join(cls.xml_dir, year, url.split("/")[-1][1:])+".xml"
                        if os.path.exists(save_name):
                            continue
                        try:
                            a = cls.get_xml(url, save_name)
                            #time.sleep(10)
                        except urllib.error.URLError as e:
                            print(e.reason)
                        except ET.ParseError as e:
                            print(e)
                            with open("error.log","a") as f:
                                f.write(url+"\n")
                                #time.sleep(5)

    def get_old(cls):
        finished_list = os.listdir("html/2016")
        haihu_list = cls.get_haihu_name(True)
        for haihu_gz_url in haihu_list:
            sys.stderr.write("\rurl={}".format(haihu_gz_url))
            sys.stdout.flush()
            if haihu_gz_url[-19:-3] not in finished_list:
                haihu_gz = download_file(haihu_gz_url)
                html_str = gz_extract(haihu_gz)
                with open("html/2016/"+haihu_gz[7:-3],"wb") as f:
                    f.write(html_str)
