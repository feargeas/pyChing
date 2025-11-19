# I Ching Hexagram Data

This directory contains comprehensive data resources for the 64 hexagrams of the I Ching (易經).

## Files

### `hexagrams.json`
Complete dataset of all 64 hexagrams including:
- **Number**: King Wen sequence (1-64)
- **Unicode**: Unicode character (U+4DC0 to U+4DFF)
- **Binary**: 6-digit binary representation (1=yang/solid, 0=yin/broken)
- **Chinese**: Traditional Chinese name
- **Pinyin**: Romanization using pinyin
- **Wade-Giles**: Wade-Giles romanization
- **English**: Common English translation
- **Trigrams**: Upper and lower trigram components
- **Binary Decimal**: Decimal value of binary representation

### `hexagram_lookup.py`
Python module for easy access to hexagram data. Provides:
- Lookup by number, unicode, binary, or trigrams
- Search by name (Chinese, pinyin, or English)
- Calculate opposite and nuclear hexagrams
- Format hexagrams for display

### `hexagram_svg.py`
SVG generator for creating visual representations of hexagrams. Features:
- Generate SVG for any hexagram
- Customizable styling (colors, dimensions)
- Batch generate all hexagrams
- Support for trigrams

### `svg/`
Directory containing pre-generated SVG files for all hexagrams and trigrams.

## Usage Examples

### Python Lookup

```python
from data.hexagram_lookup import HexagramData

# Initialize
data = HexagramData()

# Lookup by number
hex1 = data.get_by_number(1)
print(hex1['unicode'])  # ䷀
print(hex1['english'])  # The Creative

# Lookup by unicode character
hex_qian = data.get_by_unicode('䷀')

# Lookup by binary
hex_bin = data.get_by_binary('111111')

# Search by name
results = data.search_by_name('peace')

# Get by trigrams
hex_pi = data.get_by_trigrams('heaven', 'earth')

# Get opposite hexagram
opposite = data.get_opposite(1)  # Returns Hexagram 2 (Kun)

# Get nuclear hexagram
nuclear = data.get_nuclear(1)
```

### Generate SVG

```python
from data.hexagram_svg import HexagramSVG
from pathlib import Path

# Create generator
generator = HexagramSVG(
    line_width=100,
    line_height=8,
    stroke_color="#000000"
)

# Generate SVG for a specific hexagram
svg = generator.number_to_svg(1)
print(svg)

# Generate from binary
svg = generator.binary_to_svg('111111', title='Qian')

# Generate all hexagrams
output_dir = Path('output/svg')
generator.generate_all(output_dir)
```

### Command Line

```bash
# Generate all SVG files
python -m data.hexagram_svg

# Run lookup examples
python -m data.hexagram_lookup
```

## Data Structure

### Hexagram Object
```json
{
  "number": 1,
  "unicode": "䷀",
  "unicode_point": "U+4DC0",
  "binary": "111111",
  "chinese": "乾",
  "pinyin": "qián",
  "wade_giles": "ch'ien",
  "english": "The Creative",
  "upper_trigram": "heaven",
  "lower_trigram": "heaven",
  "binary_decimal": 63,
  "king_wen": 1
}
```

### Trigram Object
```json
{
  "binary": "111",
  "chinese": "乾",
  "pinyin": "qián",
  "attributes": ["creative", "strong", "father"]
}
```

## Unicode Information

The 64 hexagrams occupy the Unicode block **Yijing Hexagram Symbols** (U+4DC0–U+4DFF):
- First hexagram (☰☰ Qian): U+4DC0 ䷀
- Last hexagram (☲☵ Wei Ji): U+4DFF ䷿

## Binary Representation

Lines are read from bottom to top:
- `1` = Yang line (solid) ⚊
- `0` = Yin line (broken) ⚋

Example: Hexagram 1 (Qian) = `111111`
```
Line 6 (top):    1  ⚊
Line 5:          1  ⚊
Line 4:          1  ⚊
Line 3:          1  ⚊
Line 2:          1  ⚊
Line 1 (bottom): 1  ⚊
```

## The Eight Trigrams

| Name     | Binary | Character | Attributes           |
|----------|--------|-----------|----------------------|
| Heaven   | 111    | 乾 (qián)  | Creative, Father     |
| Earth    | 000    | 坤 (kūn)   | Receptive, Mother    |
| Thunder  | 001    | 震 (zhèn)  | Arousing, Eldest Son |
| Water    | 010    | 坎 (kǎn)   | Abysmal, Middle Son  |
| Mountain | 100    | 艮 (gèn)   | Stillness, Young Son |
| Wind     | 110    | 巽 (xùn)   | Gentle, Eldest Daughter |
| Fire     | 101    | 離 (lí)    | Clinging, Middle Daughter |
| Lake     | 011    | 兌 (duì)   | Joyous, Young Daughter |

## References

- [Wikipedia: List of hexagrams of the I Ching](https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching)
- [Unicode: Yijing Hexagram Symbols](https://unicode.org/charts/PDF/U4DC0.pdf)
- Wilhelm/Baynes Translation: *The I Ching or Book of Changes*

## License

This data is compiled from public sources and traditional I Ching texts. See the main project LICENSE file for details.
