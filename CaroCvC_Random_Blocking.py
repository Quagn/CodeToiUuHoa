import random

class CaroGameAI:
    def __init__(self, ai1, ai2, rounds=10):
        # Initialize the game board as a 15x15 grid of empty spaces
        self.board = [[' ' for _ in range(15)] for _ in range(15)]
        # Set the current player to 'X'
        self.current_player = 'X'
        # Flag to check if the game is over
        self.game_over = False
        # Number of rounds to play
        self.rounds = rounds
        # Dictionary to keep track of game results
        self.results = {'X': 0, 'O': 0, 'Draw': 0}

        self.ai1 = ai1
        self.ai2 = ai2

    def play_game(self):
        # Play the game for the specified number of rounds
        for _ in range(self.rounds):
            while not self.game_over:
                # Make a move for the current player
                self.make_move()  # Sửa ở đây
                # Check for a win or draw after the move
                if self.check_win(*self.last_move, self.current_player, self.board):
                    self.results[self.current_player] += 1
                    self.game_over = True
                elif self.is_draw():
                    self.results['Draw'] += 1
                    self.game_over = True
                # Switch to the other player
                self.toggle_player()
            # Reset the board for the next round
            self.reset_board()

    def make_move(self):
        ai = self.ai1 if self.current_player == 'X' else self.ai2
        move = ai.get_move(self.board, self.check_win)
        if move:
            row, col = move
            self.board[row][col] = self.current_player
            self.last_move = (row, col)

    def get_move(self, player):
        pass  # This will be overridden in the subclasses

    def check_win(self, row, col, player, board):
        # Check if the current player has won the game
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            blocked_1 = False
            blocked_2 = False

            # Check one direction from the last move
            for i in range(1, 5):
                x, y = row + dx * i, col + dy * i
                if 0 <= x < 15 and 0 <= y < 15:
                    if self.board[x][y] == player:
                        count += 1
                    elif self.board[x][y] != ' ':
                        blocked_1 = True
                        break
                    else:
                        break
                else:
                    blocked_1 = True
                    break

            # Check the opposite direction
            for i in range(1, 5):
                x, y = row - dx * i, col - dy * i
                if 0 <= x < 15 and 0 <= y < 15:
                    if self.board[x][y] == player:
                        count += 1
                    elif self.board[x][y] != ' ':
                        blocked_2 = True
                        break
                    else:
                        break
                else:
                    blocked_2 = True
                    break

            # Check if there are 5 in a row or 4 open-ended
            if count == 5 and not (blocked_1 and blocked_2):
                return True
            elif count == 4 and not (blocked_1 or blocked_2):
                return True

        return False

    def is_draw(self):
        # Check if the board is full and no more moves are possible
        return all(self.board[row][col] != ' ' for row in range(15) for col in range(15))

    def toggle_player(self):
        # Switch the current player
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def reset_board(self):
        # Reset the board for a new game
        self.board = [[' ' for _ in range(15)] for _ in range(15)]
        self.current_player = 'X'
        self.game_over = False

    def get_results(self):
        # Return the game results
        return self.results
    
class AI:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def get_move(self, board):
        # Phương thức này sẽ được ghi đè bởi AI1 và AI2
        pass

class AI1(AI):
    def get_move(self, board, check_win):
        # Find all empty cells on the board
        empty_cells = [(i, j) for i in range(15) for j in range(15) if board[i][j] == ' ']

        # Randomly select one of the empty cells
        if empty_cells:
            return random.choice(empty_cells)
        else:
            return None  # No move is possible

class AI2(AI):
    def get_move(self, board, check_win):
        blocking_move = self.find_blocking_move(self.symbol, board, check_win)
        return blocking_move if blocking_move else self.random_move(board)

    def random_move(self, board):
        empty_cells = [(i, j) for i in range(15) for j in range(15) if board[i][j] == ' ']
        return random.choice(empty_cells) if empty_cells else None

    def find_blocking_move(self, player, board, check_win):
        for i in range(15):
            for j in range(15):
                if board[i][j] == ' ':
                    board[i][j] = player
                    if check_win(i, j, player, board):
                        board[i][j] = ' '
                        return i, j
                    board[i][j] = ' '
        return None
        
# Khởi tạo và chạy trò chơi
ai1 = AI1("AI1", "X")
ai2 = AI2("AI2", "O")
game = CaroGameAI(ai1, ai2, rounds=100)
game.play_game()

# In kết quả
print("AI1 Results:", game.results['X'])
print("AI2 Results:", game.results['O'])
print("Draws:", game.results['Draw'])