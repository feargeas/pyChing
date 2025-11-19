"""
Test Hexagram dataclass functionality.

Tests the modern Hexagram class with Phase 3 integration.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from pyching.core.hexagram import Hexagram


def test_from_number():
    """Test creating hexagram from number."""
    print("\n=== Testing Hexagram.from_number() ===")

    # Test hexagram 1
    hex1 = Hexagram.from_number(1)
    assert hex1.number == 1
    assert hex1.english_name == "The Creative"
    assert hex1.binary == "111111"
    assert hex1.trigrams == {"upper": "qian", "lower": "qian"}
    assert len(hex1.judgment) > 0
    assert len(hex1.image) > 0
    assert hex1.source_id == "canonical"
    print(f"✓ Hexagram 1: {hex1.english_name}")

    # Test hexagram 2
    hex2 = Hexagram.from_number(2)
    assert hex2.number == 2
    assert hex2.english_name == "The Receptive"
    print(f"✓ Hexagram 2: {hex2.english_name}")

    # Test hexagram 64
    hex64 = Hexagram.from_number(64)
    assert hex64.number == 64
    assert hex64.english_name == "Before The Achievement"
    print(f"✓ Hexagram 64: {hex64.english_name}")


def test_from_lines():
    """Test creating hexagram from line values."""
    print("\n=== Testing Hexagram.from_lines() ===")

    # All yang (hexagram 1)
    hex1 = Hexagram.from_lines([7, 7, 7, 7, 7, 7])
    assert hex1.number == 1
    assert hex1.lines == [7, 7, 7, 7, 7, 7]
    print(f"✓ Lines [7,7,7,7,7,7]: Hexagram {hex1.number}")

    # All yin (hexagram 2)
    hex2 = Hexagram.from_lines([8, 8, 8, 8, 8, 8])
    assert hex2.number == 2
    assert hex2.lines == [8, 8, 8, 8, 8, 8]
    print(f"✓ Lines [8,8,8,8,8,8]: Hexagram {hex2.number}")

    # With moving lines (should identify hexagram correctly)
    hex_moving = Hexagram.from_lines([7, 9, 8, 7, 6, 7])  # Contains 6 and 9
    assert hex_moving.number is not None  # Should successfully identify
    assert hex_moving.lines == [7, 9, 8, 7, 6, 7]  # Original lines preserved
    print(f"✓ Lines with moving values: Hexagram {hex_moving.number}")


def test_from_binary():
    """Test creating hexagram from binary pattern."""
    print("\n=== Testing Hexagram.from_binary() ===")

    hex1 = Hexagram.from_binary("111111")
    assert hex1.number == 1
    assert hex1.binary == "111111"
    print(f"✓ Binary 111111: Hexagram {hex1.number}")

    hex2 = Hexagram.from_binary("000000")
    assert hex2.number == 2
    assert hex2.binary == "000000"
    print(f"✓ Binary 000000: Hexagram {hex2.number}")


def test_from_trigrams():
    """Test creating hexagram from trigram pair."""
    print("\n=== Testing Hexagram.from_trigrams() ===")

    hex1 = Hexagram.from_trigrams("qian", "qian")
    assert hex1.number == 1
    assert hex1.trigrams == {"upper": "qian", "lower": "qian"}
    print(f"✓ Trigrams qian/qian: Hexagram {hex1.number}")

    hex64 = Hexagram.from_trigrams("li", "kan")
    assert hex64.number == 64
    assert hex64.trigrams == {"upper": "li", "lower": "kan"}
    print(f"✓ Trigrams li/kan: Hexagram {hex64.number}")


def test_moving_lines():
    """Test moving line detection and transformation."""
    print("\n=== Testing Moving Lines ===")

    # No moving lines
    hex_stable = Hexagram.from_lines([7, 7, 8, 8, 7, 8])
    assert not hex_stable.has_moving_lines()
    assert hex_stable.get_moving_lines() == []
    print(f"✓ Stable hexagram: no moving lines")

    # With moving lines
    hex_moving = Hexagram.from_lines([7, 9, 8, 7, 6, 7])
    assert hex_moving.has_moving_lines()
    moving = hex_moving.get_moving_lines()
    assert 2 in moving  # Line 2 is 9
    assert 5 in moving  # Line 5 is 6
    print(f"✓ Moving hexagram: lines {moving}")

    # Test to_stable_lines transformation
    stable = hex_moving.to_stable_lines()
    assert stable == [7, 7, 8, 7, 8, 7]  # 9→7, 6→8
    print(f"✓ Stable transformation: {stable}")


def test_serialization():
    """Test hexagram serialization/deserialization."""
    print("\n=== Testing Serialization ===")

    # Create hexagram
    hex1 = Hexagram.from_number(1)
    hex1.lines = [7, 7, 7, 7, 7, 7]

    # Convert to dict
    hex_dict = hex1.to_dict()
    assert hex_dict['number'] == 1
    assert hex_dict['english_name'] == "The Creative"
    assert hex_dict['lines'] == [7, 7, 7, 7, 7, 7]
    print(f"✓ to_dict(): {len(hex_dict)} fields")

    # Recreate from dict
    hex1_copy = Hexagram.from_dict(hex_dict)
    assert hex1_copy.number == hex1.number
    assert hex1_copy.english_name == hex1.english_name
    assert hex1_copy.lines == hex1.lines
    print(f"✓ from_dict(): Hexagram {hex1_copy.number} restored")


def test_source_selection():
    """Test using different interpretation sources."""
    print("\n=== Testing Source Selection ===")

    # Canonical source (default)
    hex1_canonical = Hexagram.from_number(1, source="canonical")
    assert hex1_canonical.source_id == "canonical"
    print(f"✓ Canonical source: {hex1_canonical.metadata.get('translator', 'Unknown')}")

    # Nonexistent source falls back to canonical
    hex1_fallback = Hexagram.from_number(1, source="nonexistent")
    assert hex1_fallback.source_id == "canonical"
    print(f"✓ Nonexistent source falls back to canonical")


def test_string_representations():
    """Test string representations."""
    print("\n=== Testing String Representations ===")

    hex1 = Hexagram.from_number(1)

    # __str__
    str_repr = str(hex1)
    assert "Hexagram 1" in str_repr
    assert "The Creative" in str_repr
    print(f"✓ str(): {str_repr}")

    # __repr__
    repr_str = repr(hex1)
    assert "Hexagram(" in repr_str
    assert "number=1" in repr_str
    print(f"✓ repr(): {repr_str[:60]}...")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("HEXAGRAM DATACLASS TESTS")
    print("=" * 70)

    try:
        test_from_number()
        test_from_lines()
        test_from_binary()
        test_from_trigrams()
        test_moving_lines()
        test_serialization()
        test_source_selection()
        test_string_representations()

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
