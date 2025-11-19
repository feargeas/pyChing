"""
Test HexagramResolver functionality.

Tests multi-source resolution, comparison, and fallback logic.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from pyching.data.loader import HexagramDataLoader
from pyching.data.resolver import HexagramResolver


def test_resolve_canonical():
    """Test resolving canonical source."""
    print("\n=== Testing Canonical Resolution ===")
    resolver = HexagramResolver()

    # Resolve canonical for hexagram 1
    hex_data = resolver.resolve("hexagram_01", source="canonical")

    assert hex_data['hexagram_id'] == "hexagram_01"
    assert hex_data['number'] == 1
    assert hex_data['source_id'] == "canonical"
    assert 'english_name' in hex_data
    assert 'judgment' in hex_data
    assert 'image' in hex_data
    assert 'lines' in hex_data

    print(f"✓ Resolved canonical: {hex_data['english_name']}")
    print(f"  Source: {hex_data.get('metadata', {}).get('translator', 'Unknown')}")


def test_resolve_default():
    """Test that default source is canonical."""
    print("\n=== Testing Default Source ===")
    resolver = HexagramResolver()

    # Resolve without specifying source
    hex_data = resolver.resolve("hexagram_01")

    assert hex_data['source_id'] == "canonical"
    print(f"✓ Default source is canonical")


def test_resolve_nonexistent_source():
    """Test fallback to canonical for nonexistent source."""
    print("\n=== Testing Nonexistent Source Fallback ===")
    resolver = HexagramResolver()

    # Request nonexistent source
    hex_data = resolver.resolve("hexagram_01", source="nonexistent_source")

    # Should fall back to canonical
    assert hex_data['source_id'] == "canonical"
    print(f"✓ Nonexistent source falls back to canonical")


def test_get_available_sources():
    """Test getting available sources for a hexagram."""
    print("\n=== Testing Get Available Sources ===")
    resolver = HexagramResolver()

    sources = resolver.get_available_sources("hexagram_01")

    # Should always include canonical
    assert 'canonical' in sources
    print(f"✓ Available sources: {sources}")

    # Test a few different hexagrams
    for hex_num in [1, 2, 64]:
        hex_id = f"hexagram_{hex_num:02d}"
        sources = resolver.get_available_sources(hex_id)
        assert 'canonical' in sources
        print(f"✓ Hexagram {hex_num} sources: {sources}")


def test_resolve_multiple():
    """Test resolving multiple sources."""
    print("\n=== Testing Resolve Multiple ===")
    resolver = HexagramResolver()

    # Request canonical and a nonexistent source
    sources = ['canonical', 'nonexistent']
    result = resolver.resolve_multiple("hexagram_01", sources)

    # Should have canonical
    assert 'canonical' in result
    assert result['canonical']['source_id'] == "canonical"

    print(f"✓ Resolved sources: {list(result.keys())}")


def test_compare_sources_all_fields():
    """Test comparing all fields across sources."""
    print("\n=== Testing Compare All Fields ===")
    resolver = HexagramResolver()

    # Compare all available sources
    comparison = resolver.compare_sources("hexagram_01")

    # Should have at least canonical
    assert 'canonical' in comparison
    assert comparison['canonical']['source_id'] == "canonical"

    print(f"✓ Compared sources: {list(comparison.keys())}")
    for source_id, data in comparison.items():
        print(f"  {source_id}: {data.get('english_name', 'Unknown')}")


def test_compare_sources_specific_field():
    """Test comparing specific field across sources."""
    print("\n=== Testing Compare Specific Field ===")
    resolver = HexagramResolver()

    # Compare judgment field
    comparison = resolver.compare_sources("hexagram_01", field="judgment")

    assert 'canonical' in comparison
    assert isinstance(comparison['canonical'], str)

    print(f"✓ Compared 'judgment' field across sources")
    for source_id, judgment in comparison.items():
        preview = judgment[:80] + "..." if len(judgment) > 80 else judgment
        print(f"  {source_id}: {preview}")


def test_compare_sources_lines():
    """Test comparing lines field."""
    print("\n=== Testing Compare Lines Field ===")
    resolver = HexagramResolver()

    comparison = resolver.compare_sources("hexagram_01", field="lines")

    assert 'canonical' in comparison
    assert isinstance(comparison['canonical'], dict)
    assert '1' in comparison['canonical']  # Should have line 1

    print(f"✓ Compared 'lines' field")
    for source_id, lines in comparison.items():
        print(f"  {source_id}: {len(lines)} lines")


def test_validate_completeness():
    """Test source completeness validation."""
    print("\n=== Testing Source Completeness Validation ===")
    resolver = HexagramResolver()

    # Validate canonical source
    completeness = resolver.validate_source_completeness("hexagram_01", "canonical")

    assert isinstance(completeness, dict)
    assert 'name' in completeness
    assert 'english_name' in completeness
    assert 'judgment' in completeness
    assert 'image' in completeness
    assert 'lines' in completeness

    print(f"✓ Completeness check results:")
    for field, is_complete in completeness.items():
        status = "✓" if is_complete else "✗"
        print(f"  {status} {field}: {is_complete}")


def test_source_metadata():
    """Test getting source metadata."""
    print("\n=== Testing Source Metadata ===")
    resolver = HexagramResolver()

    # List all sources
    all_sources = resolver.list_all_sources()
    print(f"✓ Total registered sources: {len(all_sources)}")

    for source in all_sources:
        print(f"  - {source.get('id', 'unknown')}: {source.get('translator', 'Unknown')}")

    # Get specific source info
    canonical_info = resolver.get_source_info('canonical')
    if canonical_info:
        print(f"\n✓ Canonical source info:")
        print(f"  Translator: {canonical_info.get('translator', 'Unknown')}")
        print(f"  Year: {canonical_info.get('year', 'Unknown')}")


def test_source_priority():
    """Test getting source priority order."""
    print("\n=== Testing Source Priority ===")
    resolver = HexagramResolver()

    priority = resolver.get_source_priority()

    assert isinstance(priority, list)
    assert len(priority) > 0
    assert 'legge_1882' in priority  # Canonical source should be in priority list

    print(f"✓ Source priority order: {priority}")


def test_format_for_display():
    """Test that resolved data is properly formatted."""
    print("\n=== Testing Display Format ===")
    resolver = HexagramResolver()

    hex_data = resolver.resolve("hexagram_01")

    # Check all expected fields are present
    required_fields = [
        'hexagram_id', 'number', 'binary', 'trigrams',
        'name', 'english_name', 'judgment', 'image',
        'lines', 'metadata', 'source_id'
    ]

    for field in required_fields:
        assert field in hex_data, f"Missing field: {field}"

    print(f"✓ All required fields present in display format:")
    print(f"  hexagram_id: {hex_data['hexagram_id']}")
    print(f"  number: {hex_data['number']}")
    print(f"  binary: {hex_data['binary']}")
    print(f"  trigrams: {hex_data['trigrams']}")
    print(f"  english_name: {hex_data['english_name']}")
    print(f"  source_id: {hex_data['source_id']}")


def test_multiple_hexagrams():
    """Test resolution across multiple hexagrams."""
    print("\n=== Testing Multiple Hexagrams ===")
    resolver = HexagramResolver()

    test_hexagrams = ["hexagram_01", "hexagram_02", "hexagram_64"]

    for hex_id in test_hexagrams:
        hex_data = resolver.resolve(hex_id)
        assert hex_data['hexagram_id'] == hex_id
        print(f"✓ {hex_id}: {hex_data['english_name']}")


def test_all_64_hexagrams():
    """Test that all 64 hexagrams can be resolved."""
    print("\n=== Testing All 64 Hexagrams Resolution ===")
    resolver = HexagramResolver()

    success_count = 0
    for i in range(1, 65):
        hex_id = f"hexagram_{i:02d}"
        try:
            hex_data = resolver.resolve(hex_id)
            assert hex_data['number'] == i
            success_count += 1
        except FileNotFoundError as e:
            print(f"✗ Hexagram {i} not found: {e}")

    print(f"✓ Successfully resolved {success_count}/64 hexagrams")
    return success_count


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("HEXAGRAM RESOLVER TESTS")
    print("=" * 70)

    try:
        test_resolve_canonical()
        test_resolve_default()
        test_resolve_nonexistent_source()
        test_get_available_sources()
        test_resolve_multiple()
        test_compare_sources_all_fields()
        test_compare_sources_specific_field()
        test_compare_sources_lines()
        test_validate_completeness()
        test_source_metadata()
        test_source_priority()
        test_format_for_display()
        test_multiple_hexagrams()
        hexagram_count = test_all_64_hexagrams()

        print("\n" + "=" * 70)
        print("ALL TESTS PASSED!")
        print(f"Resolved {hexagram_count}/64 hexagrams successfully")
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
