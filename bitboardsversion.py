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
    def __init__(self):
        self.width = 7
        self.height = 6
        self.size = self.width * self.height
        self.player1_board = 0  # Bitboard for Player 1
        self.player2_board = 0  # Bitboard for Player 2

    def make_move(self, player_board, column):
        """Make a move for the current player."""
        # Find the lowest empty row in the column
        for row in range(self.height):
            position = column * self.height + row  # Calculate the bit position
            if not ((self.player1_board | self.player2_board) & (1 << position)):
                self.player_board = player_board | (1 << position)
                if player_board == self.player1_board:
                    self.player1_board = self.player_board
                else:
                    self.player2_board = self.player_board
                return self.player_board  # Place the piece
        raise ValueError("Column is full")

    def is_valid_move(self, column):
        """Check if a move in the column is valid."""
        for row in range(self.height):
            position = column * self.height + row  # Calculate the bit position
            if not ((self.player1_board | self.player2_board) & (1 << position)):
                return True
        return False

    def check_win(self, player_board):
        """Check if the player has won."""
        return self.check_vertical(player_board) or \
               self.check_horizontal(player_board) or \
                self.check_diagonal(player_board)
    
    def check_vertical(self, player_board):
        """Check for vertical win."""
        for column in range(self.width):
            count = 0
            for row in range(self.height):
                position = column * self.height + row
                if (player_board >> position) & 1:
                    count += 1
                    if count == 4:
                        return True
                else:
                    count = 0
        return False

    def check_horizontal(self, player_board):
        """Check for horizontal win."""
        for row in range(self.height):
            count = 0
            for column in range(self.width):
                position = column * self.height + row
                if (player_board >> position) & 1:
                    count += 1
                    if count == 4:
                        return True
                else:
                    count = 0
        return False
    
    def check_diagonal(self, player_board):
        """Check for diagonal win."""
        for row in range(self.height - 1, -1, -1):
            for column in range(self.width):
                position = column * self.height + row
                if (player_board >> position) & 1:
                    # Check diagonal down-right
                    if column <= self.width - 4 and row <= self.height - 4:
                        if (player_board >> (position + 3 * self.height + 3)) & 1 and \
                           (player_board >> (position + 2 * self.height + 2)) & 1 and \
                           (player_board >> (position + self.height + 1)) & 1:
                            return True
                    # Check diagonal down-left
                    if column <= self.width-4 and row >= 3:
                        if (player_board >> (position + 3 * self.height - 3)) & 1 and \
                           (player_board >> (position + 2 * self.height - 2)) & 1 and \
                           (player_board >> (position + self.height - 1)) & 1:
                            return True
        return False

    def print_board(self):
        """Print the current state of the board."""
        print("  0  1  2  3  4  5  6")  # Column numbers for reference
        for row in range(self.height - 1, -1, -1):  # Start from the top row
            line = ""
            for col in range(self.width):
                position = col * self.height + row  # Calculate the bit position
                if (self.player1_board >> position) & 1:
                    line += " X "  # Player 1's piece
                elif (self.player2_board >> position) & 1:
                    line += " O "  # Player 2's piece
                else:
                    line += " . "  # Empty spot
            print(line)

# Example usage
board = Board()
board.print_board()

# Simulate some moves
board.make_move(board.player1_board, 0)  # Player 1 places in Column 0
board.make_move(board.player2_board, 1)  # Player 2 places in Column 1
board.make_move(board.player1_board, 1)  # Player 1 places in Column 0
board.make_move(board.player2_board, 2)  # Player 2 places in Column 1
board.make_move(board.player2_board, 2)  # Player 2 places in Column 1
board.make_move(board.player1_board, 2)  # Player 1 places in Column 0
board.make_move(board.player2_board, 3)  # Player 2 places in Column 1
board.make_move(board.player1_board, 3)  # Player 1 places in Column 0
board.make_move(board.player2_board, 3)  # Player 2 places in Column 1
board.make_move(board.player1_board, 3)  # Player 1 places in Column 0

board.print_board()

# Check for a win
if board.check_win(board.player1_board):
    print("Player 1 wins!")
elif board.check_win(board.player2_board):
    print("Player 2 wins!")
else:
    print("No winner yet.")


class BasePlayer:
    def __init__ (self):
        self.name = name
        self.is_AI = is_AI

    def flip_bit(self, player, row, column):
        pass

    def get_Nth_bit(self, num, n):
        pass
    
    def set_Nth_bit(self, num, n):
        pass

class Player:
    def __init__ (self):
        pass