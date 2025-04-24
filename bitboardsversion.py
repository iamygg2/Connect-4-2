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
    def __init__(self, player1, player2):
        self.width = 7
        self.height = 6
        self.size = self.width * self.height
        self.player = (player1, player2)  # Tuple to hold the players
        self.bitboards = [0, 0]  # List to hold the bitboards for both players

    def make_move(self, player, column):
        """Make a move for the current player."""
        # Find the lowest empty row in the column
        for row in range(self.height):
            position = column * self.height + row  # Calculate the bit position
            if not ((self.bitboards[0] | self.bitboards[1]) & (1 << position)):
                self.bitboards[self.player.index(player)] |= (1 << position)
                return self.bitboards[self.player.index(player)]  # Place the piece
        raise ValueError("Column is full")

    def is_valid_move(self, column):
        """Check if a move in the column is valid."""
        for row in range(self.height):
            position = column * self.height + row  # Calculate the bit position
            if not ((self.bitboards[0] | self.bitboard[1]) & (1 << position)):
                return True
        return False

    def check_win(self, player):
        """Check if the player has won."""
        player_board = self.bitboards[self.player.index(player)]
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
        print("\n 1  2  3  4  5  6  7")  # Column numbers for reference
        for row in range(self.height - 1, -1, -1):  # Start from the top row
            line = ""
            for col in range(self.width):
                position = col * self.height + row  # Calculate the bit position
                if (self.bitboards[0] >> position) & 1:
                    line += " X "  # Player 1's piece
                elif (self.bitboards[1] >> position) & 1:
                    line += " O "  # Player 2's piece
                else:
                    line += " . "  # Empty spot
            print(line)

    def isFull(self):
        """Check if the board is full."""
        return all((self.bitboards[0] | self.bitboards[1]) & (1 << (column * self.height + row)) for column in range(self.width) for row in range(self.height))

# Example usage
board = Board("Alex", "Bob")
board.print_board()

# Simulate some moves
board.make_move(board.player[1], 0)  # Player 1 places in Column 0
board.make_move(board.player[0], 0)  # Player 1 places in Column 0
board.make_move(board.player[1], 0)  # Player 1 places in Column 0
board.make_move(board.player[1], 0)  # Player 1 places in Column 0
board.make_move(board.player[0], 0)  # Player 1 places in Column 0
board.make_move(board.player[0], 0)  # Player 1 places in Column 0

board.make_move(board.player[1], 1)  # Player 2 places in Column 1
board.make_move(board.player[1], 1)  # Player 2 places in Column 1
board.make_move(board.player[0], 1)  # Player 2 places in Column 1
board.make_move(board.player[1], 1)  # Player 2 places in Column 1
board.make_move(board.player[0], 1)  # Player 2 places in Column 1
board.make_move(board.player[1], 1)  # Player 2 places in Column 1

board.make_move(board.player[0], 2)  # Player 1 places in Column 0
board.make_move(board.player[1], 2)  # Player 1 places in Column 0
board.make_move(board.player[0], 2)  # Player 1 places in Column 0
board.make_move(board.player[1], 2)  # Player 1 places in Column 0
board.make_move(board.player[0], 2)  # Player 1 places in Column 0
board.make_move(board.player[1], 2)  # Player 1 places in Column 0

board.make_move(board.player[0], 3)  # Player 2 places in Column 1
board.make_move(board.player[1], 3)  # Player 2 places in Column 1
board.make_move(board.player[0], 3)  # Player 2 places in Column 1
board.make_move(board.player[1], 3)  # Player 2 places in Column 1
board.make_move(board.player[1], 3)  # Player 2 places in Column 1
board.make_move(board.player[1], 3)  # Player 2 places in Column 1

board.make_move(board.player[0], 4)  # Player 2 places in Column 1
board.make_move(board.player[0], 4)  # Player 2 places in Column 1
board.make_move(board.player[0], 4)  # Player 2 places in Column 1
board.make_move(board.player[1], 4)  # Player 2 places in Column 1
board.make_move(board.player[1], 4)  # Player 2 places in Column 1
board.make_move(board.player[1], 4)  # Player 2 places in Column 1

board.make_move(board.player[1], 5)  # Player 2 places in Column 1
board.make_move(board.player[1], 5)  # Player 2 places in Column 1
board.make_move(board.player[1], 5)  # Player 2 places in Column 1
board.make_move(board.player[1], 5)  # Player 2 places in Column 1
board.make_move(board.player[1], 5)  # Player 2 places in Column 1
board.make_move(board.player[1], 5)  # Player 2 places in Column 1

board.make_move(board.player[1], 6)  # Player 2 places in Column 1
board.make_move(board.player[1], 6)  # Player 2 places in Column 1
board.make_move(board.player[1], 6)  # Player 2 places in Column 1
board.make_move(board.player[1], 6)  # Player 2 places in Column 1
board.make_move(board.player[1], 6)  # Player 2 places in Column 1




board.print_board()

# Check for a win
if board.check_win(board.player[0]):
    print(f"{board.player[0]} wins!")
elif board.check_win(board.player[1]):
    print(f"{board.player[1]} wins!")
else:
    print("No winner yet.")




class CorePlayer:
    def __init__ (self, id, name, is_AI):
        self.name = name
        self.id = id
        self.is_AI = is_AI

    def flip_bit(self, row, board, column):
        position = row * board.width + column  # Calculate the bit position
        self.board ^= (1 << position)  # Flip the bit at the position
        return self.board

    def get_Nth_bit(self, n, board):
        return (board.bitboards[board.player.index(self.name)] >> n) & 1
    
    def set_Nth_bit(self, n, board):
        board.bitboards[board.player.index(self.name)] |= (1 << n)

class Human(CorePlayer):
    def __init__ (self, id, name):
        super().__init__(id, name, False)

class AI(CorePlayer):
    def __init__ (self, id, name):
        super().__init__(id, name, True)
    
    def make_move(self, board):
        pass
    
    def check_possible_4(self, board):
        return self.check_vertical(board, 4) + \
               self.check_horizontal(board, 4) + \
                self.check_diagonal(board, 4)
        
    def check_possible_3(self, board):
        my_board = board.bitboards[board.player.index(self.name)]
        opponent_board = board.bitboards[1-board.player.index(self.name)]

        combined_board = my_board | opponent_board 

        right_shift_6 = my_board >> 6
        left_shift_6 = my_board << 6
        right_shift_12 = my_board >> 12
        left_shift_12 = my_board << 12
        right_shift_14 = my_board >> 14
        left_shift_14 = my_board << 14
        right_shift_7 = my_board >> 7
        left_shift_7 = my_board << 7

    def valid_columns(self, board):
        combined_board = board.bitboards[0] | board.bitboards[1]
        valid_columns = []
        for column in range(board.width):
            position = column * self.height + 5
            if not (combined_board & (1 << position)):
                valid_columns.append(column)

        return valid_columns

    def valid_moves(self, board):
        valid_columns = valid_columns(board)
        valid_moves = []
        combined_board = board.bitboards[0] | board.bitboards[1]
        for column in valid_columns:
            for row in range(board.height):
                position = column * board.height + row
                if not (combined_board) & (1 << position):
                    valid_moves.append((column, row))

        return valid_moves
    


    def check_3(self, board, offset):
        my_board = board.bitboards[board.player.index(self.name)]
        board_boundary_mask = (1 << (self.width * self.height)) - 1
        opponent_board = board.bitboards[1-board.player.index(self.name)]
        combined_board = (my_board | opponent_board) & board_boundary_mask
        empty_board = ~(my_board | opponent_board) 
        horizontal_mask_one = (1 << ((board.width-3) * board.height)) - 1
        horizontal_mask_two = (1 << ((board.width-3) * board.height)) << board.height
        horizontal_mask_three = (1 << ((board.width-3) * board.height)) << (board.height * 2)
        horizontal_mask_four  = (1 << ((board.width-3) * board.height)) << (board.height * 3)

        vertical_mask = 0

        for column in range(board.width):
            for row in range(board.height-3, board.height):
                position = column * board.height + row
                vertical_mask |= (1 << position)


        diagonal_mask_one = 0
        for column in range(board.width-4, board.width):
            for row in range(board.height-3, board.height):
                diagonal_mask_one |= (1 << (column * board.height + row))


        diagonal_mask_one = 0
        for column in range(0, board.width-4):
            for row in range(0, board.height-3):
                diagonal_mask_one |= (1 << (column * board.height + row))

        diagonal_mask_two = (diagonal_mask_one) << (board.height + 1)
        diagonal_mask_three = (diagonal_mask_two) << ((board.height + 1) * 2)
        diagonal_mask_four = (diagonal_mask_three) << ((board.height+1) * 3)

        # Check _XXX Horizontal
        result = empty_board & (my_board >> 6) & (my_board >> 12) & (my_board >> 18) & horizontal_mask_one & board_boundary_mask

        # Check X_XX Horizontal
        result |= (my_board << 6) & empty_board & (my_board >> 6) & (my_board >> 12) & horizontal_mask_two & board_boundary_mask

        # Check XX_X Horizontal
        result |= (my_board << 12) & (my_board << 6) & empty_board & (my_board >> 6) & horizontal_mask_three & board_boundary_mask

        # Check XXX_ Horizontal
        result |= my_board & (my_board >> 6) & (my_board >> 12) & (empty_board >> 18) & horizontal_mask_four & board_boundary_mask

        # Check XXX_ Vertical   
        result |= my_board & (my_board >> 1) & (my_board >> 2) & (empty_board >> 3) & vertical_mask & board_boundary_mask

        # Check _XXX Diagonal /
        result |= empty_board & (my_board >> 7) & (my_board >> 14) & (my_board >> 21) & board_boundary_mask

        # Check X_XX Diagonal /
        result |= my_board & (empty_board >> 7) & (my_board >> 14) & (my_board >> 21) & board_boundary_mask

        # Check XX_X Diagonal /
        result |= my_board & (my_board >> 7) & (empty_board >> 14) & (my_board >> 21) & board_boundary_mask

        # Check XXX_ Diagonal /
        result |= my_board & (my_board >> 7) & (my_board >> 14) & (empty_board >> 21) & board_boundary_mask

        # Check _XXX Diagonal \
        result |= empty_board & (my_board >> 5) & (my_board >> 10) & (my_board >> 15) & board_boundary_mask

        # Check X_XX Diagonal \
        result |= my_board & (empty_board >> 5) & (my_board >> 10) & (my_board >> 15) & board_boundary_mask

        # Check XX_X Diagonal \
        result |= my_board & (my_board >> 5) & (empty_board >> 10) & (my_board >> 15) & board_boundary_mask

        # Check XXX_ Diagonal \ 
        result |= my_board & (my_board >> 5) & (my_board >> 10) & (empty_board >> 15) & board_boundary_mask           

    def check_possible_2(self, board):
        pass

    def check_possible_1(self, board):
        return self.check_vertical(board, 1) + \
                self.check_horizontal(board, 1) + \
                self.check_diagonal(board, 1)

    def check_vertical(self, player_board, offset):
        """Check for vertical win."""
        total = 0
        for column in range(self.width):
            count = 0
            for row in range(self.height):
                position = column * self.height + row
                if (player_board >> position) & 1:
                    count += 1
                    if count == offset:
                        total += 1
                else:
                    count = 0
        return total

    def check_horizontal(self, player_board, offset):
        """Check for horizontal win."""
        total = 0
        for row in range(self.height):
            count = 0
            for column in range(self.width):
                position = column * self.height + row
                if (player_board >> position) & 1:
                    count += 1
                    if count == offset:
                        total += 1
                else:
                    count = 0
        return total
    
    def check_diagonal(self, player_board, offset):
        """Check for diagonal win."""
        total = 0

        for row in range(self.height - 1, -1, -1):
            for column in range(self.width):
                position = column * self.height + row
                if (player_board >> position) & 1:
                    # Check diagonal down-right
                    if column <= self.width - offset and row <= self.height - offset:
                        count = 0
                        for i in range(1, offset):
                            if (player_board >> (position + i * self.height + i)) & 1:
                                count += 1
                                if count == offset:
                                    total += 1
                            else:
                                break
                    if column <= self.width - offset and row >= offset - 1:
                        count = 0
                        for i in range(1, offset):
                            if (player_board >> (position + i * self.height - i)) & 1:
                                count += 1
                                if count == offset:
                                    total += 1
                            else:
                                break

    def evaluate_board(self, board):
        """Evaluate the board for the AI."""
        pass

        return total