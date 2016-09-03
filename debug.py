"""

1:[[  0,   1,   2,   3],#萬
2:[  4,   5,   6,   7],
3:[  8,   9,  10,  11],
4:[ 12,  13,  14,  15],
5:[ 16,  17,  18,  19],
6:[ 20,  21,  22,  23],
7:[ 24,  25,  26,  27],
8:[ 28,  29,  30,  31],
9:[ 32,  33,  34,  35],

1:[ 36,  37,  38,  39],#筒
2:[ 40,  41,  42,  43],
3:[ 44,  45,  46,  47],
4:[ 48,  49,  50,  51],
5:[ 52,  53,  54,  55],
6:[ 56,  57,  58,  59],
7:[ 60,  61,  62,  63],
8:[ 64,  65,  66,  67],
9:[ 68,  69,  70,  71],

1:[ 72,  73,  74,  75],#索
2:[ 76,  77,  78,  79],
3:[ 80,  81,  82,  83],
4:[ 84,  85,  86,  87],
5:[ 88,  89,  90,  91],
6:[ 92,  93,  94,  95],
7:[ 96,  97,  98,  99],
8:[100, 101, 102, 103],
9:[104, 105, 106, 107],

[108, 109, 110, 111],#字
[112, 113, 114, 115],
[116, 117, 118, 119],
[120, 121, 122, 123],
[124, 125, 126, 127],
[128, 129, 130, 131],
[132, 133, 134, 135]])
"""

from mj2 import Helper, Pai, Yama, Tehai
from tenho_replay import TenhouGame, TenhouPlayer

class Debug:
        '''for debug'''

        TEST_HOHRA = [
            [2, 3, 3, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7],
            [0, 1, 28, 29, 40, 41, 52, 53, 72, 73, 88, 89, 104, 105],      # ちーといつ
            [0, 32, 36, 68, 72, 104, 108, 112, 116, 120, 124, 128, 132, 133],      # こくしむそう
            [33, 33, 33, 32, 32, 32, 31, 31, 31, 0, 0, 0, 2, 2],    # だいさんげん
            [0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 8, 1],      # ちゅうれんぽうとう
            [19, 19, 20, 20, 21, 21, 23, 23, 23, 25, 25, 32, 32, 32],      # りゅういーそう
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 5, 5, 0, 1, 2],      # ちんいつ いっつー いーぺーこう
        ]

        TEST_TENPAI = [
                [0, 32, 36, 68, 72, 104, 108, 112, 116, 120, 124, 128, 132],      # 国士13
                [0, 32, 33, 36, 68, 72, 104, 108, 112, 116, 124, 128, 132],      # 国士13
                [0, 1, 2, 4, 8, 12, 16, 20, 24, 28, 32, 33, 34],      # 純正ちゅうれんぽうとう
                [0, 4, 8, 12, 16, 17, 18, 20, 40, 40, 60, 64, 68],  # かんちゃん しゃぼ(順子がからむやつ)
                [40, 44, 48, 72, 76, 80, 88, 89, 100, 101, 102, 128, 129],   #かんちゃん
                [24, 25, 26, 0, 4, 8, 40, 44, 48, 41, 100, 101, 102],  # りゃんめん たんき
                [24, 25, 26, 0, 4, 8, 40, 44, 48, 52, 100, 101, 102],  # のべたん
                [96, 97, 98, 0, 4, 8, 40, 44, 48, 41, 45, 88, 89],   # りゃんめん
                [0, 1, 28, 29, 40, 41, 52, 53, 72, 73, 88, 104, 105],      # ちーといつ
                [0, 4, 8, 12, 13, 16, 20, 24, 25, 28, 32, 128, 129],    # しゃぼ
                [0, 4, 8, 12, 13, 16, 20, 24, 25, 28, 32, 100, 104],    # しゃぼ

        ]
        TEST_ISHAN = [
                [0, 1, 2, 4, 8, 12, 16, 20, 24, 28, 32, 33, 34],      # 純正ちゅうれんぽうとう
                [0, 4, 8, 12, 16, 17, 18, 20, 40, 40, 60, 64, 68],  # かんちゃん しゃぼ(順子がからむやつ)
                [40, 44, 48, 72, 76, 80, 88, 89, 100, 101, 102, 128, 129],   #かんちゃん
                [24, 25, 26, 0, 4, 8, 40, 44, 48, 41, 100, 101, 102],  # りゃんめん たんき
                [24, 25, 26, 0, 4, 8, 40, 44, 48, 52, 100, 101, 102],  # のべたん
                [96, 97, 98, 0, 4, 8, 40, 44, 48, 41, 45, 88, 89],   # りゃんめん
                [0, 1, 28, 29, 40, 41, 52, 53, 72, 73, 88, 104, 105],      # ちーといつ
                [0, 4, 8, 12, 13, 16, 20, 24, 25, 28, 32, 128, 129],    # しゃぼ
                [0, 4, 8, 12, 13, 16, 20, 24, 25, 28, 32, 100, 116],    # しゃぼ
                [17, 21, 24, 41, 42, 48, 59, 61, 66, 67, 88, 93, 99], 
        ]

        @classmethod
        def tehai_from_indexes(cls, indexes):
            assert(len(indexes) == 13 or len(indexes) == 14)
            return Tehai([ Pai.from_index(x) for x in indexes ])

        @classmethod
        def test_hohra(cls, idx = None):
            '''和了形のテスト'''
            return cls.tehai_from_indexes(cls.TEST_HOHRA[idx])

        @classmethod
        def test_tenpai(cls, idx = 0):
            '''聴牌形のテスト'''
            return cls.tehai_from_indexes(cls.TEST_TENPAI[idx])

        @classmethod
        def gen_tehai(cls, num = 14):
            '''適当に配牌形を作る'''
            assert(num == 13 or num == 14)
            yama = Yama()
            return Tehai([ yama.tsumo() for x in range(num) ])

        @classmethod
        def gen_hohra(cls):
            '''適当にアガリ形を作る'''
            tehai = Tehai()

            def gen_syuntsu():
                '''順子作る'''
                first = Pai.from_index(random.choice(range(Pai.TOTAL_KIND_NUM)))
                if first.suit == Pai.Suit.J:
                    # 字牌は順子できない
                    return None

                if first.num > 7:
                    # (7 8 9) 以上は順子できない
                    return None

                second = Pai(first.suit, first.num+1)
                third  = Pai(first.suit, first.num+2)

                if tehai.count(first) == 4 or tehai.count(second) == 4 or tehai.count(third) == 4:
                    # 残枚数不足
                    return None

                return [first, second, third]

            def gen_kohtu():
                '''刻子作る'''
                pai = Pai.from_index(random.choice(range(Pai.TOTAL_KIND_NUM)))
                if tehai.count(pai) >= 2:
                    # 残枚数不足
                    return None
                return [pai, pai, pai]

            def gen_atama():
                '''雀頭作る'''
                pai = Pai.from_index(random.choice(range(Pai.TOTAL_KIND_NUM)))
                if tehai.count(pai) >= 3:
                    # 残枚数不足
                    return None
                return [pai, pai]

            tehai.extend(gen_atama())   # 雀頭

            # 順子と刻子が同じ出現確率だとアレなので重み付けしておく
            weighted_choices = [(gen_syuntsu, 3), (gen_kohtu, 1)]
            population = [val for val, cnt in weighted_choices for i in range(cnt)]
            while len(tehai) < 14:
                ret = random.choice(population)()
                if ret is not None:
                    tehai.extend(ret)
            return tehai

        @classmethod
        def gen_tenpai(cls):
            '''適当に聴牌形を作る'''
            tehai = cls.gen_hohra()
            assert(len(tehai) == 14)
            # アガリ形から適当に1個ぶっコ抜く
            tehai.pop(random.randrange(len(tehai)))
            return tehai


class Test:
        '''for test'''

        @classmethod
        def check_tenho(cls):
            '''天和チェック'''
            import sys
            for cnt in (x for x in itertools.count()):
                print >>sys.stderr, cnt
                yama = Yama()
                oya, _, _, _ = yama.haipai()
                ret = check_hohra(oya)
                if ret:
                    print ("---------------------------------------------")
                    print (cnt)
                    oya.show()
                    for atama, mentsu in ret:
                        print (atama, mentsu)
                    break

        @classmethod
        def check_machi(cls, times = 100):
            '''待ちを大量にチェック'''
            for x in range(times):
                tehai = Debug.gen_tenpai()
                ret = check_tenpai(tehai.rihai())
                print(tehai)
                print(ret)
                print("----------------------------------------------------------")
                if not ret:
                    # ここに来たらテンパってない。要は不具合。修正対象の手牌。
                    print (oya)
                    print ([ Pai.from_name(repr(x)).index for x in oya ])
            print ("complete.")
        @classmethod
        def tenpai(cls):
                for pai in Debug.TEST_TENPAI:
                        tehai = Tehai([Pai.from_index(i) for i in pai])
                        ans = Helper.check_tenpai(tehai)
                        print ("tehai:",tehai)
                        print (ans)
                        print("----------------------------------------------------------")

if __name__ == '__main__':
    #Test.check_machi()
    pass
