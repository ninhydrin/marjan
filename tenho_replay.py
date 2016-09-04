import sys
import xml.etree.ElementTree as ET

import numpy as np

from mj2 import Pai, Tehai

class TenhouPlayer():
    class DataSet:
        def __init__(self, oya, ten):
            #self.vec = np.zeros(136+(136 + 136 + 1)*4 + 136)
            self.tehai = vec[:136]
            self.sutehai = [np.zeros(136) for i in range(4)]
            self.naki = [np.zeros(136) for i in range(4)]
            self.reach = 3
            self.dora = np.zeros(136)

    def __init__(self, num):
        self.seat = int(num)
        self.ten =25000
        self.my_tsumo, self.my_sute = [("T","D"),("U","E"),("V","F"),("W","G")][self.seat]
        self.jihai = ["東","西","南","北","白","發","中"]

    def match_ready(self, tehai):
        self.oya = 0
        self.sute =[]
        self.tehai = Tehai([Pai.from_index(int(i)) for i in tehai])
        self.tehai.rihai()
        self.reach = None
        self.tsumo_num = 0
        self.naki_hais=[]

    @property
    def sute_num(self):
        return len(self.my_sute)

    def adjustment(self, ten):
        self.ten += ten

    def throw(self, hai):
        hai = Pai.from_index(int(hai))
        self.tehai.remove(hai)
        self.sute.append(hai)
        print("捨て:{}".format(hai))

    def set_reach(self):
        self.reach = (self.tsumo_num)

    def tsumo(self, hai):
        hai = Pai.from_index(hai)
        print ("P{}: ツモ:{} 手牌:{} 鳴:{}".format(self.seat, hai, self.tehai, self.naki_hais))
        self.tsumo_num+=1
        self.tehai.append(hai)
        self.tehai.sort()

    def naki(self, naki_info):
        """
        naki_info = (鳴きの種類, 誰から, 鳴いた牌, 鳴いたセット)
        """
        self.tsumo_num+=1
        naki_kind = naki_info[0]
        naki_hai = naki_info[2]
        self.tehai.append(naki_hai)
        naki_hai_list = [i.my_num for i in naki_info[3]]
        print(naki_hai_list)
        for i in naki_info[3]:
            for j in range(len(self.tehai)):
                if self.tehai[j].my_num == i.my_num:
                    self.tehai.pop(j)
                    break
        self.tehai.sort()
        self.naki_hais.append(naki_info[3])
        print ("P{}: {}:{} 手牌:{} 鳴:{}".format(self.seat, naki_kind, naki_hai, self.tehai, self.naki_hais))


class TenhouGame:

    def __init__(self, xml_path):
        xml = ET.fromstring(open(xml_path).read())
        data = self.match_parse(xml)
        self.seed = data[0]
        self.taikyoku = data[1:]
        self.player = [TenhouPlayer(i) for i in range(4)]

    def make_data(self):
        pass

    def replay (self, num):

        if len(self.taikyoku) <= num:
            print("num < {}".format(len(self.taikyoku)))
            return None

        match = self.taikyoku[num]
        self.__init_player(match["INIT"])
        players = self.player

        tsumo_moji = ["T","U","V","W"]
        sute_moji = ["D","E","F","G"]

        for i in match["SUTE"]:
            if "REACH" in i.tag:
                for j in i.items():
                    if j[0]=="who":
                        players[int(j[1])].reach=1
                if i.get("step")=="2":
                    print ("REACH")

            elif "N" in i.tag[0]:
                item =  dict(i.items())
                naki_info =self.__naki(item)
                players[int(item["who"])].naki(naki_info)
            else:
                for j, k in enumerate(tsumo_moji):
                    if k == i.tag[0]:
                        players[j].tsumo(int(i.tag[1:]))

                for j, k in enumerate(sute_moji):
                    if k == i.tag[0]:
                        players[j].throw(int(i.tag[1:]))


        if "AGARI" in self.taikyoku[num]:
            self.__agari(match["AGARI"])

        elif "RYUUKYOKU" in self.taikyoku[num]:
            self.__ryuukyoku(match["RYUUKYOKU"])

    @classmethod
    def match_parse(cls, xml):
        all_list = xml
        match_list = [all_list[0].items()]
        #assert all_list[3].tag == "TAIKYOKU"
        match = None
        for i in all_list[4:]:
            if i.tag == "INIT":
                if match:
                    match_list.append(match)
                match = {"SUTE":[],"INIT":dict(i.items())}


            elif i.tag == "AGARI":
                match["AGARI"] = dict(i.items())

            elif i.tag == "RYUUKYOKU":
                match["RYUUKYOKU"] = dict(i.items())

            else:
                match["SUTE"].append(i)
        return match_list

    def __agari(self, data):
        print("AGARI {}".format(data["who"]))
        print ("atari = {}".format(Pai.from_index(int(data["machi"]))))
        #print ("hai ={}".format([Pai.from_index(int(i)) for i in data["hai"].rsplit(",")]))
        sc = [int(i) for i in data["sc"].rsplit(",")]
        for i, ten in enumerate(sc[1::2]):
            self.player[i].ten += ten
            print("P{}:{}".format(i,self.player[i].ten))

    def __ryuukyoku(self, data):
        print("RYUUKYOKU")
        sc = [int(i) for i in data["sc"].rsplit(",")]
        for i, ten in enumerate(sc[1::2]):
            self.player[i].ten += ten
            print("P{}:{}".format(i,self.player[i].ten))

    def __init_player(self, init):
        ten_list = map(int, init["ten"].rsplit(","))
        for i,ten in enumerate(ten_list):
            self.player[i].match_ready(init["hai"+str(i)].rsplit(","))
            self.player[i].ten = ten
        self.player[int(init["oya"])].oya = 1

    @classmethod
    def __naki(cls, item):
        num = int(item["m"])
        who = int(item["who"])
        bit = "{0:016}".format(int(bin(num)[2:]))
        who_sute = int(bit[-2:],2)
        if int(bit[-3]):
            hai_min = int(bit[-5:-3],2)
            hai_mid = int(bit[-7:-5],2)
            hai_max = int(bit[-9:-7],2)
            type_six = int(bit[:6],2)
            min_pai = type_six // 3
            naki_pai = type_six % 3

            if min_pai > 13:
                min_pai += 4
            elif min_pai > 6:
                min_pai += 2

            min_pai = Pai.all()[min_pai]

            hai_min = Pai.from_index(min_pai.suit*36+min_pai.num*4+hai_min)
            hai_mid = Pai.from_index(min_pai.suit*36+min_pai.num*4+hai_mid+4)
            hai_max = Pai.from_index(min_pai.suit*36+min_pai.num*4+hai_max+8)
            mentsu = [hai_min, hai_mid, hai_max]
            naki_pai = mentsu[naki_pai]
            return ("チー", who_sute, naki_pai, mentsu)
        else:
            who_sute = (who_sute + who) % 4
            if bit[-6:-2]=="0000":
                kan_pai = Pai.from_index(int(bit[:8],2))
                kind = "明槓" if who else "暗槓"
                mentsu = [Pai.from_index(kan_pai.suit*36 + kan_pai.num*4 + i) for i in range(4)]
                return (kind, who_sute, kan_pai, mentsu)
            else:
                kind = "ポン" if int(bit[-4]) else "加槓"
                type_seven = int(bit[:7],2)
                pon_pai = Pai.all()[type_seven // 3]
                amari_pai = int(bit[-7:-5],2)
                mentsu = [Pai.from_index(pon_pai.suit*36+pon_pai.num*4+i) for i in range(4) if i != amari_pai]
                naki_pai = mentsu[type_seven % 3]
                return (kind, who_sute, naki_pai, mentsu)
