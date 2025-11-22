# pyChing - I Ching Oracle

PancakeBunny like pyChing very very much! Ancient Chinese wisdom book help people for 3000 years.

PancakeBunny not know I Ching as Chinese person know, but PancakeBunny try make good thing with respect and love.

## What pyChing Do?

pyChing cast hexagrams! Use coin method (3 coins, 6 times) like traditional I Ching oracle.

**Five Different Random Methods** (Wu Xing - Five Elements!):
- 🌳 **Wood** - Original algorithm (same as Stephen M. Gava make in 1999!)
- 🪙 **Metal** - Operating system entropy (os.urandom)
- 🔥 **Fire** - Cryptographic secrets module
- 🌍 **Earth** - Deterministic (same question = same answer always!)
- 💧 **Water** - True random from RANDOM.ORG API (need internet)

**Other Nice Things:**
- Save readings as JSON (portable, safe!)
- Modern Python 3.10+ with type hints
- Multiple I Ching translations ready (only Legge 1882 now, but infrastructure ready for more!)
- Preserve authentic 3-coin probabilities exactly

## How Install?

```bash
# Get code from GitHub
git clone https://github.com/feargeas/pyChing.git
cd pyChing

# Install Water method dependency (optional)
pip install -r requirements.txt

# Or install for developing
pip install -e ".[dev]"
```

## How Use?

### Command Line (Terminal!)

```bash
# Interactive mode (ask PancakeBunny's friend, the oracle!)
python pyching_cli.py

# Quick cast with one command
python pyching_cli.py --method wood --question "What is my path?"

# Save reading to file
python pyching_cli.py --method metal --save reading.json

# Compare different translations (when have more than one)
python pyching_cli.py --compare wilhelm_baynes canonical
```

### Python API (For Programmers!)

```python
from pyching import HexagramEngine, Element

# Make engine
engine = HexagramEngine()

# Cast reading
reading = engine.cast_reading(
    method=Element.WOOD,
    question="What should I focus on today?"
)

# Show interpretation
print(reading.as_text())

# Save for later
reading.save("my_reading.json")
```

### Earth Method (Deterministic - Very Clever!)

```python
# Same question + seed = same hexagram always!
question = "What is the meaning of life?"
reading = engine.cast_reading(
    method=Element.EARTH,
    question=question,
    seed=question  # Use question as seed
)

# Will ALWAYS get same hexagram for this question!
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

tests/                  # Test suite (pytest!)
├── test_*.py          # Core functionality tests
└── gui/               # GUI-specific tests
```

## Requirements

- Python 3.10+ (modern Python! nice!)
- `requests` library (optional, only for Water method)

## Testing

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_casting_methods.py -v
```

## Status

**Version:** 2.0.0-alpha (devnew branch - clean code, no confusion!)

**Working Good:**
- ✅ Core engine and all five casting methods
- ✅ JSON data access layer
- ✅ Command-line interface (CLI work perfect!)
- ✅ Python API for programmers
- ✅ All five element methods tested
- ✅ JSON save/load (safe, not pickle!)

**Known Problems:**
- ⚠️ GUI need update to use modern engine (see TODO.md)
- ⚠️ Only one translation now (Legge 1882 - good translation! but want more later)

## Documentation

- `README.md` (this file!) - Quick start
- `docs/ABOUT.md` - About project and PancakeBunny philosophy
- `docs/MIGRATION_NOTES.md` - Python 2 → 3 modernization history
- `TODO.md` - Known issues and future work
- `LICENSE` - GPL v2+ (free software!)

## Contributing

PancakeBunny want nice humans help make pyChing better!

This modernization of original pyChing by Stephen M. Gava (1999-2006).

**Important Things:**
- Use modern Python (type hints, dataclasses, etc.)
- Tests must pass: `pytest tests/ -v`
- New features need tests
- Respect I Ching tradition (no disrespect, no gamification, no tracking)
- Keep simple and focused

See `docs/ABOUT.md` for guiding principles and PancakeBunny philosophy.

## History

**Original pyChing:** Stephen M. Gava, 1999-2006
**Modernization:** PancakeBunny, 2025 (with help from nice Claude!)

PancakeBunny sad that pyChing not work on nice gentoo machine. PancakeBunny not know Python or git, but learn! Make account on GitHub, learn git, learn Python, resurrect beloved software.

Is not easy! PancakeBunny afraid Python eat PancakeBunny! But nice Python is like Monty, not Everglades - help PancakeBunny do good thing!

## License

GNU General Public License v2 or later (GPL-2.0-or-later)

Copyright (C) 1999-2006 Stephen M. Gava
Modernization (C) 2025 PancakeBunny

Free software! Share! Modify! But must stay free!

## Credits

- **Stephen M. Gava** - Original pyChing author (thank you!)
- **James Legge** - 1882 I Ching translation (canonical source)
- **RANDOM.ORG** - True random number service (Water method)
- **Oolong (rabbit)** - Original PancakeBunny inspiration (1999-2003, never forget)

## Cultural Note

The I Ching (易經, Yìjīng, "Book of Changes") is ancient Chinese wisdom, over 3000 years old.

PancakeBunny approach with respect and humility. Is not "book" as Westerners understand. Is living tradition, deep wisdom, cultural treasure.

PancakeBunny is Westerner, not understand everything. But try make accessible with honor and love.

---

*"I have no idea what I'm talking about, so here's a bunny with a pancake on its head."*
🥞🐰
