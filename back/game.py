from datetime import datetime


class Game:
    def __init__(self, id):
        self.time_created = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.p1Went = False
        self.p2Went = False
        self.p1Name = ''
        self.p2Name = ''
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0
        self.close = False

    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    def set_name(self, name, p):
        if p == 0:
            self.p1Name = name
        else:
            self.p2Name = name

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:

            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):

        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = -1
        if p1 == "R" and p2 == "S":
            winner = 0
        elif p1 == "S" and p2 == "R":
            winner = 1
        elif p1 == "P" and p2 == "R":
            winner = 0
        elif p1 == "R" and p2 == "P":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1
        return winner

    def isTie(self, p, op):
        return self.wins[p] == self.wins[op]

    def isWinner(self, p, op):
        return self.wins[p] > self.wins[op]

    def getWinnerName(self):
        if self.wins[0] == self.wins[1]:
            return "-"
        return self.p1Name if self.wins[0] > self.wins[1] else self.p2Name

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False

    def isEqual(self, game):
        if not (self.wins[0] == game.wins[0] and self.wins[1] == game.wins[1]):
            return False
        elif self.p1Name != game.p1Name:
            return False
        elif self.p2Name != game.p2Name:
            return False
        else:
            return True
