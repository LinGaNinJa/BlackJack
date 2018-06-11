import random
from Card import Card


class Deck:
    '''
    生成一個六副牌組成且隨機排序的牌堆，top為準備要發出去的牌
    '''

    def __init__(self, nDeck=6, seed=None, presetCards=None):
        self.nDeck = nDeck
        self.top = 0
        self.playcard = []
        if seed is not None:
            random.seed(seed)

        if presetCards is not None:
            self.playcard = []
            for i in presetCards:
                self.playcard.append(i)
            return

        # 六副牌
        # temp = [0, 1, 2, 3, ..., 51, 0, 1, ..., 51]
        temp = [x for x in range(52)] * self.nDeck
        random.shuffle(temp)  # 將temp中的數字隨機排序
        for num in temp:  # 每個數字代表一張牌
            s = num // 13
            r = num % 13 + 1
            self.playcard.append(Card(s, r))

    def DealACard(self):
        self.top += 1
        return self.playcard[self.top - 1]

    # 檢查牌堆還有沒有牌可以發
    def HasMoreCard(self):
        return self.top < 52

    def Show(self):
        for card in self.playcard:
            card.Dump()
