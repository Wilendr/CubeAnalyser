from collections import defaultdict
from card_utilities import *
import numpy as np
import pandas as pd

def export_card_analysis(deck_list_dict, cube_list, magic_cards, card_filter, archetype_dict, save_folder='results'):
    
    '''Analyzes card representation and win rates and exports them to csv. If the normalize argument is true, it normalizes 
    card win rates to the deck win rates.'''
    
    card_dict = defaultdict(lambda: {'win': 0, 'loss': 0, 'num': 0, 'archetypes': [], 'main %': []})

    # loop through dictionary, extract info on individual cards
    for deck_dict in deck_list_dict.values():

        # extract deck, get its record
        deck, side = deck_dict['main'], deck_dict['side']
        win, loss = map(int, deck_dict['record'])

        # get the deck archetype for normalization
        archetypes = deck_dict['archetypes']
        if len(archetypes) == 1: archetype = 'Pure ' + archetypes[0]
        else: archetype = archetypes[-1]

        # loop through cards in deck, check if they exist in Scryfall. If they do, store game information.
        for card in deck:
            
            if not magic_cards.get(card) or (cube_list and card not in cube_list): continue

            else: 
                card_dict[card]['num'] += 1
                card_dict[card]['win'] += win
                card_dict[card]['loss'] += loss
                card_dict[card]['archetypes'] += [archetype]
                
                # if there is SB info for this deck, note that the card is in the main over the side
                if side: card_dict[card]['main %'] += [1]

        # loop through sideboard if not empty, noting that the cards are in the side over main
        for card in side:

            if not magic_cards.get(card) or (cube_list and card not in cube_list): continue

            else: card_dict[card]['main %'] += [0]
            

    print('{} unique cards identified in decklists'.format(len(card_dict)))

    # extract information about the cards from scryfall dictionary
    for card in card_dict.keys():
        color, mana_value, card_type = magic_cards[card].values()

        # add card characteristics
        for characteristic, value in zip(['color', 'mana_value', 'type'], [color, mana_value, find_card_type(card_type)]):
            card_dict[card][characteristic] = value

        # calculate the maindeck % rate if sideboard information exists for any of the decks that contain the card
        if len(card_dict[card]['main %']) != 0:
            card_dict[card]['main %'] = np.average(card_dict[card]['main %'])

            # if the card has only ever been sideboarded, it won't contain a win %, etc so skip those analyses.
            if card_dict[card]['main %'] == 0:
                card_dict[card]['win %'], card_dict[card]['norm %'] = np.nan, np.nan
                continue

        else:
            card_dict[card]['main %'] = np.nan

        # get win rates and perform normalization by archetype win rate
        card_dict[card]['win %'] = card_dict[card]['win']/(card_dict[card]['win'] + card_dict[card]['loss'])
        archetype_winrates = [archetype_dict[archetype]['Win %'] for archetype in card_dict[card]['archetypes']]
        card_dict[card]['norm %'] = card_dict[card]['win %']/np.average(archetype_winrates)

    # store the results of the card analysis in a dataframe. Then calculate win %, apply filter, and export to csv.
    results = {card: {key: card_dict[card][key] for key in ['win', 'loss', 'num', 'color', 'mana_value', 'type', 'main %', 'win %', 'norm %']} for card in card_dict.keys()}
    results_df = pd.DataFrame.from_dict(results, orient = 'index').reset_index()
    results_df.columns = ['Name','Win', 'Loss','Num','Color', 'Mana Value', 'Type', 'Main %', 'Win %', 'Norm %']

    if card_filter:
        results_df = results_df.loc[results_df['Num'] > card_filter]

    #export analyses, sorting by Win %, Norm %, and Main %
    win_df = results_df.sort_values(by = 'Win %', ascending = False)
    norm_df = results_df.sort_values(by = 'Norm %', ascending = False)
    main_df = results_df.sort_values(by = 'Main %', ascending = False)

    os.makedirs(os.path.join(save_folder, 'csv-files'), exist_ok=True)
    win_df.to_csv(os.path.join(save_folder, 'csv-files/Card_Analysis_Win%.csv'), index = False)
    norm_df.to_csv(os.path.join(save_folder, 'csv-files/Card_Analysis_Norm%.csv'), index = False)
    main_df.to_csv(os.path.join(save_folder, 'csv-files/Card_Analysis_Main%.csv'), index = False)


def export_player_analysis(deck_list_dict, save_folder='results'):
    
    '''Analyzes player distribution and exports to csv. Will analyze by subtypes as well.'''
    
    player_dict = defaultdict(lambda: {'num':0, 'win': 0, 'loss': 0})

    players = []

    # loop through each deck, and store player information
    for deck_dict in deck_list_dict.values():
        
        wins, losses = map(int, deck_dict['record'])

        players.extend(deck_dict['player'])    
        
        for player in deck_dict['player']:
            player_dict[player]['num'] += 1
            player_dict[player]['win'] += wins
            player_dict[player]['loss'] += losses

    # calculate win rates for each player
    for player in player_dict:
        player_dict[player]['Win %'] = player_dict[player]['win']/(player_dict[player]['win'] + player_dict[player]['loss'])
    
    # convert player analysis to dataframe, calculate winrates, then export.
    player_df = pd.DataFrame.from_dict(player_dict, orient = 'index').reset_index()
    player_df.columns = ['Player','Num','Win', 'Loss', 'Win %']

    os.makedirs(os.path.join(save_folder, 'csv-files'), exist_ok=True)
    player_df.to_csv(os.path.join(save_folder, 'csv-files/Player_Analysis.csv'), index=False)


def export_archetype_analysis(deck_list_dict, save_folder='results'):
    
    '''Analyzes archetype distribution and exports to csv. Will analyze by subtypes as well.'''
    
    archetype_dict = defaultdict(lambda: {'num':0, 'win': 0, 'loss': 0})

    archetypes = []

    # loop through each deck, and store archetype information
    for deck_dict in deck_list_dict.values():
        
        wins, losses = map(int, deck_dict['record'])

        archetypes.extend(deck_dict['archetypes'])    
        
        if len(deck_dict['archetypes']) == 1:
            archetype = deck_dict['archetypes'][0]
            archetype_dict['Pure ' + archetype]['num'] += 1
            archetype_dict['Pure ' + archetype]['win'] += wins
            archetype_dict['Pure ' + archetype]['loss'] += losses

        for archetype in deck_dict['archetypes']:

            archetype_dict[archetype]['num'] += 1
            archetype_dict[archetype]['win'] += wins
            archetype_dict[archetype]['loss'] += losses

    # calculate win rates for each archetype
    for archetype in archetype_dict:
        archetype_dict[archetype]['Win %'] = archetype_dict[archetype]['win']/(archetype_dict[archetype]['win'] + archetype_dict[archetype]['loss'])

    # convert archetype analysis to dataframe, calculate winrates, then export.
    archetype_df = pd.DataFrame.from_dict(archetype_dict, orient = 'index').reset_index()
    archetype_df.columns = ['Archetype','Num','Win', 'Loss', 'Win %']

    os.makedirs(os.path.join(save_folder, 'csv-files'), exist_ok=True)
    archetype_df.to_csv(os.path.join(save_folder, 'csv-files/Archetype_Analysis.csv'), index=False)

    return archetype_dict


def export_color_analysis(deck_dict, magic_cards, save_folder='results'):

    num_decks = len(deck_dict)
    num_decks_w_color = {}
    num_decks_w_splash = {}
    avg_card_count = {}

    for deck in deck_dict.values():

        num_nonlands = len([card for card in deck['main'] if find_card_type(magic_cards[card]['type']) != 'Land'])

        for color in deck['color'].keys():
            if deck['color'][color] != 0:
                if color in num_decks_w_color:
                    num_decks_w_color[color] += 1
                else:
                    num_decks_w_color[color] = 1
                if color in avg_card_count:
                    avg_card_count[color].append(deck['color'][color] / num_nonlands)
                else:
                    avg_card_count[color] = [deck['color'][color] / num_nonlands]

        for color in deck['splash'].keys():
            if deck['splash'][color] != 0:
                if color in num_decks_w_splash:
                    num_decks_w_splash[color] += 1
                else:
                    num_decks_w_splash[color] = 1

    color_dict = {}
    for color in deck['color'].keys():
        deck_spread = num_decks_w_color[color] / num_decks
        splash_spread = num_decks_w_splash[color] / (num_decks - num_decks_w_splash[color])
        card_spread = np.average(avg_card_count[color])
        color_dict[color] = {'Deck %': deck_spread, 'Splash %': splash_spread, 'Avg Card %': card_spread}

    color_df = pd.DataFrame.from_dict(color_dict, orient = 'index').reset_index()
    color_df.columns = ['Color', 'Deck %', 'Splash %', 'Avg Card %']

    os.makedirs(os.path.join(save_folder, 'csv-files'), exist_ok=True)
    color_df.to_csv(os.path.join(save_folder, 'csv-files/Color_Analysis.csv'), index=False)


def export_color_curve(deck_dict):
    num_colors = {'One': 0, 'One + Splash': 0,
                  'Two': 0, 'Two + Splash': 0,
                  'Three': 0, 'Three + Splash': 0,
                  'Four': 0, 'Four + Splash': 0,
                  'Five': 0}

    for deck in deck_dict.values():
        splash = False
        colors = 0
        for color in deck['color'].keys():
            if deck['color'][color] != 0:
                colors += 1
        for color in deck['splash'].keys():
            if deck['splash'][color] != 0:
                splash = True
        
        num_colors[list(num_colors.keys())[2 * colors + splash - 2]] += 1

    num_decks = len(deck_dict)
    for colors in list(num_colors.keys()):
        num_colors[colors] /= num_decks

    return num_colors

def export_timecourse_analysis(deck_dict, window):
    '''If specified, analyze the decklists and the archetype win rates over time. Returns a dataframe that is then plotted.'''

    # Extract all the archetypes present in the decklists, and the corresponding dates
    decklists = deck_dict.values()
    archetypes = [deck['archetypes'] for deck in decklists]
    archetypes = list(set([archetype for archetype_list in archetypes for archetype in archetype_list]))
    dates = [int(deck['date']) for deck in decklists]

    # Sort the decklists based on the date they were added.
    sorted_decklists = [deck for _, deck in sorted(zip(dates, decklists))]
    window_num = len(sorted_decklists) - window + 1
    storage_matrix = np.zeros([len(archetypes), window_num])

    # Conduct a sliding window analysis, storing the average win rate for the archetypes during this window.
    for i in range(window_num):
        decklist_window = sorted_decklists[i:i + window]
        for j, archetype in enumerate(archetypes):
            records = np.array([deck['record'] for deck in decklist_window if archetype in deck['archetypes']])
            
            # Handle empty records
            if len(records) == 0:
                storage_matrix[j, i] = np.nan  # Use NaN for missing data
            else:
                total_wins = np.sum(records[:, 0])  # Sum of wins
                total_games = np.sum(records)       # Sum of wins + losses
                if total_games > 0:
                    storage_matrix[j, i] = total_wins / total_games
                else:
                    storage_matrix[j, i] = np.nan  # Avoid division by zero

    return archetypes, storage_matrix