# Multi-Source I Ching Interpretation System

pyChing supports multiple translations and interpretations of the I Ching through a flexible, extensible source system.

## Overview

The multi-source system allows pyChing to:

- **Load** hexagram interpretations from different translators/sources
- **Compare** different translations side-by-side
- **Switch** between sources at runtime
- **Validate** all source data for consistency
- **Extend** easily with new sources

## Architecture

### Data Layer

```
data/
├── interpretations/          # YAML files for each source
│   ├── legge/               # James Legge (canonical)
│   │   ├── hexagram_01.yaml
│   │   └── ...
│   ├── wilhelm/             # Wilhelm/Baynes
│   │   ├── hexagram_01.yaml
│   │   └── ...
│   └── [future sources]/
├── sources/                  # Raw source materials
│   ├── legge/
│   ├── wilhelm/
│   │   ├── wilhelm.md       # Markdown format
│   │   └── source_url.txt
│   └── [future sources]/
├── mappings.json            # Hexagram lookup tables
└── sources_metadata.json    # Source registry
```

### Code Layer

```
pyching/data/
├── loader.py                # HexagramDataLoader - loads YAML
├── resolver.py              # HexagramResolver - multi-source resolution

tools/extractors/
├── base.py                  # BaseExtractor abstract class
├── registry.py              # ExtractorRegistry
├── validator.py             # YAMLValidator
├── wilhelm.py               # Wilhelm extractor implementation
└── [future extractors]/
```

## Using Multiple Sources

### Loading from Different Sources

```python
from pyching.data import HexagramDataLoader

# Load from Legge (default/canonical)
loader = HexagramDataLoader(source='legge')
hex_data = loader.get_hexagram_by_number(1)

# Load from Wilhelm
loader = HexagramDataLoader(source='wilhelm')
hex_data = loader.get_hexagram_by_number(1)
```

### Comparing Sources

```python
from pyching.data import HexagramResolver

resolver = HexagramResolver()

# Compare judgment text across sources
comparison = resolver.compare_sources(
    'hexagram_01',
    sources=['legge', 'wilhelm'],
    field='judgment'
)

for source, judgment in comparison.items():
    print(f"{source}:")
    print(judgment)
    print()
```

### Listing Available Sources

```python
from pyching.data import HexagramResolver

resolver = HexagramResolver()

# Get all available sources for a hexagram
sources = resolver.get_available_sources('hexagram_01')
print(f"Available sources: {sources}")

# Get metadata about a source
info = resolver.get_source_info('wilhelm_baynes')
print(f"Translator: {info['translator']}")
print(f"Year: {info['year']}")
```

## Adding New Sources

### Quick Start

1. **Place source files** in `data/sources/{source_id}/`

2. **Create extractor** at `tools/extractors/{source_id}.py`:

```python
from .base import BaseExtractor, SourceMetadata, HexagramData
from .registry import ExtractorRegistry

METADATA = SourceMetadata(
    source_id='mysource',
    name='My Translation',
    translator='Translator Name',
    year=2000
)

@ExtractorRegistry.register('mysource', METADATA)
class MySourceExtractor(BaseExtractor):
    def extract_hexagram(self, hexagram_number: int):
        # Your extraction logic
        return HexagramData(...)

    def validate_source_files(self):
        # Check source files exist
        return True
```

3. **Import in** `tools/extractors/__init__.py` and `tools/extract_source.py`

4. **Extract and validate**:

```bash
python tools/extract_source.py mysource --all
python tools/extract_source.py mysource --validate
```

See `tools/extractors/README.md` for detailed instructions.

## Source Metadata

All sources are registered in `data/sources_metadata.json`:

```json
{
  "sources": {
    "legge_1882": {
      "id": "legge_1882",
      "name": "James Legge Translation (1882)",
      "translator": "James Legge",
      "year": 1882,
      "canonical": true,
      "completeness": 100,
      "verified": true
    },
    "wilhelm_baynes": {
      "id": "wilhelm_baynes",
      "name": "Wilhelm/Baynes Translation",
      "translator": "Richard Wilhelm / Cary F. Baynes",
      "year": 1950,
      "canonical": false,
      "completeness": 100,
      "verified": true
    }
  },
  "source_priority": [
    "legge_1882",
    "wilhelm_baynes"
  ]
}
```

## YAML Format

All sources use a standardized YAML format:

```yaml
metadata:
  hexagram: 1
  king_wen_sequence: 1
  fu_xi_sequence: 1
  binary: '111111'
  source: wilhelm_baynes
  translator: Richard Wilhelm / Cary F. Baynes
  year: 1950
  language: en
  verified: true

name: Ch'ien
english_name: The Creative
title: 1. Ch'ien / The Creative

trigrams:
  upper: qian
  lower: qian

judgment: |
  THE CREATIVE works sublime success,
  Furthering through perseverance.

image: |
  The movement of heaven is full of power.
  Thus the superior man makes himself strong and untiring.

lines:
  '1':
    position: bottom
    type: nine
    text: |
      Hidden dragon. Do not act.
  # ... lines 2-6

# Optional for hexagrams 1 and 2
all_lines_changing: |
  When all the lines are nines...
```

## Validation

The `YAMLValidator` ensures data quality:

```bash
# Validate all files for a source
python tools/extract_source.py wilhelm --validate

# Strict mode (warnings become errors)
python tools/extract_source.py wilhelm --validate --strict
```

Checks include:
- Required fields present
- Correct data types
- All 6 lines included
- No placeholder text
- Reasonable text lengths
- Valid metadata

## Planned Sources

Sources currently available or planned:

| Source | Status | Translator | Year |
|--------|--------|------------|------|
| Legge | ✅ Complete | James Legge | 1882 |
| Wilhelm/Baynes | ✅ Complete | Richard Wilhelm / Cary F. Baynes | 1950 |
| Simplified Legge | 📋 Planned | TwoDreams.us | 2020 |
| Hermetica | 📋 Planned | Various | - |
| Gnostic (DeKorne) | 📋 Planned | James DeKorne | - |

## Benefits of Multi-Source System

1. **Scholarly Comparison**: Compare different translations to understand nuances
2. **User Preference**: Users can choose their preferred translation
3. **Completeness**: Fall back to canonical source if a source is incomplete
4. **Extensibility**: Easy to add new sources without modifying core code
5. **Validation**: Automated quality checks ensure data integrity
6. **Attribution**: Full metadata for each source (translator, year, URL)

## Design Principles

1. **Separation of Concerns**: Extraction, loading, and resolution are separate
2. **Plugin Architecture**: New sources register themselves automatically
3. **Canonical Reference**: Legge serves as reference for trigrams, binary, etc.
4. **Backward Compatibility**: Loader returns data in format compatible with v1.x
5. **Data-Driven**: Source metadata in JSON, not hardcoded
6. **Validation-First**: All sources must pass validation before use

## Future Enhancements

- **Multi-language support**: Chinese, German, French translations
- **Merge strategies**: Combine strengths of multiple sources
- **User annotations**: Personal notes on hexagrams
- **Source weighting**: Prefer certain sources for specific fields
- **Historical versions**: Track changes in translations over time
- **Community sources**: Allow user-contributed interpretations

## References

- **James Legge Translation (1882)**: First complete English translation
- **Wilhelm/Baynes Translation (1950)**: Most influential Western version
- **Source extraction tools**: `tools/extractors/`
- **Data loading**: `pyching/data/loader.py`
- **Multi-source resolution**: `pyching/data/resolver.py`

For detailed implementation guide, see `tools/extractors/README.md`.
