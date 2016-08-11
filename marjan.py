# coding:utf-8
import sys, os

class Player():

    def __init__(self, num, tehai):
        self.my_num = int(num)
        self.tehai = tehai
        self.oya = 0
        self.sute =[]
        self.reach = 0
        self.ten =25000
        self.my_tsumo, self.my_sute = [("T","D"),("U","E"),("V","F"),("W","G")][self.my_num]
        self.jihai = ["東","西","南","北","白","發","中"]

    def set_oya(self, oya=0):
        self.oya=oya

    def adjustment(self, ten):
        self.ten += ten

    def throw(self, hai):
        try:
           self.tehai.remove(hai)
           self.sute.append(hai)
           self.tehai.sort()
           print (self.my_num, self.print_tehai())
        except ValueError:
            pass

    def tsumo(self, hai):
        self.tehai.append(hai)
        self.tehai.sort()
        print (self.my_num, self.print_tehai())

    def shonpai_tahai(self):
        assert len(self.tehai) == 13

    def print_tehai(self):
        kari_tehai = [int(i)//4 for i in self.tehai]
        tehai = []
        for i in kari_tehai:
            if i < 9:
                hai = "m{}".format(i+1)
            elif i< 18:
                hai = "p{}".format(i-8)
            elif i < 27:
                hai = "s{}".format(i-16)
            else:
                hai = self.jihai[ i-27]
            tehai.append(hai)
        return tehai
