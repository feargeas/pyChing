"""
I Ching Hexagram Data Lookup Module

Provides easy access to hexagram information including unicode characters,
Chinese names, translations, and binary representations.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Union


class HexagramData:
    """Class for accessing I Ching hexagram data."""

    def __init__(self, data_file: Optional[Path] = None):
        """Initialize hexagram data from JSON file."""
        if data_file is None:
            data_file = Path(__file__).parent / "hexagrams.json"

        with open(data_file, 'r', encoding='utf-8') as f:
            self._data = json.load(f)

        self.hexagrams = self._data['hexagrams']
        self.trigrams = self._data['trigrams']

        # Create lookup indices
        self._by_number = {h['number']: h for h in self.hexagrams}
        self._by_unicode = {h['unicode']: h for h in self.hexagrams}
        self._by_binary = {h['binary']: h for h in self.hexagrams}
        self._by_king_wen = {h['king_wen']: h for h in self.hexagrams}

    def get_by_number(self, number: int) -> Optional[Dict]:
        """Get hexagram by King Wen sequence number (1-64)."""
        return self._by_number.get(number)

    def get_by_unicode(self, unicode_char: str) -> Optional[Dict]:
        """Get hexagram by unicode character (e.g., '䷀')."""
        return self._by_unicode.get(unicode_char)

    def get_by_binary(self, binary: str) -> Optional[Dict]:
        """Get hexagram by binary string (e.g., '111111')."""
        return self._by_binary.get(binary)

    def get_by_trigrams(self, upper: str, lower: str) -> Optional[Dict]:
        """Get hexagram by upper and lower trigram names."""
        for hexagram in self.hexagrams:
            if (hexagram['upper_trigram'] == upper.lower() and
                hexagram['lower_trigram'] == lower.lower()):
                return hexagram
        return None

    def get_trigram(self, name: str) -> Optional[Dict]:
        """Get trigram information by name."""
        return self.trigrams.get(name.lower())

    def search_by_name(self, query: str) -> List[Dict]:
        """Search hexagrams by Chinese, pinyin, or English name."""
        query = query.lower()
        results = []
        for hexagram in self.hexagrams:
            if (query in hexagram['chinese'].lower() or
                query in hexagram['pinyin'].lower() or
                query in hexagram['english'].lower()):
                results.append(hexagram)
        return results

    def get_opposite(self, number: int) -> Optional[Dict]:
        """Get the opposite hexagram (all lines inverted)."""
        hexagram = self.get_by_number(number)
        if not hexagram:
            return None

        # Invert binary
        binary = hexagram['binary']
        inverted = ''.join('1' if b == '0' else '0' for b in binary)
        return self.get_by_binary(inverted)

    def get_nuclear(self, number: int) -> Optional[Dict]:
        """Get the nuclear hexagram (inner hexagram)."""
        hexagram = self.get_by_number(number)
        if not hexagram:
            return None

        binary = hexagram['binary']
        # Nuclear hexagram uses lines 2,3,4 for lower and 3,4,5 for upper
        nuclear_binary = binary[1:4] + binary[2:5]
        return self.get_by_binary(nuclear_binary)

    def get_all(self) -> List[Dict]:
        """Get all hexagrams."""
        return self.hexagrams

    def get_unicode_range(self) -> str:
        """Get the unicode range for I Ching hexagrams."""
        return "U+4DC0 to U+4DFF"

    def format_hexagram(self, hexagram: Dict, style: str = 'full') -> str:
        """
        Format hexagram information as a string.

        Args:
            hexagram: Hexagram dictionary
            style: 'full', 'compact', or 'minimal'
        """
        if style == 'minimal':
            return f"{hexagram['number']}. {hexagram['unicode']} {hexagram['english']}"

        elif style == 'compact':
            return (f"{hexagram['number']}. {hexagram['unicode']} "
                   f"{hexagram['chinese']} ({hexagram['pinyin']}) - "
                   f"{hexagram['english']}")

        else:  # full
            return f"""
Hexagram {hexagram['number']}: {hexagram['english']}
Unicode: {hexagram['unicode']} ({hexagram['unicode_point']})
Chinese: {hexagram['chinese']}
Pinyin: {hexagram['pinyin']}
Wade-Giles: {hexagram['wade_giles']}
Binary: {hexagram['binary']}
Trigrams: {hexagram['upper_trigram'].title()} over {hexagram['lower_trigram'].title()}
""".strip()


# Convenience functions
_default_data = None

def get_data() -> HexagramData:
    """Get the default HexagramData instance."""
    global _default_data
    if _default_data is None:
        _default_data = HexagramData()
    return _default_data


def lookup(identifier: Union[int, str]) -> Optional[Dict]:
    """
    Lookup hexagram by various identifiers.

    Args:
        identifier: Can be:
            - int: King Wen number (1-64)
            - str: Unicode character, binary string, or name query
    """
    data = get_data()

    if isinstance(identifier, int):
        return data.get_by_number(identifier)

    elif isinstance(identifier, str):
        # Try unicode character
        if len(identifier) == 1 and ord(identifier) >= 0x4DC0:
            return data.get_by_unicode(identifier)

        # Try binary
        if len(identifier) == 6 and all(c in '01' for c in identifier):
            return data.get_by_binary(identifier)

        # Try name search
        results = data.search_by_name(identifier)
        return results[0] if results else None

    return None


def get_hexagram_unicode(number: int) -> str:
    """Get the unicode character for a hexagram number."""
    hexagram = lookup(number)
    return hexagram['unicode'] if hexagram else ''


def binary_to_hexagram(binary: str) -> Optional[Dict]:
    """Convert binary string to hexagram."""
    return get_data().get_by_binary(binary)


def trigrams_to_hexagram(upper: str, lower: str) -> Optional[Dict]:
    """Get hexagram from trigram names."""
    return get_data().get_by_trigrams(upper, lower)


if __name__ == '__main__':
    # Example usage
    data = HexagramData()

    print("=== I Ching Hexagram Lookup Examples ===\n")

    # Lookup by number
    hex1 = data.get_by_number(1)
    print(data.format_hexagram(hex1, 'compact'))

    # Lookup by unicode
    hex_unicode = data.get_by_unicode('䷀')
    print(f"\nUnicode lookup: {hex_unicode['english']}")

    # Lookup by binary
    hex_binary = data.get_by_binary('111111')
    print(f"Binary lookup: {hex_binary['english']}")

    # Search by name
    results = data.search_by_name('peace')
    print(f"\nSearch 'peace': {results[0]['english']}")

    # Trigram lookup
    hex_trig = data.get_by_trigrams('heaven', 'earth')
    print(f"Heaven over Earth: {hex_trig['english']}")

    # Get opposite
    opposite = data.get_opposite(1)
    print(f"\nOpposite of Hexagram 1: {opposite['english']}")

    # Print all hexagrams
    print("\n=== All 64 Hexagrams ===")
    for h in data.get_all():
        print(f"{h['number']:2d}. {h['unicode']} {h['english']}")
