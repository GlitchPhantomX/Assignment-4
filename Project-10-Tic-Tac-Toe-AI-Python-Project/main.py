import random

def print_board(board):
    """Prints the Tic-Tac-Toe board."""
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_winner(board):
    """Checks if there's a winner."""
    for row in board:
        if row.count(row[0]) == 3 and row[0] != " ":
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return board[0][2]
    return None

def minimax(board, depth, is_maximizing):
    """Minimax algorithm for AI move selection."""
    scores = {'X': -1, 'O': 1, 'tie': 0}
    winner = check_winner(board)
    if winner:
        return scores.get(winner, 0)
    
    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = " "
                    best_score = min(score, best_score)
        return best_score

def best_move(board):
    """Finds the best move for the AI."""
    best_score = -float('inf')
    move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = 'O'
                score = minimax(board, 0, False)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

def get_valid_input():
    """Gets a valid row and column input from the user."""
    while True:
        user_input = input("Enter your move (row and column, separated by space): ").strip()
        parts = user_input.split()
        
        if len(parts) != 2:
            print("⚠️ Invalid input! Please enter **two** numbers separated by a space (e.g., `1 2`).")
            continue

        if not all(part.isdigit() for part in parts):
            print("⚠️ Invalid input! Please enter **only numbers** (e.g., `1 2`).")
            continue

        row, col = map(int, parts)
        if row in range(3) and col in range(3):
            return row, col
        else:
            print("⚠️ Invalid move! Please enter numbers **between 0 and 2**.")

def play_game():
    """Main function to play Tic-Tac-Toe."""
    board = [[" " for _ in range(3)] for _ in range(3)]
    print_board(board)

    while True:
        while True:
            row, col = get_valid_input()
            if board[row][col] == " ":
                board[row][col] = 'X'
                break
            else:
                print("⚠️ That spot is already taken! Try again.")

        if check_winner(board):
            print_board(board)
            print("🎉 You win!")
            break

        if all(cell != " " for row in board for cell in row):
            print_board(board)
            print("🤝 It's a tie!")
            break

        print("🤖 Computer's turn:")
        move = best_move(board)
        board[move[0]][move[1]] = 'O'

        if check_winner(board):
            print_board(board)
            print("😞 Computer wins!")
            break

        print_board(board)

play_game()
