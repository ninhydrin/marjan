import numpy as np

class TrainData:
    def __init__(self):
        self.sutehai = np.zeros([4,24,136])
        self.sute_num = [0]*4
        self.vec =[]

    def make_vec(self, players, num):
        ans = np.zeros(136)
        tehai = np.zeros(136)
        for i in players[num].tehai:
            tehai[i] = 1
        ans[players[num].sute[-1]]=1
        self.sutehai[num][self.sute_num[num]][players[num].sute[-1]]=1
        self.sute_num[num]+=1
        self.vec.append(np.hstack([tehai,self.sutehai.flatten(), ans.copy()]))
