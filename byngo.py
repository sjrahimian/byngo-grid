#!/usr/bin/env python

""" Byngo Card

    Random bingo card generator.
"""

__author__ = ["Sama Rahimian"]
__email__ = [""]
__credits__ = [__author__, ""]
__title__ = "Byngo Card"
__copyright__ = f"{__title__} © 2024"
__version__ = "0.7.6"
__status__ = "development"
__license__ = "Unlicense"


import argparse
from pathlib import Path
import sys
import random
from math import ceil

# 3rd party Libs
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

from pyhtml2pdf import converter
from pypdf import PdfWriter

def arguments(): 
    parser = argparse.ArgumentParser(description='Generate unique random bingo cards and export to PDF.', epilog='')

    # Bingo card options
    freeSpaceGroup = parser.add_mutually_exclusive_group()
    freeSpaceGroup.add_argument('-F', '--free-space', action='store_true', help='Force a free space')
    freeSpaceGroup.add_argument('-x', '--no-free-space', action='store_false', dest='free_space', help='Remove free space')
    parser.set_defaults(free_space=None)

    parser.add_argument('-c', '--num_cards', action='store', default=1, type=int, help="Number of cards to be generated (max=100)")
    parser.add_argument('-g', '--grid', action='store', default=5, type=int, choices=range(3, 6), help="Size of grid: 3x3, 4x4, or 5x5")

    # PDF options
    pdf_parser = parser.add_argument_group("PDF Options")
    pdf_parser.add_argument('-f', '--file', action="store", default="byngo-cards.pdf", type=str, help="Provide PDF filename.")
    pdf_parser.add_argument('-H', '--no-headers', action='store_false', help='Remove the extra row for the column headers.')
    pdf_parser.add_argument('-p', '--per-page', type=int, choices={1, 2, 4}, default=4, help='Cards per PDF page')
    pdf_parser.add_argument('-t', '--title', action='store', default=f"{__title__}", type=str, help="Place a custom title for the game card")

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
    gridSize = f'{args.grid}x{args.grid}'
    print(f'Selected grid size of "{gridSize}", and {args.num_cards} card(s) to be generated')
    print("Generating cards")

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

def export_to_pdf(args, cards, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    pageWidth, pageHeight = letter
    
    # Configuration based on cards per page
    layout_configs = {
        1: {"cols": 1, "rows": 1},
        2: {"cols": 1, "rows": 2},
        4: {"cols": 2, "rows": 2}
    }
    
    cfg = layout_configs[args.per_page]
    width, height = 250, 250 # cell size
    padding, panelRowPadding = 40, 40

    
    # Calculate cell distribution
    for i, df in enumerate(cards):
        print(f" >> preparing card {i + 1} of {len(cards)}")

        # Determine position on current page
        pos_on_page = i % args.per_page
        col = pos_on_page % cfg["cols"]
        row = pos_on_page // cfg["cols"]
        
        # Calculate X and Y coordinates (ReportLab Y starts at bottom)
        x_offset = padding + (col * (width + padding))
        y_offset = pageHeight - ((row + 1) * (height + padding + panelRowPadding))
        
        draw_card(c, df, x_offset, y_offset, width, height, args.no_headers, args.title)
        
        # If page is full or it's the last card, start a new page
        if (i + 1) % args.per_page == 0 and (i + 1) < len(cards):
            c.showPage()
            
    print("Saving to PDF...", end="")
    c.save()
    print("completed")

def draw_card(canvas_obj, df, x, y, card_w, card_h, headers=False, title=None):
    """
    Draws a single bingo card. 
    Adjusts cell height based on whether headers are included.
    """
    num_data_rows = len(df)
    num_cols = len(df.columns)
    
    # Total visual rows depends on if we show the header row or not
    total_visual_rows = num_data_rows + 1 if headers else num_data_rows
    
    cell_w = card_w / num_cols
    cell_h = card_h / total_visual_rows

    # Add title
    if title:
        canvas_obj.setFont("Helvetica-Bold", 16)
        canvas_obj.setFillColor(colors.black)
        canvas_obj.drawCentredString(x + (card_w / 2), y + card_h + 12, str(title))
    
    # Draw Outer Border
    canvas_obj.setLineWidth(2)
    canvas_obj.rect(x, y, card_w, card_h)
    canvas_obj.setLineWidth(1)

    # 1. Handle Headers
    current_y = y + card_h
    if headers:
        canvas_obj.setFont("Helvetica-Bold", 14)
        for c_idx, col_name in enumerate(df.columns):
            cell_x = x + (c_idx * cell_w)
            # Center text in the top-most row
            canvas_obj.drawCentredString(cell_x + (cell_w/2), current_y - (cell_h * 0.7), str(col_name))
            canvas_obj.rect(cell_x, current_y - cell_h, cell_w, cell_h)
        current_y -= cell_h # Move the starting point for data rows down

    # 2. Handle Data Rows
    canvas_obj.setFont("Helvetica", 12)
    for r_idx in range(num_data_rows):
        row_y = current_y - ((r_idx + 1) * cell_h)
        for c_idx, col_name in enumerate(df.columns):
            cell_x = x + (c_idx * cell_w)
            val = df.iloc[r_idx, c_idx]
            
            # Formatting for "FREE" space
            if str(val) == "FREE":
                canvas_obj.setFillColor(colors.red)
                canvas_obj.setFont("Helvetica-Bold", 10)
            else:
                canvas_obj.setFillColor(colors.black)
                canvas_obj.setFont("Helvetica", 12)
                
            canvas_obj.drawCentredString(cell_x + (cell_w/2), row_y + (cell_h * 0.35), str(val))
            canvas_obj.rect(cell_x, row_y, cell_w, cell_h)
            
    canvas_obj.setFillColor(colors.black) # Reset

def main(args):
    print(args)
    if not (1 <= args.num_cards <= 100):
        print(f"Error: You requested {args.num_cards} cards, but the limit is 100.")
        sys.exit(1)

    if args.free_space is True:
        print("FREE SPACE on")
    elif args.free_space is False:
        print("FREE SPACE off")


    cards = generateMultipleCards(args)

    try:
        print("Exporting to PDF...")
        export_to_pdf(args, cards, args.file)
    except PermissionError as error:
        print(f"{error}\nClose PDF and run again.\n")
        sys.exit(-1)

    print("Finished")


if __name__ == "__main__":
    try:
        args = arguments()
        main(args)
    except KeyboardInterrupt:
        sys.exit(-1)

    sys.exit(0)

