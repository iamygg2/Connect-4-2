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
        for row in range(0,self.rows-3):
            for column in range(0,self.columns):
                self.vertical = self.npBoard[row:row+4, column]
                if np.all(self.vertical[1:] == self.vertical[:-1]) and self.vertical[0] == "R":
                    return "R"
                if np.all(self.vertical[1:] == self.vertical[:-1]) and self.vertical[0] == "Y":
                    return "Y"

        # Check Horizontals
        for row in range(0, self.rows):
            for column in range(0, self.columns-3):
                self.horizontal = self.npBoard[row,column:column+4]
                if np.all(self.horizontal[1:] == self.vertical[:-1]) and self.vertical[0] == "R":
                    return "R"
                if np.all(self.vertical[1:] == self.vertical[:-1]) and self.vertical[0] == "Y":
                    return "Y"

    def printBoard(self):
        print("\n")
        print("-" * 43)
        for row in self.board:
            # Make sure each cell has the same width
            print("| " + " | ".join(f" {cell if cell != '' else ' '} " for cell in row) + " |")
        print("-" * 43)
        print("\n")

    def move(self, column, player):
        if self.board[0][column] != "":
            print("COLUMN FULL! TRY AGAIN!")
            return False

        for row in range(self.rows - 1, -1, -1):
            if self.board[row][column] == "":
                self.board[row][column] = player
                self.printBoard()
                return True
            else:
                counter += 1

    def reset(self):
        self.board = [["" for _ in range(self.columns)] for _ in range(self.rows)]


    def game(self):
        notWinner = True
        winner = None
        counter = 0


        while notWinner and counter < self.rows*self.columns:            
            while True:
                try:
                    redColumn = input("Red -- Enter Column (0-6): ")
                    redColumn = int(redColumn) - 1
                    if redColumn < 0 or redColumn >= self.columns:
                        print("Column must be between 0 and 6. Try again.")
                    else:
                        if self.move(redColumn, self.player1):
                            counter += 1
                            break
                except ValueError:
                    print("INVALID COLUMN ENTERED. TRY AGAIN")
            winner = self.checkBoard()
            if winner == "R":
                print(f"Player {winner} wins!")
                break

            while True:
                try:
                    yellowColumn = input("Yellow -- Enter Column (0-6): ")
                    yellowColumn = int(yellowColumn) - 1
                    if yellowColumn < 0 or yellowColumn >= self.columns:
                        print("Column must be between 0 and 6. Try again.")
                    else:
                        if self.move(yellowColumn, self.player2):
                            counter += 1
                            break
                except ValueError:
                    print("INVALID COLUMN ENTERED. TRY AGAIN")
            winner = self.checkBoard()
            if winner == "Y":
                print(f"Player {winner} wins!")
                break

            self.checkBoard()
        else:
            print("All spots filled!!")

board = Board()


board.game()