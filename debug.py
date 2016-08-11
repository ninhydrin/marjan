class Debug:
        '''for debug'''

        TEST_HOHRA = [
            [2, 3, 3, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7],
            [0, 0, 8, 8, 13, 13, 20, 20, 25, 25, 29, 29, 31, 31],      # ちーといつ
            [0, 8, 9, 17, 18, 26, 27, 28, 29, 30, 31, 32, 33, 9],      # こくしむそう
            [33, 33, 33, 32, 32, 32, 31, 31, 31, 0, 0, 0, 2, 2],    # だいさんげん
            [0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 8, 1],      # ちゅうれんぽうとう
            [19, 19, 20, 20, 21, 21, 23, 23, 23, 25, 25, 32, 32, 32],      # りゅういーそう
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 5, 5, 0, 1, 2],      # ちんいつ いっつー いーぺーこう
        ]

        TEST_TENPAI = [
            [0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 8],      # 純正ちゅうれんぽうとう
            [1, 2, 3, 4, 5, 5, 5, 6, 20, 20, 21, 22, 23],  # かんちゃん しゃぼ(順子がからむやつ)
            [13, 14, 15, 18, 19, 19, 20, 21, 24, 24, 24, 31, 31],   # りゃんめん かんちゃん
            [25, 25, 25, 1, 2, 3, 11, 12, 13, 11, 23, 23, 23],  # りゃんめん たんき
            [25, 25, 25, 1, 2, 3, 11, 12, 13, 11, 12, 23, 24],   # りゃんめん
            [1, 2, 3, 4, 4, 6, 7, 8, 9, 10, 11, 29, 29],    # しゃぼ
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


if __name__ == '__main__':
    #Test.check_machi()
    pass
