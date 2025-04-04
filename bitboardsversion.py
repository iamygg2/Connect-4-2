def createBoard():
        player1Board = [[0 for _ in range(7)] for _ in range(6)]
        player2Board = [[0 for _ in range(7)] for _ in range(6)]

def checkWin():
    pass

def move():
    pass

def game():
    pass


class Board:
    def __init__ (self):
        self.width = 7
        self.height = 6
        self.size = self.width * self.height
        self.player1_board = 0
        self.player2_board = 0

    def make_move(self):
        pass



class BasePlayer:
    def __init__ (self):
        self.name = name
        self.is_AI = is_AI

class Player:
    def __init__ (self):
        pass