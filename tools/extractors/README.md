# Source Extractor Framework

This framework provides a flexible, extensible system for extracting I Ching hexagram data from various sources and formats.

## Architecture

The extractor framework consists of:

1. **Base Classes** (`base.py`)
   - `BaseExtractor`: Abstract base class for all extractors
   - `SourceMetadata`: Metadata container for sources
   - `HexagramData`: Format-agnostic data structure

2. **Registry** (`registry.py`)
   - `ExtractorRegistry`: Central registry for discovering and instantiating extractors
   - Decorator-based registration system

3. **Validator** (`validator.py`)
   - `YAMLValidator`: Schema validation for extracted YAML files
   - Comprehensive error and warning reporting

4. **Concrete Extractors** (e.g., `wilhelm.py`)
   - Source-specific extraction logic
   - Auto-registered with the registry

## Adding a New Source

### Step 1: Prepare Source Files

Place source files in `data/sources/{source_id}/`:

```
data/sources/
├── wilhelm/
│   └── wilhelm.md
├── dekorne/
│   └── Hexagram 01.doc
│   └── Hexagram 02.doc
│   └── ...
└── your_source/
    └── [your source files]
```

### Step 2: Create Extractor Class

Create a new file `tools/extractors/your_source.py`:

```python
#!/usr/bin/env python3
"""
Your Source Name extractor.

Description of the source and format.
"""

from pathlib import Path
from typing import Optional

from .base import BaseExtractor, SourceMetadata, HexagramData
from .registry import ExtractorRegistry


# Define source metadata
YOUR_SOURCE_METADATA = SourceMetadata(
    source_id='your_source',
    name='Full Source Name',
    translator='Translator Name',
    year=2000,
    language='en',
    description='Description of this translation/interpretation',
    source_url='https://example.com/source',
    license='Public Domain',  # or other
    notes='Any additional notes'
)


# Register with decorator
@ExtractorRegistry.register('your_source', YOUR_SOURCE_METADATA)
class YourSourceExtractor(BaseExtractor):
    """
    Extractor for Your Source.

    Describe the expected file format and structure.
    """

    def __init__(self, source_dir: Path, metadata: SourceMetadata = YOUR_SOURCE_METADATA):
        super().__init__(source_dir, metadata)

        # Initialize your extractor
        # - Load files
        # - Parse format
        # - Set up any required state

    def extract_hexagram(self, hexagram_number: int) -> Optional[HexagramData]:
        """
        Extract data for a single hexagram.

        Args:
            hexagram_number: Hexagram number (1-64)

        Returns:
            HexagramData object or None if extraction failed
        """
        # Your extraction logic here
        # Parse the source file(s)
        # Extract: chinese_name, english_name, judgment, image, lines

        # Return HexagramData
        return HexagramData(
            hexagram_number=hexagram_number,
            chinese_name='Ch\'ien',
            english_name='The Creative',
            judgment='[extracted judgment text]',
            image='[extracted image text]',
            lines={
                '1': {'position': 'bottom', 'type': 'nine', 'text': '[line 1]'},
                '2': {'position': 'second', 'type': 'nine', 'text': '[line 2]'},
                '3': {'position': 'third', 'type': 'nine', 'text': '[line 3]'},
                '4': {'position': 'fourth', 'type': 'nine', 'text': '[line 4]'},
                '5': {'position': 'fifth', 'type': 'nine', 'text': '[line 5]'},
                '6': {'position': 'topmost', 'type': 'nine', 'text': '[line 6]'},
            },
            all_lines_changing=None  # Optional, only for hexagrams 1 and 2
        )

    def validate_source_files(self) -> bool:
        """
        Validate that required source files exist.

        Returns:
            True if all required files are present
        """
        # Check that your source files exist
        # Return True if valid, False otherwise
        pass
```

### Step 3: Import in __init__.py

Update `tools/extractors/__init__.py` to import your extractor:

```python
from .your_source import YourSourceExtractor  # noqa
```

This ensures your extractor is registered when the module is imported.

### Step 4: Update extract_source.py

Import your extractor in `tools/extract_source.py`:

```python
from tools.extractors.your_source import YourSourceExtractor  # noqa
```

### Step 5: Extract and Validate

```bash
# List available sources (should include yours)
python tools/extract_source.py --list

# Extract all hexagrams
python tools/extract_source.py your_source --all

# Validate extracted YAML
python tools/extract_source.py your_source --validate
```

## Format-Specific Tips

### HTML Sources

Use `BeautifulSoup` or `lxml` for parsing:

```python
from bs4 import BeautifulSoup

def extract_hexagram(self, hexagram_number: int):
    html_file = self.source_dir / f'hexagram_{hexagram_number}.html'
    with open(html_file, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Extract using CSS selectors or tag navigation
    judgment = soup.find('div', class_='judgment').get_text()
    # ...
```

### Markdown Sources

See `wilhelm.py` for a complete example using regex patterns.

### Word Documents (.doc, .docx)

Use `python-docx` (for .docx) or `antiword` (for .doc):

```python
from docx import Document

def extract_hexagram(self, hexagram_number: int):
    doc_file = self.source_dir / f'Hexagram {hexagram_number:02d}.docx'
    doc = Document(doc_file)

    # Extract from paragraphs
    for para in doc.paragraphs:
        # Parse structure
        pass
```

For old `.doc` format, convert to text first:
```bash
antiword "Hexagram 01.doc" > hexagram_01.txt
```

### PDF Sources

Use `PyPDF2` or `pdfplumber`:

```python
import pdfplumber

def extract_hexagram(self, hexagram_number: int):
    with pdfplumber.open(self.source_dir / 'source.pdf') as pdf:
        # Find pages for this hexagram
        # Extract text
        pass
```

## YAML Output Format

All extractors must produce YAML files with this structure:

```yaml
metadata:
  hexagram: 1
  king_wen_sequence: 1
  fu_xi_sequence: 1
  binary: '111111'
  source: your_source
  translator: Translator Name
  year: 2000
  language: en
  verified: false

name: Ch'ien
english_name: The Creative
title: 1. Ch'ien / The Creative

trigrams:
  upper: qian
  lower: qian

judgment: |
  Multi-line judgment text.

  Can contain multiple paragraphs.

image: |
  Multi-line image text.

lines:
  '1':
    position: bottom
    type: nine
    text: Line 1 interpretation text
  '2':
    position: second
    type: nine
    text: Line 2 interpretation text
  # ... through line 6

# Optional: only for hexagrams 1 and 2
all_lines_changing: |
  Special commentary when all lines are changing.
```

## Validation

The `YAMLValidator` checks for:

- **Required fields**: metadata, name, judgment, image, lines, etc.
- **Metadata completeness**: hexagram number, source, translator, year, etc.
- **Line completeness**: All 6 lines with position, type, and text
- **Content quality**: No placeholders, reasonable text lengths
- **Type correctness**: Proper data types for all fields

Run validation:

```bash
python tools/extract_source.py your_source --validate
```

Strict mode (warnings become errors):

```bash
python tools/extract_source.py your_source --validate --strict
```

## Testing

Test your extractor:

```python
# Test single hexagram
python tools/extract_source.py your_source --hexagram 1

# Test all hexagrams
python tools/extract_source.py your_source --all

# Validate
python tools/extract_source.py your_source --validate
```

## Best Practices

1. **Handle Encoding**: Always use `encoding='utf-8'` when reading files
2. **Error Handling**: Return `None` from `extract_hexagram()` on failure
3. **Clean Text**: Remove artifacts from source format (HTML tags, markdown links, etc.)
4. **Preserve Structure**: Maintain paragraph breaks with `\n\n`
5. **Normalize Names**: Handle variant spellings (Ch'ien, Qian, etc.)
6. **Document Format**: Add docstrings explaining source format expectations
7. **Verify Output**: Always validate extracted YAML before committing

## Example: Wilhelm Extractor

See `wilhelm.py` for a complete, working example of:
- Markdown parsing with regex
- Section extraction
- Line parsing with multiple patterns
- Artifact cleaning
- Special handling for hexagrams 1 and 2

## Troubleshooting

**Extractor not found**:
- Ensure you imported it in `__init__.py` or `extract_source.py`
- Check that `@ExtractorRegistry.register()` decorator is present

**Validation failures**:
- Check field names match exactly
- Ensure all 6 lines are present with keys '1' through '6'
- Verify metadata fields are correct types (int, bool, etc.)

**Encoding errors**:
- Use `encoding='utf-8'` for file operations
- Check source file encoding with `file -i filename`

**Import errors**:
- Ensure `tools/extractors/` has `__init__.py`
- Check Python path includes project root
