#!/usr/bin/env python3
"""
Example usage of the I Ching hexagram data package.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from data import HexagramData, lookup, get_hexagram_unicode
from data import HexagramSVG


def main():
    print("=" * 60)
    print("I Ching Hexagram Data - Usage Examples")
    print("=" * 60)

    # Initialize data
    data = HexagramData()

    # Example 1: Lookup by number
    print("\n1. Lookup by King Wen Number:")
    hex1 = data.get_by_number(1)
    print(data.format_hexagram(hex1, 'compact'))

    # Example 2: Lookup by unicode
    print("\n2. Lookup by Unicode Character:")
    hex_unicode = data.get_by_unicode('䷀')
    print(f"   {hex_unicode['unicode']} = {hex_unicode['english']}")

    # Example 3: Lookup by binary
    print("\n3. Lookup by Binary:")
    hex_binary = data.get_by_binary('111111')
    print(f"   Binary 111111 = {hex_binary['english']}")

    # Example 4: Search by name
    print("\n4. Search by Name:")
    results = data.search_by_name('peace')
    for result in results:
        print(f"   {result['number']:2d}. {result['unicode']} {result['english']}")

    # Example 5: Lookup by trigrams
    print("\n5. Lookup by Trigrams:")
    hex_trig = data.get_by_trigrams('heaven', 'earth')
    print(f"   Heaven over Earth = {hex_trig['english']}")

    # Example 6: Get opposite hexagram
    print("\n6. Opposite Hexagrams:")
    opposite = data.get_opposite(1)
    print(f"   Opposite of {hex1['english']} is {opposite['english']}")
    print(f"   {hex1['unicode']} ↔ {opposite['unicode']}")

    # Example 7: Get nuclear hexagram
    print("\n7. Nuclear Hexagram:")
    nuclear = data.get_nuclear(11)
    hex11 = data.get_by_number(11)
    print(f"   Nuclear of {hex11['english']} is {nuclear['english']}")

    # Example 8: Display all trigrams
    print("\n8. The Eight Trigrams:")
    for name, trigram in data.trigrams.items():
        print(f"   {name.title():10s} {trigram['chinese']} ({trigram['pinyin']:5s}) - {trigram['binary']}")

    # Example 9: Unicode convenience function
    print("\n9. Unicode Quick Lookup:")
    for i in [1, 2, 11, 12, 29, 30, 63, 64]:
        char = get_hexagram_unicode(i)
        print(f"   Hexagram {i:2d}: {char}")

    # Example 10: Display first 10 hexagrams
    print("\n10. First 10 Hexagrams:")
    for h in data.get_all()[:10]:
        print(f"    {h['number']:2d}. {h['unicode']} {h['chinese']:3s} "
              f"{h['pinyin']:12s} - {h['english']}")

    # Example 11: Generate SVG examples
    print("\n11. SVG Generation:")
    generator = HexagramSVG()

    # Generate SVG for Hexagram 1
    svg = generator.number_to_svg(1)
    print(f"    SVG length for Hexagram 1: {len(svg)} bytes")

    # Show binary representation
    print("\n12. Binary Representations (bottom to top):")
    examples = [1, 2, 11, 12]
    for num in examples:
        h = data.get_by_number(num)
        print(f"    {num:2d}. {h['unicode']} {h['english']:20s} = {h['binary']}")

    print("\n" + "=" * 60)
    print(f"Total hexagrams: {len(data.get_all())}")
    print(f"Unicode range: {data.get_unicode_range()}")
    print("=" * 60)


if __name__ == '__main__':
    main()
