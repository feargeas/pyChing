#!/usr/bin/env python3
"""
Test data loading from JSON files.

This demonstrates the basic data access patterns for the new
JSON-based hexagram data.
"""

import json
import sys
from pathlib import Path


def load_hexagram(hex_num, data_dir):
    """Load a hexagram by number."""
    hex_file = data_dir / 'hexagrams' / f"hexagram_{hex_num:02d}.json"

    with open(hex_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_mappings(data_dir):
    """Load mapping tables."""
    mappings_file = data_dir / 'mappings.json'

    with open(mappings_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_sources_metadata(data_dir):
    """Load sources metadata."""
    sources_file = data_dir / 'sources_metadata.json'

    with open(sources_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def display_hexagram_summary(hex_data):
    """Display a summary of hexagram data."""
    canonical = hex_data['canonical']

    print(f"Hexagram {hex_data['number']}: {canonical['name']} / {canonical['english_name']}")
    print(f"Binary: {hex_data['binary']}")
    print(f"Trigrams: {hex_data['trigrams']['upper']} over {hex_data['trigrams']['lower']}")
    print()
    print("Judgment:")
    print(f"  {canonical['judgment']}")
    print()
    print("Image:")
    print(f"  {canonical['image']}")
    print()
    print("Lines:")
    for line_num in range(1, 7):
        line = canonical['lines'][str(line_num)]
        print(f"  {line['position']} ({line['type']}): {line['text'][:60]}...")
    print()


def test_loading():
    """Test all loading functions."""
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data'

    print("=" * 70)
    print("TESTING DATA LOADING")
    print("=" * 70)
    print()

    # Test mappings
    print("Loading mappings...")
    mappings = load_mappings(data_dir)
    print(f"  ✓ Loaded {len(mappings['number_to_id'])} hexagram mappings")
    print(f"  ✓ Loaded {len(mappings['trigrams'])} trigram definitions")
    print()

    # Test sources metadata
    print("Loading sources metadata...")
    sources = load_sources_metadata(data_dir)
    print(f"  ✓ Loaded {len(sources['sources'])} source definitions")
    print(f"  ✓ Canonical source: {[s for s, d in sources['sources'].items() if d.get('canonical')]}")
    print()

    # Test hexagram loading
    print("Loading hexagram data...")
    print()

    for hex_num in [1, 2, 64]:
        print("-" * 70)
        hex_data = load_hexagram(hex_num, data_dir)
        display_hexagram_summary(hex_data)

    print("=" * 70)
    print("✓ All data loading tests passed!")
    print("=" * 70)


def demo_lookup_by_binary():
    """Demonstrate looking up hexagram by binary pattern."""
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data'

    print()
    print("=" * 70)
    print("DEMO: LOOKUP BY BINARY PATTERN")
    print("=" * 70)
    print()

    mappings = load_mappings(data_dir)

    # Example: look up hexagram with pattern 111111 (all yang)
    binary = "111111"
    hex_id = mappings['binary_to_id'][binary]
    hex_num = int(hex_id.split('_')[1])

    print(f"Binary pattern: {binary} (all yang lines)")
    print(f"Hexagram ID: {hex_id}")
    print()

    hex_data = load_hexagram(hex_num, data_dir)
    canonical = hex_data['canonical']

    print(f"Result: Hexagram {hex_num} - {canonical['name']} / {canonical['english_name']}")
    print()


def demo_lookup_by_trigrams():
    """Demonstrate looking up hexagram by trigram pair."""
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data'

    print()
    print("=" * 70)
    print("DEMO: LOOKUP BY TRIGRAM PAIR")
    print("=" * 70)
    print()

    mappings = load_mappings(data_dir)

    # Example: Fire over Water (hexagram 64, which we have)
    trigram_pair = "li_kan"
    hex_id = mappings['trigram_pairs_to_id'][trigram_pair]
    hex_num = int(hex_id.split('_')[1])

    upper = mappings['trigrams']['li']['name']
    lower = mappings['trigrams']['kan']['name']

    print(f"Trigrams: {upper} over {lower}")
    print(f"Pair key: {trigram_pair}")
    print(f"Hexagram ID: {hex_id}")
    print()

    hex_data = load_hexagram(hex_num, data_dir)
    canonical = hex_data['canonical']

    print(f"Result: Hexagram {hex_num} - {canonical['name']} / {canonical['english_name']}")
    print()


def main():
    """Run all tests and demos."""
    try:
        test_loading()
        demo_lookup_by_binary()
        demo_lookup_by_trigrams()
        return 0
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
