import numpy as np

class Board:
    def __init__(self):
        self.board = [["" for _ in range(7)] for _ in range(6)]
        self.npBoard = np.array(self.board)
        self.rows = 6
        self.columns = 7
        self.player1 = "R"
        self.player2 = "Y"

    def checkBoard(self):
        # Check Diagonals
        self.npBoard = np.array(self.board)
        for row in range(0, 3):
            for column in range(0, 5):
                self.diagonal = np.diagonal(self.npBoard[row:, column:])[0:4]
                if np.all(self.diagonal[1:] == self.diagonal[:-1]) and self.diagonal[0] == "R":
                    return "R"
                elif np.all(self.diagonal[1:] == self.diagonal[:-1]) and self.diagonal[0] == "Y":
                    return "Y"
                            
        # Check Reverse Diagonals
        self.flippedBoard = np.flipud(self.board)
        for row in range(0, 3):
            for column in range(0, 5):
                self.diagonal = np.diagonal(self.flippedBoard[row:, column:])[0:4]

                if np.all(self.diagonal[1:] == self.diagonal[:-1]) and self.diagonal[0] == "R":
                    return "R"
                elif np.all(self.diagonal[1:] == self.diagonal[:-1]) and self.diagonal[0] == "Y":
                    return "Y"
        
        # Check Verticals
        for row in range(0,self.rows):
            for column in range(0,self.columns):
                self.vertical = self.npBoard[row:row+4, column]
                if np.all(self.vertical[1:] == self.vertical[:-1]) and self.vertical[0] == "R":
                    return "R"
                if np.all(self.vertical[1:] == self.vertical[:-1]) and self.vertical[0] == "Y":
                    return "Y"

        # Check Horizontals


    def printBoard(self):
        print("\n")
        print("-" * 43)
        for row in self.board:
            # Make sure each cell has the same width
            print("| " + " | ".join(f" {cell if cell != '' else ' '} " for cell in row) + " |")
        print("-" * 43)
        print("\n")

    def move(self, column, player):
        for row in range(5, -1, -1):
            if self.board[row][column] == "":
                self.board[row][column] = player
                break

        self.printBoard()
        return True

    def reset(self):
        pass

    def game(self):
        notWinner = True
        winner = None
        counter = 0


        while notWinner and counter < self.rows*self.columns:            
            while True:
                try:
                    redColumn = input("Red -- Enter Column (0-6): ")
                    self.move(int(redColumn), self.player1)
                    break
                except:
                    print("INVALID COLUMN ENTERED. TRY AGAIN")
            self.checkBoard()
            while True:
                try:
                    yellowColumn = input("Yellow -- Enter Column: ")
                    self.move(int(yellowColumn), self.player2)
                    break
                except:
                    print("INVALID COLUMN ENTERED. TRY AGAIN")
            self.checkBoard()


board = Board()


board.game()