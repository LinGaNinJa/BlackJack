class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    # 顯示這張牌本身具有的花色跟點數
    def Dump(self):
        switcher = {0: "CLUB", 1: "DIAMOND", 2: "HEART", 3: "SPADE"}
        ranks = ["A", "2", "3", "4", "5", "6",
                 "7", "8", "9", "10", "J", "Q", "K"]

        prtSuit = switcher[self.suit]
        prtRank = ranks[self.rank - 1]
        print(prtSuit + ' ' + prtRank, end=',\t')
