import tkinter as tk
from tkinter import messagebox
import random

class CaroGame:
    def __init__(self, master):
        self.master = master
        self.master.title('Caro Game')
        self.board = [[' ' for _ in range(15)] for _ in range(15)]
        self.current_player = 'X'
        self.buttons = []
        self.game_over = False
        self.create_buttons()

    def create_buttons(self):
        for i in range(15):
            row_buttons = []
            for j in range(15):
                button = tk.Button(self.master, text=' ', width=4, height=2,
                                   command=lambda i=i, j=j: self.click(i, j))
                button.grid(row=i, column=j)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def click(self, row, col):
        if self.board[row][col] == ' ' and not self.game_over:
            self.board[row][col] = 'X'
            self.buttons[row][col].config(text='X')
            if self.check_win(row, col, 'X'):
                self.game_over = True
                messagebox.showinfo('Winner', 'Player X wins!')
                self.ask_restart()
            else:
                self.make_ai_move()

    def check_win(self, row, col, player):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            blocked_1 = False
            blocked_2 = False
            for i in range(1, 5):  # Extend to 5 for possibility of 5 in a row
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

            for i in range(1, 5):  # Extend to 5 for possibility of 5 in a row
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

            if count == 5 and (not blocked_1 or not blocked_2):
                return True
            elif count == 4 and not (blocked_1 and blocked_2):
                return True

        return False

    def ask_restart(self):
        play_again = messagebox.askyesno('Play Again?', 'Would you like to play again?')
        if play_again:
            self.restart_game()
        else:
            self.master.quit()

    def restart_game(self):
        self.board = [[' ' for _ in range(15)] for _ in range(15)]
        for i in range(15):
            for j in range(15):
                self.buttons[i][j].config(text=' ')
        self.current_player = 'X'
        self.game_over = False

    def make_ai_move(self):
        if not self.game_over:
            blocking_move = self.find_blocking_move()
            if blocking_move:
                row, col = blocking_move
            else:
                empty_cells = [(i, j) for i in range(15) for j in range(15) if self.board[i][j] == ' ']
                row, col = random.choice(empty_cells) if empty_cells else (None, None)

            if row is not None and col is not None:
                self.board[row][col] = 'O'
                self.buttons[row][col].config(text='O')
                if self.check_win(row, col, 'O'):
                    self.game_over = True
                    messagebox.showinfo('Winner', 'Player O wins!')
                    self.ask_restart()

    def find_blocking_move(self):
        for i in range(15):
            for j in range(15):
                if self.board[i][j] == ' ':
                    # Thử một nước đi tạm thời
                    self.board[i][j] = 'X'
                    if self.check_win(i, j, 'X'):
                        # Đây là nước đi cần chặn
                        self.board[i][j] = ' '
                        return i, j
                    self.board[i][j] = ' '
        return None


# Tạo cửa sổ giao diện và khởi chạy ứng dụng
root = tk.Tk()
game = CaroGame(root)
root.mainloop()
