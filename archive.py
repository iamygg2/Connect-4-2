"""
import numpy as np
import pygame

# Create board
board = [["" for _ in range(7)] for _ in range(6)]

rows = 6
columns = 7

# Print board aesthetically

def printBoard(board):
    print("\n")
    print("-" * 43)
    for row in board:
        # Make sure each cell has the same width
        print("| " + " | ".join(f" {cell if cell != '' else ' '} " for cell in row) + " |")
    print("-" * 43)
    print("\n")


# First Move

def dropPiece(board, col, player):
    for row in range(5, -1, -1):
        if board[row][col] == "":
            board[row][col] = player
            break

# check for diagonals

def checkWin(board, player):
    for column in range(columns):
        count = 0
        for row in range(rows-1, -1, -1):
            if board[row][column] == player:
                count += 1
                if count == 4:
                    print(player, "wins! on column", (column+1))
                    quit()
                
            else:
                break


dropPiece(board, 1, "R")
dropPiece(board, 1, "R")
dropPiece(board, 1, "R")
dropPiece(board, 1, "R")
printBoard(board)
checkWin(board, "R")
"""