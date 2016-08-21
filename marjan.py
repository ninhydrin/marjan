# coding:utf-8
import sys, os
from mj2 import Pai

class Player():

    def __init__(self, num, tehai):
        self.my_num = int(num)
        self.tehai = [int(i) for i in tehai]
        self.oya = 0
        self.sute =[]
        self.reach = None
        self.ten =25000
        self.my_tsumo, self.my_sute = [("T","D"),("U","E"),("V","F"),("W","G")][self.my_num]
        self.jihai = ["東","西","南","北","白","發","中"]
        self.tsumo_num = 0
        self.naki_info=[]

    @property
    def sute_num(self):
        return len(self.my_sute)

    def set_oya(self, oya=0):
        self.oya=oya

    def adjustment(self, ten):
        self.ten += ten

    def throw(self, hai):
        try:
           self.tehai.remove(hai)
           self.sute.append(hai)
           self.tehai.sort()
           print("捨て:{} {}".format(Pai.from_index(int(hai)),hai))
        except ValueError:
            pass

    def add_naki_info(self, info):
        self.naki_info.append(info)

    def set_reach(self):
        self.reach = (self.tsumo_num)

    def tsumo(self, hai):
        print ("ツモ:{}".format(Pai.from_index(hai)))
        self.tsumo_num+=1
        self.tehai.append(hai)
        self.tehai.sort()
        print (self.my_num, self.print_tehai())

    def shonpai_tahai(self):
        assert len(self.tehai) == 13

    def print_tehai(self):
        kari_tehai = [Pai.from_index(i) for i in self.tehai]
        return kari_tehai
        tehai = []
        for i in kari_tehai:
            if i < 9:
                hai = "m{}".format(i)
            elif i< 18:
                hai = "p{}".format(i-9)
            elif i < 27:
                hai = "s{}".format(i-18)
            else:
                hai = self.jihai[ i-27]
            tehai.append(hai)
        return tehai
