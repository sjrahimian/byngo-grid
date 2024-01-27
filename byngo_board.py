#!/usr/bin/env python

""" Byngo: Board Generator

    Random bingo board generator.
"""

__author__ = [""]
__email__ = [""]
__maintainer__ = [""]
__credits__ = [__author__, ""]
__title__ = "Byngo"
__copyright__ = "Copyright 2024"
__version__ = "0.0.1"
__status__ = "development"
__license__ = ""


import argparse
from pathlib import Path
import sys
import random

def arguments(): 
    parser = argparse.ArgumentParser(prog='Bango', description='Random ningo board generator.', epilog='')

    parser.add_argument('-o', '--output', action="store", default=Path("./bango-output.pdf"), help="Location and filename.")

    parser.add_argument('-x', '--no-free', action='store_true', default=False, help="Remove free space.")
    parser.add_argument('-g', '--grid', action='store', default=1, type=int, choices=range(1, 99), help="Number of players/grids.")
    parser.add_argument('-s', '--size', action='store', default=5, type=int, choices=range(3, 5), help="Size of grid: 3x3, 4x4, or 5x5.")
    parser.add_argument('-m', '--min', action='store', default=1, type=int, help="Minimum value to appear on the grid.")
    parser.add_argument('-n', '--max', action='store', default=50, type=int, help="Maximum value to appear on the grid.")
    parser.add_argument('-p', '--page', action='store', default=4, type=int, choices={1, 2, 4}, help="1, 2, or 4 grids/page when exporting.")

    return parser.parse_args()


def generateGrid(min: int=1, max: int=50, size: int=5):
        if min >= max:
            raise ValueError(f"Minimum value ({min}) cannot be greater than maximum value ({max}).")

        if min < 0:
            raise ValueError(f"Minimum value ({min}) cannot be a negative.")
        elif max > 999:
            raise ValueError(f"Maximum value ({max}) cannot excceed 999.")

        length = size * size
        unique = []
        while len(unique) != (length):
            if (val:= random.randint(min, max)) not in unique:
                unique.append(val)

        # print(unique)

        # split into matrix
        return [ [ unique.pop() for i in range(0, grid) ] for j in range(0, grid) ]

def main(args):
    numPlayers = 2
    for x in range(0, numPlayers):
        matrix = generateGrid()
        for i in range(0, len(matrix)):
            print(matrix[i])

        print()


    

if __name__ == "__main__":
    args = arguments()
    main(args)


sys.exit(0)

