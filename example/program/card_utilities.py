import requests
import json
import os

def fetch_cards(update=False, filename='program/magic_cards.json'):

    existing_cards = {}
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            existing_cards = json.load(file)

    if not update:
        print(f'Loading data from {filename}...')
        return existing_cards

    print('Fetching cards from Scryfall...')
    response = requests.get('https://api.scryfall.com/bulk-data')
    bulk_data = response.json()

    for data in bulk_data['data']:
        if data['type'] == 'default_cards':
            card_data_url = data['download_uri']
            break
    else:
        raise Exception("Could not find default cards in Scryfall bulk data.")

    response = requests.get(card_data_url)
    json_data = response.json()

    updated_cards = existing_cards.copy()

    for card in json_data:
        try:
            card_name = card.get('name')
            if not card_name:
                continue

            color_identity = card.get('color_identity', [])
            mana_value = card.get('cmc', 0)
            type_line = card.get('type_line', '')

            if card_name not in updated_cards:
                updated_cards[card_name] = {
                    'color': ''.join(color_identity),
                    'mana_value': mana_value,
                    'type': type_line
                }

            if card.get('layout') == 'transform':
                transformed_name = card_name.split('//')[0].strip()
                if transformed_name not in updated_cards:
                    updated_cards[transformed_name] = updated_cards[card_name]

        except KeyError as e:
            print(f"Skipping card due to missing key: {e}")
            continue

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(updated_cards, file, ensure_ascii=False, indent=4)

    return updated_cards


def find_card_type(full_type):
    
    '''Takes in a card_type (str) and returns its shortened type (Artifact, Creature, Enchantment, PW, Land, Sorcery, Instant)'''

    for card_type in ['Creature', 'Artifact', 'Enchantment', 'Planeswalker', 'Land', 'Sorcery', 'Instant']:
        if card_type in full_type:
            return card_type

    return None