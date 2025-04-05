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
        self.top_mask = (1 << (self.height - 1)) * ((1 << self.width) - 1)  # Top row mask

    def make_move(self, player_board, column):
        """Make a move for the current player."""
        # Find the lowest empty row in the column
        column_mask = (1 << column) * ((1 << self.height) - 1)
        empty_spots = ~(self.player1_board | self.player2_board) & column_mask
        if empty_spots == 0:
            raise ValueError("Column is full")
        move = empty_spots & -empty_spots  # Get the lowest empty bit
        return player_board | move

    def is_valid_move(self, column):
        """Check if a move in the column is valid."""
        column_mask = (1 << column) * ((1 << self.height) - 1)
        return (self.player1_board | self.player2_board) & column_mask != column_mask

    def check_win(self, player_board):
        """Check if the player has won."""
        # Horizontal check
        board = player_board
        for direction in [1, self.height, self.height + 1, self.height - 1]:  # Right, Up, Diagonal /
            shifted = board & (board >> direction)
            if shifted & (shifted >> (2 * direction)):
                return True
        return False

    def print_board(self):
        """Print the current state of the board."""
        print("0 1 2 3 4 5 6")  # Column numbers for reference
        for row in range(self.height - 1, -1, -1):  # Start from the top row
            line = ""
            for col in range(self.width):
                position = row + col * self.height  # Calculate the bit position
                if (self.player1_board >> position) & 1:
                    line += "X "  # Player 1's piece
                elif (self.player2_board >> position) & 1:
                    line += "O "  # Player 2's piece
                else:
                    line += ". "  # Empty spot
            print(line)



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


board = Board()
board.print_board()