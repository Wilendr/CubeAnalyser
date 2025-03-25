import os
from card_utilities import *

def make_cube_list(infile, magic_cards, update = False):
    '''Parses the cube list file and writes any missing cards to misspellings.txt'''
    
    with open('program/misspellings.txt', 'w') as misspellings:
        if not update and os.path.exists('magic_cards.json'):
            misspellings.write("The following cards in the cube list are not found in magic_cards.json:\n")
        else:
            misspellings.write("The following cards in the cube list are not found in Scryfall's database::\n")
        
        with open(infile) as cube_file:
            cube_list = [line.strip() for line in cube_file]
            
            for card in cube_list:
                if card not in magic_cards:
                    misspellings.write(f"{card} in file {infile}\n")
    
    return cube_list


def get_colors(maindeck, magic_cards):
    deck_colors = {'White': 0, 'Blue': 0, 'Black': 0, 'Red': 0, 'Green': 0}
    splash_colors = {'white': 0, 'Blue': 0, 'Black': 0, 'Red': 0, 'Green': 0}
    
    for card in maindeck:
        if find_card_type(magic_cards[card]['type']) != 'Land':
            card_color = magic_cards[card]['color']
            if 'W' in card_color:
                deck_colors['White'] += 1
            if 'U' in card_color:
                deck_colors['Blue'] += 1
            if 'B' in card_color:
                deck_colors['Black'] += 1
            if 'R' in card_color:
                deck_colors['Red'] += 1
            if 'G' in card_color:
                deck_colors['Green'] += 1

    num_nonlands = len([card for card in maindeck if find_card_type(magic_cards[card]['type']) != 'Land'])
    #temp_color_dict = color_dict.copy()
    for color in deck_colors.keys():
        if deck_colors[color]/num_nonlands < 0.15 and deck_colors[color] != 0:
            splash_colors[color] = deck_colors[color]
            deck_colors[color] = 0

    return deck_colors, splash_colors


def make_deck(infile, magic_cards):

    '''Given a deck text file, analyze its contents. Outputs the main/sideboard rate of cards, the win/loss, deck colors, archetypes'''

    maindeck, side = [], []

    with open(infile) as deck_file:

        # extract deck "meta-data" - the colors, archetypes, and game records. Does not currently do anything with match records
        summary = [line.strip('\n') for line in deck_file.readlines()]
        player = summary[0].split(':')[1].strip(' ').split('_')
        deck_archetypes = summary[1].split(':')[1].strip(' ').split('_')
        deck_record = list(map(float,summary[3].split(':')[1].strip(' ').split('-')))

        # extract the cards in the decklist - will extract sideboard as well.
        cards = []
        for card_info in summary[5:]:
            card_info = card_info.strip('\n')
            if card_info == '':
                cards.extend([card_info])
                continue
            else:
                num, card = card_info.split(' ')[0],' '.join(card_info.split(' ')[1:])
                cards.extend([card]*int(num))

        try:
            div = cards.index('')
            maindeck, side = cards[:div], cards[div+1:]
        except:
            maindeck = cards
            side = []
        win, loss = deck_record

        deck_color, splash_color = get_colors(maindeck, magic_cards)
        #splash_color = []

    return maindeck, side, player, deck_color, splash_color, deck_archetypes, win, loss


def extract_decklists(directory, magic_cards, cube_list, date_arg, update = False):

    '''Parses all the decklists in a directory and creates a dictionary to contain this info.'''
    if cube_list:
        misspellings = open('program/misspellings.txt', 'a')
        if not update and os.path.exists('magic_cards.json'):
            misspellings.write("\nThe following cards in deck lists are not found in magic_cards.json:\n")
        else:
            misspellings.write("\nThe following cards in deck lists are not found in Scryfall's database:\n")
    else:
        misspellings = open('program/misspellings.txt', 'w')
        if not update and os.path.exists('magic_cards.json'):
            misspellings.write("The following cards in deck lists are not found in magic_cards.json:\n")
        else:
            misspellings.write("The following cards in deck lists are not found in Scryfall's database:\n")
            
    deck_dict = {}

    # extract and make the decklist for every deck file in the input directory
    for i, infile in enumerate(os.listdir(directory)):

        if infile[-4:] != '.txt': continue # added to avoid '.DS_store', etc

        # attempt to analyze decklist. If unable, skip it. Will extract date if it exists.
        try:
            maindeck, side, player, deck_color, splash_color, archetypes, win, loss = make_deck(os.path.join(directory,infile), magic_cards)
            
            if date_arg:
                date = infile.split('_')[-1][:-4]
        except:
            print('File {} could not be analyzed.'.format(infile))
            continue

        for card in maindeck + side: 
            if not magic_cards.get(card): 
                misspellings.write('{} in file {}\n'.format(card, infile))

        deck_dict[i] = {'main': maindeck, 'side': side, 'player': player, 'color': deck_color, 'splash': splash_color, 'archetypes': archetypes, 'record':[win, loss]}
        if date_arg: deck_dict[i]['date'] = date

    return deck_dict