import tkinter as tk
from tkinter import messagebox

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
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            if self.check_win(row, col):
                self.game_over = True
                messagebox.showinfo('Winner', f'Player {self.current_player} wins!')
                self.ask_restart()
            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_win(self, row, col):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            for i in range(1, 5):
                x, y = row + dx * i, col + dy * i
                if 0 <= x < 15 and 0 <= y < 15 and self.board[x][y] == self.current_player:
                    count += 1
                else:
                    break
            for i in range(1, 5):
                x, y = row - dx * i, col - dy * i
                if 0 <= x < 15 and 0 <= y < 15 and self.board[x][y] == self.current_player:
                    count += 1
                else:
                    break
            if count >= 5:
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

# Create a Tkinter root window
root = tk.Tk()
game = CaroGame(root)
root.mainloop()