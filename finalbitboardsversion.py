import copy

class Board:
    def __init__(self, player1, player2):
        self.width = 7
        self.height = 6
        self.size = self.width * self.height
        self.player = (player1, player2)  # Tuple to hold the players
        self.bitboards = [0, 0]  # List to hold the bitboards for both players

    def __deepcopy__(self, memo):
        # Create a new board without copying the players
        copied_board = Board.__new__(Board)
        memo[id(self)] = copied_board

        # Manually copy values
        copied_board.width = self.width
        copied_board.height = self.height
        copied_board.size = self.size

        # Keep the same player tuple reference
        copied_board.player = self.player

        # Deepcopy bitboards (they're integers, so fine)
        copied_board.bitboards = copy.deepcopy(self.bitboards, memo)

        return copied_board


    def make_move(self, player, column):
        """Make a move for the current player."""
        # Find the lowest empty row in the column
        for row in range(self.height):
            position = column * self.height + row  # Calculate the bit position
            if not ((self.bitboards[0] | self.bitboards[1]) & (1 << position)):
                self.bitboards[self.player.index(player)] |= (1 << position)
                return # Place the piece
        raise ValueError(f"Column {column} is full")
    
    def is_valid_move(self, column):
        """Check if a move in the column is valid."""
        top_row = self.height - 1  # Start from the top row
        position = column * self.height + top_row  # Calculate the bit position
        if column < 0 or column >= self.width:
            return False
        return not ((self.bitboards[0] | self.bitboards[1]) & (1 << position))
    
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

    def is_full(self):
        """Check if the board is full."""
        return all((self.bitboards[0] | self.bitboards[1]) & (1 << (column * self.height + row)) for column in range(self.width) for row in range(self.height))

    def undo_move(self, player, column):
        """Undo the last move in the specified column."""
        for row in range(self.height):
            position = column * self.height + row
            if (self.bitboards[0] | self.bitboards[1]) & (1 << position):
                # Remove the piece from the bitboard
                self.bitboards[self.player.index(player)] &= ~(1 << position)
                return self.bitboards[self.player.index(player)]  # Undo the piece

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

    def get_is_AI(self):
        return self.is_AI

    def get_name(self):
        return self.name
    
class Human(CorePlayer):
    def __init__(self, id, name, bitboard, is_AI=False):
        """Initialize a human player."""
        super().__init__(id, name, is_AI)
        self.board = bitboard

    def get_move(self, board):
        try:
            move = int(input(f"{self.name}, enter your move (1-{board.width}): ")) - 1
        except ValueError:
            print(f"Invalid input. Please enter a number between 1 and {board.width}.")
            return self.get_move(board)  # Retry if input is invalid
        
        if move < 0 or move >= board.width:
            print(f"Invalid move. Please enter a number between 1 and {board.width}.")
            return self.get_move(board)
        
        if not board.is_valid_move(move):
            print(f"Column {move + 1} is full. Please choose another column.")
            return self.get_move(board)

        return move  # Return the valid move
    
class AI(CorePlayer):
    def __init__(self, id, name, bitboard, is_AI=True):
        """Initialize an AI player."""
        super().__init__(id, name, is_AI)
        self.bitboard = bitboard

    def make_move(self, board):
        """Make a move for the AI player."""
        for column in range(board.width):
            if board.is_valid_move(column):
                return column
            
    def valid_columns(self, board):
        combined_board = board.bitboards[0] | board.bitboards[1]
        valid_columns = []
        for column in range(board.width):
            position = column * board.height + board.height - 1  # Check the top row of the column
            if not (combined_board & (1 << position)):
                valid_columns.append(column)

        return valid_columns  # Return the list of valid columns

    def valid_moves(self, board):
        """Get a list of valid moves."""
        combined_board = board.bitboards[0] | board.bitboards[1]
        valid_columns = self.valid_columns(board)
        valid_moves = []
        for column in range(board.width):
            for row in range(board.height):
                position = column * board.height + row
                if not (combined_board & (1 << position)):
                    valid_moves.append((column, row))
                    break
        # Return the list of valid moves as tuples (column, row)
        return valid_moves
    
    def check_3(self, board, my_board, opponent_board):
        board_boundary_mask = (1 << (board.width * board.height)) - 1
        empty_board = board_boundary_mask & ~(my_board | opponent_board)

        horizontal_mask_one = (1 << ((board.width-3) * board.height)) - 1
        horizontal_mask_two = horizontal_mask_one << board.height
        horizontal_mask_three = horizontal_mask_one << (2 * board.height)
        horizontal_mask_four = horizontal_mask_one << (3 * board.height)

        vertical_mask = 0
        
        for column in range(0, board.width):
            for row in range(board.height-3, board.height):
                position = column * board.height + row
                vertical_mask |= (1 << position)
        
        diagonal_mask_one = 0
        
        for column in range(0, board.width-3):
            for row in range(0, board.height-3):
                diagonal_mask_one |= (1 << (column * board.height + row))
        
        diagonal_mask_two = (diagonal_mask_one) << (board.height + 1)
        diagonal_mask_three = (diagonal_mask_one) << (2 * (board.height + 1))
        diagonal_mask_four = (diagonal_mask_one) << (3 * (board.height + 1))

        diagonal_mask_five = 0
        for column in range(0, board.width-3):
            for row in range(board.width-3, board.width):
                diagonal_mask_five |= (1 << (column * board.height + row))

        diagonal_mask_six = (diagonal_mask_five) << (board.height - 1)
        diagonal_mask_seven = (diagonal_mask_five) << (2 * (board.height - 1))
        diagonal_mask_eight = (diagonal_mask_five) << (3 * (board.height - 1))

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
        result |= empty_board & (my_board >> 7) & (my_board >> 14) & (my_board >> 21) & diagonal_mask_one & board_boundary_mask

        # Check X_XX Diagonal /
        result |= my_board & (empty_board >> 7) & (my_board >> 14) & (my_board >> 21) & diagonal_mask_two & board_boundary_mask

        # Check XX_X Diagonal /
        result |= my_board & (my_board >> 7) & (empty_board >> 14) & (my_board >> 21) & diagonal_mask_three & board_boundary_mask

        # Check XXX_ Diagonal /
        result |= my_board & (my_board >> 7) & (my_board >> 14) & (empty_board >> 21) & diagonal_mask_four & board_boundary_mask

        # Check _XXX Diagonal \
        result |= empty_board & (my_board >> 5) & (my_board >> 10) & (my_board >> 15) & diagonal_mask_five & board_boundary_mask

        # Check X_XX Diagonal \
        result |= my_board & (empty_board >> 5) & (my_board >> 10) & (my_board >> 15) & diagonal_mask_six & board_boundary_mask

        # Check XX_X Diagonal \
        result |= my_board & (my_board >> 5) & (empty_board >> 10) & (my_board >> 15) & diagonal_mask_seven & board_boundary_mask

        # Check XXX_ Diagonal \ 
        result |= my_board & (my_board >> 5) & (my_board >> 10) & (empty_board >> 15) & diagonal_mask_eight & board_boundary_mask           

        return result
    
    def check_2(self, board, my_board, opponent_board):
        board_boundary_mask = (1 << (board.width * board.height)) - 1
        empty_board = board_boundary_mask & ~(my_board | opponent_board)

        horizontal_mask_one = (1 << ((board.width-2) * board.height)) - 1
        horizontal_mask_two = horizontal_mask_one << board.height
        horizontal_mask_three = horizontal_mask_one << (2 * board.height)

        vertical_mask = 0
        for column in range(0, board.width):
            for row in range(board.height-2, board.height):
                position = column * board.height + row
                vertical_mask |= (1 << position)

        diagonal_mask_one = 0
        for column in range(0, board.width-2):
            for row in range(0, board.height-2):
                diagonal_mask_one |= (1 << (column * board.height + row))
        diagonal_mask_two = (diagonal_mask_one) << (board.height + 1)
        diagonal_mask_three = (diagonal_mask_one) << (2 * (board.height + 1))

        diagonal_mask_four = 0
        for column in range(0, board.width-2):
            for row in range(board.width-2, board.width):
                diagonal_mask_four |= (1 << (column * board.height + row))
        diagonal_mask_five = (diagonal_mask_four) << (board.height - 1)
        diagonal_mask_six = (diagonal_mask_four) << (2 * (board.height - 1))

        # Check _XX Horizontal
        result = empty_board & (my_board >> 6) & (my_board >> 12) & horizontal_mask_one & board_boundary_mask

        # Check X_X Horizontal
        result |= (my_board << 6) & empty_board & (my_board >> 6) & horizontal_mask_two & board_boundary_mask

        # Check XX_ Horizontal
        result |= (my_board << 12) & (my_board << 6) & empty_board & horizontal_mask_three & board_boundary_mask

        # Check XX_ Vertical
        result |= my_board & (my_board >> 1) & (empty_board >> 2) & vertical_mask & board_boundary_mask

        # Check _XX Diagonal /
        result |= empty_board & (my_board >> 7) & (my_board >> 14) & diagonal_mask_one & board_boundary_mask

        # Check X_X Diagonal /
        result |= my_board & (empty_board >> 7) & (my_board >> 14) & diagonal_mask_two & board_boundary_mask

        # Check XX_ Diagonal /
        result |= my_board & (my_board >> 7) & (empty_board >> 14) & diagonal_mask_three & board_boundary_mask

        # Check _XX Diagonal \
        result |= empty_board & (my_board >> 5) & (my_board >> 10) & diagonal_mask_four & board_boundary_mask

        # Check X_X Diagonal \
        result |= my_board & (empty_board >> 5) & (my_board >> 10) & diagonal_mask_five & board_boundary_mask

        # Check XX_ Diagonal \
        result |= my_board & (my_board >> 5) & (empty_board >> 10) & diagonal_mask_six & board_boundary_mask

        return result        

    def check_1(self, board, my_board, opponent_board):
        # Maybe skip diagonals as they are worthless
        board_boundary_mask = (1 << (board.width * board.height)) - 1
        empty_board = board_boundary_mask & ~(my_board | opponent_board)

        horizontal_mask_one = (1 << ((board.width-1) * board.height)) - 1
        horizontal_mask_two = horizontal_mask_one << board.height

        vertical_mask = 0
        for column in range(0, board.width):
            for row in range(board.height-1, board.height):
                position = column * board.height + row
                vertical_mask |= (1 << position)

        # Check _X Horizontal
        result = empty_board & (my_board >> 6) & board_boundary_mask
 
        # Check X_ Horizontal
        result |= (my_board << 6) & empty_board & horizontal_mask_two & board_boundary_mask

        # Check X_ Vertical
        result |= my_board & (empty_board >> 1) & vertical_mask & board_boundary_mask

        return result

    def count_bits(self, board, result):
        bourd_boundary_mask = (1 << (board.width * board.height)) - 1
        result &= bourd_boundary_mask

        # PARALLEL BIT COUNTING IS FASTER -- TALK ABOUT BIG O

        n = (result & 0x5555555555555555) + ((result & 0xAAAAAAAAAAAAAAAA) >> 1)
        n = (result & 0x3333333333333333) + ((result & 0xCCCCCCCCCCCCCCCC) >> 2)
        n = (result & 0x0F0F0F0F0F0F0F0F) + ((result & 0xF0F0F0F0F0F0F0F0) >> 4)
        n = (result & 0x00FF00FF00FF00FF) + ((result & 0xFF00FF00FF00FF00) >> 8)
        n = (result & 0x0000FFFF0000FFFF) + ((result & 0xFFFF0000FFFF0000) >> 16)
        n = (result & 0x00000000FFFFFFFF) + ((result & 0xFFFFFFFF00000000) >> 32) # This last & isn't strictly necessary.
        return n
    
    def evaluate_board(self, board, my_board, opponent_board, player, opponent):
        # Check for winning moves

        win_reward = float('inf')
        lose_penalty = float('-inf')
        my_cost_3 = 1000
        opponent_cost_3 = 1000
        my_cost_2 = 100
        opponent_cost_2 = 100
        my_cost_1 = 10
        opponent_cost_1 = 10

        # Check for immediate win or loss
        if board.check_win(player):
            return float('inf')  # Winning move
        if board.check_win(opponent):
            return float('-inf')

        # Check for potential winning moves
        possible_3 = self.check_3(board, my_board, opponent_board)
        winning_3 = self.count_bits(board, possible_3) * my_cost_3

        possible_2 = self.check_2(board, my_board, opponent_board)
        winning_2 = self.count_bits(board, possible_2) * my_cost_2

        possible_1 = self.check_1(board, my_board, opponent_board)
        winning_1 = self.count_bits(board, possible_1) * my_cost_1

        # Check for opponent's potential winning moves
        opponent_possible_3 = self.check_3(board, opponent_board, my_board)
        opponent_winning_3 = self.count_bits(board, opponent_possible_3) * -opponent_cost_3

        opponent_possible_2 = self.check_2(board, opponent_board, my_board)
        opponent_winning_2 = self.count_bits(board, opponent_possible_2) * -opponent_cost_2

        opponent_possible_1 = self.check_1(board, opponent_board, my_board)
        opponent_winning_1 = self.count_bits(board, opponent_possible_1) * -opponent_cost_1

        # Calculate the total score
        score = (winning_3 + winning_2 + winning_1 +
                 opponent_winning_3 + opponent_winning_2 + opponent_winning_1)
        return score

    def minimax2(self, board, depth, player, opponent, maximizing_player):
        if board.check_win(player):
            return float("-inf"), -1
        elif board.check_win(opponent):
            return float("inf"), -1
        elif depth == 0 or board.is_full():
            return self.evaluate_board(board, board.bitboards[board.player.index(player)], board.bitboards[board.player.index(opponent)], player, opponent), -1
        
        copied_board = copy.deepcopy(board)

        if maximizing_player:
            max_eval = float("-inf")
            best_move = -1
            for column in range(board.width):
                if board.is_valid_move(column):
                    copied_board.make_move(player, column)
                    temp = self.minimax2(board, depth - 1, player, opponent, False)[0]
                    copied_board.undo_move(player, column)
                    if temp > max_eval:
                        max_eval = temp
                        best_move = column
            return max_eval, best_move
        else:
            min_eval = float("inf")
            best_move = -1
            for column in range(board.width):
                if board.is_valid_move(column):
                    copied_board.make_move(opponent, column)
                    temp = self.minimax2(board, depth - 1, player, opponent, True)[0]
                    copied_board.undo_move(opponent, column)
                    if temp < min_eval:
                        min_eval = temp
                        best_move = column
            return min_eval, best_move


    def minimax(self, board, depth, player, opponent, maximizing_player, alpha, beta, current_best_move):
        """Minimax algorithm with alpha-beta pruning."""
        if depth == 0 or board.is_full() or board.check_win(player) or board.check_win(opponent):
            return current_best_move, self.evaluate_board(board, board.bitboards[board.player.index(player)], board.bitboards[board.player.index(opponent)], player, opponent)


        best_score = float('-inf') if maximizing_player else float('inf')
        best_move = None

        if maximizing_player:
            max_eval = float('-inf')
            for column in range(board.width):
                if board.is_valid_move(column):
                    board_copy = copy.deepcopy(board)  # Create a copy of the board
                    board_copy.make_move(player, column)  # Make the move on the copy
                    temp_move, eval = self.minimax(board_copy, depth - 1, opponent, player, False, alpha, beta, current_best_move)
                    if eval > max_eval:
                        max_eval = eval
                        best_move = column
            return best_move, max_eval
        else:
            min_eval = float('inf')
            for column in range(board.width):
                if board.is_valid_move(column):
                    board_copy = copy.deepcopy(board)  # Create a copy of the board
                    board_copy.make_move(player, column)  # Make the move on the copy
                    temp_move, eval = self.minimax(board_copy, depth - 1, opponent, player, True, alpha, beta, current_best_move)
                    if eval < min_eval:
                        min_eval = eval
                        best_move = column
                        break
            return best_move, min_eval
        
    def get_move(self, board):
        """Get the AI's move using the minimax algorithm."""
        _, best_move = self.minimax2(board, 4, self, board.player[1-board.player.index(self)], True)
        print(f"AI chooses column {best_move}")
        return best_move
        
class Game:
    def __init__(self, player1, player2):
        self.board = Board(player1, player2)  # Initialize the board with players
        self.current_player = player1  # Start with player 1
        self.game_over = False  # Flag to check if the game is over
        self.player = (player1, player2)

    def play(self):
        while True:
            self.board.print_board()  # Print the current state of the board
            if self.board.is_full():
                print("The board is full. It's a draw!")
                break

            while True:
                #try:
                    if self.current_player.get_is_AI():
                        move = self.current_player.get_move(self.board)  # Get the AI's move

                        #FOR TESTING PURPOSES ONLY
                        #print(f"AI chooses column {move + 1}")

                    else:
                        move = self.current_player.get_move(self.board)  # Get the human player's move
                    
                    self.board.make_move(self.current_player, move)  # Make the move on the board
                    break
                #except ValueError:
                 #   print("Invalid move. Please try again.")
                 #   quit()

            if self.board.check_win(self.current_player):  # Check for a win
                self.board.print_board()
                print(f"{self.current_player.get_name()} wins!")
                break

            # Switch players
            self.current_player = self.player[1] if self.current_player == self.player[0] else self.player[0]

player1 = Human(1, "Player 1", 0)
player2 = AI(2, "AI", 0)  # Initialize the AI player
game = Game(player1, player2)  # Create a new game instance
game.play()  # Start the game