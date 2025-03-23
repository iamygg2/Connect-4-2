import numpy as np
# removed to check


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
            for column in range(0, 4):
                diagonal = [self.board[row + i][column + i] for i in range(4)]
                if diagonal[0] != "" and len(set(diagonal)) == 1:
                    return diagonal[0]
                            
        # Check Reverse Diagonals
        self.flippedBoard = np.flipud(self.board)
        for row in range(0, 3):
            for column in range(3, 7):
                self.reverseDiagonal = [self.board[row + i][column - i] for i in range(4)]
                if self.reverseDiagonal[0] != "" and len(set(self.reverseDiagonal)) == 1:
                    return self.reverseDiagonal[0]
        
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
                self.vertical = self.npBoard[row,column:column+4]
                if np.all(self.vertical[1:] == self.vertical[:-1]) and self.vertical[0] == "R":
                    return "R"
                if np.all(self.vertical[1:] == self.vertical[:-1]) and self.vertical[0] == "Y":
                    return "Y"

                    
    def altCheckBoard(self, row, column):
        result = self.checkVertical(row, column)
        if result is not None:
            return result
        result = self.checkHorizontal(row, column)
        if result is not None:
            return result
        result = self.checkDiagonal(row, column)
        if result is not None:
            return result

    def checkDiagonal(self, row, column):
        if row < 3 and column <= 3:
            self.diagonal = [self.board[row+i][column+i] for i in range(4)]
            if self.diagonal[0] != "" and len(set(self.diagonal)) == 1:
                return self.diagonal[0]
        if row >= 3 and column <= 3:
            self.diagonal = [self.board[row-i][column+i] for i in range(4)]
            if self.diagonal[0] != "" and len(set(self.diagonal)) == 1:
                return self.diagonal[0]
        if row < 3  and column >= 3:
            self.diagonal = [self.board[row+i][column-i] for i in range(4)]
            if self.diagonal[0] != "" and len(set(self.diagonal)) == 1:
                return self.diagonal[0]
        if row >= 3 and column >=3:
            self.diagonal = [self.board[row-i][column-i] for i in range(4)]
            if self.diagonal[0] != "" and len(set(self.diagonal)) == 1:
                return self.diagonal[0]     

    def checkVertical(self, row, column):
        if row <= 2:
            self.vertical = [self.board[row+i][column] for i in range(4)]
            if self.vertical[0] != "" and len(set(self.vertical)) == 1:
                return self.vertical[0]
            
    def checkHorizontal(self, row, column):
        if column <= 3:
            self.horizontal = [self.board[row][column+i] for i in range(4)]
            if self.horizontal[0] != "" and len(set(self.horizontal)) == 1:
                return self.horizontal[0]
        if column >= 3:
            self.horizontal = [self.board[row][column-i] for i in range(4)]
            if self.horizontal[0] != "" and len(set(self.horizontal)) == 1:
                return self.horizontal[0]

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
                return row

    def reset(self):
        self.board = [["" for _ in range(self.columns)] for _ in range(self.rows)]


    def game(self):
        notWinner = True
        winner = None
        counter = 0
        while notWinner and counter < self.rows*self.columns:            
            while True:
                try:
                    redColumn = input("Red -- Enter Column (1-7): ")
                    redColumn = int(redColumn) - 1
                    if redColumn < 0 or redColumn >= self.columns:
                        print("Column must be between 1 and 7. Try again.")
                    else:
                        row = self.move(redColumn, self.player1)
                        if row != False:
                            counter += 1
                            break
                except ValueError:
                    print("INVALID COLUMN ENTERED. TRY AGAIN")
            winner = self.altCheckBoard(row, redColumn)
            if winner == "R":
                print(f"Player {winner} wins!")
                break

            while True:
                try:
                    yellowColumn = input("Yellow -- Enter Column (1-7): ")
                    yellowColumn = int(yellowColumn) - 1
                    if yellowColumn < 0 or yellowColumn >= self.columns:
                        print("Column must be between 1 and 7. Try again.")
                    else:
                        row = self.move(yellowColumn, self.player2)
                        if row != False:
                            counter += 1
                            break
                except ValueError:
                    print("INVALID COLUMN ENTERED. TRY AGAIN")
            winner = self.altCheckBoard(row, yellowColumn)
            if winner == "Y":
                print(f"Player {winner} wins!")
                break
        else:
            print("All spots filled! TIE!")

board = Board()
board.game()
