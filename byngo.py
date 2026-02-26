#!/usr/bin/env python

""" Byngo Card

    Random bingo card generator.
"""

__author__ = [""]
__email__ = [""]
__maintainer__ = [""]
__credits__ = [__author__, ""]
__title__ = "Byngo Card"
__copyright__ = "Copyright 2024"
__version__ = "0.5.0"
__status__ = "development"
__license__ = "Unlicense"


import argparse
from pathlib import Path
import sys
import random
from math import ceil

# 3rd party Libs
import pandas as pd
from pyhtml2pdf import converter
from pypdf import PdfWriter

def arguments(): 
    parser = argparse.ArgumentParser(description='Generate unique random bingo cards and export to PDF.', epilog='')

    freeSpaceGroup = parser.add_mutually_exclusive_group()
    freeSpaceGroup.add_argument('-f', '--free-space', action='store_true', help='Force a free space')
    freeSpaceGroup.add_argument('-x', '--no-free-space', action='store_false', dest='free_space', help='Remove free space')
    parser.set_defaults(free_space=None)

    parser.add_argument('-c', '--cards', action='store', default=1, type=int, help="Number of cards to be generated (max=100).")
    parser.add_argument('-g', '--grid', action='store', default=5, type=int, choices=range(3, 6), help="Size of grid: 3x3, 4x4, or 5x5.")
    parser.add_argument('-t', '--title', action='store', default="Byngo Card", type=str, help="Place a custom title for the game card.")

    return parser.parse_args()


import pandas as pd
import random

def generateBingoCard(gridSize=None, freeSpaceOverride=None):
    """
    Generates a randomized bingo card DataFrame based on grid size.
    
    Parameters:
    - gridSize (str): "5x5" (75-ball), "4x4" (80-ball), or "3x3" (30-ball).
    - freeSpaceOverride (bool): Override the default free space rule. 
                               If None, defaults to True for 5x5, False for others.
    """
    # Configuration dictionary for the rules of each grid size
    configs = {
        "5x5": {
            "cols": ["B", "I", "N", "G", "O"],
            "ranges": [(1, 15), (16, 30), (31, 45), (46, 60), (61, 75)],
            "default_free": True
        },
        "4x4": {
            "cols": ["Col_1", "Col_2", "Col_3", "Col_4"],
            "ranges": [(1, 20), (21, 40), (41, 60), (61, 80)],
            "default_free": False
        },
        "3x3": {
            "cols": ["BY", "N", "GO"],
            "ranges": [(1, 10), (11, 20), (21, 30)],
            "default_free": False
        }
    }

    if gridSize not in configs:
        raise ValueError("Invalid grid size. Choose from '5x5', '4x4', or '3x3'.")

    cfg = configs[gridSize]
    n = len(cfg["cols"])
    
    # Generate the random numbers for each column
    data = {}
    for colName, (minVal, maxVal) in zip(cfg["cols"], cfg["ranges"]):
        data[colName] = random.sample(range(minVal, maxVal + 1), n)

    df = pd.DataFrame(data)
    df.columns = cfg["cols"]

    # Handle the free space if required
    freeSpace = cfg["default_free"] if freeSpaceOverride is None else freeSpaceOverride
    if freeSpace:
        df = freeSpaceHandler(df, cfg)

    return df

def freeSpaceHandler(df, cfg):
    # Note: Even grids (4x4) don't have a true center; defaults to the bottom-right of the inner 2x2.
    df = df.astype(object)

    # Calculate the center index. 
    index = len(cfg["cols"]) // 2
    colName = cfg["cols"][index]
    df.loc[index, colName] = "FREE"

    return df

def generateMultipleCards(args):
    """
    Generates a specified number of unique Bingo cards.
    """
    cards = []
    seenSignatures = set()
    gridSize = f'{args.grid_size}x{args.grid_size}'
    print(f'Selected grid size of "{gridSize}", and {args.num_cards} card(s) to be generated.')
    
    # Keep generating until we have the exact number of unique cards requested
    while len(cards) < args.num_cards:
        # 1. Generate a single card using our previous function
        cardDf = generateBingoCard(gridSize, args.free_space)
        
        # 2. Convert the DataFrame's values into a flat, hashable tuple
        # e.g., (4, 18, 40, 52, 68, 12, 29, ...)
        cardSignature = tuple(cardDf.values.flatten())
        
        # 3. Check if we've seen this exact layout before
        if cardSignature not in seenSignatures:
            seenSignatures.add(cardSignature)
            cards.append(cardDf)
            
    return cards


def main(args):
    
    if not (1 <= args.num_cards <= 100):
        print(f"Error: You requested {args.count} cards, but the limit is 100.")
        sys.exit(1)

    if args.free_space is True:
        print("User forced FREE SPACE on.")
    elif args.free_space is False:
        print("User forced FREE SPACE off.")


    print("Generating cards...")
    cards = generateMultipleCards(args)

    pd.set_option('colheader_justify', 'center')   # FOR TABLE <th>
    template = '''
    <html>
    <head><title></title></head>
    <link rel="stylesheet" type="text/css" href="style.css"/>
    <body>
        <div id="byngo-container">
            <h1>{title}</h1>
            {table}
            <script src="script.js"></script> 
        </div>
    </body>
    </html>
    '''

    for i, card in enumerate(cards):
        print(f"Printing card {i + 1} of {len(cards)}...")

        # OUTPUT AN HTML FILE
        tempHTML = Path(f'temp.{i}.html')
        with open(tempHTML, 'w') as f:
            f.write(template.format(title=args.title, table=card.to_html(header=True, index=False, classes='mystyle')))

        converter.convert(f'file:///{tempHTML.resolve()}', f'temp.{i}.pdf')
        tempHTML.unlink()

    print("Packaging neatly...")
    merger = PdfWriter()
    pdfs = [ x for x in Path('./').glob('*temp.*.pdf') if x.is_file() ]
    for pdf in pdfs:
        merger.append(pdf)

    try:
        merger.write("byngo-cards.pdf")
        merger.close()
    except PermissionError as error:
        print(f"{error}\nClose PDF and run again.\n")
        sys.exit(-1)

    # Clean-up
    print("Cleaning up...")
    pdfs = [ x for x in Path(r'./').glob('*temp*.pdf') if x.is_file() ]
    for pdf in pdfs:
        pdf.unlink()


    print("Finished.")

if __name__ == "__main__":
    args = arguments()
    main(args)


sys.exit(0)

