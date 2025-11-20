# pyChing - I Ching Oracle

A modern Python program to cast and interpret I Ching hexagrams.

## Features

- **Five Casting Methods** (Wu Xing / Five Elements):
  - 🌳 **Wood** - Traditional PRNG (original algorithm)
  - 🪙 **Metal** - OS entropy (os.urandom)
  - 🔥 **Fire** - Cryptographic CSPRNG (secrets module)
  - 🌍 **Earth** - Deterministic seeded (same question = same hexagram)
  - 💨 **Air** - True random numbers (RANDOM.ORG API)

- **Multi-Source Translations** - Infrastructure ready for multiple I Ching translations
- **JSON Persistence** - Save and load readings in portable JSON format
- **Modern Architecture** - Type hints, dataclasses, clean separation of concerns
- **Authentic** - Preserves traditional 3-coin oracle probabilities

## Installation

```bash
# Clone repository
git clone https://github.com/feargeas/pyChing.git
cd pyChing

# Install (optional dependencies for Air method)
pip install -r requirements.txt

# Or install for development
pip install -e ".[dev]"
```

## Quick Start

### Command Line Interface

```bash
# Interactive mode
python pyching_cli.py

# Non-interactive cast
python pyching_cli.py --method wood --question "What is my path?"

# Save reading to file
python pyching_cli.py --method metal --save reading.json

# Compare translations (when available)
python pyching_cli.py --compare wilhelm_baynes canonical
```

### Python API

```python
from pyching import HexagramEngine, Element

# Create engine
engine = HexagramEngine()

# Cast a reading
reading = engine.cast_reading(
    method=Element.WOOD,
    question="What should I focus on today?"
)

# Display interpretation
print(reading.as_text())

# Save for later
reading.save("my_reading.json")
```

### Deterministic Readings (Earth Method)

```python
# Same question + seed always produces same hexagram
question = "What is the meaning of life?"
reading = engine.cast_reading(
    method=Element.EARTH,
    question=question,
    seed=question  # Use question as seed
)

# Will always get the same hexagram for this question
```

## Project Structure

```
pyching/                 # Modern package
├── casting/            # Five element casting methods
├── core/               # Engine, hexagram, reading dataclasses
└── data/               # Data loader and resolver

data/
├── hexagrams/          # 64 JSON files with interpretations
├── mappings.json       # Lookup tables
└── sources_metadata.json  # Translation source registry

tests/                  # Test suite
├── test_*.py          # Core functionality tests
└── gui/               # GUI-specific tests
```

## Requirements

- Python 3.10+
- `requests` (optional, for Air method only)

## Testing

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest tests/ -v

# Run specific test suite
pytest tests/test_casting_methods.py -v
```

## Status

**Version:** 2.0.0-alpha (devnew branch)

**Working:**
- ✅ Core engine and casting methods
- ✅ JSON data access layer
- ✅ Command-line interface
- ✅ Python API
- ✅ All five element methods
- ✅ JSON save/load

**Known Issues:**
- ⚠️ GUI needs updating to use modern engine (see TODO.md)
- ⚠️ Only one translation source currently available (Legge 1882)

## Documentation

- `README.md` (this file) - Quick start and overview
- `MIGRATION_NOTES.md` - Notes on the Python 2 → 3 modernization
- `TODO.md` - Known issues and planned improvements
- `LICENSE` - GPL v2+ license

## Contributing

This is a modernization of the original pyChing by Stephen M. Gava (1999-2006).
Contributions welcome! Please ensure:

- Code follows modern Python conventions (type hints, dataclasses, etc.)
- Tests pass: `pytest tests/ -v`
- New features include tests

## License

GNU General Public License v2 or later (GPL-2.0-or-later)

Copyright (C) 1999-2006 Stephen M. Gava
Modernization (C) 2025

## Credits

- **Stephen M. Gava** - Original pyChing author
- **James Legge** - 1882 I Ching translation (canonical source)
- **RANDOM.ORG** - True random number service (Air method)

## Cultural Note

This project aims to preserve and honor the I Ching tradition while making it accessible through modern technology. The I Ching (易經, Yìjīng, "Book of Changes") is an ancient Chinese divination text dating back over 3,000 years.
