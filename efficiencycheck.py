import numpy as np

class Board:
    def __init__(self):
        self.board = [["" for _ in range(7)] for _ in range(6)]
        self.rows = 6
        self.columns = 7
        self.player1 = "R"
        self.player2 = "Y"

    def checkBoard(self, row, column):
        # Check Vertical
        if self.checkVertical(row, column):
            return self.board[row][column]

        # Check Horizontal
        if self.checkHorizontal(row, column):
            return self.board[row][column]

        # Check Diagonal
        if self.checkDiagonal(row, column):
            return self.board[row][column]

        # Check Reverse Diagonal
        if self.checkReverseDiagonal(row, column):
            return self.board[row][column]

        return None

    def checkVertical(self, row, column):
        player = self.board[row][column]
        for i in range(row, min(row + 4, self.rows)):
            if self.board[i][column] != player:
                return False
        return True

    def checkHorizontal(self, row, column):
        player = self.board[row][column]
        for i in range(column, min(column + 4, self.columns)):
            if self.board[row][i] != player:
                return False
        return True

    def checkDiagonal(self, row, column):
        player = self.board[row][column]
        for i in range(4):
            if row + i >= self.rows or column + i >= self.columns or self.board[row + i][column + i] != player:
                return False
        return True

    def checkReverseDiagonal(self, row, column):
        player = self.board[row][column]
        for i in range(4):
            if row - i < 0 or column + i >= self.columns or self.board[row - i][column + i] != player:
                return False
        return True

    def printBoard(self):
        print("\n")
        print("-" * 43)
        for row in self.board:
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
                return row, column  # Return the position where the move happened

        return None  # This shouldn't happen since we check column full before

    def reset(self):
        self.board = [["" for _ in range(self.columns)] for _ in range(self.rows)]

    def game(self):
        winner = None
        counter = 0

        while counter < self.rows * self.columns:
            # Red Player Move
            while True:
                try:
                    redColumn = int(input("Red -- Enter Column (0-6): ")) - 1
                    if redColumn < 0 or redColumn >= self.columns:
                        print("Column must be between 0 and 6. Try again.")
                    else:
                        move_position = self.move(redColumn, self.player1)
                        if move_position:
                            counter += 1
                            row, column = move_position
                            winner = self.checkBoard(row, column)
                            if winner:
                                print(f"Player {winner} wins!")
                                return
                            break
                except ValueError:
                    print("INVALID COLUMN ENTERED. TRY AGAIN")

            # Yellow Player Move
            while True:
                try:
                    yellowColumn = int(input("Yellow -- Enter Column (0-6): ")) - 1
                    if yellowColumn < 0 or yellowColumn >= self.columns:
                        print("Column must be between 0 and 6. Try again.")
                    else:
                        move_position = self.move(yellowColumn, self.player2)
                        if move_position:
                            counter += 1
                            row, column = move_position
                            winner = self.checkBoard(row, column)
                            if winner:
                                print(f"Player {winner} wins!")
                                return
                            break
                except ValueError:
                    print("INVALID COLUMN ENTERED. TRY AGAIN")

        print("All spots filled! TIE!")

# Start the game
board = Board()
board.game()
