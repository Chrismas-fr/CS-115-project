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
            new_row.append("tgn")
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




def display_board(letters, numbers, scores, tile_indexes):
    # outer loop iterates rows
    for row, row_num, row_score, row_index in zip(letters, numbers, scores, tile_indexes):
        # inner loop iterates columns
        for letter, number, score, tile_index in zip(row, row_num, row_score, row_index):
            print(f'[{letter} {number} {score} - {tile_index}]', end=" ")
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

def find_cell(numbers, roll, triggered_yn):
    if triggered_yn:
        index_y = 0
        index_x = 0
        triggered_cells = []
        # iterating vertically through tile numbers
        for nums_row in numbers:
            # iterating horizontally through tile numbers
            for number in nums_row:
                # finding tiles if rolled number is on tile
                if roll == number:
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
        
        #print(triggered_cells)
        return triggered_cells
    else:
        #take index round down to multiple of 5 subtract that from original to get remainder (eg 21 becomes 20 21-20 = 1 getting 20 and 1) divide 20 by 5 and that gives y value | remainder gives x value
        # multipurposing to find a number's coordinates from its index, so I am using the "numbers" parameter as index
        triggered_cells = []
        tens = math.floor(numbers / 5) * 5
        cell_input = []
        cell_input.append(int(tens/5))
        cell_input.append(numbers-tens)
        return cell_input

# finds the score of a tile from its coordinates
def score_cell(cell_yx, tile_scores):
    score = 0
    cell_x = 0
    cell_y = 0
    '''
    for yx in cell_yx:
        print(yx)
        cell_x = yx[1]
        cell_y = yx[0]
    '''
    cell_x = cell_yx[1]
    cell_y = cell_yx[0]
    index_y = 0
    index_x = 0
    for row in tile_scores:
        if index_y == cell_y:
            for tile_score in row:    
                if index_x == cell_x:
                    score += tile_score
                index_x += 1
        index_y += 1
    
    return score

def play_out_round(user, tile_number, tile_score, tile_type, tile_index, game_score, game_charges):
    end_of_round = True
    game_generations = 5



    if end_of_round:
        if user.lower() == "ro":
            round_roll = game_roll()
            print("Rolled: ", round_roll) 
        elif user.lower() == "re":
            deck_reroll()
            game_score -= round(score*0.1)
        elif user.lower() == "sh":
            pass
    end_of_round = False
    
    tiles_to_score = find_cell(tile_number, round_roll, True)
    print(tiles_to_score, "tiles to score")

    tts_copy = copy.deepcopy(tiles_to_score)

    while game_generations > 0:
        for tile_being_scored in tiles_to_score:
            print(tile_being_scored)
            game_tile = Trigger_Tiles(tile_type, tile_index, tile_number, tile_being_scored[1], tile_being_scored[0])
            #print("neighbors ", game_tile.find_neighbors())
            print("tile type ", tile_type[tile_being_scored[1]][tile_being_scored[0]])
            if tile_type[tile_being_scored[1]][tile_being_scored[0]] == "nor":
                add_score = score_cell(tile_being_scored, tile_score)
                game_score += add_score
                print("adding score: ", add_score)
                tiles_to_score.remove(tiles_to_score[0])
            if tile_type[tile_being_scored[1]][tile_being_scored[0]] == "tgn":
                del tts_copy[:]

                add_score = score_cell(tile_being_scored, tile_score)
                game_score += add_score
                print("adding score: ", add_score)
                tiles_to_score.remove(tiles_to_score[0])

                for neighbor in game_tile.find_neighbors():
                    tts_copy.append(neighbor)
                tiles_to_score = copy.deepcopy(tts_copy)
                print(tiles_to_score, "tiles to score")
        game_generations -= 1
        print("end of gen")
        if len(tiles_to_score) < 1:
            game_generations = 0


    return game_score, game_charges


    #create tile from class as first thing, create array of each tile effected by last round (first round just defaults to the numbers from ball) then run each tile separately from array and put each tile affected into the array and repeat until generations are used up
    '''
    if end_of_round:
        if user_input.lower() == "ro":
            round_roll = game_roll()
            print("Rolled: ", round_roll) 
            triggered_cells_yx = find_cell(cell_number, round_roll, True)
            score_round = score_cell(triggered_cells_yx, cell_score)
            score += score_round
            charges -= 1
        elif user_input.lower() == "re":
            deck_reroll()
            score -= round(score*0.1)
        elif user_input.lower() == "sh":
            show_shop = True
    end_of_round = False
    
    while not end_of_round:
        for cell in triggered_cells_yx:
            test_tile = Trigger_Tiles(cell_type, cell_index, cell_number, cell[1], cell[0])
            print("neighbors: ", test_tile.find_neighbors())
            for neighbor in test_tile.find_neighbors():
                add_score = score_cell(neighbor, cell_score)
                score += add_score
                print("adding score: ", add_score, neighbor)
            end_of_round = True
    '''

# classes
class Trigger_Tiles:
    def __init__(self, tile_type, tile_index, tile_number, cur_x, cur_y):
        self.tile_type = tile_type
        self.tile_index = tile_index
        self.tile_number = tile_number
        self.cur_x = cur_x
        self.cur_y = cur_y

    def find_neighbors(self):
        row_num = len(self.tile_index)
        col_num = len(self.tile_index[0])

        left = (self.cur_x - 1) % col_num
        right = (self.cur_x + 1) % col_num

        above = (self.cur_y - 1) % row_num
        below = (self.cur_y + 1) % row_num

        neighbors = [
                                              self.tile_index[above][self.cur_x],                     
            self.tile_index[self.cur_y][left],                                  self.tile_index[self.cur_y][right],
                                              self.tile_index[below][self.cur_x]                     
        ]
        neighbor_locations = []
        for neighbor in neighbors:
            neighbor_locations.append(find_cell(neighbor, 0, False))

        return neighbor_locations

    


# ----- global variables -----
num_rows = int(input("number of rows: >>\t"))
# num_rows = 5 #num rows can be increased to extend board downward num cols can not, things break
num_cols = 5

charges = 150
bingo_discard = []
round_generations = 5

alive = "x"
dead = "."

game_end = False
show_shop = False

score = 0

# ----- main code -----
grid = create_grid(num_rows, num_cols)
cell_letter, cell_number, cell_score, cell_addons, cell_type, bingo_deck, cell_index = create_cells(num_rows, num_cols)

#for generation in range(0, 5):
while not game_end:
        # input
    
    user_input = game_interaction(score)

        # update

    if charges <= 1:
        game_end = True
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

    new_score, new_charges = play_out_round(user_input, cell_number, cell_score, cell_type, cell_index, score, charges)
    score = new_score
    charges = new_charges

        # output
    #print("charges: ", charges)
    display_board(cell_letter, cell_number, cell_score, cell_index)
    #print("deck ", bingo_deck, "discard ", bingo_discard)
    print("score ", score)
    print()

    time.sleep(0)

print(f"Game over! Your final score was: {score}")

'''
game stuff to remember

game loop:
    input
    update
    output

bingo numbers will be drawn until empty, then will be reshuffled
bingo balls only have numbers, not letters, tile letters are used for tile abilities to combo
tiles can be activated, triggered, or scored: 
    activated means the tile gives score and uses its effect
    triggered means the tile only uses its effect
    scored means the tile only gives score

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

to add a pre game settings menu make a separate file that writes to the file that main reads from
'''