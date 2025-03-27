import time
import math

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_winner(board):
    for row in board:
        if row.count(row[0]) == len(row) and row[0] != " ":
            return True
    for col in range(len(board)):
        if all(board[row][col] == board[0][col] and board[0][col] != " " for row in range(len(board))):
            return True
    if all(board[i][i] == board[0][0] and board[0][0] != " " for i in range(len(board))) or \
       all(board[i][len(board)-1-i] == board[0][len(board)-1] and board[0][len(board)-1] != " " for i in range(len(board))):
        return True
    return False

def tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]
    current_player = 0

    for turn in range(9):
        print_board(board)
        print(f"Player {players[current_player]}'s turn:")
        row = int(input("Enter row (0, 1, 2): "))
        col = int(input("Enter column (0, 1, 2): "))

        if board[row][col] == " ":
            board[row][col] = players[current_player]
            if check_winner(board):
                print_board(board)
                print(f"Player {players[current_player]} wins! 🎉")
                return
            current_player = (current_player + 1) % 2
        else:
            print("Invalid move! Try again.")
            time.sleep(1)

    print_board(board)
    print("It's a tie! 🤝")

if __name__ == "__main__":
    tic_tac_toe()
