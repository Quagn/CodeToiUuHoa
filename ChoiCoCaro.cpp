#include <iostream>
#include <vector>

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

int main() {
    vector<vector<char>> board(BOARD_SIZE, vector<char>(BOARD_SIZE, '.')); // Tạo bàn cờ rỗng

    int player = 1; // 1 đại diện cho người chơi X, 2 đại diện cho người chơi O
    int row, col;

    int totalMoves = 0; // Đếm số lượt đã đi để kiểm tra điều kiện hòa

    while (true) {
        // In bàn cờ hiện tại và phiên của người chơi
        PrintBoard(board);
        char symbol = (player == 1) ? 'X' : 'O';
        cout << "Player " << player << " (Symbol " << symbol << "), enter row and column (1-15): ";

        cin >> row >> col;

        // Kiểm tra nếu ô đã được đánh dấu
        if (board[row - 1][col - 1] != '.') {
            cout << "Invalid move. This cell is already occupied." << endl;
            continue;
        }

        // Đánh dấu ô được chọn bởi người chơi hiện tại
        board[row - 1][col - 1] = symbol;
        totalMoves++;

        // Kiểm tra chiến thắng
        if (CheckWin(board, symbol, row - 1, col - 1)) {
            // Người chơi hiện tại chiến thắng
            PrintBoard(board);
            cout << "Player " << player << " (Symbol " << symbol << ") wins!" << endl;
            break;
        }

        // Kiểm tra điều kiện hòa
        if (totalMoves == BOARD_SIZE * BOARD_SIZE) {
            // Trò chơi hòa
            PrintBoard(board);
            cout << "It's a draw!" << endl;
            break;
        }

        // Chuyển lượt chơi sang người chơi khác
        player = (player == 1) ? 2 : 1;
    }

    return 0;
}
