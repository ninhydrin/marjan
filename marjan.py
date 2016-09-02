# coding:utf-8
import sys, os
from mj2 import Pai,Tehai

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
        self.tehai.sort()
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
