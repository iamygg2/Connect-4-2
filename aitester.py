import numpy as np

class Board:
    def __init__(self):
        self.board = [["" for _ in range(7)] for _ in range(6)]
        self.npBoard = np.array(self.board)
        self.rows = 6
        self.columns = 7
        self.player1 = "R"
        self.player2 = "Y"
                    
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
        self.board = [["" for i in range(self.columns)] for i in range(self.rows)]


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

    def minimax(self, depth, maximizingPlayer, player):
        pass

    def heuristic(self, player):
        if player == "R":
            playerLines = 0
            playerLines += self.countHorizontal("R")
            playerLines += self.countVertical("R")
            playerLines += self.countDiagonal("R")
            playerLines += self.countReverseDiagonal("R")

            opponentLines = 0
            opponentLines += self.countHorizontal("Y")
            opponentLines += self.countVertical("Y")
            opponentLines += self.countDiagonal("Y")
            opponentLines += self.countReverseDiagonal("Y")
        else:
            playerLines = 0
            playerLines += self.countHorizontal("Y")
            playerLines += self.countVertical("Y")
            playerLines += self.countDiagonal("Y")
            playerLines += self.countReverseDiagonal("Y")

            opponentLines = 0
            opponentLines += self.countHorizontal("R")
            opponentLines += self.countVertical("R")
            opponentLines += self.countDiagonal("R")
            opponentLines += self.countReverseDiagonal("R")
        
        return playerLines - opponentLines


    def npCheck(self):
        print(np.array(self.board))

    def countHorizontal(self, player):
        count = 0
        for row in range(self.rows):
            for column in range(self.columns-3):
                window = self.board[row][column:column+4]
                if self.checkFour(window, player):
                    count += 1
        return count


    def countVertical(self, player):
        count = 0
        for row in range(self.rows-3):
            for column in range(self.columns):
                window = self.board[row:row+4][column]
                if self.checkFour(window, player):
                    count += 1
        return count

    def countDiagonal(self, player):
        count = 0
        for row in range(self.rows-3):
            for column in range(self.columns-3):
                window = [self.board[row+i][column+i] for i in range(4)]
                if self.checkFour(window, player):
                    count += 1

        return count
    
    def countReverseDiagonal(self, player):
        count = 0
        for row in range(self.rows, 3, -1):
            for column in range(self.columns-3):
                window = [[self.board[row-1][column+i] for i in range(4)]]
                if self.checkFour(window, player):
                    count += 1

        return count

    def checkFour(self, window, player):
        if player == "R":
            playerCount = window.count(player)
            opponentCount = window.count("Y")
        else:
            playerCount = window.count(player)
            opponentCount = window.count("R")

        return opponentCount == 0 and playerCount > 0
    
    

board = Board()
board.npCheck()
board.game()