"""
Test HexagramEngine functionality.

Tests the complete integration of Phase 2 (casting) and Phase 3 (data access).
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from pyching.core.engine import HexagramEngine
from pyching.casting.base import Element
from pyching.casting import WoodMethod, MetalMethod, FireMethod, EarthMethod


def test_engine_initialization():
    """Test engine initialization."""
    print("\n=== Testing Engine Initialization ===")

    # Default initialization
    engine = HexagramEngine()
    assert engine.registry is not None
    print(f"✓ Engine initialized with registry")

    # Check available methods
    methods = engine.get_available_methods()
    assert 'wood' in methods
    assert 'metal' in methods
    assert 'fire' in methods
    assert 'earth' in methods
    # Note: air might not be available if no network
    print(f"✓ Available methods: {methods}")


def test_cast_reading_basic():
    """Test basic reading casting."""
    print("\n=== Testing Basic Reading Casting ===")

    engine = HexagramEngine()

    # Cast with Wood method (default/original)
    reading = engine.cast_reading(
        method=Element.WOOD,
        question="Test question"
    )

    assert reading.primary is not None
    assert reading.primary.number >= 1
    assert reading.primary.number <= 64
    assert len(reading.primary.lines) == 6
    assert reading.question == "Test question"
    assert reading.method == "wood"
    print(f"✓ Cast reading: Hexagram {reading.primary.number}")
    print(f"  Lines: {reading.primary.lines}")
    print(f"  Moving lines: {reading.changing_lines}")


def test_cast_with_different_methods():
    """Test casting with all five element methods."""
    print("\n=== Testing Different Casting Methods ===")

    engine = HexagramEngine()

    # Wood method
    reading_wood = engine.cast_reading(Element.WOOD)
    assert reading_wood.method == "wood"
    print(f"✓ Wood method: Hexagram {reading_wood.primary.number}")

    # Metal method
    reading_metal = engine.cast_reading(Element.METAL)
    assert reading_metal.method == "metal"
    print(f"✓ Metal method: Hexagram {reading_metal.primary.number}")

    # Fire method
    reading_fire = engine.cast_reading(Element.FIRE)
    assert reading_fire.method == "fire"
    print(f"✓ Fire method: Hexagram {reading_fire.primary.number}")

    # Earth method (with seed)
    reading_earth = engine.cast_reading(Element.EARTH, seed="test_seed")
    assert reading_earth.method == "earth"
    print(f"✓ Earth method: Hexagram {reading_earth.primary.number}")


def test_earth_method_determinism():
    """Test that Earth method produces same results with same seed."""
    print("\n=== Testing Earth Method Determinism ===")

    engine = HexagramEngine()

    # Cast twice with same seed
    reading1 = engine.cast_reading(Element.EARTH, seed="my_question")
    reading2 = engine.cast_reading(Element.EARTH, seed="my_question")

    assert reading1.primary.number == reading2.primary.number
    assert reading1.primary.lines == reading2.primary.lines
    assert reading1.changing_lines == reading2.changing_lines
    print(f"✓ Same seed produces same hexagram: {reading1.primary.number}")
    print(f"  Lines: {reading1.primary.lines}")

    # Different seed produces different result (probably)
    reading3 = engine.cast_reading(Element.EARTH, seed="different_question")
    # Note: Could be same hexagram by chance, so we just verify it casts
    assert reading3.primary.number >= 1
    assert reading3.primary.number <= 64
    print(f"✓ Different seed: Hexagram {reading3.primary.number}")


def test_moving_lines_logic():
    """Test moving lines create relating hexagram."""
    print("\n=== Testing Moving Lines Logic ===")

    engine = HexagramEngine()

    # Cast multiple readings until we get one with moving lines
    for _ in range(100):  # Try up to 100 times
        reading = engine.cast_reading(Element.WOOD)

        if reading.has_moving_lines():
            assert reading.relating is not None
            assert reading.relating.number != reading.primary.number
            print(f"✓ Moving lines detected: {reading.primary.number} → {reading.relating.number}")
            print(f"  Changing lines: {reading.changing_lines}")

            # Verify transformation logic (6→7, 9→8)
            for i, (primary_line, relating_line) in enumerate(zip(reading.primary.lines, reading.relating.lines)):
                if primary_line == 6:
                    assert relating_line == 7, f"Line {i+1}: 6 should become 7"
                elif primary_line == 9:
                    assert relating_line == 8, f"Line {i+1}: 9 should become 8"
                else:
                    assert relating_line == primary_line, f"Line {i+1}: Stable lines should not change"
            print(f"✓ Transformation logic verified")
            break
    else:
        print(f"⚠ No moving lines in 100 casts (rare but possible)")


def test_source_selection():
    """Test using different interpretation sources."""
    print("\n=== Testing Source Selection ===")

    engine = HexagramEngine()

    # Canonical source (default)
    reading_canonical = engine.cast_reading(Element.METAL, source="canonical")
    assert reading_canonical.source_id == "canonical"
    assert reading_canonical.primary.source_id == "canonical"
    print(f"✓ Canonical source: {reading_canonical.primary.metadata.get('translator', 'Unknown')}")

    # Nonexistent source (falls back to canonical)
    reading_fallback = engine.cast_reading(Element.METAL, source="nonexistent")
    assert reading_fallback.source_id == "canonical"
    print(f"✓ Nonexistent source falls back to canonical")


def test_cast_hexagram():
    """Test casting single hexagram without full reading."""
    print("\n=== Testing cast_hexagram() ===")

    engine = HexagramEngine()

    hexagram, oracle_values = engine.cast_hexagram(Element.WOOD)

    assert hexagram.number >= 1
    assert hexagram.number <= 64
    assert len(hexagram.lines) == 6
    assert len(oracle_values) == 6  # One set of values per line
    print(f"✓ Cast hexagram: {hexagram.number} - {hexagram.english_name}")
    print(f"  Lines: {hexagram.lines}")


def test_check_method_available():
    """Test checking method availability."""
    print("\n=== Testing Method Availability ===")

    engine = HexagramEngine()

    # Wood method should always be available
    available, error = engine.check_method_available(Element.WOOD)
    assert available
    assert error is None
    print(f"✓ Wood method available")

    # Metal method should always be available
    available, error = engine.check_method_available(Element.METAL)
    assert available
    print(f"✓ Metal method available")

    # Air method might not be available (network required)
    available, error = engine.check_method_available(Element.AIR)
    if available:
        print(f"✓ Air method available (network connected)")
    else:
        print(f"✓ Air method unavailable: {error}")


def test_oracle_values_preservation():
    """Test that oracle values are preserved in reading."""
    print("\n=== Testing Oracle Values Preservation ===")

    engine = HexagramEngine()

    reading = engine.cast_reading(Element.WOOD)

    # Should have 6 sets of oracle values (one per line)
    assert len(reading.oracle_values) == 6
    print(f"✓ Oracle values preserved: {len(reading.oracle_values)} lines")

    # Each line should have oracle values (for Wood/Metal/Fire methods)
    for i, values in enumerate(reading.oracle_values):
        if values:  # Some methods might not provide values
            # For coin method, should be 3 values each 2 or 3
            if reading.method in ['wood', 'metal', 'fire']:
                assert len(values) == 3
                assert all(v in [2, 3] for v in values)
    print(f"✓ Oracle values format correct for {reading.method} method")


def test_line_value_validation():
    """Test that line values are always valid (6, 7, 8, or 9)."""
    print("\n=== Testing Line Value Validation ===")

    engine = HexagramEngine()

    # Cast multiple readings
    for method in [Element.WOOD, Element.METAL, Element.FIRE]:
        reading = engine.cast_reading(method)

        # All line values must be 6, 7, 8, or 9
        for i, line in enumerate(reading.primary.lines):
            assert line in [6, 7, 8, 9], f"Invalid line value {line} at position {i+1}"

        print(f"✓ {method.value} method: all lines valid")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("HEXAGRAM ENGINE TESTS")
    print("=" * 70)

    try:
        test_engine_initialization()
        test_cast_reading_basic()
        test_cast_with_different_methods()
        test_earth_method_determinism()
        test_moving_lines_logic()
        test_source_selection()
        test_cast_hexagram()
        test_check_method_available()
        test_oracle_values_preservation()
        test_line_value_validation()

        print("\n" + "=" * 70)
        print("ALL TESTS PASSED!")
        print("=" * 70)

        return True
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
