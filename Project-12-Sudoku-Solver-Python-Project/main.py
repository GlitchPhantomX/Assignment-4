import time

def print_board(board):
    """Prints the Sudoku board in a user-friendly format."""
    print("\nSudoku Board:")
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("-" * 21) 
        print(" ".join(str(num) if num != 0 else "." for num in row[:3]) + " | " +
              " ".join(str(num) if num != 0 else "." for num in row[3:6]) + " | " +
              " ".join(str(num) if num != 0 else "." for num in row[6:]))
    print()

def find_empty(board):
    """Finds an empty cell in the Sudoku board (returns row, col)."""
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  
    return None

def is_valid(board, num, row, col):
    """Checks if a number is valid in the given row, column, and 3x3 box."""
    if num in board[row]:
        return False

    if num in [board[i][col] for i in range(len(board))]:
        return False

    box_row, box_col = row // 3 * 3, col // 3 * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False
                
    return True

def solve(board, visualize=False):
    """Solves the Sudoku puzzle using backtracking."""
    empty = find_empty(board)
    if not empty:
        return True  

    row, col = empty

    for num in range(1, 10):
        if is_valid(board, num, row, col):
            board[row][col] = num
            
            if visualize:  
                print_board(board)
                time.sleep(0.2)  

            if solve(board, visualize):
                return True
            
            board[row][col] = 0  
            
    return False

def get_user_board():
    """Allows the user to enter a custom Sudoku board or use the default."""
    choice = input("Do you want to enter your own Sudoku board? (yes/no): ").strip().lower()
    if choice == "yes":
        print("Enter 9 rows of 9 numbers (use 0 for empty spaces), separated by spaces:")
        board = []
        for i in range(9):
            while True:
                try:
                    row = list(map(int, input(f"Row {i+1}: ").split()))
                    if len(row) == 9:
                        board.append(row)
                        break
                    else:
                        print("⚠️ Each row must contain exactly 9 numbers.")
                except ValueError:
                    print("⚠️ Invalid input! Please enter numbers only.")
        return board
    else:
        return [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]

if __name__ == "__main__":
    board = get_user_board()
    
    print_board(board)
    
    start_time = time.time()
    solved = solve(board, visualize=False)  
    end_time = time.time()
    
    if solved:
        print("\n🎉 Solved Sudoku Board:")
        print_board(board)
    else:
        print("\n❌ No solution exists for the given Sudoku board.")
    
    print(f"⏳ Execution Time: {end_time - start_time:.4f} seconds")
