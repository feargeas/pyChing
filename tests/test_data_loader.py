"""
Test HexagramDataLoader functionality.

Tests all lookup methods, caching behavior, and error handling.
"""

import json
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from pyching.data.loader import HexagramDataLoader


def test_load_by_id():
    """Test loading hexagram by ID."""
    print("\n=== Testing Load by ID ===")
    loader = HexagramDataLoader()

    # Load hexagram 1
    hex_data = loader.load_hexagram("hexagram_01")

    assert hex_data['hexagram_id'] == "hexagram_01"
    assert hex_data['number'] == 1
    assert hex_data['binary'] == "111111"
    assert 'canonical' in hex_data
    assert hex_data['canonical']['english_name'] == "The Creative"

    print(f"✓ Loaded hexagram_01: {hex_data['canonical']['english_name']}")
    print(f"  Binary: {hex_data['binary']}")
    print(f"  Trigrams: {hex_data['trigrams']}")


def test_load_by_number():
    """Test loading hexagram by King Wen number."""
    print("\n=== Testing Load by Number ===")
    loader = HexagramDataLoader()

    # Test a few different hexagrams
    test_cases = [
        (1, "hexagram_01", "The Creative"),
        (2, "hexagram_02", "The Receptive"),
        (64, "hexagram_64", "Before The Achievement")
    ]

    for number, expected_id, expected_name in test_cases:
        hex_data = loader.get_hexagram_by_number(number)
        assert hex_data['hexagram_id'] == expected_id
        assert hex_data['number'] == number
        assert hex_data['canonical']['english_name'] == expected_name
        print(f"✓ Number {number}: {expected_name}")


def test_load_by_binary():
    """Test loading hexagram by binary pattern."""
    print("\n=== Testing Load by Binary ===")
    loader = HexagramDataLoader()

    test_cases = [
        ("111111", 1, "The Creative"),
        ("000000", 2, "The Receptive"),
        ("101010", 64, "Before The Achievement")
    ]

    for binary, expected_num, expected_name in test_cases:
        hex_data = loader.get_hexagram_by_binary(binary)
        assert hex_data['binary'] == binary
        assert hex_data['number'] == expected_num
        assert hex_data['canonical']['english_name'] == expected_name
        print(f"✓ Binary {binary}: {expected_name}")


def test_load_by_trigrams():
    """Test loading hexagram by trigram pair."""
    print("\n=== Testing Load by Trigrams ===")
    loader = HexagramDataLoader()

    test_cases = [
        ("qian", "qian", 1, "The Creative"),
        ("kun", "kun", 2, "The Receptive"),
        ("li", "kan", 64, "Before The Achievement")
    ]

    for upper, lower, expected_num, expected_name in test_cases:
        hex_data = loader.get_hexagram_by_trigrams(upper, lower)
        assert hex_data['trigrams']['upper'] == upper
        assert hex_data['trigrams']['lower'] == lower
        assert hex_data['number'] == expected_num
        assert hex_data['canonical']['english_name'] == expected_name
        print(f"✓ Trigrams {upper}/{lower}: {expected_name}")


def test_load_by_lines():
    """Test loading hexagram by line values."""
    print("\n=== Testing Load by Lines ===")
    loader = HexagramDataLoader()

    # Test with stable lines (all yang = hexagram 1)
    lines = [7, 7, 7, 7, 7, 7]
    hex_data = loader.get_hexagram_by_lines(lines)
    assert hex_data['number'] == 1
    assert hex_data['binary'] == "111111"
    print(f"✓ Lines {lines}: {hex_data['canonical']['english_name']}")

    # Test with moving lines (should convert 9→7, 6→8)
    lines = [9, 7, 7, 7, 7, 9]  # Should still match qian pattern
    hex_data = loader.get_hexagram_by_lines(lines)
    assert hex_data['number'] == 1  # Moving lines converted to stable
    print(f"✓ Lines {lines} (moving): {hex_data['canonical']['english_name']}")

    # Test all yin (hexagram 2)
    lines = [8, 8, 8, 8, 8, 8]
    hex_data = loader.get_hexagram_by_lines(lines)
    assert hex_data['number'] == 2
    assert hex_data['binary'] == "000000"
    print(f"✓ Lines {lines}: {hex_data['canonical']['english_name']}")


def test_load_by_name():
    """Test loading hexagram by name variant."""
    print("\n=== Testing Load by Name ===")
    loader = HexagramDataLoader()

    # Test various name forms (using names that exist in mappings.json)
    test_names = ["Tch'ien", "Koun"]

    for name in test_names:
        try:
            hex_data = loader.get_hexagram_by_name(name)
            print(f"✓ Name '{name}': {hex_data['canonical']['english_name']} (#{hex_data['number']})")
        except KeyError as e:
            print(f"✗ Name '{name}' not found: {e}")


def test_caching():
    """Test that caching works correctly."""
    print("\n=== Testing Caching ===")
    loader = HexagramDataLoader()

    # Clear cache
    loader.clear_cache()
    stats = loader.get_cache_stats()
    assert stats['hexagrams_cached'] == 0
    print(f"✓ Cache cleared: {stats}")

    # Load hexagram
    loader.load_hexagram("hexagram_01")
    stats = loader.get_cache_stats()
    assert stats['hexagrams_cached'] == 1
    print(f"✓ First load: {stats}")

    # Load same hexagram again (should be cached)
    loader.load_hexagram("hexagram_01")
    stats = loader.get_cache_stats()
    assert stats['hexagrams_cached'] == 1  # Still 1 (cached)
    print(f"✓ Second load (from cache): {stats}")

    # Load different hexagram
    loader.load_hexagram("hexagram_02")
    stats = loader.get_cache_stats()
    assert stats['hexagrams_cached'] == 2
    print(f"✓ Load different hexagram: {stats}")


def test_all_64_hexagrams():
    """Test that all 64 hexagrams can be loaded."""
    print("\n=== Testing All 64 Hexagrams ===")
    loader = HexagramDataLoader()

    success_count = 0
    for i in range(1, 65):
        try:
            hex_data = loader.get_hexagram_by_number(i)
            assert hex_data['number'] == i
            success_count += 1
        except FileNotFoundError as e:
            print(f"✗ Hexagram {i} not found: {e}")

    print(f"✓ Successfully loaded {success_count}/64 hexagrams")
    return success_count


def test_error_handling():
    """Test error handling for invalid inputs."""
    print("\n=== Testing Error Handling ===")
    loader = HexagramDataLoader()

    # Test invalid hexagram ID
    try:
        loader.load_hexagram("hexagram_99")
        assert False, "Should have raised FileNotFoundError"
    except FileNotFoundError:
        print("✓ Invalid hexagram ID raises FileNotFoundError")

    # Test invalid number
    try:
        loader.get_hexagram_by_number(0)
        assert False, "Should have raised ValueError"
    except (ValueError, FileNotFoundError):
        print("✓ Invalid number (0) raises error")

    try:
        loader.get_hexagram_by_number(65)
        assert False, "Should have raised ValueError"
    except (ValueError, FileNotFoundError):
        print("✓ Invalid number (65) raises error")

    # Test invalid binary
    try:
        loader.get_hexagram_by_binary("invalid")
        assert False, "Should have raised ValueError"
    except (ValueError, KeyError, FileNotFoundError):
        print("✓ Invalid binary raises error")

    # Test invalid lines count
    try:
        loader.get_hexagram_by_lines([7, 7, 7])  # Only 3 lines
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"✓ Invalid lines count raises ValueError: {e}")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("HEXAGRAM DATA LOADER TESTS")
    print("=" * 70)

    try:
        test_load_by_id()
        test_load_by_number()
        test_load_by_binary()
        test_load_by_trigrams()
        test_load_by_lines()
        test_load_by_name()
        test_caching()
        hexagram_count = test_all_64_hexagrams()
        test_error_handling()

        print("\n" + "=" * 70)
        print("ALL TESTS PASSED!")
        print(f"Loaded {hexagram_count}/64 hexagrams successfully")
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
