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
            new_z = []
            for x in range(0, 3):
                new_z.append("nor")
            new_row.append(new_z)
        addons.append(new_row)

    for y in range(0, rows):
        for x in range(0, cols):
            addons[y][x][0] = "nor"

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

# gets user input and sanitizes it
def game_interaction(game_score, input_type, price_coe, base_charges, current_charges):
    good_input = False
    global score

    while not good_input:
        # sanitization for beginning of round
        if input_type == "begin":
            user = input("ro for roll | re to refresh deck | sh to open shop | he for item help | ve to view addons\n >>\t").lower()
            if not user == "ro" and not user == "re" and not user == "sh" and not user == "he" and not user == "ve":
                print("Not a valid input, use one of the options.")
            elif user == "re" and game_score < 100:
                print("You need at least 100 score to refresh.")
            elif user == "sh" and base_charges - current_charges < 20:
                print(f"You need to have roll {20 - (base_charges - current_charges)} more times before you can open the shop.")
            else:
                good_input = True

        # sanitization for interacting with the shop
        elif input_type == "shop":
            # using base_charges as available refreshes current_charges as shop level
            user = input(f"b to buy an item | r to refresh ({base_charges} available) | u to upgrade shop ({round((4600+400**(1+0.3*current_charges))+2500*current_charges)} score) currently level {current_charges} | e to exit shop\n >>\t").lower()

            if len(user) != 1 or user not in "brue":
                print("Not a valid input, use one of the options.")
            elif user == "r" and base_charges < 1:
                print("You do not have any available refreshes")
            elif user == "u" and (game_score < round((4600+400**(1+0.3*current_charges))+2500*current_charges)):
                print(f"You do not have enough score, you need {round((4600+400**(1+0.3*current_charges))+2500*current_charges)}, and you have {game_score}")
            else:
                good_input = True

        # sanitization for first phase of buying
        elif input_type == "buy1":
            user = input("1 for upgrades | 2 for addons | 3 for tiles\n >>\t")

            if len(str(user)) != 1 or str(user) not in "123":
                print("Not a valid input, use one of the options.")
            else:
                user = int(user)
                good_input = True

        # sanitization for second phase of buying (if buying upgrades)
        elif input_type == "buy2a":
            user = input("input the number of the item you want to purchace, or 0 to exit.\n >>\t")

            if user not in "1234567890":
                print("Not a valid input, enter the number corresponding to the item")
            elif len(str(user)) != 1 or int(user) > len(available_upgrades):
                print("Not a valid input, enter the number corresponding to the item")
            elif user == 0:
                good_input = True
            elif (available_upgrades[int(user)-1][1]) > game_score:
                print(f"You don't have enough money to purchace this item, you need {available_upgrades[int(user)-1][1]}, you have {game_score}.")
            else:
                user = int(user)
                good_input = True
                score = score - (available_upgrades[user-1][1])
                
        # sanitization for second phase of buying (if buying addons)
        elif input_type == "buy2b":
            user = input("input the number of the item you want to purchace, or 0 to exit.\n >>\t")

            if user not in "1234567890":
                print("Not a valid input, enter the number corresponding to the item")
            elif len(str(user)) != 1 or int(user) > len(available_addons):
                print("Not a valid input, enter the number corresponding to the item")
            elif user == 0:
                good_input = True
            elif (available_addons[int(user)-1][1]) > game_score:
                print(f"You don't have enough money to purchace this item, you need {available_addons[int(user)-1][1]}, you have {game_score}.")
            else:
                user = int(user)
                good_input = True
                score = score - (available_addons[user-1][1])

        # sanitization for second phase of buying (if buying tiles)
        elif input_type == "buy2c":
            user = input("input the number of the item you want to purchace, or 0 to exit.\n >>\t")

            if user not in "1234567890":
                print("Not a valid input, enter the number corresponding to the item")
            elif len(user) != 1 or int(user) > len(available_tiles):
                print("Not a valid input, enter the number corresponding to the item")
            elif user == "0":
                good_input = True
            elif (available_tiles[int(user)-1][1]) > game_score:
                print(f"You don't have enough money to purchace this item, you need {available_tiles[int(user)-1][1]}, you have {game_score}.")
            else:
                user = int(user)
                good_input = True
                score = score - (available_tiles[user-1][1])

        # sanitization for adding a new tile/ball to the board (index)
        elif input_type == "tile":
            user = input("enter the index of the item you want to replace\n >>\t")

            bad_letter = 0
            for letter in user:
                if letter not in "1234567890":
                    bad_letter += 1

            print("bad letter", bad_letter)
            cell_index_len = 0
            for row in cell_index:
                for col in row:
                    cell_index_len += 1

            if bad_letter == 0:    
                if int(user) > cell_index_len:
                    print("len cell index", cell_index_len)
                    print("Not a valid input")
                elif bad_letter == 0:
                    user = int(user)
                    good_input = True
            else:
                print("Not a valid input.")

        # sanitization for adding a new addon to the board (index)
        elif input_type == "addon":
            user = input("enter the index of the item you want to replace or 99 to exit\n >>\t")

            if user == 99:
                good_input = True
                return user

            bad_letter = 0
            for letter in user:
                if letter not in "1234567890":
                    bad_letter += 1
            
            temp_tile = find_cell(int(user), None, False)
            slots = 0
            for tile in cell_addons[temp_tile[0]][temp_tile[1]]:
                if tile == "nor":
                    slots += 1
            
            if slots <= 0:
                print("This tile has the maximum number of addons")
            elif bad_letter == 0:
                user = int(user)
                good_input = True
            else:
                print("Not a valid input.")

        # sanitization for finding a tile
        elif input_type == "findaddon":
            user = input("ender the index of the tile you want to view\n >>\t")
            
            bad_letter = 0
            for letter in user:
                if letter not in "1234567890":
                    bad_letter += 1

            if bad_letter == 0:
                user = int(user)
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
def score_cell(cell_xy, tile_scores):
    # keeping the really inefficient code I used before, iterated through the rows and cols of tile scores and if the index of the scored cell's coordinates matched, added the score from tile score
    '''
    score = 0
    cell_x = 0
    cell_y = 0
    cell_x = cell_xy[0]
    cell_y = cell_xy[1]
    index_y = 0
    index_x = 0
    for row in tile_scores:
        if index_y == cell_y:
            for tile_score in row:    
                if index_x == cell_x:
                    score += tile_score
                index_x += 1
        index_y += 1'''

    score = tile_scores[cell_xy[1]][cell_xy[0]]
    return score

# tells the user about every item in the game
def item_help():
    print("\nItem Help tells you the exact effects of each item in the game!")

    print("\nDeck Upgrades:")
    print("\tnor type upgrades: The default upgrade type, has no effect\n")
    print("\tcrg type upgrades: Doesn't consume charges when rolled\n")
    print("\tadc type upgrades: Adds a certain amount of charges based on random chance:\n\t\t60% to do nothing\n\t\t17.5% to add 1\n\t\t12.5% to add 2\n\t\t5% to add 4\n\t\t4.5% to add 10\n\t\t0.5% to add 25\n")
    print("\trnd type upgrades: Triggers two additional tiles\n")
    print("\ttrg type upgrades: 25% chance to trigger 10 additional tiles\n")
    print("\trsc type upgrades: Adds temporary 20% to the round score\n")
    print("\tpml type upgrades: 35% chance to add a permanent 12% multiplier to all tiles\n")
    print("\taat type upgrades: 5% chance to additionally trigger all tiles\n")

    print("\nAddon Types:")
    print("\tmul type addons: Adds a 1.2x multiplier to the tile\n")
    print("\txmp type addons: 25% chance to multiply the tile's mult by 2.5x\n")
    print("\tphl type addons: Adds 20% of this tile's mult to the round multiplier\n")
    print("\tscr type addons: Adds a random number between 50 and 100 to the tile's score each round\n")

    print("\nTile Types:")
    print("\tnor type tiles: The default tile type, has no effect\n")
    print("\ttgn type tiles: Triggers the 4 tiles that touch it\n")
    print("\tTile Subcategory: Jump In tiles:")
    print("\tJump In tiles are activated after a tile of a certain type is triggered")
    print("\t\ttbb type tiles: Triggered after a tile of the letter B is triggered")
    print("\t\ttbi type tiles: Triggered after a tile of the letter I is triggered")
    print("\t\ttbn type tiles: Triggered after a tile of the letter N is triggered")
    print("\t\ttbg type tiles: Triggered after a tile of the letter G is triggered")
    print("\t\ttbo type tiles: Triggered after a tile of the letter O is triggered")
    print("\t\ttbd type tiles: Triggered after a tile with an odd number is triggered")
    print("\t\ttbe type tiles: Triggered after a tile with an even number is triggered")
    print("\t\tjmp type tiles: A special Jump in tile, has a 10% chance to trigger after any tile is triggered\n")
    print("\tacb type tiles: Additionally triggers between 3 and 8 random unique tiles\n")
    
    print("\nSpecial Items:")
    print("\tSPECIAL ITEM: Global Multiplier 1.2x: Multiplies the global round multiplier by 1.2x\n")
    print("\tSPECIAL ITEM: Max Generations + 1: Increases the amount of generations in a round by 1\n")

    print("\nTips to Remember:")
    print("\tBuying a tile removes any permanent multipliers it may have, and reverts its associated ball back to a normal type\n")
    print("\tRefreshing your deck takes 10% of your current score, and needs at least 100 score to work\n")
    print("\tYou need to roll 20 times before you can open the shop\n")
    print("\tGlobal multiplier is increased every shop level: global mult = 1.25^shop_level\n")
    print("\tShop level 5 is the last level to upgrade the items, but levels past it will still increase the global multiplier\n")
    print("\tShop prices are increased each time you refresh and upgrade the shop\n")
    print()
    
# determines what items show up in the shop
def roll_shop(upgrades_list, addons_list, tiles_list, cost_coe):
    upgrades = []
    addons = []
    tiles = []
    letters = ['B', 'I', 'N', 'G', 'O']

    for item in range(1, 6):
        if item < 5:
        # creates a list for each item type of random items, and multiplies their prices by a random percent between -12.50% and +15.00%
            new_upgrade = []
            upgrade_index = random.randint(0, len(upgrades_list)-1)
            for upgrade in upgrades_list[upgrade_index]:
                new_upgrade.append(upgrade)
            new_upgrade[1] = round(math.floor((new_upgrade[1] * (random.randint(8750, 11500) / 10000)) * cost_coe))
            upgrades.append(new_upgrade)


            new_tile = []
            tile_index = random.randint(0, len(tiles_list)-1)
            for tile in tiles_list[tile_index]:
                new_tile.append(tile)
            new_tile[1] = round(math.floor((new_tile[1] * (random.randint(8750, 11500) / 10000)) * cost_coe))
            # gives the new tile a letter, score, and number
            new_tile.append(random.choice(letters))
            new_tile.append(random.randint(1,90))
            new_tile.append(random.randint(1,75))

            # nnb type tiles have a number that can't be rolled and a much higher number so they are generated separately
            if new_tile[0] == "nnb":
                new_tile[4] = random.randint(125, 550)
                new_tile[5] = -1

            tiles.append(new_tile)

        new_addon = []
        addon_index = random.randint(0, len(addons_list)-1)
        for addon in addons_list[addon_index]:
            new_addon.append(addon)
        new_addon[1] = round(math.floor(new_addon[1] * (random.randint(8750, 11500) / 10000)) * cost_coe)
        addons.append(new_addon)

    return upgrades, addons, tiles

# handles shop interactions
def open_shop(upgrades, addons, tiles):
    global refreshes_available, shop_level, score, refreshes_used, items_bought

    # the price coefficient is based increased by the shop level, amount of refreshes used, and amount of items bought
    price_coefficient = round(100*(0.3 ** -abs(((shop_level*0.75)+(refreshes_used*0.14))*(1+refreshes_used*0.002)+(items_bought*0.02))))/100
    print(shop_level, refreshes_used, items_bought)
    print(price_coefficient, "price coe")

    print("Deck Upgrades:")
    for index, upgrade in enumerate(upgrades):
        # calculating the chance of rolling the item relative to the total weight of all items
        weight = 0
        for number in possible_balls:
            weight += number[2]
        chance = (100*upgrade[2]) / weight
        print(f"\t Upgrade {index + 1}: {upgrade[0]} | price: {upgrade[1]} points | chance of dropping: {round(chance)}")

    print("Tile Addons:")
    for index, addon in enumerate(addons):
        weight = 0
        for number in possible_addons:
            weight += number[2]
        chance = (100*addon[2]) / weight
        print(f"\t Addon {index + 1}: {addon[0]} | price: {addon[1]} points | chance of dropping: {round(chance)}")
        
    print("New Tiles:")
    for index, tile in enumerate(tiles):
        weight = 0
        for number in possible_tiles:
            weight += number[2]
        chance = (100*tile[2]) / weight
        print(f"\t Tile {index + 1}: {tile[0]} | price: {tile[1]} points | chance of dropping: {round(chance)} | letter: {tile[3]} | score: {tile[4]} | number: {tile[5]}")
    user_input = game_interaction(score, "shop", None, refreshes_available, shop_level)

    buying = False

    if user_input == "e":
        return False
    elif user_input == "r":
        global available_upgrades, available_addons, available_tiles
        available_upgrades, available_addons, available_tiles = roll_shop(weighted_balls, weighted_addons, weighted_tiles, price_coefficient)
        refreshes_available -= 1
        refreshes_used += 1
    elif user_input == "b":
        new_y = game_interaction(None, "buy1", None, None, None)
        buying = True
    elif user_input == "u":
        score = score - round((4600+400**(1+0.3*shop_level))+2500*shop_level)
        shop_level += 1
        update_shop_level(shop_level)

    if buying:
        if int(new_y) == 1: # buying a ball
            new_x = game_interaction(score, "buy2a", price_coefficient, None, None)
            if int(new_x) == 0:
                return
            buy_ball(upgrades, new_x)
        elif int(new_y) == 2: # buying an addon
            new_x = game_interaction(score, "buy2b", price_coefficient, None, None)
            if int(new_x) == 0:
                return
            buy_addon(addons, new_x)
        elif int(new_y) == 3: # buying a tile
            new_x = game_interaction(score, "buy2c", price_coefficient, None, None)
            if int(new_x) == 0: # breaking from the function
                return
            buy_tile(tiles, new_x)
        
    return True

# prompts the user for what tile they want to buy, and replaces it
def buy_tile(shop_tiles, new_x):
    global items_bought

    user_input = game_interaction(None, "tile", None, None, None)

    old_tile = find_cell(user_input, 0, False)

    # replacing the data for the tile
    cell_type[old_tile[0]][old_tile[1]] = shop_tiles[new_x-1][0]
    cell_letter[old_tile[0]][old_tile[1]] = shop_tiles[new_x-1][3]
    cell_score[old_tile[0]][old_tile[1]] = shop_tiles[new_x-1][4]
    cell_number[old_tile[0]][old_tile[1]] = shop_tiles[new_x-1][5]

    # resetting the addons of the tile
    for row in cell_addons:
        for col in row:
            for addon in col:
                addon = "nor"

    # replacing the associated ball with a blank new one of the correct number
    all_deck = bingo_deck + bingo_discard
    for ball in all_deck:
        if ball[2] == user_input:
            ball[1] = "nor"
            if not shop_tiles[new_x-1][0] == "nnb": # nnb tiles do not have a number, so if one is bought, don't add a number to the reset ball
                ball[0] = shop_tiles[new_x-1][5]


    #removing the purchaced tile from the shop
    del shop_tiles[new_x-1]
    items_bought += 1

# prompts the user for what addon they want to buy, and replaces it
def buy_addon(shop_addons, new_x):
    global items_bought

    if not len(str(new_x)) == 3:
        if shop_addons[new_x-1][0] == "SPECIAL ITEM: Max Generations + 1":
            print("asdfasdasdfasdf")
            global allowed_generations
            allowed_generations += 1
            items_bought += 1
            return

    user_input = game_interaction(None, "addon", None, None, None)

    if user_input == 99:
        return

    old_tile = find_cell(user_input, 0, False)

    # checking how many slots have been already filled
    available_slots = 0
    for addon in cell_addons[old_tile[0]][old_tile[1]]:
        if addon == "nor":
            available_slots += 1

    if available_slots == 3:
        cell_addons[old_tile[0]][old_tile[1]][0] = shop_addons[new_x-1][0]
    if available_slots == 2:
        cell_addons[old_tile[0]][old_tile[1]][1] = shop_addons[new_x-1][0]
    if available_slots == 1:
        cell_addons[old_tile[0]][old_tile[1]][2] = shop_addons[new_x-1][0]

    del shop_addons[new_x-1]
    items_bought += 1

# prompts the user for what ball they want to buy, and replaces it
def buy_ball(shop_upgrades, new_x):
    global items_bought

    if not len(str(new_x)) == 3:
        if shop_upgrades[new_x-1][0] == "SPECIAL ITEM: Global Multiplier 1.2x":
            global mult_increaser
            mult_increaser += 1
            items_bought += 1
            return

    user_input = game_interaction(None, "tile", None, None, None)

    all_deck = bingo_deck + bingo_discard
    for ball in all_deck:
        if ball[2] == user_input:
            ball[1] = shop_upgrades[new_x-1][0]

    del shop_upgrades[new_x-1]
    items_bought += 1

# shows the addons for a specific tile
def find_addons():
    user_input = game_interaction(None, "findaddon", None, None, None)

    tile = find_cell(user_input, None, False)
    print(f"Tile {user_input}'s addons: {cell_addons[tile[0]][tile[1]]}")

# handles everything in a roll
def play_out_round(user, tile_number, tile_score, tile_type, tile_index, tile_mult, tile_letter, tile_addons, round_mult, game_generations):
    end_of_round = True
    round_roll = None
    tiles_to_score = []
    roll_type = None
    global score, charges, cell_mult, rolls_counter
    rolling = False
    add_extra_tiles = False

    # at beginning of round, determines user input
    if end_of_round:
        if user.lower() == "ro":
            round_roll, roll_type = game_roll()
            print("Rolled: ", round_roll, "| Roll type: ", roll_type) 
            charges -= 1
            rolling = True
            rolls_counter += 1
        elif user.lower() == "re":
            deck_reroll()
            score -= round(score*0.1)
        elif user.lower() == "sh":
            show_shop = True
            while show_shop == True:
                show_shop = open_shop(available_upgrades, available_addons, available_tiles)
        elif user.lower() == "he":
            item_help()
        elif user.lower() == "ve":
            find_addons()

    end_of_round = False
        
    if rolling:
        # handles the roll's effect
        round_ball = Call_Balls()
        if roll_type == "crg": # doesn't consume charges
            round_ball.add_charge(1)
        if roll_type == "adc": # randomly adds charges
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
        if roll_type == "rnd": # activates 1 random other number
            extra_tiles = []
            for i in range(0,2):
                rnd_tile = random.randint(0,24)
                extra_tiles.append(find_cell(rnd_tile, None, False))
            add_extra_tiles = True
        if roll_type == "trg": # chance to trigger 10 random unique tiles
            chance = random.randint(0,100)
            if chance >= 75:
                extra_tiles = []
                while len(extra_tiles) < 10:
                    rnd_tile = random.randint(0,24)
                    if not find_cell(rnd_tile, None, False) in extra_tiles:
                        extra_tiles.append(find_cell(rnd_tile, None, False))
                add_extra_tiles = True
        if roll_type == "rsc": # multiplies the round score by 1.35
            round_mult = round(100 * (round_mult * 1.35)) / 100
        if roll_type == "pml": # chance to add a permanent mult to all tiles
            global cell_mult
            chance = random.randint(0,100)
            if chance >= 65:
                for row in range(0, num_rows):
                    for col in range(0, num_cols):
                        cell_mult[row][col] = round(1000*(cell_mult[row][col] + 0.12))/1000
        if roll_type == "aat": # very small chance to additionally activate all tiles
            chance = random.randint(0,100)
            if chance > 95:
                extra_tiles = []
                for row in tile_index:
                    for index in row:
                        extra_tiles.append(find_cell(index, None, False))
                add_extra_tiles = True

        
        # finds all tiles that need to be scored
        tiles_to_score = find_cell(tile_number, round_roll, True)
        if add_extra_tiles: tiles_to_score = tiles_to_score + extra_tiles

        # resetting these variables for possible later reuse
        extra_tiles = []
        add_extra_tiles = False
        
        # creates copy
        tts_copy = copy.deepcopy(tiles_to_score)


        while game_generations > 0:
            # adds tiles that are activated by the triggering of another tile
            jump_in_tiles = []
            for tile in tiles_to_score:
                if tile_letter[tile[1]][tile[0]] == "B":
                    for index_row, row in enumerate(tile_type):
                        for index_col, type in enumerate(row):
                            if type == "tbb":
                                new_tile = []
                                new_tile.append(index_row)
                                new_tile.append(index_col)
                                jump_in_tiles.append(new_tile)
                                 
                if tile_letter[tile[1]][tile[0]] == "I":
                    for index_row, row in enumerate(tile_type):
                        for index_col, type in enumerate(row):
                            if type == "tbi":
                                new_tile = []
                                new_tile.append(index_row)
                                new_tile.append(index_col)
                                jump_in_tiles.append(new_tile)
                                 
                if tile_letter[tile[1]][tile[0]] == "N":
                    for index_row, row in enumerate(tile_type):
                        for index_col, type in enumerate(row):
                            if type == "tbn":
                                new_tile = []
                                new_tile.append(index_row)
                                new_tile.append(index_col)
                                jump_in_tiles.append(new_tile)
                                 
                if tile_letter[tile[1]][tile[0]] == "G":
                    for index_row, row in enumerate(tile_type):
                        for index_col, type in enumerate(row):
                            if type == "tbg":
                                new_tile = []
                                new_tile.append(index_row)
                                new_tile.append(index_col)
                                jump_in_tiles.append(new_tile)
                                 
                if tile_letter[tile[1]][tile[0]] == "O":
                    for index_row, row in enumerate(tile_type):
                        for index_col, type in enumerate(row):
                            if type == "tbo":
                                new_tile = []
                                new_tile.append(index_row)
                                new_tile.append(index_col)
                                jump_in_tiles.append(new_tile)
                                 
                if not tile_number[tile[1]][tile[0]] % 2 == 0:
                    for index_row, row in enumerate(tile_type):
                        for index_col, type in enumerate(row):
                            if type == "tbd":
                                new_tile = []
                                new_tile.append(index_row)
                                new_tile.append(index_col)
                                jump_in_tiles.append(new_tile)
                                 
                if tile_number[tile[1]][tile[0]] % 2 == 0:
                    for index_row, row in enumerate(tile_type):
                        for index_col, type in enumerate(row):
                            if type == "tbe":
                                new_tile = []
                                new_tile.append(index_row)
                                new_tile.append(index_col)
                                jump_in_tiles.append(new_tile)
                                 
                add_jmp = random.randint(0, 10)
                if add_jmp >= 10:
                    for index_row, row in enumerate(tile_type):
                        for index_col, type in enumerate(row):
                            if type == "jmp":
                                new_tile = []
                                new_tile.append(index_row)
                                new_tile.append(index_col)
                                jump_in_tiles.append(new_tile)

            for tile_being_scored in tiles_to_score:

                # handling addon effects
                xml_chance = random.randint(0, 4)
                additive_score = random.randint(50,100)
                for addon in tile_addons[tile_being_scored[1]][tile_being_scored[0]]:
                    if addon == "mul":
                        tile_mult[tile_being_scored[1]][tile_being_scored[0]] += 0.2
                    
                    if addon == "xml":
                        if xml_chance == 5:
                            tile_mult[tile_being_scored[1]][tile_being_scored[0]] = tile_mult[tile_being_scored[1]][tile_being_scored[0]] * 2.5

                    if addon == "phl":
                        round_mult += (tile_mult[tile_being_scored[1]][tile_being_scored[0]] / 5)

                    if addon == "scr":
                        tile_score[tile_being_scored[1]][tile_being_scored[0]] += additive_score

                    
                
                # creates a tile from the Trigger Tiles class each loop
                game_tile = Trigger_Tiles(tile_type, tile_index, tile_number, tile_mult, tile_being_scored[1], tile_being_scored[0])
                print(f"tile being scored, number {tile_number[tile_being_scored[1]][tile_being_scored[0]]} | score {tile_score[tile_being_scored[1]][tile_being_scored[0]]} | tile type {tile_type[tile_being_scored[1]][tile_being_scored[0]]} | index {tile_index[tile_being_scored[1]][tile_being_scored[0]]} | mult {tile_mult[tile_being_scored[1]][tile_being_scored[0]]}")
                print(f"round mult {round_mult}")

                # for effectless tile types, scores the cell, adds the score, and removes it from the list of cells to score
                if (
                    tile_type[tile_being_scored[1]][tile_being_scored[0]] == "nor" or
                    tile_type[tile_being_scored[1]][tile_being_scored[0]] == "tbb" or
                    tile_type[tile_being_scored[1]][tile_being_scored[0]] == "tbi" or
                    tile_type[tile_being_scored[1]][tile_being_scored[0]] == "tbn" or
                    tile_type[tile_being_scored[1]][tile_being_scored[0]] == "tbg" or
                    tile_type[tile_being_scored[1]][tile_being_scored[0]] == "tbo" or
                    tile_type[tile_being_scored[1]][tile_being_scored[0]] == "tbe" or
                    tile_type[tile_being_scored[1]][tile_being_scored[0]] == "tbd" or
                    tile_type[tile_being_scored[1]][tile_being_scored[0]] == "jmp" or
                    tile_type[tile_being_scored[1]][tile_being_scored[0]] == "nnb"
                    ):
                    add_score = score_cell(tile_being_scored, tile_score)
                    score += round(add_score * tile_mult[tile_being_scored[1]][tile_being_scored[0]] * round_mult)
                    print("adding score:", round(add_score * tile_mult[tile_being_scored[1]][tile_being_scored[0]] * round_mult))
                    tts_copy.remove(tts_copy[0])

                # for trigger neighbors tile type, scores the cell, and adds all neighbors to tiles to score array
                if tile_type[tile_being_scored[1]][tile_being_scored[0]] == "tgn":
                    add_score = score_cell(tile_being_scored, tile_score)
                    score += round(add_score * tile_mult[tile_being_scored[1]][tile_being_scored[0]] * round_mult)
                    print("adding score:", round(add_score * tile_mult[tile_being_scored[1]][tile_being_scored[0]] * round_mult))
                    tts_copy.remove(tts_copy[0])

                    for neighbor in game_tile.find_neighbors():
                        tts_copy.append(neighbor)

                # adds a random number of tiles between 3 and 8
                if tile_type[tile_being_scored[1]][tile_being_scored[0]] == "acb":
                    add_score = score_cell(tile_being_scored, tile_score)
                    score += round(add_score * tile_mult[tile_being_scored[1]][tile_being_scored[0]] * round_mult)
                    print("adding score:", round(add_score * tile_mult[tile_being_scored[1]][tile_being_scored[0]] * round_mult))
                    tts_copy.remove(tts_copy[0])

                    num_to_add = random.randint(3, 8)
                    while len(extra_tiles) < num_to_add:
                        new_tile = game_tile.get_random_tile()
                        print(new_tile, tile_being_scored)
                        if not new_tile in extra_tiles and not new_tile == tile_being_scored:
                            extra_tiles.append(new_tile)

                # 85% chance to score normally, 15% chance to have 20x score
                if tile_type[tile_being_scored[1]][tile_being_scored[0]] == "gmb":
                    chance = random.randint(0,100)

                    if chance >= 85:
                        add_score = score_cell(tile_being_scored, tile_score)
                        score += round(add_score * tile_mult[tile_being_scored[1]][tile_being_scored[0]] * round_mult) * 20
                        print("adding score:", round(add_score * tile_mult[tile_being_scored[1]][tile_being_scored[0]] * round_mult) * 20)
                        tts_copy.remove(tts_copy[0])
                    else:
                        add_score = score_cell(tile_being_scored, tile_score)
                        score += round(add_score * tile_mult[tile_being_scored[1]][tile_being_scored[0]] * round_mult)
                        print("adding score:", round(add_score * tile_mult[tile_being_scored[1]][tile_being_scored[0]] * round_mult))
                        tts_copy.remove(tts_copy[0])

                # multiplies the tile's multiplier by 1.15x when scored
                if tile_type[tile_being_scored[1]][tile_being_scored[0]] == "prm":
                    cell_mult[tile_being_scored[1]][tile_being_scored[0]] += round(1000*(cell_mult[tile_being_scored[1]][tile_being_scored[0]] * 0.15))/1000

                    add_score = score_cell(tile_being_scored, tile_score)
                    score += round(add_score * tile_mult[tile_being_scored[1]][tile_being_scored[0]] * round_mult)
                    print("adding score:", round(add_score * tile_mult[tile_being_scored[1]][tile_being_scored[0]] * round_mult))
                    tts_copy.remove(tts_copy[0])


                # undoes tile addon effects
                for addon in tile_addons[tile_being_scored[1]][tile_being_scored[0]]:
                    if addon == "mul":
                        tile_mult[tile_being_scored[1]][tile_being_scored[0]] -= 0.2

                    if addon == "xml":
                        if xml_chance == 5:
                            tile_mult[tile_being_scored[1]][tile_being_scored[0]] = tile_mult[tile_being_scored[1]][tile_being_scored[0]] / 2.5

                    if addon == "phl":
                        round_mult -= (tile_mult[tile_being_scored[1]][tile_being_scored[0]] / 5)

                    if addon == "scr":
                        tile_score[tile_being_scored[1]][tile_being_scored[0]] -= additive_score

            print("generation", game_generations)
                
            # converts the main array into the copy (changing an array while iterating though it causes problems, using a copy is a workaround)
            for tile in jump_in_tiles:
                tts_copy.append(tile)
                pass
            if not len(extra_tiles) == 0:
                for tile in extra_tiles:
                    tts_copy.append(tile)
            del extra_tiles[:]
            tiles_to_score = copy.deepcopy(tts_copy)

            game_generations -= 1
            #stops the round if theres nothing left to do
            if len(tiles_to_score) < 1:
                game_generations = 0

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

# changes the items that can show up in the shop depending on the shop level
def update_shop_level(shop_level):
    global possible_balls, possible_addons, possible_tiles

    # update shop items depending on shop level
    if shop_level == 0:
        del possible_balls[:]
        del possible_addons[:]
        del possible_tiles[:]
        possible_balls = [["nor", 1000, 30], ["crg", 2100, 9], ["rnd", 1850, 11], ["rsc", 3750, 4]]
        possible_addons = [["scr", 1200, 15]]
        possible_tiles = [["nor", 400, 30], ["acb", 1125, 8], ["gmb", 1350, 4], ["prm", 1500, 2]]
    elif shop_level == 1:
        del possible_balls[:]
        del possible_addons[:]
        del possible_tiles[:]
        possible_balls = [["SPECIAL ITEM: Global Multiplier 1.2x", 6000, 2], ["nor", 1000, 25], ["crg", 2100, 10], ["rnd", 1850, 12], ["rsc", 3750, 5], ["pml", 5000, 3]]
        possible_addons = [["mul", 1650, 5], ["scr", 1200, 15]]
        possible_tiles = [["nor", 400, 26], ["tbb", 750, 2], ["tbi", 750, 2], ["tbn", 750, 2], ["tbg", 750, 2], ["tbo", 750, 2], ["tbd", 750, 2], ["tbe", 750, 2], ["acb", 1125, 9], ["gmb", 1350, 3], ["prm", 1500, 2]]
    elif shop_level == 2:
        del possible_balls[:]
        del possible_addons[:]
        del possible_tiles[:]
        possible_balls = [["SPECIAL ITEM: Global Multiplier 1.2x", 6000, 2], ["nor", 1000, 38], ["crg", 2100, 11], ["adc", 2750, 7], ["rnd", 1850, 12], ["rsc", 3750, 6], ["pml", 5000, 3]]
        possible_addons = [["SPECIAL ITEM: Max Generations + 1", 5550, 1], ["mul", 1650, 18], ["xml", 1900, 12], ["phl", 2250, 3], ["scr", 1200, 42]]
        possible_tiles = [["nor", 400, 26], ["tgn", 1050, 10], ["tbb", 750, 2], ["tbi", 750, 2], ["tbn", 750, 2], ["tbg", 750, 2], ["tbo", 750, 2], ["tbd", 750, 2], ["tbe", 750, 2], ["jmp", 850, 3], ["acb", 1125, 11], ["gmb", 1350, 3], ["prm", 1500, 3]]
    elif shop_level == 3:
        del possible_balls[:]
        del possible_addons[:]
        del possible_tiles[:]
        possible_balls = [["SPECIAL ITEM: Global Multiplier 1.2x", 6000, 2], ["nor", 1000, 65], ["crg", 2100, 25], ["adc", 2750, 9], ["rnd", 1850, 36], ["trg", 5000, 5], ["rsc", 3750, 7], ["pml", 5000, 3], ["aat", 7000, 1]]
        possible_addons = [["SPECIAL ITEM: Max Generations + 1", 5550, 1], ["mul", 1650, 30], ["xml", 1900, 21], ["phl", 2250, 3], ["scr", 1200, 42]]
        possible_tiles = [["nor", 400, 20], ["tgn", 1050, 9], ["tbb", 750, 2], ["tbi", 750, 2], ["tbn", 750, 2], ["tbg", 750, 2], ["tbo", 750, 2], ["tbd", 750, 2], ["tbe", 750, 2], ["jmp", 850, 4], ["acb", 1125, 12], ["nnb", 1250, 7], ["gmb", 1350, 4], ["prm", 1500, 3]]
    elif shop_level == 4:
        del possible_balls[:]
        del possible_addons[:]
        del possible_tiles[:]
        possible_balls = [["SPECIAL ITEM: Global Multiplier 1.2x", 6000, 2], ["nor", 1000, 50], ["crg", 2100, 25], ["adc", 2750, 12], ["rnd", 1850, 40], ["trg", 5000, 8], ["rsc", 3750, 11], ["pml", 5000, 3], ["aat", 7000, 2]]
        possible_addons = [["SPECIAL ITEM: Max Generations + 1", 5550, 1], ["mul", 1650, 36], ["xml", 1900, 27], ["phl", 2250, 6], ["scr", 1200, 39]]
        possible_tiles = [["nor", 400, 18], ["tgn", 1050, 13], ["tbb", 750, 2], ["tbi", 750, 2], ["tbn", 750, 2], ["tbg", 750, 2], ["tbo", 750, 2], ["tbd", 750, 2], ["tbe", 750, 2], ["jmp", 850, 5], ["acb", 1125, 15], ["nnb", 1250, 10], ["gmb", 1350, 5], ["prm", 1500, 4]]
    elif shop_level == 5:
        del possible_balls[:]
        del possible_addons[:]
        del possible_tiles[:]
        possible_balls = [["SPECIAL ITEM: Global Multiplier 1.2x", 6000, 2], ["nor", 1000, 40], ["crg", 2100, 25], ["adc", 2750, 13], ["rnd", 1850, 32], ["trg", 5000, 10], ["rsc", 3750, 11], ["pml", 5000, 4], ["aat", 7000, 3]]
        possible_addons = [["SPECIAL ITEM: Max Generations + 1", 5550, 1], ["mul", 1650, 39], ["xml", 1900, 27], ["phl", 2250, 9], ["scr", 1200, 36]]
        possible_tiles = [["nor", 400, 17], ["tgn", 1050, 15], ["tbb", 750, 2], ["tbi", 750, 2], ["tbn", 750, 2], ["tbg", 750, 2], ["tbo", 750, 2], ["tbd", 750, 2], ["tbe", 750, 2], ["jmp", 850, 6], ["acb", 1125, 15], ["nnb", 1250, 10], ["gmb", 1350, 6], ["prm", 1500, 4]]

    # creating the weighted lists of items
    global weighted_balls, weighted_addons, weighted_tiles

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

# classes

# handles the longer code snippits for tiles
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
    
    def get_random_tile(self):
        rannum = random.randint(0, 24)
        return find_cell(rannum, None, False)

# handles the longer code snippits for tiles    
class Call_Balls:
    def __init__(self):
        pass

    def add_charge(self, num_to_add):
        global charges
        charges += num_to_add


# ----- global variables -----
num_rows = 5
num_cols = 5

starting_charges = 500
charges = copy.deepcopy(starting_charges)
bingo_discard = []
round_generations = 5
rolls_counter = 0
refreshes_available = 0
refreshes_used = 0
allowed_generations = 5
items_bought = 0
mult_increaser = 0

game_end = False

possible_balls = [["nor", 1000, 30], ["crg", 2100, 9], ["rnd", 1850, 11], ["rsc", 3750, 4]]
possible_addons = [["scr", 1200, 15]]
possible_tiles = [["nor", 400, 30], ["acb", 1125, 8], ["gmb", 1350, 4], ["prm", 1500, 2]]
shop_level = 0

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
global_multiplier = 1

# ----- main code -----
cell_letter, cell_number, cell_score, cell_addons, cell_type, bingo_deck, cell_index, cell_mult = create_cells(num_rows, num_cols)
available_upgrades, available_addons, available_tiles = roll_shop(weighted_balls, weighted_addons, weighted_tiles, 1)

#for generation in range(0, 5):
while not game_end:
        # input
    
    user_input = game_interaction(score, "begin", None, starting_charges, charges)

        # update

    if charges <= 1:
        game_end = True

    play_out_round(user_input, cell_number, cell_score, cell_type, cell_index, cell_mult, cell_letter, cell_addons, global_multiplier, allowed_generations)

    if rolls_counter >= 20:
        rolls_counter = 0
        refreshes_available += 1

    global_multiplier = (round(100 * (1.25 ** shop_level)) / 100) * (1 + (0.2 * mult_increaser))

    
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


shop levels:
level 0: 
    tiles:
        nor 30
        acb 8
        gmb 3
        prm 2
    addons:
        scr 1
    balls:
        nor 30
        crg 9
        rnd 11
        rsc 4

level 1:
    tiles:
        nor 26
        tbb 2 each
        acb 9
        gmb 3
        prm 2
    addons:
        mul 5
        scr 15
    balls:
        nor 25
        crg 10
        rnd 12
        rsc 5
        pml 3

level 2:
    tiles:
        nor 26
        tgn4 10
        tbb 2 each
        acb 11
        gmb 3
        jmp 3
        prm 3
    addons:
        mul 6
        xml 4
        phl 1
        scr 14
    balls:
        nor 38
        crg 11
        adc 7
        rnd 12
        rsc 6
        pml 3

level 3:
    tiles:
        nor 20
        tgn4 9
        tbb 2 each
        acb 12
        nnb 7
        gmb 4
        jmp 4
        prm 3
    addons:
        mul 10
        xml 7
        phl 1
        scr 15
    balls:
        nor 65
        crg 25
        adc 9
        rnd 36
        trg 5
        rsc 7
        pml 2
        aat 1

level 4:
    tiles:
        nor 18
        tgn4 13
        tbb 2 each
        acb 15
        nnb 10
        gmb 5
        jmp 5
        prm 4
    addons:
        mul 12
        xml 9
        phl 2
        scr 13
    balls:
        nor 50
        crg 25
        adc 12
        rnd 40
        trg 8
        rsc 11
        pml 3
        aat 2

level 5:
    tiles:
        nor 17
        tgn8 15
        tbb 2 each
        acb 15
        nnb 10
        gmb 6
        jmp 6
        prm 4
    addons:
        mul 13
        xml 9
        phl 3
        scr 12
    balls:
        nor 40
        crg 25
        adc 13
        rnd 34
        trg 10
        rsc 11
        pml 4
        aat 3



'''