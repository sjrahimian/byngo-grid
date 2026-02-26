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
__version__ = "0.0.1"
__status__ = "development"
__license__ = ""


import argparse
from pathlib import Path
import sys
import random
from math import ceil

# 3rd party Libs
import pandas as pd
from pyhtml2pdf import converter
from pypdf import PdfWriter
print()


def arguments(): 
    parser = argparse.ArgumentParser(prog='Byngo Card', description='Random bingo card generator.', epilog='')

    # parser.add_argument('-o', '--output', action="store", default=Path("path/to/byngo-cards.pdf"), help="Custom directory to save file.")

    parser.add_argument('-x', '--no-free', action='store_true', default=False, help="Remove free space.")
    parser.add_argument('-i', '--num-players', action='store', default=1, type=int, help="Number of players/grids.")
    parser.add_argument('-g', '--grid-size', action='store', default=5, type=int, choices=range(3, 6), help="Size of grid: 3x3, 4x4, or 5x5.")
    parser.add_argument('-m', '--min', action='store', default=1, type=int, help="Minimum value to appear on the grid.")
    parser.add_argument('-n', '--max', action='store', default=50, type=int, help="Maximum value to appear on the grid.")
    parser.add_argument('-t', '--title', action='store', default="Byngo Card", type=str, help="A title for the game grid.")
    # parser.add_argument('-p', '--page', action='store', default=4, type=int, choices={1, 2, 4}, help="1, 2, or 4 grids/page when exporting.")



    return parser.parse_args()


def generateGrid(min: int=1, max: int=50, grid: int=5):
        if min >= max:
            raise ValueError(f"Minimum value ({min}) cannot be greater than maximum value ({max}).")
        if min < 0:
            raise ValueError(f"Minimum value ({min}) cannot be a negative.")
        elif max > 999:
            raise ValueError(f"Maximum value ({max}) cannot excceed 999.")

        length = grid * grid
        unique = []
        while len(unique) != (length):
            if (val:= random.randint(min, max)) not in unique:
                unique.append(val)

        # print(unique)

        # split into matrix
        return [ [ unique.pop() for i in range(0, grid) ] for j in range(0, grid) ]

def addFreeSpace(matrix, grid: int=5):
    if (grid % 2) == 0:
        row = random.randint(2, 3) - 1
        col = random.randint(2, 3) - 1
    else:
        row = ceil(grid / 2) - 1
        col = row

    matrix[row][col] = "FREE"

def header(grid: int=5):
    h = []
    if grid == 3:
        h = "BY N GO".split()
    elif grid == 4:
        h = "B Y N GO".split()
    else:
        h = "B Y N G O".split()
        
    return h

def main(args):
    for x in range(0, args.num_players):
        print(f"Creating gird {x + 1} of {args.num_players}...")
        matrix = generateGrid(args.min, args.max, args.grid_size)
        if not args.no_free:
            addFreeSpace(matrix, args.grid_size)

        df = pd.DataFrame(matrix)
        df.columns = header(args.grid_size)

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

        # OUTPUT AN HTML FILE
        tempHTML = Path(f'temp{x}.html')
        with open(tempHTML, 'w') as f:
            f.write(template.format(title=args.title, table=df.to_html(header=True, index=False, classes='mystyle')))

        converter.convert(f'file:///{tempHTML.resolve()}', f'temp{x}.pdf')
        tempHTML.unlink()

    print("Packaging neatly...")
    merger = PdfWriter()
    pdfs = [ x for x in Path('./').glob('*temp*.pdf') if x.is_file() ]
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

