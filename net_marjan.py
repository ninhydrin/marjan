import chainer
import chainer.functions as F
import chainer.links as L
import numpy as np
#from MaskLinear import *
#from MaskConv import *

class ValueNetwork(chainer.Chain):
    self.insize = 14 + 24*3 + 12*4

    def __init__(self):
        super(Alex, self).__init__(
            fc1=L.Linear(self.insize, 4096),
            fc2=L.Linear(4096, 4096),
            fc3=L.Linear(4096, 2048),
            fc4=L.Linear(2048, 1024),
            fc5=L.Linear(1024, 14),
        )
        self.train = True
        self.fc1_dropout_rate=0.5
        self.fc2_dropout_rate=0.5
        self.fc3_dropout_rate=0.5
        self.fc4_dropout_rate=0.5

    def clear(self):
        self.loss = None
        self.accuracy = None

    def cal_ratio(self):
        self.fc6_dropout_rate=np.sqrt(float((self.fc6.W.data != 0).sum())/float(self.fc6.W.data.size))*0.5
        self.fc7_dropout_rate=np.sqrt(float((self.fc7.W.data != 0).sum())/float(self.fc7.W.data.size))*0.5

    def __call__(self, x, t):
        self.clear()
        h = F.dropout(F.relu(self.fc1(h)), ratio=self.fc1_dropout_rate, train=self.train)
        h = F.dropout(F.relu(self.fc2(h)), ratio=self.fc2_dropout_rate, train=self.train)
        h = F.dropout(F.relu(self.fc3(h)), ratio=self.fc3_dropout_rate, train=self.train)
        h = F.dropout(F.relu(self.fc4(h)), ratio=self.fc4_dropout_rate, train=self.train)
        h = self.fc5(h)
        self.loss = F.softmax_cross_entropy(h, t)
        self.accuracy = F.accuracy(h, t)
        return self.loss,self.accuracy


class PoricyNetwork(chainer.Chain):
    self.insize = 14 + 24*3 + 12*4

    def __init__(self):
        super(Alex, self).__init__(
            fc1=L.Linear(self.insize, 4096),
            fc2=L.Linear(4096, 4096),
            fc3=L.Linear(4096, 2048),
            fc4=L.Linear(2048, 1024),
            fc5=L.Linear(1024, 14),
        )
        self.train = True
        self.fc1_dropout_rate=0.5
        self.fc2_dropout_rate=0.5
        self.fc3_dropout_rate=0.5
        self.fc4_dropout_rate=0.5

    def clear(self):
        self.loss = None
        self.accuracy = None

    def cal_ratio(self):
        self.fc6_dropout_rate=np.sqrt(float((self.fc6.W.data != 0).sum())/float(self.fc6.W.data.size))*0.5
        self.fc7_dropout_rate=np.sqrt(float((self.fc7.W.data != 0).sum())/float(self.fc7.W.data.size))*0.5

    def __call__(self, x, t):
        self.clear()
        h = F.dropout(F.relu(self.fc1(h)), ratio=self.fc1_dropout_rate, train=self.train)
        h = F.dropout(F.relu(self.fc2(h)), ratio=self.fc2_dropout_rate, train=self.train)
        h = F.dropout(F.relu(self.fc3(h)), ratio=self.fc3_dropout_rate, train=self.train)
        h = F.dropout(F.relu(self.fc4(h)), ratio=self.fc4_dropout_rate, train=self.train)
        h = self.fc5(h)
        self.loss = F.softmax_cross_entropy(h, t)
        self.accuracy = F.accuracy(h, t)
        return self.loss,self.accuracy
