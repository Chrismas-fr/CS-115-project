'''
Christopher Berkowitz
Python final project
Bingo roguelike game
4/20/26
'''

import copy
import time
import random
import math
import os

# functions

# UNUSED /!\ /!\ --- creates a grid of cells
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

# creates all the starting attributes for each tile, and the deck of numbers
def create_cells(rows, cols):
    letter = []
    number = []
    score = []
    addons = []
    tile_type = []
    bingo_numbers = []
    tile_index = []
    tile_multiplier = []

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
    score = copy.deepcopy(number)

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
    for index, num in enumerate(random_numbers):
        entry = []
        entry.append(num)
        entry.append("nor")
        entry.append(index)
        bingo_numbers.append(entry)
    random.shuffle(bingo_numbers)

    # a unique index for each tile for identification
    for y in range(0, rows):
        new_row = []
        for x in range(0, cols):
            new_row.append(x + (y * 5))
        tile_index.append(new_row)

    # multiplier for score added by a tile
    for y in range(0, rows):
        new_row = []
        for x in range(0, cols):
            new_row.append(1)
        tile_multiplier.append(new_row)


    return letter, number, score, addons, tile_type, bingo_numbers, tile_index, tile_multiplier

# displays each tile and its attributes
def display_board(letters, numbers, scores, tile_indexes, types):
    # outer loop iterates rows
    for row, row_num, row_score, row_index, row_type in zip(letters, numbers, scores, tile_indexes, types):
        # inner loop iterates columns
        for letter, number, score, tile_index, type in zip(row, row_num, row_score, row_index, row_type):
            print(f'[{letter} {number} {score} - {tile_index} {type}]', end=" ")
        print()

# UNUSED /!\ /!\ --- counts neighbors of a cell
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

# UNUSED /!\ /!\ --- does nothing
def update_cell(cell, num_neighbors):
    pass

# gets user input and sanitizes it
def game_interaction(game_score, input_type, price_coe):
    good_input = False
    global score

    while not good_input:
        # sanitization for beginning of round
        if input_type == "begin":
            user = input("ro for roll | re to refresh deck | sh to open shop\n >>\t").lower()

            if not user == "ro" and not user == "re" and not user == "sh":
                print("Not a valid input, use one of the options.")
            elif user == "re" and game_score < 100:
                print("You need at least 100 score to refresh.")
            else:
                good_input = True

        # sanitization for interacting with the shop
        elif input_type == "shop":
            user = input("b to buy an item | r to refresh | e to exit shop\n >>\t").lower()

            if len(user) != 1 or user not in "bre":
                print("Not a valid input, use one of the options.")
            else:
                good_input = True


        # sanitization for first phase of buying
        elif input_type == "buy1":
            user = int(input("1 for upgrades | 2 for addons | 3 for tiles\n >>\t"))

            if len(str(user)) != 1 or str(user) not in "123":
                print("Not a valid input, use one of the options.")
            else:
                good_input = True

        # sanitization for second phase of buying (if buying upgrades)
        elif input_type == "buy2a":
            user = int(input("input the number of the item you want to purchace, or 0 to exit.\n >>\t"))

            if len(str(user)) != 1 or user > len(available_upgrades):
                print("Not a valid input, enter the number corresponding to the item")
            elif user == 0:
                good_input = True
            elif (available_upgrades[user-1][1] * price_coe) > game_score:
                print(f"You don't have enough money to purchace this item, you need {available_upgrades[user-1][1] * price_coe}, you have {game_score}.")
            else:
                good_input = True
                score = score - (available_upgrades[user-1][1] * price_coe)
                
        # sanitization for second phase of buying (if buying addons)
        elif input_type == "buy2b":
            user = int(input("input the number of the item you want to purchace, or 0 to exit.\n >>\t"))

            if len(str(user)) != 1 or user > len(available_addons):
                print("Not a valid input, enter the number corresponding to the item")
            elif user == 0:
                good_input = True
            elif (available_addons[user-1][1] * price_coe) > game_score:
                print(f"You don't have enough money to purchace this item, you need {available_addons[user-1][1] * price_coe}, you have {game_score}.")
            else:
                good_input = True
                score = score - (available_addons[user-1][1] * price_coe)

        # sanitization for second phase of buying (if buying upgrades)
        elif input_type == "buy2c":
            user = int(input("input the number of the item you want to purchace, or 0 to exit.\n >>\t"))

            if len(str(user)) != 1 or user > len(available_tiles):
                print("Not a valid input, enter the number corresponding to the item")
            elif user == 0:
                good_input = True
            elif (available_tiles[user-1][1] * price_coe) > game_score:
                print(f"You don't have enough money to purchace this item, you need {available_tiles[user-1][1] * price_coe}, you have {game_score}.")
            else:
                good_input = True
                score = score - (available_tiles[user-1][1] * price_coe)

        # sanitization for adding a new tile to the board (index)
        elif input_type == "tile":
            user = int(input("enter the index of the tile you want to replace\n >>\t"))

            bad_letter = 0
            for letter in str(user):
                if letter not in "1234567890":
                    bad_letter += 1
            
            if bad_letter == 0:
                good_input = True
            else:
                print("Not a valid input.")

    return user

# rolls and rerolls the deck
def game_roll():
    roll = bingo_deck[0][0]
    ball_type = bingo_deck[0][1]
    # removes number from the deck and adds it to the discard only if there are still numbers in deck
    if not len(bingo_deck) <= 1:
        bingo_discard.append(bingo_deck[0])
        bingo_deck.remove(bingo_deck[0])
    else:
        #if not adds all numbers from discard into deck and shuffles
        deck_reroll()
    return roll, ball_type

# adding the draw and discard decks, then shuffles
def deck_reroll():
    bingo_deck.extend(bingo_discard)
    del bingo_discard[:]
    random.shuffle(bingo_deck)

# finds a cell based off of its number or index
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
                    cell_input.append(index_x)
                    cell_input.append(index_y)
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
    print("adding score:", score)
    return score

# determines what items show up in the shop
def roll_shop(upgrades_list, addons_list, tiles_list):
    upgrades = []
    addons = []
    tiles = []
    letters = ['B', 'I', 'N', 'G', 'O']

    for item in range(1, 6):
        if item < 5:
        # creates a list for each item type of random items, and multiplies their prices by a random percent between -12.50% and +12.50%
            new_upgrade = []
            upgrade_index = random.randint(0, len(upgrades_list)-1)
            for upgrade in upgrades_list[upgrade_index]:
                new_upgrade.append(upgrade)
            new_upgrade[1] = math.floor(new_upgrade[1] * (random.randint(8750, 11250) / 10000))
            upgrades.append(new_upgrade)


            new_tile = []
            tile_index = random.randint(0, len(tiles_list)-1)
            for tile in tiles_list[tile_index]:
                new_tile.append(tile)
            new_tile[1] = math.floor(new_tile[1] * (random.randint(8750, 11250) / 10000))
            # gives the new tile a letter, score, and number
            new_tile.append(random.choice(letters))
            new_tile.append(random.randint(1,90))
            new_tile.append(random.randint(1,75))

            tiles.append(new_tile)



        new_addon = []
        addon_index = random.randint(0, len(addons_list)-1)
        for addon in addons_list[addon_index]:
            new_addon.append(addon)
        new_addon[1] = math.floor(new_addon[1] * (random.randint(8750, 11250) / 10000))
        addons.append(new_addon)

    return upgrades, addons, tiles

# handles shop interactions
def open_shop(upgrades, addons, tiles):
    price_coefficient = 1

    print("Deck Upgrades:")
    for index, upgrade in enumerate(upgrades):
        weight = 0
        for number in possible_balls:
            weight += number[2]
        chance = (100*upgrade[2]) / weight
        print(f"\t Upgrade {index + 1}: {upgrade[0]} | price: {upgrade[1] * price_coefficient} points | chance of dropping: {round(chance)}")

    print("Tile Addons:")
    for index, addon in enumerate(addons):
        weight = 0
        for number in possible_addons:
            weight += number[2]
        chance = (100*addon[2]) / weight
        print(f"\t Addon {index + 1}: {addon[0]} | price: {addon[1] * price_coefficient} points | chance of dropping: {round(chance)}")
        
    print("New Tiles:")
    for index, tile in enumerate(tiles):
        weight = 0
        for number in possible_tiles:
            weight += number[2]
        chance = (100*tile[2]) / weight
        print(f"\t Tile {index + 1}: {tile[0]} | price: {tile[1]* price_coefficient} points | chance of dropping: {round(chance)} | letter: {tile[3]} | score: {tile[4]} | number: {tile[5]}")
    user_input = game_interaction(None, "shop", None)

    if user_input == "e":
        return False
    elif user_input == "r":
        global available_upgrades, available_addons, available_tiles
        available_upgrades, available_addons, available_tiles = roll_shop(weighted_balls, weighted_addons, weighted_tiles)
    elif user_input == "b":
        buy_tile(tiles, addons, upgrades, price_coefficient)

    
    
    return True

# prompts the user for what they buy, and replaces the item
def buy_tile(shop_tiles, shop_addons, shop_upgrades, price_coe):
    new_y = game_interaction(None, "buy1", None)
    global score

    if int(new_y) == 1:
        new_x = game_interaction(score, "buy2a", price_coe)
    elif int(new_y) == 2:
        new_x = game_interaction(score, "buy2b", price_coe)
    elif int(new_y) == 3:
        new_x = game_interaction(score, "buy2c", price_coe)
    
    # stops the function if user returned 0
    if int(new_x) == 0:
        return

    user_input = game_interaction(None, "tile", None)

    old_tile = find_cell(user_input, 0, False)
    #print(old_tile, "old tile")

    # replacing the data for the tilee
    global cell_type
    cell_type[old_tile[0]][old_tile[1]] = shop_tiles[new_x-1][0]
    cell_letter[old_tile[0]][old_tile[1]] = shop_tiles[new_x-1][3]
    cell_score[old_tile[0]][old_tile[1]] = shop_tiles[new_x-1][4]
    cell_number[old_tile[0]][old_tile[1]] = shop_tiles[new_x-1][5]

    # replacing the associated ball with a blank new one of the correct number
    all_deck = bingo_deck + bingo_discard
    print(all_deck)
    for tile in all_deck:
        print(tile[2], user_input)
        if tile[2] == user_input:
            print("TESTIGNG")
            tile[0] = shop_tiles[new_x-1][5]
            tile[1] = ""


    #removing the purchaced tile from the shop
    del shop_tiles[new_x-1]

    #print(shop_tiles[new_x-1][0], new_x, shop_tiles)

    #add pricing for shop items

# handles everything in a roll
def play_out_round(user, tile_number, tile_score, tile_type, tile_index, tile_mult):
    end_of_round = True
    game_generations = 5
    round_roll = None
    tiles_to_score = []
    roll_type = None
    global score
    global charges
    rolling = False
    add_extra_tiles = False


    # at beginning of round, determines user input
    if end_of_round:
        if user.lower() == "ro":
            round_roll, roll_type = game_roll()
            print("Rolled: ", round_roll, "| Type: ", roll_type) 
            charges -= 1
            rolling = True
        elif user.lower() == "re":
            deck_reroll()
            score -= round(score*0.1)
        elif user.lower() == "sh":
            show_shop = True
            while show_shop == True:
                show_shop = open_shop(available_upgrades, available_addons, available_tiles)
    end_of_round = False
        
    if rolling:
        # handles the roll's effect
        round_ball = Call_Balls()
        if roll_type == "crg":
            round_ball.add_charge(1)
        if roll_type == "adc":
            chance = random.randint(0,1000)
            if chance > 600 and chance <= 775:
                round_ball.add_charge(2)
            if chance > 775 and chance <= 900:
                round_ball.add_charge(3)
            if chance > 900 and chance <= 950:
                round_ball.add_charge(5)
            if chance > 950 and chance <= 995:
                round_ball.add_charge(11)
            if chance > 995:
                round_ball.add_charge(26)
        if roll_type == "rnd":
            rnd_tile = random.randint(0,24)
            extra_tiles = find_cell(rnd_tile, None, False)
            add_extra_tiles = True
        if roll_type == "trg":
            extra_tiles = []
            while len(extra_tiles) < 10:
                rnd_tile = random.randint(0,24)
                if not find_cell(rnd_tile, None, False) in extra_tiles:
                    extra_tiles.append(find_cell(rnd_tile, None, False))
            add_extra_tiles = True

        
        # finds all tiles that need to be scored
        tiles_to_score = find_cell(tile_number, round_roll, True)
        if add_extra_tiles: tiles_to_score = tiles_to_score + extra_tiles

        print(tiles_to_score, "tiles to score")
        # creates copy
        tts_copy = copy.deepcopy(tiles_to_score)

        while game_generations > 0:
            for tile_being_scored in tiles_to_score:
                #print(tile_being_scored)

                # i need to remove the tile being scored after it is scored, but removing it from tiles_to_score messes with with the amount of times the for loop runs.
                
                # creates a tile from the Trigger Tiles class each loop
                game_tile = Trigger_Tiles(tile_type, tile_index, tile_number, tile_mult, tile_being_scored[1], tile_being_scored[0])
                #print("neighbors ", game_tile.find_neighbors())
                print(f"tile being scored, number {tile_number[tile_being_scored[1]][tile_being_scored[0]]} | score {tile_score[tile_being_scored[1]][tile_being_scored[0]]} | type {tile_type[tile_being_scored[1]][tile_being_scored[0]]} | index {tile_index[tile_being_scored[1]][tile_being_scored[0]]}")
                
                # for basic tile type, scores the cell, adds the score, and removes it from the list of cells to score
                if tile_type[tile_being_scored[1]][tile_being_scored[0]] == "nor":
                    add_score = score_cell(tile_being_scored, tile_score)
                    score += add_score * tile_mult[tile_being_scored[1]][tile_being_scored[0]]
                    #print("adding score: ", add_score)
                    #print("tile type ", tile_type[tile_being_scored[1]][tile_being_scored[0]], "tile location ", tile_being_scored[0], tile_being_scored[1])
                    #print(" the current tile being scored ", tiles_to_score[0])
                    tts_copy.remove(tts_copy[0])
                    #print("rest of tiles to score", tiles_to_score)
                    #print(add_score)

                # for trigger neighbors tile type, scores the cell, and adds all neighbors to tiles to score array
                if tile_type[tile_being_scored[1]][tile_being_scored[0]] == "tgn":
                    add_score = score_cell(tile_being_scored, tile_score)
                    score += add_score * tile_mult[tile_being_scored[1]][tile_being_scored[0]]
                    #print("adding score: ", add_score)
                    tts_copy.remove(tts_copy[0])
                    #print("\t\t\t", tile_being_scored[1], tile_being_scored[0])

                    for neighbor in game_tile.find_neighbors():
                        tts_copy.append(neighbor)
                    #print("\tall the neighbors: ttscopy", tts_copy)
                    #print(tiles_to_score, "tiles to score")
                    #print(add_score, end=", ")
                
            # converts the main array into the copy (changing an array while iterating though it causes problems, using a copy is a workaround)
            tiles_to_score = copy.deepcopy(tts_copy)

            game_generations -= 1
            #print("end of gen\n\n\n")
            #stops the round if theres nothing left to do
            if len(tiles_to_score) < 1:
                game_generations = 0
            #print(game_generations, "generations")
            time.sleep(0.5)


        #create tile from class as first thing, create array of each tile effected by last round (first round just defaults to the numbers from ball) then run each tile separately from array and put each tile affected into the array and repeat until generations are used up
        #memorial of the awful code i was trying to use to run a round (rip)
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

# a class that gives different functions for different types of tiles
class Trigger_Tiles:
    def __init__(self, tile_type, tile_index, tile_number, tile_mult, cur_x, cur_y):
        self.tile_type = tile_type
        self.tile_index = tile_index
        self.tile_number = tile_number
        self.tile_mult = tile_mult
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
        
        # finds the coordinates of each neighbor from their index
        neighbor_locations = []
        for neighbor in neighbors:
            neighbor_locations.append(find_cell(neighbor, 0, False))

        return neighbor_locations

    
class Call_Balls:
    def __init__(self):
        pass

    def add_charge(self, num_to_add):
        global charges
        charges += num_to_add


# ----- global variables -----
#num_rows = int(input("number of rows: >>\t"))
num_rows = 5 #num rows can be increased to extend board downward num cols can not, things break
num_cols = 5

starting_charges = 100
charges = copy.deepcopy(starting_charges)
bingo_discard = []
round_generations = 5

alive = "x"
dead = "."

game_end = False
show_shop = False

possible_balls = [["nor", 1000, 65], ["crg", 2100, 25], ["adc", 2750, 9], ["trg", 5000, 5]]
possible_addons = [["nor", 500, 22]]
possible_tiles = [["nor", 400, 20], ["tgn", 750, 9]]

# creating the weighted lists of items
weighted_balls = []
weighted_addons = []
weighted_tiles = []

for ball in possible_balls:
    for index in range(0, ball[2]):
        weighted_balls.append(ball)

for addon in possible_addons:
    for index in range(0, addon[2]):
        weighted_addons.append(addon)

for tile in possible_tiles:
    for index in range(0, tile[2]):
        weighted_tiles.append(tile)
        
score = 0

# ----- main code -----
grid = create_grid(num_rows, num_cols)
cell_letter, cell_number, cell_score, cell_addons, cell_type, bingo_deck, cell_index, cell_mult = create_cells(num_rows, num_cols)
available_upgrades, available_addons, available_tiles = roll_shop(weighted_balls, weighted_addons, weighted_tiles)

#for generation in range(0, 5):
while not game_end:
        # input
    
    user_input = game_interaction(score, "begin", None)

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

    play_out_round(user_input, cell_number, cell_score, cell_type, cell_index, cell_mult)


        # output

    display_board(cell_letter, cell_number, cell_score, cell_index, cell_type)
    print("deck ", bingo_deck, "discard ", bingo_discard)
    print("score ", score)
    print("charges: ", charges)
    print()

        


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
    activated when another column activates: tbb, tbi, tbn, tbg, tbo
    activates 1-x tiles across board: acb
    large score but no number: nnb
    chance to give score when activated; large score: gmb
    50% chance to activate when any number rolled: jmp
    score multiplied x1.04 permanently: prm

addon types + code names: (additive means can be added to a tile multiple times)
    1.x extra score (additive): mul
    %chance to multiply score x times: xml
    gives all tiles 20% of this tiles mult for 2 rounds after activation: phl
    chance traits are 20x% more likely (additive): xch
    adds flat score to tile: scr

deck addons + code names:
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

tile weights:
    nor 20
    tgn 9
    tbb 2
    tbi 2
    tbn 2
    tbg 2
    tbo 2
    acb 12
    nnb 7
    gmb 4
    jmp 4
    prm 3

addon weights:
    nor 22
    mul 10
    xml 7
    phl 1
    xch 1
    scr 15

deck weights:
    nor 65
    crg 25
    adc 9
    rnd 36
    trg 5
    rsc 7
    pml 2
    aat 1

to add a pre game settings menu make a separate file that writes to the file that main reads from
'''