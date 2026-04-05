'''
Christopher Berkowitz
Python final project
Bingo roguelike game
'''

import copy
import time
import random


# functions
def create_grid(rows, cols, dead_s):
    board = []
    # outer loop iterates over rows
    for y in range(0,  rows):
        new_row = []
        # inner loop iterates over columns
        for x in range(0, cols):
            new_row.append(dead_s)
        board.append(new_row)

    return board

def create_cells(board, rows, cols):
    letter = []
    number = []
    score = []
    addons = []

    # adding a letter to each cell
    for y in range(0, rows):
        new_row = []
        for x in range(0, cols):
            if x == 0:
                new_row.append('B')
            elif x == 1:
                new_row.append('I')
            elif x == 2:
                new_row.append('N')
            elif x == 3:
                new_row.append('G')
            elif x == 4:
                new_row.append('O')
        letter.append(new_row)
    
    # adding a number to each cell
    random_numbers = []
    
    for y in range(0, rows):
        index = 0
        # creating random numbers for the scoring of each cell
        while len(random_numbers) < 5*(y+1):
            # creates a random number relating to the amount of times the first for loop has ran, creating 5 unique random numbers from 1-15 for the first loop, 5 from 16-30 for the second, etc.
            num = random.randint((2 + ((15*index) - 1)), (16 + ((15*index) - 1)))
            if num not in random_numbers:
                random_numbers.append(num)
                index += 1
                if index > 4:
                    index = 0
        #print(random_numbers)

    for y in range(0, rows):
        new_row = []
        for x in range(0, cols):
            #print(y + (x * 5))
            new_row.append(random_numbers[x + (y * 5)])
        number.append(new_row)

    # at game start, score is equal to the cell's number
    score = number

    return letter, number, score




def display_board(letters, numbers, scores):
    # outer loop iterates rows
    for row, row_num, row_score in zip(letters, numbers, scores):
        # inner loop iterates columns
        for letter, number, score in zip(row, row_num, row_score):
            print(f'[{letter} {number} {score}]', end=" ")
        print()

def count_neighbors(board, cur_x, cur_y, alive_s):
    row_num = len(board)
    col_num = len(board[0])

    left = (cur_x - 1) % col_num
    right = (cur_x + 1) % col_num

    above = (cur_y - 1) % row_num
    below = (cur_y + 1) % row_num
    # holds count of alive neighbors
    neighbor_count = 0

    neighbors = [
        board[above][left], board[above][cur_x], board[above][right],
        board[cur_y][left],                      board[cur_y][right],
        board[below][left], board[below][cur_x], board[below][right]
    ]

    for cell in neighbors:
        if cell == alive_s:
            neighbor_count += 1

    return neighbor_count

def update_cell(cell, num_neighbors, alive_s, dead_s):
    if cell == alive_s and (num_neighbors == 2 or num_neighbors == 3):
        return alive_s
    elif cell == dead_s and num_neighbors == 3:
        return alive_s
    else:
        return dead_s

# ----- global variables -----
alive = "X"
dead = "."

num_rows = 5
num_cols = 5

# cell arrays

# ----- main code -----
grid = create_grid(num_rows, num_cols, dead)
cell_letter, cell_number, cell_score = create_cells(grid, num_rows, num_cols)
grid[1][1] = grid[1][2] = grid[1][3] = alive
#grid[2][0] = grid[2][1] = grid[2][2] = grid[1][2] = grid[0][1] = alive

#grid, num_rows, num_cols = read_file("test_board.txt")

for generation in range(0, 5):
    # create a copy of grid
    grid_copy = copy.deepcopy(grid)

    # outer loop - rows
    for y in range(0, num_rows):
        # inner loop - columns
        for x in range(num_cols):

            # count alive neighbors
            alive_neighbors = count_neighbors(grid_copy, x, y, alive)

            #update cell state
            grid[y][x] = update_cell(grid_copy[y][x], alive_neighbors, alive, dead)

    # print board
    display_board(cell_letter, cell_number, cell_score)
    #print(random_numbers)
    print()
    time.sleep(0.65)