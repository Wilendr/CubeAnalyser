from PIL import Image
import requests
from io import BytesIO
from card_utilities import *

CARD_WIDTH = 488
CARD_HEIGHT = 680

def create_deck_image(deck_list_dict, magic_cards, deck_id=0, output_file='deck_image.png'):
    
    deck = deck_list_dict[deck_id]['main']
    categorized_cards = { 'land': [], 0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [] }

    for card_name in deck:
        card_info = magic_cards.get(card_name, None)
        if not card_info:
            continue

        card_type = find_card_type(card_info['type'])
        mana_value = int(card_info['mana_value'])

        if card_type == 'Land':
            categorized_cards['land'].append(card_name)
        else:
            key = mana_value if mana_value <= 6 else 7
            categorized_cards[key].append(card_name)

    ordered_keys = ['land', 0, 1, 2, 3, 4, 5, 6, 7]
    columns = []
    for key in ordered_keys:
        card_names = categorized_cards[key]
        images = [fetch_card_image(card_name) for card_name in card_names if fetch_card_image(card_name)]
        if images:
            columns.append(images)

    card_width, card_height = 488, 580
    vertical_padding = 90
    horizontal_padding = 20
    outer_padding = 40

    num_columns = len(columns)
    max_rows = max(len(col) for col in columns)

    total_width = num_columns * card_width + (num_columns - 1) * horizontal_padding + 2 * outer_padding
    total_height = max_rows * vertical_padding + 2 * outer_padding + card_height

    final_image = Image.new('RGB', (total_width, total_height), color=(255, 255, 255))

    for col_idx, col_images in enumerate(columns):
        x = outer_padding + col_idx * (card_width + horizontal_padding)
        for row_idx, img in enumerate(col_images):
            y = outer_padding + row_idx * vertical_padding
            final_image.paste(img, (x, y))

    final_image.save(output_file)

    
def sanitize_filename(card_name):
    clean_name = card_name.split('//')[0].strip()
    clean_name = clean_name.replace(" ", "_").replace("'", "").replace(",", "").replace("/", "")
    return clean_name + '.png'

def fetch_card_image(card_name, folder='program/card_images'):
    os.makedirs(folder, exist_ok=True)
    file_name = sanitize_filename(card_name)
    local_path = os.path.join(folder, file_name)

    if os.path.exists(local_path):
        try:
            return resize_image(Image.open(local_path))
        except Exception as e:
            print(f"Error while opening of {local_path}, will try to fetch new image. ({e})")

    try:
        url = f'https://api.scryfall.com/cards/named?exact={card_name}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        image_url = data['image_uris']['normal']
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content))
        image = resize_image(image)
        image.save(local_path)
        return image
    except Exception as e:
        print(f'Error fetching image for {card_name}: {e}')
        return None


def resize_image(image, width=CARD_WIDTH, height=CARD_HEIGHT):
    image = image.convert("RGBA")
    image.thumbnail((width, height), Image.ANTIALIAS)

    background = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    offset = ((width - image.width) // 2, (height - image.height) // 2)
    background.paste(image, offset)
    return background.convert("RGB")


def make_deck_images(decklist_folder, deck_dict, magic_cards, save_folder):
    deck_files = [f for f in os.listdir(decklist_folder) if f.endswith('.txt')]

    deck_ids = list(deck_dict.keys())
    total = len(deck_files)

    output_folder = os.path.join(save_folder, 'deck_images')
    os.makedirs(output_folder, exist_ok=True)
    
    for deck_id, deck_file in zip(deck_ids, deck_files):
        image_name = os.path.splitext(deck_file)[0] + '.png'
        output_path = os.path.join(output_folder, image_name)

        try:
            if not os.path.exists(output_path):
                create_deck_image(deck_list_dict=deck_dict, magic_cards=magic_cards,
                                deck_id=deck_id, output_file=output_path)
                
            percent = (deck_id) * 100 / total
            print(f'Completed images for {deck_id} of {total} decks ({percent:.1f}%)')
            print('\x1b[F', end='')

        except Exception as e:
            print(f'Error with image for {deck_file}: {e}')
    