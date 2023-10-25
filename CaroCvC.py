import tkinter as tk
from tkinter import messagebox
import random

class CaroGame:
    def __init__(self, master):
        self.master = master
        self.master.title('Caro Game')
        self.board = [[' ' for _ in range(15)] for _ in range(15)]
        self.game_over = False
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        for i in range(15):
            row_buttons = []
            for j in range(15):
                button = tk.Button(self.master, text=' ', width=4, height=2,
                                   command=self.click)
                button.grid(row=i, column=j)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def click(self):
        # Khi một ô được nhấp, máy sẽ thực hiện nước đi cho cả hai người chơi: 'X' và 'O'
        self.make_ai_move('X')
        self.make_ai_move('O')

    def check_win(self, row, col, player):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            for i in range(1, 4):
                x, y = row + dx * i, col + dy * i
                if 0 <= x < 15 and 0 <= y < 15 and self.board[x][y] == player:
                    count += 1
                else:
                    break
            for i in range(1, 4):
                x, y = row - dx * i, col - dy * i
                if 0 <= x < 15 and 0 <= y < 15 and self.board[x][y] == player:
                    count += 1
                else:
                    break
            if count >= 4:
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
        self.game_over = False

    def make_ai_move(self, player):
        if not self.game_over:
            empty_cells = [(i, j) for i in range(15) for j in range(15) if self.board[i][j] == ' ']
            if empty_cells:
                row, col = random.choice(empty_cells)
                self.board[row][col] = player
                self.buttons[row][col].config(text=player)
                if self.check_win(row, col, player):
                    self.game_over = True
                    messagebox.showinfo('Winner', f'Player {player} wins!')
                    self.ask_restart()

# Tạo cửa sổ giao diện và khởi chạy ứng dụng
root = tk.Tk()
game = CaroGame(root)
root.mainloop()
