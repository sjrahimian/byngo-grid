# Byngo Board Generator

Generates random bingo boards based on a given values (or go with the defaults).

## Run

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pandas pyhtml2pdf pypdf
python .\byngo_board.py --help
```

### Options

* Maximum and minimum values
* Number of players (grids)
* grid size: 3x3, 4x4, or 5x5
* Toggle free space (default)
* Board title: "Byngo Board"

### Fix/Future

* 1 grid/page when writing to PDF; make it so that it can be 4 grids/page.
* Switch random number generator to numpy.
