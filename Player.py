from Card import Card
from StatusChecker import StatusList
from StatusChecker import StatusChecker

'''
player.reset
'''


class Player:

    def __init__(self, name=None):
        # status
        self.safe = True
        self.burst = False
        self.blackJack = False
        self.win = False  # 紀錄點數是否比莊家大
        self.push = False
        # Game status
        self.totalPoints = 0
        self.hand = []
        # Result status
        self.result = ""
        self.gambleCash = 0.0  # 下注的錢
        self.totalCash = 2500.0  # 現有的錢

        if name is not None:
            self.name = name
        else:
            self.name = "Unknown Player"

    def Reset(self):
        # status
        self.safe = True
        self.burst = False
        self.blackJack = False
        self.win = False
        self.push = False
        # Game status
        self.totalPoints = 0
        self.hand = []
        # Result status
        self.result = ""
        self.gambleCash = 0

    # 新增Card類別的物件到hand之中
    def SaveACard(self, card):
        self.hand.append(card)
        status, self.totalPoints = StatusChecker.DetermineStatusAndTotalPoints(
            self.hand)

        if status == StatusList.BLACK_JACK:
            self.safe = False
            self.blackJack = True
        elif status == StatusList.BURST:
            self.safe = False
            self.burst = True

    def Dump(self):
        print()
        print(self.name + " 的手牌：", end='')
        for card in self.hand:
            card.Dump()
        print()
        print("{0} 總點數：{1}".format(self.name, self.totalPoints))

    def WantOneMoreCard(self):
        print()
        print("{0} 要再一張牌嗎？".format(self.name))
        ans = input()
        return ans == 'Y' or ans == 'y'


class Dealer(Player):
    def __init__(self, name=None):
        self.safe = True
        self.burst = False
        self.blackJack = False
        self.totalPoints = 0
        self.hand = []

        self.hide = 0
        self.name = "莊家"

    def Dump(self, show=False):
        print()
        print(self.name + " 的手牌：", end='')

        if show == True:
            for card in self.hand:
                card.Dump()
            print()
            print("{0} 總點數：{1}".format(self.name, self.totalPoints))
            return

        first = False
        for card in self.hand:
            if first == False:
                print("暗牌", end=',\t')
                first = True
                continue
            card.Dump()
        print()

    def WantOneMoreCard(self):
        return self.totalPoints < 17
