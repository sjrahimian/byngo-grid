# Byngo Card Generator

Generate unique bingo cards and export to PDF.

## Getting Started

Download the application from the latest [releases page](https://github.com/sjrahimian/game-library-index/releases/latest) for the target operating system.

Then open your command line interface and run by executing the `byngo.exe`.

### Options

*Byngo Card* allows you to customize several options:

#### Card Options

* Number of cards (max = 100)
* Grid size: 3x3, 4x4, or 5x5
* Add or remove free space override

#### PDF Options

* Add title to each card
* Enable/disable column headers
* Custom filename
* Number of cards/page: 1, 2, or 4

## Development

```bash
python -m venv .venv
. .venv/bin/activate
pip install pandas reportlab
python ./byngo.py --help
```

## License

This project is licensed under modified version of: [Unlicense](./LICENSE) © Byngo Card
