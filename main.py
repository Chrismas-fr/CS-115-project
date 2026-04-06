'''
Christopher Berkowitz
Python final project
Bingo roguelike game
'''

import copy
import time
import random


# functions
def create_grid(rows, cols):
    board = []
    # outer loop iterates over rows
    for y in range(0,  rows):
        new_row = []
        # inner loop iterates over columns
        for x in range(0, cols):
            new_row.append('x')
        board.append(new_row)

    return board

def create_cells(rows, cols):
    letter = []
    number = []
    score = []
    addons = []
    tile_type = []
    bingo_numbers = []

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

    # ball numbers mean the
    bingo_numbers = random_numbers

    for y in range(0, rows):
        new_row = []
        for x in range(0, cols):
            new_row.append(random_numbers[x + (y * 5)])
        number.append(new_row)

    # at game start, score is equal to the cell's number
    score = number

    # setting a 2d list of addons for tiles (none when game starts)
    for y in range(0, rows):
        new_row = []
        for x in range(0, cols):
            new_row.append("")
        addons.append(new_row)

    # at game start, all tiles are normal type (abbreviated as "no")
    for y in range(0, rows):
        new_row = []
        for x in range(0, cols):
            new_row.append("no")
        tile_type.append(new_row)


    return letter, number, score, addons, tile_type, bingo_numbers




def display_board(letters, numbers, scores):
    # outer loop iterates rows
    for row, row_num, row_score in zip(letters, numbers, scores):
        # inner loop iterates columns
        for letter, number, score in zip(row, row_num, row_score):
            print(f'[{letter} {number} {score}]', end=" ")
        print()

def count_neighbors(board, cur_x, cur_y):
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
        if cell == 'x':
            neighbor_count += 1

    return neighbor_count

def update_cell(cell, num_neighbors):
    pass

def game_interaction():
    user = input("ro for roll | re to refresh deck | sh to open shop\n")
    return user

def game_roll(deck):
    return deck[random.randint(0,len(deck)-1)]

# ----- global variables -----
num_rows = 5 #num rows can be increased to extend board downward num cols can not, things break
num_cols = 5

charges = 15
bingo_discard = []

alive = "x"
dead = "."

end_of_round = True
game_end = False

# ----- main code -----
grid = create_grid(num_rows, num_cols)
cell_letter, cell_number, cell_score, cell_addons, cell_type, bingo_deck = create_cells(num_rows, num_cols)

#for generation in range(0, 5):
while not game_end:
    # input
    if end_of_round:
        user_input = game_interaction()

        if user_input.lower() == "ro":
            print(game_roll(bingo_deck))

        

    # update
    # create a copy of grid
    grid_copy = copy.deepcopy(grid)

    # outer loop - rows
    for y in range(0, num_rows):
        # inner loop - columns
        for x in range(num_cols):

            # count alive neighbors
            alive_neighbors = count_neighbors(grid_copy, x, y)

            #update cell state
            grid[y][x] = update_cell(grid_copy[y][x], alive_neighbors)

    # output
    display_board(cell_letter, cell_number, cell_score)
    print()
    time.sleep(0.65)



'''
game stuff to remember

game loop:
    input
    update
    output

bingo numbers will be drawn until empty, then will be reshuffled
bingo balls only have numbers, not letters, tile letters are used for tile abilities to combo
tiles can be activated or triggered: 
    activated means the tile gives score and uses its effect
    triggered means the tile only uses its effect
'''