import numpy as np
import pygame
import sys
import math

ROW_COUNT = 6
COLUMN_COUNT = 7


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def main():
    pygame.init()
    width = COLUMN_COUNT * 100
    height = (ROW_COUNT + 1) * 100
    size = (width, height)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Connect Four")
    
    blue = (0, 0, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    yellow = (255, 255, 0)

    board = create_board()
    print_board(board)
    game_over = False
    turn = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, black, (0, 0, width, 100))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, red, (posx, 50), 50)
                else:
                    pygame.draw.circle(screen, yellow, (posx, 50), 50)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, black, (0, 0, width, 100))

                if turn == 0:
                    posx = event.pos[0]
                    col = int(posx // 100)

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            print("Player 1 wins!")
                            game_over = True


                else:
                    posx = event.pos[0]
                    col = int(posx // 100)

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winning_move(board, 2):
                            print("Player 2 wins!")
                            game_over = True

                print_board(board)

                turn += 1
                turn = turn % 2

    pygame.quit()

if __name__ == "__main__":
    main()
