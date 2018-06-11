class StatusList:
    PASS = 0
    BLACK_JACK = 1
    BURST = 2


class StatusChecker:

    # 判斷手牌點數和的狀態
    @staticmethod
    def JudgeStatus(sumPoint):
        if sumPoint == 21:
            status = StatusList.BLACK_JACK
        elif sumPoint > 21:
            status = StatusList.BURST
        else:
            status = StatusList.PASS
        return status

    @staticmethod
    def DetermineStatusAndTotalPoints(hand):
        sumPoint = 0  # 手牌的點數和
        point = []  # 依序排列每張手牌的點數
        for card in hand:
            pt = card.rank
            if card.rank > 10:
                pt = 10
            point.append(pt)  # 紀錄點數
            sumPoint += pt

        status = StatusChecker.JudgeStatus(sumPoint)
        if status != StatusList.PASS:
            return status, sumPoint

        # 檢查手牌中有沒有Ace
        isWithAce = False
        for i in point:
            if i == 1:
                isWithAce = True
                break  # 兩張Ace就會等於二十二點，所以只要有一張就停止

        if isWithAce:
            sumPoint += 10
            if sumPoint == 21:
                status = StatusList.BLACK_JACK
                return status, sumPoint
            elif sumPoint < 21:
                return status, sumPoint
            else:
                sumPoint -= 10  # 如果大於二十一點就扣回來

        return status, sumPoint
