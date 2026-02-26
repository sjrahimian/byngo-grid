# Byngo Card Generator

Generates random bingo cards based on a given values (or go with the defaults) and export to PDF.

## Run

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pandas pyhtml2pdf pypdf
python .\byngo.py --help
```

### Options

* Maximum and minimum values
* Number of players (grids)
* grid size: 3x3, 4x4, or 5x5
* Toggle free space (default)
* Card title: "Byngo Card"

### Fix/Future

* 1 grid/page when writing to PDF; make it so that it can be 4 grids/page.
* Switch random number generator to numpy.

## License

[Unlicense](./LICENSE) © Byngo Card
