# Byngo Cards Generator

Generate bingo cards and export to PDF.

## Getting Started

Download the application from the latest [releases page](https://github.com/sjrahimian/game-library-index/releases/latest) for the target operating system.

If you try running the executable without any arguments (e.g., `-h\--help`), it will launch a basic GUI.

### Options

*Byngo Cards* allows you to customize several options:

#### Card Options

* Number of cards (1 - 100)
* Grid size: 3x3, 4x4, or 5x5
* Add or remove free space override

#### PDF Options

* Add title to each card (30 characters limit)
* Remove column headers
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
