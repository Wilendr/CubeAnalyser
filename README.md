# CubeAnalyser – Cube Draft Analysis Tool

This tool lets you analyze your own cube draft decklists using a graphical user interface (GUI). It's based on the original command-line version described in the Tireless Tracker article *"Analyzing Your Own Cube Drafts"* but extended with new features and usability improvements.

---


## Features

- Analyze cube draft decklists with just a few clicks
- Card performance metrics (Win %, Main %, Norm %)
- Archetype analysis
- Color curve and color usage insights
- Time trend analysis (rolling win rate over time)
- Automatic generation of visualization images
- Deck image generation (optional)
- GUI-based and beginner friendly – no terminal knowledge required!
- Support for custom cards

---


## How to Use

1. **Launch the Program**  
   Run `CubeAnalyser.command` (Mac) or `CubeAnalyser.bat` (Windows)

2. **Fill in the Fields**:
   - **Select deck folder**: Folder containing `.txt` files for each deck
   - **Select cube list**: Text file listing all cube cards, one per line (optional)
   - **Select output folder**: Where results and images should be saved
   - Optionally:
     - Enable "Update card data" to refresh data collected from Scryfall (1)
     - Enable "Generate deck images" for visual deck overviews
     - Enable "Time trend analysis" to track winrates over time

(1): To speed up the program data from Scryfall is stored in a .json file for next time you want to analyse your collected data. It is needed to update the stored .json-file when new cards are released.

3. **Click "Start Analysis"**

4. **Click "View Analysis Images"** to browse the generated `.png` results

5. **Click "View README"** for help inside the app

---


## Deck File Format

Each deck file should follow this format (one deck per file):

Player: Name\
Archetype: Superarchetype_Subarchetype\
Record: MatchWins-MatchLosses\
Games: GameWins-GameLosses

1 Lightning Bolt\
.\
.\
.

1 One with Nothing\
.\
.\
.

Note: Incorrect formatting may cause errors.

---


## How to add Custom cards

1. Go to program/magic_cards.json and add the card’s attributes 
(use the same format as the existing entries)

2. Add an image of the card to program/card_images/
Use the same name as in magic_cards.json (e.g., Lightning_Bolt.png)

Note: Step 2 is optional and is only required for generating images of decks

---


## Requirements

- Python 3.8+
- Required Python packages:
  - `requests`
  - `Pillow`
  - `matplotlib`
  - `tkinter` (usually preinstalled)

---


## Credit

Originally based on Jett Crowdis' Tireless Tracker analysis scripts, 
extended with a graphical interface and additional visualizations.
