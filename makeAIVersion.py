import numpy as np

class Board:
    def __init__(self):
        self.board = [["" for _ in range(7)] for _ in range(6)]
        self.npBoard = np.array(self.board)
        self.rows = 6
        self.columns = 7
        self.player1 = "R"
        self.player2 = "Y"

    def checkBoard(self, board):
        # Check Diagonals
        self.npBoard = np.array(board)
        for row in range(0, 3):
            for column in range(0, 4):
                diagonal = [board[row + i][column + i] for i in range(4)]
                if diagonal[0] != "" and len(set(diagonal)) == 1:
                    return diagonal[0]
                            
        # Check Reverse Diagonals
        self.flippedBoard = np.flipud(board)
        for row in range(0, 3):
            for column in range(3, 7):
                self.reverseDiagonal = [board[row + i][column - i] for i in range(4)]
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
        self.board = [["" for i in range(self.columns)] for i in range(self.rows)]


    def possibleMoves(self, board):
        moves = []
        for column in range(self.columns):
            if board[0][column] == "":
                moves.append(column)

        return moves


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


    def aiGame(self):
        print("You are Red and AI is Yellow")
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

            print("AI's turn")

            _, bestMove = self.minimax(self.board, 3, True, "Y")
            
            if bestMove is None:
                print(2)
            row = self.move(bestMove, self.player2)
            counter += 1
            winner = self.altCheckBoard(row, bestMove)
            if winner == "Y":
                print(f"Player {winner} wins!")
                notWinner = False
                break
        else:
            print("All spots filled! TIE!")




    def checkWin(self, board):
        if self.checkBoard(board) is not None:
            return True
            
    def minimax(self, board, depth, maximizingPlayer, player):
        if depth == 0 or self.checkWin(board):
            winner = self.checkBoard(board)
            if winner == "R":
                return float("-inf"), None
            elif winner == "Y":
                return float("inf"), None
            return self.heuristic(board, player), None
        
        if maximizingPlayer:
            maxEval = float("-inf")
            bestMove = None

            for move in self.possibleMoves(board):
                copyBoard = [row.copy() for row in board]
                for row in range(self.rows - 1, -1, -1):
                    if copyBoard[row][move] == "":
                        copyBoard[row][move] = "Y"
                        eval, _ = self.minimax(copyBoard, depth-1, False, "R")
                        if eval > maxEval:
                            maxEval = eval
                            bestMove = move 
                        break
            return maxEval, bestMove
            
        else:
            minEval = float("inf")
            for move in self.possibleMoves(board):
                copyBoard = [row.copy() for row in board]
                for row in range(self.rows - 1, -1, -1):
                    if copyBoard[row][move] == "":
                        copyBoard[row][move] = "R"
                        eval, _ = self.minimax(copyBoard, depth-1, True, "Y")
                        if eval < minEval:
                            minEval = eval
                            bestMove = move 
                        break
            return minEval, bestMove
                    

    def heuristic(self, board, player):
        if player == "R":
            playerLines = 0
            playerLines += self.countHorizontal("R", board)
            playerLines += self.countVertical("R", board)
            playerLines += self.countDiagonal("R", board)
            playerLines += self.countReverseDiagonal("R", board)

            opponentLines = 0
            opponentLines += self.countHorizontal("Y", board)
            opponentLines += self.countVertical("Y", board)
            opponentLines += self.countDiagonal("Y", board)
            opponentLines += self.countReverseDiagonal("Y", board)
        else:
            playerLines = 0
            playerLines += self.countHorizontal("Y", board)
            playerLines += self.countVertical("Y", board)
            playerLines += self.countDiagonal("Y", board)
            playerLines += self.countReverseDiagonal("Y", board)

            opponentLines = 0
            opponentLines += self.countHorizontal("R", board)
            opponentLines += self.countVertical("R", board)
            opponentLines += self.countDiagonal("R", board)
            opponentLines += self.countReverseDiagonal("R", board)
        
        return playerLines - opponentLines


    def npCheck(self):
        print(np.array(self.board))

    def countHorizontal(self, player, board):
        count = 0
        for row in range(self.rows):
            for column in range(self.columns-3):
                window = board[row][column:column+4]
                if self.checkFour(window, player):
                    count += 1
        return count


    def countVertical(self, player, board):
        count = 0
        for row in range(self.rows-3):
            for column in range(self.columns):
                window = [board[row+i][column] for i in range(4)]
                if self.checkFour(window, player):
                    count += 1
        return count

    def countDiagonal(self, player, board):
        count = 0
        for row in range(self.rows-3):
            for column in range(self.columns-3):
                window = [board[row+i][column+i] for i in range(4)]
                if self.checkFour(window, player):
                    count += 1

        return count
    
    def countReverseDiagonal(self, player, board):
        count = 0
        for row in range(self.rows-1, 3, -1):
            for column in range(self.columns-3):
                window = [[board[row-i][column+i] for i in range(4)]]
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
board.aiGame()