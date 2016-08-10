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

    def set_oya(self, oya=0):
        self.oya=oya

    def adjustment(self, ten):
        self.ten += ten

    def throw(self, hai):
        try:
           self.tehai.remove(hai)
           self.sute.append(hai)
           print (self.my_num, self.tehai)
        except ValueError:
            pass

    def tsumo(self, hai):
        self.tehai.append(hai)
        print (self.my_num, self.tehai)

    def shonpai_tahai(self):
        assert len(self.tehai) == 13
