# -*- coding: utf-8 -*-
import random

from mj2 import Yama,Pai,Tehai

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

    def think(self):
        a = random.randint(0,13)
        self.sutehai(a)

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

    def check_players(self):
        """アガるもしくは鳴くかを確認する
        """
        pass

    def player_turn(self):
        self.turn+=1
        now_player = self.players[self.who_turn]
        now_player.tsumo(self.yama)
        now_player.think()
        self.check_players()
        self.who_turn = self.who_turn+1 if self.who_turn < 3 else 0

    @property
    def remaining_yama(self):
        return len(self.yama)-14

    def auto_play(self):
        while self.remaining_yama:
            self.player_turn()
