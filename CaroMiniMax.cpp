#include <iostream>
#include <vector>
#include <ctime>
#include <cstdlib>
#include <climits>

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
bool CheckWin(const vector<vector<char>>& board, char symbol) {
    // Kiểm tra hàng và cột
    for (int i = 0; i < BOARD_SIZE; i++) {
        for (int j = 0; j <= BOARD_SIZE - WINNING_LENGTH; j++) {
            bool rowWin = true, colWin = true;
            for (int k = 0; k < WINNING_LENGTH; k++) {
                if (board[i][j + k] != symbol) rowWin = false;
                if (board[j + k][i] != symbol) colWin = false;
            }
            if (rowWin || colWin) return true;
        }
    }

    // Kiểm tra đường chéo
    for (int i = 0; i <= BOARD_SIZE - WINNING_LENGTH; i++) {
        for (int j = 0; j <= BOARD_SIZE - WINNING_LENGTH; j++) {
            bool primaryDiagonalWin = true, secondaryDiagonalWin = true;
            for (int k = 0; k < WINNING_LENGTH; k++) {
                if (board[i + k][j + k] != symbol) primaryDiagonalWin = false;
                if (board[i + k][j + WINNING_LENGTH - 1 - k] != symbol) secondaryDiagonalWin = false;
            }
            if (primaryDiagonalWin || secondaryDiagonalWin) return true;
        }
    }

    return false;
}

int Minimax(vector<vector<char>>& board, char player, int depth, int alpha, int beta) {
    // Nếu một người chơi thắng, trả về giá trị heuristic tương ứng
    if (CheckWin(board, player)) return 10 - depth;
    if (CheckWin(board, player)) return depth - 10;
    if (depth == 0) return 0;

    // Duyệt tất cả các ô trên bàn cờ
    int bestValue;
    if (player == 'O') {
        bestValue = INT_MAX;
        for (int i = 0; i < BOARD_SIZE; i++) {
            for (int j = 0; j < BOARD_SIZE; j++) {
                if (board[i][j] == '.') {
                    board[i][j] = 'O';
                    int value = Minimax(board, 'X', depth - 1, alpha, beta);
                    bestValue = min(bestValue, value);
                    board[i][j] = '.';
                    beta = min(beta, value);
                    if (alpha >= beta) break; // Cắt tỉa alpha-beta
                }
            }
        }
    } else {
        bestValue = INT_MIN;
        for (int i = 0; i < BOARD_SIZE; i++) {
            for (int j = 0; j < BOARD_SIZE; j++) {
                if (board[i][j] == '.') {
                    board[i][j] = 'X';
                    int value = Minimax(board, 'O', depth - 1, alpha, beta);
                    bestValue = max(bestValue, value);
                    board[i][j] = '.';
                    alpha = max(alpha, value);
                    if (alpha >= beta) break; // Cắt tỉa alpha-beta
                }
            }
        }
    }

    return bestValue;
}

void ComputerMove(vector<vector<char>>& board) {
    int bestValue = INT_MAX;
    pair<int, int> bestMove = {-1, -1};
    int alpha = INT_MIN;
    int beta = INT_MAX;
    int maxDepth = 3; // Độ sâu tối đa mà thuật toán sẽ duyệt (điều chỉnh nếu cần)

    for (int i = 0; i < BOARD_SIZE; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            if (board[i][j] == '.') {
                board[i][j] = 'O';
                int moveValue = Minimax(board, 'X', maxDepth, alpha, beta);
                board[i][j] = '.';
                if (moveValue < bestValue) {
                    bestValue = moveValue;
                    bestMove = {i, j};
                }
            }
        }
    }

    board[bestMove.first][bestMove.second] = 'O';
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
            ComputerMove(board);
        }
        totalMoves++;

        if (CheckWin(board, symbol)) {
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