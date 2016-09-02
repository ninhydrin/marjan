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
        self.naki = []
        self.ron_pais = ()
        self.chi_pais = ()
        self.pon_pais = ()

    def tsumo(self, yama):
        hai = yama.tsumo()
        print ("player {}: tsumo_hai={}, tehai={}".format(self.seat, hai, self.tehai))
        if hai in self.ron_pais:
            print("player {} tsumo! : tehai={} tsumo_hai={}".format(self.seat, self.tehai, hai))
            return True
        self.tehai.append(hai)
        self.tehai.rihai()

    def sutehai(self, num):
        sute = self.tehai.pop(num)
        self.sute.append(sute)
        return sute

    def check_action(self, pai):
        """
        returnは
        ron:0, pon:1, chi:2
        """
        if pai in self.ron_pais:
            return 0
        elif pai in self.pon_pais:
            return 1
        elif pai in self.chi_pais:
            return 2
        else:
            return 3

    def think(self):
        """
        一応リターンする
        """
        tenpai={}
        shanten = []
        for i in range(14):
            kari_tehai = Tehai(self.tehai.copy())
            pop_pai = kari_tehai.pop(i)
            tenpai_koho = Helper.check_tenpai(kari_tehai)
            if tenpai_koho:
                tenpai[pop_pai] = set([])
                for tenpai_i in tenpai_koho:
                    for pai in tenpai_i[-1]:
                        #tenpai.append ([tenpai_i,pop_pai])
                        tenpai[pop_pai].add(pai)

            if not tenpai:
                shanten_koho = Helper.check_shanten(kari_tehai)
                if shanten_koho:
                    for shanten_i in shanten_koho:
                        if shanten_i not in shanten:
                            shanten.append([shanten_i, pop_pai])

        if tenpai:
            print (tenpai)
            pop_pai, self.ron_pais = max(tenpai.items(), key=lambda x:len(x[1]))
            return self.sutehai(self.tehai.index(pop_pai))

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

    def play(self):
        self.tsumo(self.yama)
        pai = now_player.think()
        print(self.who_turn, pai)

class Game():

    def __init__(self):
        self.players = [Player(i) for i in range(4)]
        self.yama = Yama()
        self.turn = 0
        self.who_turn = random.randint(0,3)
        haipai = self.yama.haipai()
        self.end_flag = False

        for i in range(4):
            self.players[i].new_game(haipai[i],i==self.who_turn)

    def check_players(self, pai):
        """アガるもしくは鳴くかを確認する

        """
        rons = []
        pons = []
        chies = []
        for i in range(4):
            if i == self.who_turn:
                continue
            action = self.players[i].check_action(pai)
            if action == 0:
                rons.append(i)
            elif action == 1:
                pons.append(i)
            elif action == 2:
                chies.append(i)
        if rons:
            for p in rons:
                print ("player {} ron!:tehai = {}".format(p, self.players[p].tehai))
            return True
        return False

    def player_turn(self):
        self.turn+=1
        now_player = self.players[self.who_turn]
        if now_player.tsumo(self.yama):
            self.end_flag = True
            return 0
        pai = now_player.think()
        print("sute {}\n".format(pai))
        if self.check_players(pai):
            self.end_flag = True
            return 0
        self.who_turn = self.who_turn+1 if self.who_turn < 3 else 0

    @property
    def remaining_yama(self):
        return len(self.yama)-14

    def auto_play(self):
        while self.remaining_yama and not self.end_flag:
            self.player_turn()
        if not self.remaining_yama and not self.end_flag:
            print("Ryukyoku")
