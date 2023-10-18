#include <iostream>
#include <vector>
#include <ctime>
#include <cstdlib>

using namespace std;

const int BOARD_SIZE = 15; // Kích thước bàn cờ
const int WINNING_LENGTH = 4; // Độ dài cần để chiến thắng

// Hàm in bàn cờ
void PrintBoard(const vector<vector<char>>& board) {
    cout << "Current Board:" << endl;
    for (int i = 0; i < BOARD_SIZE; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            cout << board[i][j] << " ";
        }
        cout << endl;
    }
    cout << endl;
}

// Hàm kiểm tra chiến thắng
bool CheckWin(const vector<vector<char>>& board, char symbol, int row, int col) {
    // Kiểm tra theo 8 hướng khác nhau từ ô được đánh dấu
    int directions[8][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}, {-1, -1}, {1, 1}, {-1, 1}, {1, -1}};
    
    for (int dir = 0; dir < 8; dir++) {
        int count = 1; // Đếm số lượng ô liên tiếp có cùng symbol
        
        for (int step = 1; step < WINNING_LENGTH; step++) {
            int newRow = row + directions[dir][0] * step;
            int newCol = col + directions[dir][1] * step;
            
            if (newRow >= 0 && newRow < BOARD_SIZE && newCol >= 0 && newCol < BOARD_SIZE &&
                board[newRow][newCol] == symbol) {
                count++;
            } else {
                break; // Nếu không tìm thấy ô liên tiếp cùng symbol, dừng kiểm tra theo hướng này
            }
        }
        
        if (count == WINNING_LENGTH) {
            return true; // Người chơi đã chiến thắng
        }
    }
    
    return false; // Không có chiến thắng trong tất cả các hướng
}

// Hàm cho máy đánh
void ComputerMove(vector<vector<char>>& board, int& row, int& col) {
    vector<pair<int, int>> availableMoves;
    for (int i = 0; i < BOARD_SIZE; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            if (board[i][j] == '.') {
                availableMoves.push_back({i, j});
            }
        }
    }
    
    // Chọn ngẫu nhiên một nước đi từ danh sách
    int randomIndex = rand() % availableMoves.size();
    row = availableMoves[randomIndex].first;
    col = availableMoves[randomIndex].second;
    board[row][col] = 'O';
}

int main() {
    // Khởi tạo hạt giả ngẫu nhiên
    srand(time(0));

    vector<vector<char>> board(BOARD_SIZE, vector<char>(BOARD_SIZE, '.'));
    int player = 1;
    int row, col;
    int totalMoves = 0;

    while (true) {
        PrintBoard(board);
        char symbol;
        if (player == 1) {
            symbol = 'X';
            cout << "Player " << player << " (Symbol " << symbol << "), enter row and column (1-15): ";
            cin >> row >> col;

            if (board[row - 1][col - 1] != '.') {
                cout << "Invalid move. This cell is already occupied." << endl;
                continue;
            }

            board[row - 1][col - 1] = symbol;
        } else {
            symbol = 'O';
            cout << "Computer's turn..." << endl;
            ComputerMove(board, row, col);
        }
        totalMoves++;

        if (CheckWin(board, symbol, row, col)) {
            PrintBoard(board);
            if (player == 1) {
                cout << "Player " << player << " (Symbol " << symbol << ") wins!" << endl;
            } else {
                cout << "Computer wins!" << endl;
            }
            break;
        }

        if (totalMoves == BOARD_SIZE * BOARD_SIZE) {
            PrintBoard(board);
            cout << "It's a draw!" << endl;
            break;
        }

        player = (player == 1) ? 2 : 1;
    }

    return 0;
}