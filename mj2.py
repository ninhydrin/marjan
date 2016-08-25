#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import random
"""
天鳳は0~135までで表現
"""
class Pai(object):
    '''牌'''

    TOTAL_KIND_NUM = 34          # M/P/S + 字牌合わせた全ての種類
    NUM_OF_EACH_KIND = 4         # 1種類につき4枚
    NUM_OF_EACH_NUMBER_PAIS = 9  # M/P/S の数字牌は1..9まで
    NUM_OF_CHAR_PAIS = 7  #
    RED_LIST = [16, 52, 53, 88]
    class Suit:
        M = 0   # 萬
        P = 1   # 筒
        S = 2   # 策
        J = 3   # 字

        NAMES = {
            M: u"萬",
            P: u"筒",
            S: u"策",
            J: u"　",
        }

    class Num:
        NAMES = ["一", "二", "三", "四", "五", "六", "七", "八", "九"]

    class Tsuhai:
        NAMES = ["東", "南", "西", "北", "白", "撥", "中",]

    @classmethod
    def all(cls):
        '''全ての牌'''
        return [cls(suit, num)
                for suit in cls.Suit.NAMES
                for num in range(9)
                if suit != cls.Suit.J
            ] + [ cls(cls.Suit.J, num) for num in range(7) ]

    @classmethod
    def yaochupai(cls):
        '''么九牌'''
        return [
            cls(cls.Suit.M, 0),
            cls(cls.Suit.M, 8),
            cls(cls.Suit.P, 0),
            cls(cls.Suit.P, 8),
            cls(cls.Suit.S, 0),
            cls(cls.Suit.S, 8)
        ] + [cls(cls.Suit.J, i)for i in range(7)]

    def __init__(self, suit, num, my_num=-1):
        self.suit = suit
        self.num  = num
        self.dora = 0
        self.my_num = my_num
        self.naki = []

    @classmethod
    def chuchanpai(cls):
        '''中張牌'''
        yaochupai = cls.yaochupai()
        return [ x for x in cls.all() if x not in yaochupai ]

    def set_dora(self):
        self.dora +=1

    def is_next(self, other, index=1):
        '''次の数字牌かどうか'''
        if self.suit != self.Suit.J: # 字牌でなくて
            if self.suit == other.suit: # 牌種が同じで
                if other.num == (self.num + index): # 連番
                    return True
        return False

    def is_prev(self, other, index=1):
        '''前の数字牌かどうか'''
        return self.is_next(other, -index)

    @classmethod
    def get_dora_from_dora_display(cls, display_dora):
        """ドラ表示牌からドラのインデックスを返す"""
        if display_dora.suit != cls.Suit.J:
            num = display_dora.num % cls.NUM_OF_EACH_NUMBER_PAIS
            return display_dora.suit*9 + num
        else:
            if display_dora.num == 4:
                return display_dora.suit*9
            elif display_dora.num == 7:
                return display_dora.suit*9 + 4
            else:
                return display_dora.suit*9 + display_dora.num

    @classmethod
    def is_syuntsu(cls, first, second, third):
        '''順子かどうか'''
        return first.is_next(second) and first.is_next(third, 2)

    def __repr__(self):
        if self.suit == self.Suit.J:
            return self.Tsuhai.NAMES[self.num]
        else:
            return (self.Num.NAMES[self.num] + self.Suit.NAMES[self.suit])

    def __eq__(self, other):
        return self.suit == other.suit and self.num == other.num

    def __lt__(self, other):
        return self.suit*9+self.num < other.suit*9 + other.num

    def __hash__(self):
        return self.suit*9 + self.num

    @classmethod
    def from_index(cls, index):
        '''合計136牌のindexから牌を取得'''
        if index < 0 or index > 135:
            return None #TODO Noneでいいのか
        kind = index // cls.NUM_OF_EACH_KIND

        if 0 <= kind < 9:
            suit = cls.Suit.M
            num  = kind
        elif 9 <= kind < 18:
            suit = cls.Suit.P
            num  = kind - 9
        elif 18 <= kind < 27:
            suit = cls.Suit.S
            num  = kind - 18
        elif 27 <= kind < 34:
            suit = cls.Suit.J
            num  = kind - 27

        assert(cls.Suit.M <= suit <= cls.Suit.J)
        assert(0 <= num < cls.NUM_OF_EACH_NUMBER_PAIS)

        return cls(suit, num, index)

    @classmethod
    def from_name(cls, name):
        '''名前から取得'''
        for x in cls.all():
            if name == repr(x):
                return x
        return None

class Yama(list):
    u'''牌山'''
    """王牌は後ろから14枚。14枚のうち後ろから4枚が嶺上牌
    """
    WANPAI_NUM = 14

    class TsumoDoesNotRemain(Exception):
        u'''王牌しか残ってない'''
        pass
    class RinshanTsumoDoesNotRemain(Exception):
        pass

    def __init__(self, red=True):
        pais = [ Pai.from_index(i) 
                for i in range(Pai.TOTAL_KIND_NUM * Pai.NUM_OF_EACH_KIND) ]
        #赤ドラ
        self.open_dora_num = 0
        self.all_list = pais
        self.doras = []
        if red:
            for num in Pai.RED_LIST:
                for pai in pais:
                    if pai.my_num == num:
                        pai.set_dora()
        # 洗牌
        random.shuffle(pais)
        #super(Yama, self).__init__(pais)
        self.tsumo_pai_list =[]
        super().__init__(pais)
        self.open_dora()

    def open_dora(self):
        assert self.open_dora_num < 8
        dora_hyouji = self.wanpai()[self.open_dora_num]
        self.doras.append(dora_hyouji)
        dora_index = Pai.get_dora_from_dora_display(dora_hyouji)
        for pai in self:
            if pai.index == dora_index:
                pai.set_dora()
        for pai in self.tsumo_pai_list:
            if pai.index == dora_index:
                pai.set_dora()
        self.open_dora_num+=2

    def open_ura_dora(self):
        for i in range(1, self.open_dora_num, 2):
            dora_hyouji = self.wanpai()[i]
            self.doras.append(dora_hyouji)
            dora_index = Pai.get_dora_from_dora_display(dora_hyouji)

            for pai in self:
                if pai.index == dora_index:
                    pai.set_dora()
            for pai in self.tsumo_pai_list:
                if pai.index == dora_index:
                    pai.set_dora()

    def tsumo(self):
        u'''自摸'''
        if len(self) <= self.WANPAI_NUM:
            raise self.TsumoDoesNotRemain
        pai = self.pop(0)
        self.tsumo_pai_list.append(pai)
        return pai

    def rinshan_tsumo(self):
        u'''嶺上自摸'''
        if len(self.wanpai()) <= 10:
            raise self.RinshanTsumoDoesNotRemain
        pai = self.wanpai().pop(-1)
        self.tsumo_pai_list.append(pai)
        return pai

    def wanpai(self):
        u'''王牌'''
        return self[-self.WANPAI_NUM:]

    def haipai(self):
        u'''配牌'''
        tehais = [ Tehai(), Tehai(), Tehai(), Tehai() ] # 東(親) 南 西 北

        # 4*3巡
        for j in range(0, 3):
            for tehai in tehais:
                for i in range(0, 4):
                    pai = self.tsumo()
                    tehai.append(pai)

        # ちょんちょん
        for tehai in tehais:
            pai = self.tsumo()
            tehai.append(pai)
        #pai = self.tsumo()
        #tehais[0].append(pai)
        return tehais

class Tehai(list):
    '''手牌'''
    def rihai(self):
        '''理牌'''
        self.sort(key = lambda x: x.suit*9+x.num)
        return self

    @classmethod
    def aggregate(cls, tehai):
        '''{牌種 : 枚数} の形に集計'''
        m_hash = { x: len(list(y)) for x, y in itertools.groupby(tehai.rihai()) }
        # キー（ソート済みの牌）も一緒に返す
        return m_hash, sorted(m_hash.keys(), key=lambda x:x.suit*9 + x.num)

    def show(self):
        '''見やすい形に表示'''
        line1 = u"|"
        line2 = u"|"
        for pai in self.rihai():
            if pai.suit != Pai.Suit.J:
                line1 += Pai.Num.NAMES[pai.num] + u"|"
                line2 += Pai.Suit.NAMES[pai.suit] + u"|"
            else:
                line1 += Pai.Tsuhai.NAMES[pai.num] + u"|"
                line2 += u"　|"

        print (line1.encode("utf-8"))
        print (line2.encode("utf-8"))

    @classmethod
    def search_syuntsu(cls, pais, keys):
        '''順子を探す
        引数は aggregate() の戻り値と同じ形で渡す。'''
        for i in range( len(keys)-2 ):   # ラスト2枚はチェック不要
            tmp = pais.copy()
            first = keys[i]
            if tmp[first] >= 1:
                try:
                    second = keys[i+1]
                    third  = keys[i+2]
                except IndexError as e:
                    # 残り2種無い
                    continue
                if not Pai.is_syuntsu(first, second, third):
                    continue
                if tmp[second] >= 1 and tmp[third] >= 1:
                    tmp[first]  -= 1
                    tmp[second] -= 1
                    tmp[third]  -= 1
                    # 見付かった順子, 残りの牌
                    yield (first, second, third), tmp

    @classmethod
    def search_kohtu(cls, pais, keys):
        '''刻子を探す
        引数は aggregate() の戻り値と同じ形で渡す。'''
        for i, p in enumerate(keys):
            tmp = pais.copy()
            if tmp[p] >= 3:
                tmp[p] -= 3
                # 見付かった刻子, 残りの牌
                yield (p, p, p), tmp

class Helper:
    @classmethod
    def check_shanten(cls, tehai):
        assert(len(tehai) == 13)
        candidate = []
        pais, keys = Tehai.aggregate(tehai)
        searchers = [Tehai.search_syuntsu, Tehai.search_kohtu]
        flag = [False]*2
        for p1 in searchers:
            for p2 in searchers:
                for p3 in searchers:
                    # 適用
                    for m1, a1 in p1(pais, keys):
                        for m2, a2 in p2(a1, keys):
                            for m3, a3 in p3(a2, keys):
                                mentsu = (m1, m2, m3)
                                tartsu = { x[0]:x[1] for x in a3.items() if x[1] > 0 }
                                candidate.append((mentsu,tartsu))
                                flag[0] = True

                            if flag[0]:
                                continue
                            mentsu = (m1, m2)
                            tartsu = { x[0]:x[1] for x in a2.items() if x[1] > 0 }
                            candidate.append((mentsu,tartsu))
                            flag[1]=True

                        if flag[0] or flag[1]:
                            continue
                        mentsu = (m1)
                        tartsu = { x[0]:x[1] for x in a1.items() if x[1] > 0 }
                        candidate.append((mentsu,tartsu))
        return candidate

    @classmethod
    def check_tenpai(cls, tehai):
        #聴牌の形をチェック
        # TODO: 七対子と国士無双の待ちチェック入れてない
        assert(len(tehai) == 13)
        # (アタマ, 面子, 待ち) の形
        candidate = set()

        def check_machi(mentsu, tartsu):
            '''待ちの形を調べる'''
            assert(len(mentsu) == 3)

            keys = sorted(tartsu.keys(), key = lambda x:x.suit*9 + x.num)
            #print mentsu, tartsu, keys

            def check_tanki():
                '''単騎待ちチェック'''
                for i, p in enumerate(keys):
                    tmp = tartsu.copy()

                    if tmp[p] == 3:
                        # 残った面子が刻子
                        assert(len(tmp) == 2)
                        tmp[p] -= 3
                        tanki = {pai: num for pai, num in tmp.items() if num > 0 }.keys()
                        ins = tuple( sorted(mentsu + [(p, p, p)]) )
                        candidate.add( ((), ins, tuple(tanki)) )
                    else:
                        # 残った面子が順子
                        first  = p
                        try:
                            second = keys[i+1]
                            third  = keys[i+2]
                        except IndexError as e:
                            continue

                        if not Pai.is_syuntsu(first, second, third):
                            continue

                        tmp[first]  -= 1
                        tmp[second] -= 1
                        tmp[third]  -= 1
                        tanki = { pai: num for pai, num in tmp.items() if num > 0 }.keys()
                        # 面子に突っ込む
                        ins = tuple( sorted(mentsu + [(first, second, third)]) )
                        candidate.add( ((), ins, tuple(tanki)) )

            def check_non_tanki():
                u'''単騎以外の待ちチェック'''
                for i, p in enumerate(keys):
                    tmp = tartsu.copy()

                    # 雀頭チェック
                    if not tmp[p] >= 2:
                        continue
                    tmp[p] -= 2
                    atama = (p, p)

                    for j, q in enumerate(keys):
                        # 双碰
                        if tmp[q] >= 2:
                            ins = tuple( sorted(mentsu) )
                            candidate.add( (atama, ins, (q, q), (q,)) )
                            break
                        # 両面、辺張
                        try:
                            next_pai = keys[j+1]
                        except IndexError as e:
                            continue
                        if q.is_next(next_pai):
                            n_hai = Pai.from_index(next_pai.my_num+4)
                            p_hai = Pai.from_index(q.my_num-4)
                            ins = tuple( sorted(mentsu) )
                            candidate.add( (atama, ins, (q, next_pai), (p_hai, n_hai)) )
                            break
                        # 嵌張
                        if q.is_next(next_pai, 2):
                            ins = tuple( sorted(mentsu) )
                            middle_hai = Pai.from_index(q.my_num+4)
                            candidate.add( (atama, ins, (q, next_pai), (middle_hai,)) )
                            break

            check_tanki()
            check_non_tanki()

        # 3面子探す
        pais, keys = Tehai.aggregate(tehai)

        searchers = [Tehai.search_syuntsu, Tehai.search_kohtu]
        for p1 in searchers:
            for p2 in searchers:
                for p3 in searchers:
                    # 適用
                    for m1, a1 in p1(pais, keys):
                        for m2, a2 in p2(a1, keys):
                            for m3, a3 in p3(a2, keys):
                                mentsu = [m1, m2, m3]
                                # 残りの牌
                                tartsu = { x[0]:x[1] for x in a3.items() if x[1] > 0 }
                                check_machi(mentsu, tartsu)
        return candidate

    @classmethod
    def check_hohra(cls, tehai):
        assert(len(tehai) == 14)
        candidate = set()

        def check_chitoitsu(pais):
            u'''七対子チェック'''
            if all([ num == 2 for pai, num in pais.items()]):
                return (), [ (pai, pai) for pai, num in pais.items() ]
            return None

        def check_kokushi(pais):
            u'''国士無双チェック'''
            if len(pais) != 13:
                return None

            yaochupai = Pai.yaochupai()
            mentsu = []
            for pai, num in pais.items():
                if pai not in yaochupai:
                    return None
                if num == 2:
                    atama = (pai, pai)
                else:
                    assert(num == 1)
                    mentsu.append(pai)
            return atama, mentsu

        def check_normal(pais, keys):
            searchers = [Tehai.search_syuntsu, Tehai.search_kohtu]
            for p1 in searchers:
                for p2 in searchers:
                    for p3 in searchers:
                        for p4 in searchers:
                            # 適用
                            for m1, a1 in p1(pais, keys):
                                for m2, a2 in p2(a1, keys):
                                    for m3, a3 in p3(a2, keys):
                                        for m4, a4 in p4(a3, keys):
                                            for m5 in keys:
                                                if a4[m5]==2:
                                                    atama=(m5, m5)
                                                    a4[m5]-=2
                                                    mentsu = (m1, m2, m3, m4, atama)
                                                    candidate.add(mentsu)
            return candidate

        pais, keys = Tehai.aggregate(tehai)
        chi = check_chitoitsu(pais)
        if chi:
            return chi
        kokushi = check_kokushi(pais)
        if kokushi:
            return kokushi
        normal = check_normal(pais, keys)
        if normal:
            return normal
        return None

d = Tehai([Pai.from_index(i) for i in [0, 4, 8, 12, 13, 16, 20, 24, 25, 28, 32, 128, 129]])
dd = Tehai([Pai.from_index(i) for i in [96, 97, 98, 0, 4, 8, 40, 44, 48, 41, 45, 88, 89]])
