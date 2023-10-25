import tkinter as tk
from tkinter import messagebox
import random

class CaroGame:
    def __init__(self, master):
        self.master = master
        self.master.title('Caro Game')
        self.board = [[' ' for _ in range(3)] for _ in range(3)]  # Khởi tạo bảng 3x3 để lưu trạng thái trò chơi
        self.current_player = 'X'  # Người chơi hiện tại là 'X'
        self.buttons = []  # Danh sách các nút trên giao diện
        self.game_over = False  # Trạng thái trò chơi (chưa kết thúc hay đã kết thúc)
        self.create_buttons()  # Tạo giao diện trò chơi

    def create_buttons(self):
        for i in range(3):
            row_buttons = []
            for j in range(3):
                button = tk.Button(self.master, text=' ', width=4, height=2,
                                   command=lambda i=i, j=j: self.click(i, j))
                button.grid(row=i, column=j)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def click(self, row, col):
        if self.board[row][col] == ' ' and not self.game_over:
            self.board[row][col] = 'X'  # Đánh dấu ô đã được người chơi X chọn
            self.buttons[row][col].config(text='X')  # Cập nhật giao diện
            if self.check_win(row, col):
                self.game_over = True
                messagebox.showinfo('Winner', 'Player X wins!')  # Hiển thị thông báo người chiến thắng
                self.ask_restart()
            else:
                self.make_ai_move()  # Gọi phương thức để máy thực hiện nước đi

    def check_win(self, row, col):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            for i in range(1, 3):
                x, y = row + dx * i, col + dy * i
                if 0 <= x < 3 and 0 <= y < 3 and self.board[x][y] == self.current_player:
                    count += 1
                else:
                    break
            for i in range(1, 3):
                x, y = row - dx * i, col - dy * i
                if 0 <= x < 3 and 0 <= y < 3 and self.board[x][y] == self.current_player:
                    count += 1
                else:
                    break
            if count >= 3:
                return True
        return False

    def ask_restart(self):
        play_again = messagebox.askyesno('Play Again?', 'Would you like to play again?')
        if play_again:
            self.restart_game()
        else:
            self.master.quit()

    def restart_game(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]  # Đặt lại trạng thái ban đầu
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=' ')
        self.current_player = 'X'  # Khởi tạo lại người chơi và trạng thái trò chơi
        self.game_over = False

    def make_ai_move(self):
        if not self.game_over:
            empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' ']

            if empty_cells:
                row, col = random.choice(empty_cells)  # Lựa chọn ngẫu nhiên một ô trống
                self.board[row][col] = 'O'  # Đánh dấu ô đã được máy chọn
                self.buttons[row][col].config(text='O')  # Cập nhật giao diện
                if self.check_win(row, col):
                    self.game_over = True
                    messagebox.showinfo('Winner', 'Player O wins!')  # Hiển thị thông báo người chiến thắng
                    self.ask_restart()

# Tạo cửa sổ giao diện và khởi chạy ứng dụng
root = tk.Tk()
game = CaroGame(root)
root.mainloop()
