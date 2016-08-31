# -*- coding: utf-8 -*-
import random

from mj2 import Yama,Pai,Tehai,Helper

class Player():

    def __init__(self, seat):
        self.seat = seat
        self.point = 25000

    def new_game(self, tehai, oya):
        self.tehai = tehai
        self.oya = oya
        self.sute = []

    def tsumo(self, yama):
        hai = yama.tsumo()
        self.tehai.append(hai)
        self.tehai.rihai()

    def sutehai(self, num):
        sute = self.tehai.pop(num)
        self.sute.append(sute)
        return sute

    def action(self, pai):
        pass
    
    def think(self):
        """
        一応リターンする
        """
        tenpai=[]
        shanten = []
        print (self.tehai)
        for i in range(14):
            kari_tehai = Tehai(self.tehai.copy())
            pop_pai = kari_tehai.pop(i)
            tenpai_koho = Helper.check_tenpai(kari_tehai)
            if tenpai_koho:
                for tenpai_i in tenpai_koho:
                    if tenpai_i not in tenpai:
                        tenpai.append ([tenpai_i,pop_pai])

            if not tenpai:
                shanten_koho = Helper.check_shanten(kari_tehai)
                if shanten_koho:
                    for shanten_i in shanten_koho:
                        if shanten_i not in shanten:
                            shanten.append([shanten_i, pop_pai])

        if tenpai:
            random.shuffle(tenpai)
            print (tenpai)
            return self.sutehai(self.tehai.index(tenpai[0][-1]))

        elif shanten:
            random.shuffle(shanten)
            #print ("shanten",shanten)
            shanten = shanten[0][0][1]
            #print(shanten)
            for key, item in shanten.items():
                if key.suit == Pai.Suit.J and item < 2:
                    return self.sutehai(self.tehai.index(key))

            for key, item in shanten.items():
                if key in Pai.yaochupai():
                    return self.sutehai(self.tehai.index(key))

            for key, item in shanten.items():
                if item < 2:
                    return self.sutehai(self.tehai.index(key))

        else:
            for pai in self.tehai[::-1]:
                if pai in Pai.yaochupai():
                    return self.sutehai(self.tehai.index(pai))

            if len(self.tehai)==14:
                return self.sutehai(random.randint(0,13))



class Game():

    def __init__(self):
        self.players = [Player(i) for i in range(4)]
        self.yama = Yama()
        self.turn = 0
        oya = random.randint(0,3)
        self.who_turn = oya
        haipai = self.yama.haipai()
        for i in range(4):
            self.players[i].new_game(haipai[i],i==oya)

    def check_players(self, sute_hai):
        """アガるもしくは鳴くかを確認する
        """
        for i in range(4):
            if i == self.who_turn:
                continue

        pass

    def player_turn(self):
        self.turn+=1
        now_player = self.players[self.who_turn]
        now_player.tsumo(self.yama)
        pai = now_player.think()
        print(self.who_turn, pai)
        self.check_players(pai)
        self.who_turn = self.who_turn+1 if self.who_turn < 3 else 0

    @property
    def remaining_yama(self):
        return len(self.yama)-14

    def auto_play(self):
        while self.remaining_yama:
            self.player_turn()
