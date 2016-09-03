import sys
import xml.etree.ElementTree as ET

from mj2 import Pai, Tehai


class TenhouPlayer():

    def __init__(self, num, tehai):
        self.seat = int(num)
        self.tehai = Tehai([Pai.from_index(int(i)) for i in tehai])
        self.oya = 0
        self.sute =[]
        self.reach = None
        self.ten =25000
        self.my_tsumo, self.my_sute = [("T","D"),("U","E"),("V","F"),("W","G")][self.seat]
        self.jihai = ["東","西","南","北","白","發","中"]
        self.tsumo_num = 0
        self.naki_info=[]

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

    def add_naki_info(self, info):
        self.naki_info.append(info)

    def set_reach(self):
        self.reach = (self.tsumo_num)

    def tsumo(self, hai):
        hai = Pai.from_index(hai)
        print ("player {}: ツモ:{} 手牌:{}".format(self.seat, hai, self.tehai))
        self.tsumo_num+=1
        self.tehai.append(hai)
        self.tehai.sort()

    def naki(self, hai):
        hai = Pai.from_index(hai)
        print ("player {}: 鳴き:{} 手牌:{}".format(self.seat, hai, self.tehai))
        self.tsumo_num+=1
        self.tehai.append(hai)
        self.tehai.sort()


class TenhouGame:

    def __init__(self, xml_path):
        xml = ET.fromstring(open(xml_path).read())
        data = self.match_parse(xml)
        self.seed = data[0]
        self.taikyoku = data[1:]

    def replay (self, num):

        if len(self.taikyoku) <= num:
            print("num < {}".format(len(self.taikyoku)))
            return None

        match = self.taikyoku[num]
        players = self.__init_player(match["INIT"])
        haihu = match["SUTE"]
        #datas = TrainData()

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
                naki_info =self.__naki(int(item["m"]))
                print (naki_info)
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

        if "AGARI" in self.taikyoku[num]:
            self.__agari(match["AGARI"])
        #return datas

    @classmethod
    def match_parse(cls, xml):
        all_list = xml
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

    @classmethod
    def __agari(cls, data):
        data = {i[0]:i[1] for i in data}
        print("AGARI {}".format(data["who"]))
        print ("atari = {}".format(Pai.from_index(int(data["machi"]))))
        print ("hai ={}".format([Pai.from_index(int(i)) for i in data["hai"].rsplit(",")]))

    @classmethod
    def __init_player(cls, init):
        players = {}
        sorted(init)
        for i in init:
            if "hai" in i[0]:
                players[int(i[0][-1])]=TenhouPlayer(i[0][-1],i[1].rsplit(","))
            elif "oya" in i[0]:
                oya_num=int(i[1])
        players[oya_num].oya = 1
        return players

    @classmethod
    def __naki(cls, num):
        bit = "{0:016}".format(int(bin(num)[2:]))
        who = int(bit[-2:],2)
        if int(bit[-3]):#ちー
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
            return ("qi", who, naki_pai, mentsu)
        else:
            if int(bit[-4]):#ぽん
                type_seven = int(bit[:7],2)
                pon_pai = Pai.all()[type_seven // 3]
                amari_pai = int(bit[-7:-5],2)
                naki_pai = Pai.from_index(pon_pai.suit*36+pon_pai.num*4+type_seven % 3)
                mentsu = [Pai.from_index(pon_pai.suit*36+pon_pai.num*4+i) for i in range(4) if i != amari_pai]
                return ("pon", who, naki_pai ,mentsu)

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
