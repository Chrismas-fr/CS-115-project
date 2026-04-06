'''
Christopher Berkowitz
Python final project
Bingo roguelike game
'''

import copy
import time
import random
import math


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
    tile_index = []

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

    # at game start, all tiles are normal type (abbreviated as "nor")
    for y in range(0, rows):
        new_row = []
        for x in range(0, cols):
            new_row.append("nor")
        tile_type.append(new_row)

    # ball numbers mean the deck that numbers are pulled from
    for num in random_numbers:
        entry = []
        entry.append(num)
        entry.append("")
        bingo_numbers.append(entry)
    random.shuffle(bingo_numbers)

    # a unique index for each tile for identification
    for y in range(0, rows):
        new_row = []
        for x in range(0, cols):
            new_row.append(x + (y * 5))
        tile_index.append(new_row)

    return letter, number, score, addons, tile_type, bingo_numbers, tile_index




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

def game_interaction(score):
    good_input = False

    while not good_input:
        
        user = input("ro for roll | re to refresh deck | sh to open shop\n")

        if not user == "ro" and not user == "re" and not user == "sh":
            print("Not a valid input, use one of the options.")
        elif user == "re" and score < 100:
            print("You need at least 100 score to refresh.")
        else:
            good_input = True


    return user

def game_roll():
    roll = bingo_deck[0][0]
    # removes number from the deck and adds it to the discard only if there are still numbers in deck
    if not len(bingo_deck) <= 1:
        bingo_discard.append(bingo_deck[0])
        bingo_deck.remove(bingo_deck[0])
    else:
        #if not adds all numbers from discard into deck and shuffles
        deck_reroll()
    return roll

def deck_reroll():
    bingo_deck.extend(bingo_discard)
    del bingo_discard[:]
    random.shuffle(bingo_deck)

def score_cell(numbers, tile_scores, roll):
    score = 0
    index_y = 0
    index_x = 0
    triggered_cells = []
    # iterating vertically through tile numbers and scores
    for nums_row, score_row in zip(numbers, tile_scores):
        # iterating horizontally through tile numbers and scores
        for number, tile_score in zip(nums_row, score_row):
            # scoring tiles if rolled number is on tile
            if roll == number:
                score += tile_score

                # saves the locations of scored cells
                cell_input = []
                cell_input.append(index_y)
                cell_input.append(index_x)
                triggered_cells.append(cell_input)
            index_x += 1
            if index_x > num_cols - 1:
                index_x = 0
        index_y += 1
        if index_y > num_rows - 1:
            index_y = 0
    
    print(triggered_cells)
    return score, triggered_cells

# classes
class Trigger_Tiles:
    def __init__(self, tile_type, tile_index, tile_yx):
        self.tile_type = tile_type
        self.tile_index = tile_index
        self.tile_yx = tile_yx

    def find_neighbors(tile_index, tile_yx):
        row_num = len(tile_index)
        col_num = len(tile_index[0])

        left = (cur_x - 1) % col_num
        right = (cur_x + 1) % col_num

        above = (cur_y - 1) % row_num
        below = (cur_y + 1) % row_num

        neighbors = [
                                   tile_index[above][cur_x],                     
            tile_index[cur_y][left],                        tile_index[cur_y][right],
                                   tile_index[below][cur_x]                     
        ]

        return neighbors

    


# ----- global variables -----
num_rows = int(input("number of rows: >>\t"))
# num_rows = 5 #num rows can be increased to extend board downward num cols can not, things break
num_cols = 5

charges = 15
bingo_discard = []

alive = "x"
dead = "."

end_of_round = True
game_end = False
show_shop = False

score = 0

# ----- main code -----
grid = create_grid(num_rows, num_cols)
cell_letter, cell_number, cell_score, cell_addons, cell_type, bingo_deck, cell_index = create_cells(num_rows, num_cols)

#for generation in range(0, 5):
while not game_end:
        # input
    if end_of_round:
        user_input = game_interaction(score)

        if user_input.lower() == "ro":
            round_roll = game_roll()
            print("Rolled: ", round_roll) 
            scored_cells, triggered_cells_yx = score_cell(cell_number, cell_score, round_roll)
            score += scored_cells
        elif user_input.lower() == "re":
            deck_reroll()
            score -= round(score*0.1)
        elif user_input.lower() == "sh":
            show_shop = True

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

            
    while not end_of_round:
        

        # output
    display_board(cell_letter, cell_number, cell_score)
    print("deck ", bingo_deck, "discard ", bingo_discard)
    print("score ", score)
    print()
    #print(tile_test.find_neighbors())

    time.sleep(0)

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

tile types + code names:
    trigger 4/8 neighbors: tgn
    activated when another column activates: col
    activates 1-x tiles across board: acb
    large score but no number: nnb
    chance to give score when activated; large score: gmb
    50% chance to activate when any number rolled: jmp
    score multiplied x1.04 permanently: prm

addon types + code names: (additive means can be added to a tile multiple times)
    1.x extra score (additive): mul
    adds secondary number: exn
    %chance to multiply score x times: xml
    gives all tiles 20% of this tiles mult for 2 rounds after activation: phl
    chance traits are 20x% more likely (additave): xch
    adds flat score to tile: scr

deck addons:
    doesn't consume charges: crg
    %chance to add charges: adc
    activates 1 random tile with different number: rnd
    triggers 10 random tiles: trg
    multiplies round score by x times: rsc
    small chance to add permanent mult to all affected tiles: pml
    very small chance to activate all tiles: aat

tile classes:
    triggers others: tgn, acb
    triggered by others: col, jmp
    effect when triggered: nnb, gmb, prm

addon classes:
    effect when triggered: mul, exn, xml, phl, xch, scr

deck classes: 
    changes charges: crg, adc
    triggers unrelated tiles: rnd, trg, aat
    adds a multiplier: rsc, pml
'''