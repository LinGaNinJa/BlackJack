import unittest
from Card import Card
from Deck import Deck
from Game import Game
from StatusChecker import StatusList
from Player import Player
from Player import Dealer


class TestScenario(unittest.TestCase):

    @classmethod
    def setUpClass(cls):  # 「每輪」測試開始前都執行的動作
        return

    @classmethod
    def tearDownClass(cls):  # 「每輪」測試結束後都執行的動作
        return

    def setUp(self):  # 每個測試「開始前」都執行的動作
        return

    def tearDown(self):  # 每個測試「結束後」都執行的動作
        player = None
        dealer = None
        return player, dealer

    # switcher = {0: "CLUB", 1: "DIAMOND", 2: "HEART", 3: "SPADE"}
    def test_01(self):
        # Set up
        presetCards = [Card(3, 1), Card(2, 11), Card(1, 10)]
        deck = Deck(presetCards=presetCards)
        player = Player()
        dealer = Dealer()

        # run
        player.SaveACard(deck.DealACard())
        dealer.SaveACard(deck.DealACard())
        player.SaveACard(deck.DealACard())

        # check
        self.assertTrue(player.blackJack)
        self.assertTrue(dealer.safe)

    # switcher = {0: "CLUB", 1: "DIAMOND", 2: "HEART", 3: "SPADE"}
    def test_02(self):
        # Set up
        presetCards = [Card(0, 3), Card(2, 11), Card(3, 10), Card(2, 1)]
        deck = Deck(presetCards=presetCards)
        player = Player()
        dealer = Dealer()

        # run
        player.SaveACard(deck.DealACard())
        dealer.SaveACard(deck.DealACard())
        player.SaveACard(deck.DealACard())
        dealer.SaveACard(deck.DealACard())

        # check
        self.assertTrue(player.safe)
        self.assertTrue(dealer.blackJack)

    # switcher = {0: "CLUB", 1: "DIAMOND", 2: "HEART", 3: "SPADE"}
    def test_03(self):
        # Set up
        presetCards = [Card(3, 8), Card(2, 11), Card(2, 7),
                       Card(3, 2), Card(0, 6)]
        deck = Deck(presetCards=presetCards)
        player = Player()
        dealer = Dealer()

        # run
        player.SaveACard(deck.DealACard())
        dealer.SaveACard(deck.DealACard())
        player.SaveACard(deck.DealACard())
        dealer.SaveACard(deck.DealACard())
        player.SaveACard(deck.DealACard())

        # check
        self.assertTrue(player.blackJack)
        self.assertTrue(dealer.safe)

    # switcher = {0: "CLUB", 1: "DIAMOND", 2: "HEART", 3: "SPADE"}
    def test_04(self):
        # Set up
        presetCards = [Card(3, 8), Card(2, 5), Card(2, 8),
                       Card(3, 9), Card(0, 6)]
        deck = Deck(presetCards=presetCards)
        player = Player()
        dealer = Dealer()

        # run
        player.SaveACard(deck.DealACard())
        dealer.SaveACard(deck.DealACard())
        player.SaveACard(deck.DealACard())
        dealer.SaveACard(deck.DealACard())
        player.SaveACard(deck.DealACard())

        # check
        self.assertTrue(player.burst)
        self.assertTrue(dealer.safe)

    # switcher = {0: "CLUB", 1: "DIAMOND", 2: "HEART", 3: "SPADE"}
    def test_05(self):
        # Set up
        presetCards = [Card(3, 8), Card(2, 5), Card(2, 8),
                       Card(3, 9), Card(0, 6)]
        deck = Deck(presetCards=presetCards)
        player = Player()
        dealer = Dealer()

        # run
        player.SaveACard(deck.DealACard())
        dealer.SaveACard(deck.DealACard())
        player.SaveACard(deck.DealACard())
        dealer.SaveACard(deck.DealACard())
        dealer.SaveACard(deck.DealACard())

        # check
        self.assertEqual(player.totalPoints, 16)
        self.assertEqual(dealer.totalPoints, 20)

    # switcher = {0: "CLUB", 1: "DIAMOND", 2: "HEART", 3: "SPADE"}
    def test_06(self):
        # Set up
        presetCards = [Card(3, 8), Card(2, 5), Card(2, 8),
                       Card(3, 9), Card(0, 8)]
        deck = Deck(presetCards=presetCards)
        player = Player()
        dealer = Dealer()

        # run
        player.SaveACard(deck.DealACard())
        dealer.SaveACard(deck.DealACard())
        player.SaveACard(deck.DealACard())
        dealer.SaveACard(deck.DealACard())
        dealer.SaveACard(deck.DealACard())

        # check
        self.assertEqual(player.totalPoints, 16)
        self.assertEqual(dealer.totalPoints, 22)
        self.assertTrue(dealer.burst)


class TestGame(unittest.TestCase):
    def test_random(self):
        # Set up random deck
        deck = Deck(seed=123)
        cards = []

        # Deal the card in random deck to realworld cards
        nCard = 52 * deck.nDeck
        nSuit = 4 * deck.nDeck
        nRank = 13 * deck.nDeck
        i = 0
        while i < nCard:
            cards.append(deck.DealACard())
            i += 1

        # Count the number of suit and rank in realworld cards
        suits = [0] * 4
        ranks = [0] * 13
        for card in cards:
            suits[card.suit] += 1
            ranks[card.rank - 1] += 1

        # Check if the number is right
        suit_OK = True
        for suit in suits:
            if suit != nRank:  # 6副牌
                suit_OK = False
                break

        rank_OK = True
        for rank in ranks:
            if rank != nSuit:  # 6副牌
                rank_OK = False
                break

        # Output
        self.assertTrue(suit_OK)
        self.assertTrue(rank_OK)

    def test_game(self):
        # Set up
        print("Test Seed: 123")
        game = Game()
        game.Run(seed=123)
        # Check
        return True

    def test_dealerBurst(self):
        presetCards = [Card(0, 7), Card(1, 7), Card(2, 5),
                       Card(2, 7), Card(3, 7), Card(3, 9), Card(0, 8)]
        print("Test dealer burst: 2 player, DON'T HIT CARD")
        game = Game()
        game.Run(presetCards=presetCards)
        return True

    def test_playerOutOfCash(self):
        presetCards = [Card(0, 1), Card(1, 8), Card(2, 5),
                       Card(2, 10), Card(3, 8), Card(3, 9), Card(0, 6),
                       Card(0, 4), Card(1, 10), Card(0, 5), Card(1, 9)]
        print("Test player out of cash")
        print("2 Player, Don't hit card, All-in, Next game")
        game = Game()
        game.Run(presetCards=presetCards)

    def test_NobodyAlive(self):
        presetCards = [Card(0, 1), Card(1, 1), Card(2, 5),
                       Card(2, 10), Card(3, 10), Card(3, 9), Card(0, 6),
                       Card(0, 4), Card(1, 10), Card(0, 5), Card(1, 9), Card(3, 5)]
        print("Test dealer don't hit card if nobody alive")
        print("2 Player, Don't do anything")
        game = Game()
        game.Run(presetCards=presetCards)


if __name__ == '__main__':
    unittest.main()
