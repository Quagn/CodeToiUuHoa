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
        best_score = -1
        best_move = None

        for i in range(15):
            for j in range(15):
                if board[i][j] == ' ':
                    score = self.evaluate_move(i, j, self.symbol, board)
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        return best_move

    def evaluate_move(self, row, col, player, board):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        score = 0

        for dx, dy in directions:
            line_score = 0
            count = 0
            open_ends = 0

            # Kiểm tra một hướng
            for i in range(1, 5):
                x, y = row + dx * i, col + dy * i
                if 0 <= x < 15 and 0 <= y < 15:
                    if board[x][y] == player:
                        count += 1
                    elif board[x][y] == ' ':
                        open_ends += 1
                        break
                    else:
                        break

            # Kiểm tra hướng ngược lại
            for i in range(1, 5):
                x, y = row - dx * i, col - dy * i
                if 0 <= x < 15 and 0 <= y < 15:
                    if board[x][y] == player:
                        count += 1
                    elif board[x][y] == ' ':
                        open_ends += 1
                        break
                    else:
                        break

            # Tính điểm dựa trên số quân cờ liên tiếp và mở rộng
            if count > 0:
                line_score = 10 ** count
                if open_ends > 0:  # Tăng điểm cho các dãy mở rộng
                    line_score *= open_ends

            score += line_score

        return score

class AI2(AI):
    def get_move(self, board, check_win):
        best_score = -1
        best_move = None

        for i in range(15):
            for j in range(15):
                if board[i][j] == ' ':
                    score = self.evaluate_move(i, j, self.symbol, board)
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        return best_move

    def evaluate_move(self, row, col, player, board):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        score = 0

        for dx, dy in directions:
            line_score = 0
            count = 0

            # Kiểm tra một hướng
            for i in range(1, 5):
                x, y = row + dx * i, col + dy * i
                if 0 <= x < 15 and 0 <= y < 15 and board[x][y] == player:
                    count += 1
                else:
                    break

            # Kiểm tra hướng ngược lại
            for i in range(1, 5):
                x, y = row - dx * i, col - dy * i
                if 0 <= x < 15 and 0 <= y < 15 and board[x][y] == player:
                    count += 1
                else:
                    break

            # Tính điểm dựa trên số quân cờ liên tiếp
            if count > 0:
                line_score = 10 ** count

            score += line_score

        return score
        
# Khởi tạo và chạy trò chơi
ai1 = AI1("AI1", "X")
ai2 = AI2("AI2", "O")
game = CaroGameAI(ai1, ai2, rounds=100)
game.play_game()

# In kết quả
print("AI1 Results:", game.results['X'])
print("AI2 Results:", game.results['O'])
print("Draws:", game.results['Draw'])