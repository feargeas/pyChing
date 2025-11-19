"""
Test Reading dataclass functionality.

Tests serialization, text formatting, and reading persistence.
"""

import sys
import json
import tempfile
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from pyching.core.hexagram import Hexagram
from pyching.core.reading import Reading


def test_create_reading():
    """Test creating a reading from hexagrams."""
    print("\n=== Testing Reading Creation ===")

    # Create hexagrams
    primary = Hexagram.from_number(1)
    primary.lines = [7, 7, 7, 7, 7, 7]

    # Create reading without moving lines
    reading = Reading.from_hexagrams(
        primary=primary,
        question="What is my purpose?",
        method="wood"
    )

    assert reading.primary.number == 1
    assert reading.relating is None
    assert reading.question == "What is my purpose?"
    assert reading.method == "wood"
    assert not reading.has_moving_lines()
    print(f"✓ Reading without moving lines: {reading}")

    # Create hexagrams with moving lines
    primary_moving = Hexagram.from_lines([7, 9, 8, 7, 6, 7])
    relating = Hexagram.from_lines([7, 8, 8, 7, 7, 7])

    reading_moving = Reading.from_hexagrams(
        primary=primary_moving,
        relating=relating,
        question="What should I do?",
        method="metal"
    )

    assert reading_moving.has_moving_lines()
    assert len(reading_moving.changing_lines) == 2
    assert 2 in reading_moving.changing_lines  # Line 2 (9)
    assert 5 in reading_moving.changing_lines  # Line 5 (6)
    print(f"✓ Reading with moving lines: {reading_moving}")


def test_serialization_dict():
    """Test dictionary serialization."""
    print("\n=== Testing Dictionary Serialization ===")

    # Create reading
    primary = Hexagram.from_number(1)
    primary.lines = [7, 9, 8, 7, 6, 7]
    relating = Hexagram.from_number(2)

    reading = Reading.from_hexagrams(
        primary=primary,
        relating=relating,
        question="Test question",
        method="wood"
    )

    # Convert to dict
    reading_dict = reading.to_dict()
    assert reading_dict['primary']['number'] == 1
    assert reading_dict['relating']['number'] == 2
    assert reading_dict['question'] == "Test question"
    assert reading_dict['method'] == "wood"
    assert len(reading_dict['changing_lines']) == 2
    print(f"✓ to_dict(): {len(reading_dict)} fields")

    # Recreate from dict
    reading_copy = Reading.from_dict(reading_dict)
    assert reading_copy.primary.number == reading.primary.number
    assert reading_copy.relating.number == reading.relating.number
    assert reading_copy.question == reading.question
    assert reading_copy.changing_lines == reading.changing_lines
    print(f"✓ from_dict(): Reading restored")


def test_serialization_json():
    """Test JSON serialization."""
    print("\n=== Testing JSON Serialization ===")

    # Create reading
    primary = Hexagram.from_number(1)
    primary.lines = [7, 7, 7, 7, 7, 7]

    reading = Reading.from_hexagrams(
        primary=primary,
        question="JSON test",
        method="fire"
    )

    # Convert to JSON
    json_str = reading.to_json()
    assert isinstance(json_str, str)
    json_data = json.loads(json_str)  # Validate it's valid JSON
    assert json_data['primary']['number'] == 1
    print(f"✓ to_json(): {len(json_str)} characters")

    # Recreate from JSON
    reading_copy = Reading.from_json(json_str)
    assert reading_copy.primary.number == reading.primary.number
    assert reading_copy.question == reading.question
    print(f"✓ from_json(): Reading restored")


def test_file_persistence():
    """Test saving and loading from files."""
    print("\n=== Testing File Persistence ===")

    # Create reading
    primary = Hexagram.from_lines([7, 9, 8, 7, 6, 7])
    relating = Hexagram.from_lines([7, 8, 8, 7, 7, 7])

    reading = Reading.from_hexagrams(
        primary=primary,
        relating=relating,
        question="File test",
        method="earth"
    )

    # Save to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name

    try:
        reading.save(temp_file)
        print(f"✓ Saved to {temp_file}")

        # Load from file
        loaded_reading = Reading.load(temp_file)
        assert loaded_reading.primary.number == reading.primary.number
        assert loaded_reading.relating.number == reading.relating.number
        assert loaded_reading.question == reading.question
        assert loaded_reading.changing_lines == reading.changing_lines
        print(f"✓ Loaded from file: {loaded_reading}")

    finally:
        # Cleanup
        Path(temp_file).unlink(missing_ok=True)


def test_as_text():
    """Test text representation (backward compatibility)."""
    print("\n=== Testing as_text() Format ===")

    # Reading without moving lines
    primary = Hexagram.from_number(1)
    primary.lines = [7, 7, 7, 7, 7, 7]

    reading = Reading.from_hexagrams(
        primary=primary,
        question="What is my purpose?",
        method="wood"
    )

    text = reading.as_text()
    assert "1" in text  # Hexagram number
    assert "The Creative" in text
    assert "What is my purpose?" in text
    assert "-------" in text  # Yang lines
    assert "no moving lines" in text.lower()
    print(f"✓ Text without moving lines ({len(text)} chars)")

    # Reading with moving lines
    primary_moving = Hexagram.from_lines([7, 9, 8, 7, 6, 7])
    relating = Hexagram.from_lines([7, 8, 8, 7, 7, 7])

    reading_moving = Reading.from_hexagrams(
        primary=primary_moving,
        relating=relating,
        question="What should I do?",
        method="metal"
    )

    text_moving = reading_moving.as_text()
    assert "---O---" in text_moving  # Moving yang (9)
    assert "---X---" in text_moving  # Moving yin (6)
    assert "becomes" in text_moving.lower()
    print(f"✓ Text with moving lines ({len(text_moving)} chars)")

    # Show sample output
    print("\nSample text output:")
    print(text[:200] + "...")


def test_string_representations():
    """Test string representations."""
    print("\n=== Testing String Representations ===")

    # Without moving lines
    primary = Hexagram.from_number(1)
    reading = Reading.from_hexagrams(primary=primary)

    str_repr = str(reading)
    assert "no moving lines" in str_repr.lower()
    print(f"✓ str() without moving: {str_repr}")

    # With moving lines
    primary_moving = Hexagram.from_lines([7, 9, 8, 7, 6, 7])
    relating = Hexagram.from_number(2)

    reading_moving = Reading.from_hexagrams(
        primary=primary_moving,
        relating=relating
    )

    str_moving = str(reading_moving)
    assert "2 moving lines" in str_moving or "moving" in str_moving.lower()
    print(f"✓ str() with moving: {str_moving}")

    # __repr__
    repr_str = repr(reading_moving)
    assert "Reading(" in repr_str
    print(f"✓ repr(): {repr_str[:60]}...")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("READING DATACLASS TESTS")
    print("=" * 70)

    try:
        test_create_reading()
        test_serialization_dict()
        test_serialization_json()
        test_file_persistence()
        test_as_text()
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
