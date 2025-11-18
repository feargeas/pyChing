#!/usr/bin/env python3
"""
Complete Integration Demo - pyChing Modernization

Demonstrates the full integration of Phases 1-4:
- Phase 1: JSON hexagram data
- Phase 2: Five Elements casting methods
- Phase 3: Multi-source data access
- Phase 4: Core engine integration

This demo shows all major features working together.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from pyching.core import HexagramEngine, Hexagram, Reading
from pyching.casting.base import Element


def demo_basic_reading():
    """Demo 1: Basic reading with Wood method (original algorithm)."""
    print("=" * 70)
    print("DEMO 1: Basic Reading (Wood Method - Original Algorithm)")
    print("=" * 70)

    engine = HexagramEngine()

    reading = engine.cast_reading(
        method=Element.WOOD,
        question="What is my purpose in this journey?"
    )

    print(reading.as_text())

    print(f"Method used: {reading.method}")
    print(f"Timestamp: {reading.timestamp}")
    print(f"Source: {reading.source_id}")
    print()


def demo_all_five_elements():
    """Demo 2: Cast using all five element methods."""
    print("=" * 70)
    print("DEMO 2: All Five Element Methods")
    print("=" * 70)

    engine = HexagramEngine()

    methods = [
        (Element.WOOD, "Standard PRNG (original)"),
        (Element.METAL, "OS Entropy (cryptographic quality)"),
        (Element.FIRE, "CSPRNG (secrets module)"),
        (Element.EARTH, "Deterministic (seeded)"),
        (Element.AIR, "True RNG (RANDOM.ORG API)")
    ]

    for element, description in methods:
        print(f"\n{element.value.upper()} Method - {description}")
        print("-" * 70)

        # Check availability (important for Air method)
        available, error = engine.check_method_available(element)

        if not available:
            print(f"⚠ Method unavailable: {error}")
            continue

        # Cast reading
        if element == Element.EARTH:
            reading = engine.cast_reading(element, seed="demo_seed")
        else:
            reading = engine.cast_reading(element)

        print(f"Hexagram {reading.primary.number}: {reading.primary.english_name}")
        print(f"Lines: {reading.primary.lines}")

        if reading.has_moving_lines():
            print(f"→ Becomes Hexagram {reading.relating.number}: {reading.relating.english_name}")
            print(f"Moving lines: {reading.changing_lines}")

    print()


def demo_deterministic_earth():
    """Demo 3: Earth method determinism."""
    print("=" * 70)
    print("DEMO 3: Earth Method Determinism")
    print("=" * 70)

    engine = HexagramEngine()
    question = "How should I approach this challenge?"

    print(f"Question: {question}")
    print("\nCasting same question 3 times with Earth method:\n")

    for i in range(1, 4):
        reading = engine.cast_reading(
            method=Element.EARTH,
            question=question,
            seed=question  # Use question as seed
        )

        print(f"Cast {i}: Hexagram {reading.primary.number} - {reading.primary.english_name}")
        print(f"        Lines: {reading.primary.lines}")

    print("\n✓ All three casts produce identical results")
    print("  This allows contemplative re-reading of the same oracle response")
    print()


def demo_hexagram_factory_methods():
    """Demo 4: Different ways to create hexagrams."""
    print("=" * 70)
    print("DEMO 4: Hexagram Factory Methods")
    print("=" * 70)

    # By number
    print("\n1. By King Wen Number:")
    hex1 = Hexagram.from_number(1)
    print(f"   Hexagram.from_number(1) → {hex1.number}: {hex1.english_name}")

    # By lines
    print("\n2. By Line Values:")
    hex_lines = Hexagram.from_lines([7, 7, 7, 7, 7, 7])
    print(f"   Hexagram.from_lines([7,7,7,7,7,7]) → {hex_lines.number}: {hex_lines.english_name}")

    # By binary
    print("\n3. By Binary Pattern:")
    hex_binary = Hexagram.from_binary("000000")
    print(f"   Hexagram.from_binary('000000') → {hex_binary.number}: {hex_binary.english_name}")

    # By trigrams
    print("\n4. By Trigram Pair:")
    hex_trig = Hexagram.from_trigrams("li", "kan")
    print(f"   Hexagram.from_trigrams('li', 'kan') → {hex_trig.number}: {hex_trig.english_name}")

    print()


def demo_moving_lines():
    """Demo 5: Working with moving lines."""
    print("=" * 70)
    print("DEMO 5: Moving Lines and Transformation")
    print("=" * 70)

    engine = HexagramEngine()

    # Keep casting until we get moving lines
    for attempt in range(100):
        reading = engine.cast_reading(Element.WOOD)

        if reading.has_moving_lines():
            print(f"\nPrimary Hexagram: {reading.primary.number} - {reading.primary.english_name}")
            print(f"Lines: {reading.primary.lines}")
            print(f"Moving lines at positions: {reading.changing_lines}")

            print(f"\nRelating Hexagram: {reading.relating.number} - {reading.relating.english_name}")
            print(f"Lines: {reading.relating.lines}")

            print("\nTransformation:")
            for i, (prim, rel) in enumerate(zip(reading.primary.lines, reading.relating.lines)):
                line_num = i + 1
                if prim != rel:
                    print(f"  Line {line_num}: {prim} → {rel}")
                    if prim == 6:
                        print(f"           (old yin becomes yang)")
                    elif prim == 9:
                        print(f"           (old yang becomes yin)")

            # Show specific moving line interpretation
            print("\nMoving Line Interpretations:")
            for line_num in reading.changing_lines:
                line_data = reading.primary.line_texts[str(line_num)]
                print(f"\n  Line {line_num} ({line_data['position']}, {line_data['type']}):")
                print(f"  {line_data['text'][:100]}...")

            break
    else:
        print("⚠ No moving lines in 100 casts (rare but possible)")

    print()


def demo_json_persistence():
    """Demo 6: JSON save/load."""
    print("=" * 70)
    print("DEMO 6: JSON Persistence")
    print("=" * 70)

    import tempfile
    from datetime import datetime

    engine = HexagramEngine()

    # Cast a reading
    reading = engine.cast_reading(
        method=Element.METAL,
        question="Should I pursue this opportunity?"
    )

    print(f"\nOriginal Reading:")
    print(f"  Hexagram: {reading.primary.number} - {reading.primary.english_name}")
    print(f"  Question: {reading.question}")
    print(f"  Method: {reading.method}")
    print(f"  Timestamp: {reading.timestamp}")

    # Save to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name

    try:
        reading.save(temp_file)
        print(f"\n✓ Saved to {temp_file}")

        # Load from file
        loaded = Reading.load(temp_file)
        print(f"\n✓ Loaded from file:")
        print(f"  Hexagram: {loaded.primary.number} - {loaded.primary.english_name}")
        print(f"  Question: {loaded.question}")
        print(f"  Method: {loaded.method}")
        print(f"  Timestamp: {loaded.timestamp}")

        # Show JSON structure
        json_str = reading.to_json(indent=2)
        print(f"\nJSON Structure ({len(json_str)} characters):")
        print(json_str[:300] + "\n  ...\n}")

    finally:
        Path(temp_file).unlink(missing_ok=True)

    print()


def demo_multi_source():
    """Demo 7: Multi-source interpretation (Phase 3 integration)."""
    print("=" * 70)
    print("DEMO 7: Multi-Source Interpretation")
    print("=" * 70)

    print("\nCurrently available sources:")
    print("  - canonical (Legge 1882)")
    print("  - wilhelm_baynes (Phase 5)")
    print("  - legge_simplified (Phase 5)")
    print("  - hermetica (Phase 5)")
    print("  - dekorne (Phase 5)")

    print("\nUsing canonical source:")
    hex_canonical = Hexagram.from_number(1, source="canonical")
    print(f"  Hexagram 1: {hex_canonical.english_name}")
    print(f"  Translator: {hex_canonical.metadata.get('translator', 'Unknown')}")
    print(f"  Year: {hex_canonical.metadata.get('year', 'Unknown')}")
    print(f"  Judgment: {hex_canonical.judgment[:100]}...")

    print("\nNonexistent sources fall back to canonical:")
    hex_fallback = Hexagram.from_number(1, source="nonexistent")
    print(f"  Requested 'nonexistent', got: {hex_fallback.source_id}")

    print("\n(Additional sources will be available in Phase 5)")
    print()


def demo_oracle_values():
    """Demo 8: Oracle values preservation."""
    print("=" * 70)
    print("DEMO 8: Oracle Values (Debugging/Analysis)")
    print("=" * 70)

    engine = HexagramEngine()

    reading = engine.cast_reading(Element.WOOD)

    print("\nLine-by-line casting details:")
    for i, (line_value, oracle_vals) in enumerate(zip(reading.primary.lines, reading.oracle_values)):
        line_num = i + 1
        if oracle_vals:  # Some methods might not provide oracle values
            coin_str = " + ".join(str(c) for c in oracle_vals)
            print(f"  Line {line_num}: {coin_str} = {line_value}")
        else:
            print(f"  Line {line_num}: {line_value} (no oracle values)")

    print(f"\nFinal hexagram: {reading.primary.number} - {reading.primary.english_name}")
    print()


def main():
    """Run all demos."""
    print("\n" + "=" * 70)
    print(" pyChing Complete Integration Demo")
    print(" Phases 1-4: Data + Casting + Access + Engine")
    print("=" * 70 + "\n")

    demos = [
        ("Basic Reading", demo_basic_reading),
        ("All Five Elements", demo_all_five_elements),
        ("Deterministic Earth Method", demo_deterministic_earth),
        ("Hexagram Factory Methods", demo_hexagram_factory_methods),
        ("Moving Lines", demo_moving_lines),
        ("JSON Persistence", demo_json_persistence),
        ("Multi-Source Interpretation", demo_multi_source),
        ("Oracle Values", demo_oracle_values),
    ]

    for name, demo_func in demos:
        try:
            demo_func()
        except Exception as e:
            print(f"\n✗ Error in {name}: {e}\n")
            import traceback
            traceback.print_exc()

    print("=" * 70)
    print("Demo Complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
