from Deck import Deck
from Player import Player
from Player import Dealer
from time import sleep

'''
所有玩家都沒籌碼的話
'''


class Game:

    def __init__(self):
        self.playerList = []  # playerList可顯示最後result的清單，可保持原本玩家順序，以及拿來reset
        self.removeList = []  # 沒有籌碼的人將被剔除

    # 透過seed可以控制Deck的隨機種子
    def Run(self, seed=None, presetCards=None):
        nDeck = int(input("使用幾副牌? "))
        # For test_black_jack
        if presetCards is not None:
            self.deck = Deck(nDeck=nDeck, presetCards=presetCards)
        elif seed is not None:
            self.deck = Deck(nDeck=nDeck, seed=123)
        else:
            self.deck = Deck(nDeck=nDeck)
        self.SetUpPlayer()

    def SetUpPlayer(self):
        self.nPlayer = int(input("幾位玩家？(1 or 2) "))
        i = 0
        while i < self.nPlayer:
            print("輸入玩家暱稱： ", end='')
            playerName = input()
            self.playerList.append(Player(name=playerName))
            i += 1

        self.dealer = Dealer()
        self.Play()

    def Play(self):
        # -----------------------------------------------------------
        # 檢查是否有足夠玩家
        self.DeletePlayer()
        if len(self.playerList) == 0:
            print("---------------------------------------------")
            print("Game over")
        # 下注籌碼
        self.DealMoney()
        # -----------------------------------------------------------
        # Round 1
        self.DealCard()
        # Round 2
        self.DealCard()
        self.InsuranceCheck()
        # Player hit card or stand
        self.HitCard()
        # -----------------------------------------------------------
        # Compute result
        self.CompareWithDealer()
        self.ShowResult()
        self.AskPlayAgain()

    def DealMoney(self):
        for player in self.playerList:
            print("{0}, 請輸入下注金額: ".format(player.name), end='')
            ans = int(input())
            while ans > player.totalCash or ans <= 0:
                print("下注金額應大於零，但不可大於現有籌碼，請重新輸入")
                print("{0}, 請輸入下注金額: ".format(player.name), end='')
                ans = int(input())
            # Set Cash
            player.gambleCash = ans
            player.totalCash -= player.gambleCash

    def DealCard(self):
        for player in self.playerList:
            player.SaveACard(self.deck.DealACard())
            player.Dump()
            self.ShowPlayerStatus(player)
        self.dealer.SaveACard(self.deck.DealACard())
        self.dealer.Dump()
        sleep(5)
        print("---------------------------------------------")

    def HitCard(self):
        print("加牌階段")
        AllBurst = True
        for player in self.playerList:
            while player.safe and player.WantOneMoreCard() and self.deck.HasMoreCard():
                player.SaveACard(self.deck.DealACard())
                player.Dump()
                sleep(5)
            if player.safe:
                AllBurst = False
            print("---------------------------------------------")
            self.ShowPlayerStatus(player)
        # Deal hit condition: status pass, poinnts < 17, deck has more card, still have alive player
        while not AllBurst and self.dealer.safe and self.dealer.WantOneMoreCard() and self.deck.HasMoreCard():
            self.dealer.SaveACard(self.deck.DealACard())
            self.dealer.Dump()
            sleep(5)
        print("---------------------------------------------")

    def CompareWithDealer(self):
        # 先篩選莊家爆牌
        if self.dealer.burst:
            for player in self.playerList:
                if player.burst:
                    continue
                player.win = True

        # 先跟莊家比大小確定勝負或平手
        else:
            for player in self.playerList:
                if player.burst:
                    continue
                if self.dealer.totalPoints > player.totalPoints:
                    player.win = False
                    continue
                elif self.dealer.totalPoints == player.totalPoints:
                    player.push = True
                    player.win = False
                    continue
                else:
                    player.win = True
        # 算錢
        for player in self.playerList:
            if player.blackJack and player.win:
                player.totalCash += player.gambleCash * 2.5  # 拿回賭金+獎金 (1+1.5)
                player.result = "籌碼增加" + str(player.gambleCash*2.5)
                continue

            elif player.win:
                player.totalCash += player.gambleCash * 2
                player.result = "籌碼增加" + str(player.gambleCash*2)
                continue

            elif player.push:
                player.totalCash += player.gambleCash
                player.result = "和局"
                continue

            elif not player.win or player.burst:
                player.result = "籌碼損失 " + str(player.gambleCash)

    def ShowResult(self):
        self.dealer.Dump(show=True)
        if self.dealer.burst:
            print("{0} 爆牌, 所有剩餘玩家獲勝".format(self.dealer.name))

        print("---------------------------------------------")
        for player in self.playerList:
            print("{0} 本局結果: {1}".format(player.name, player.result))
            print("{0} 剩餘籌碼: {1}".format(player.name, player.totalCash))

    def ShowPlayerStatus(self, player):
        if player.blackJack:
            print("{0} 二十一點!!!".format(player.name))

        elif player.burst:
            print("{0} 爆牌!!!".format(player.name))

    def DeletePlayer(self):
        # 刪除沒有籌碼的人
        for player in self.playerList:
            if player.totalCash == 0:
                self.removeList.append(player)
        for removePlayer in self.removeList:
            if removePlayer in self.playerList:
                self.playerList.remove(removePlayer)

    def AskPlayAgain(self):
        print("---------------------------------------------")
        print("要再玩一局嗎？(y/n)")
        ans = input()
        if ans.lower() == "y":
            # Reset Game
            for player in self.playerList:
                player.Reset()
            self.dealer.Reset()
            # Play again
            self.Play()
        else:
            print("---------------------------------------------")
            print("Game over")

    def InsuranceCheck(self):
        if self.HasInsuranceSituation():
            for player in self.playerList:
                print("{0}, 是否要保險? (y/n)".format(player.name))
                ans = input()
                if ans.lower() == "y":
                    if not self.dealer.blackJack:
                        player.gambleCash /= 2
        return

    def HasInsuranceSituation(self):
        pt = self.dealer.hand[1].rank
        if self.dealer.hand[1].rank > 10:
            pt = 10
        return pt == 1 or pt == 10
