#!/usr/bin/env python3
"""
Validate hexagram JSON data structure.

Ensures all JSON files conform to the expected schema and contain
valid data.
"""

import json
import sys
from pathlib import Path


def validate_hexagram(hex_file):
    """
    Validate a single hexagram JSON file.

    Args:
        hex_file: Path to hexagram JSON file

    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        with open(hex_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return (False, f"Invalid JSON: {e}")
    except Exception as e:
        return (False, f"Error reading file: {e}")

    # Check required top-level fields
    required_fields = [
        'hexagram_id', 'number', 'king_wen_sequence',
        'binary', 'trigrams', 'canonical', 'sources'
    ]

    for field in required_fields:
        if field not in data:
            return (False, f"Missing required field: {field}")

    # Validate hexagram_id format
    if not data['hexagram_id'].startswith('hexagram_'):
        return (False, f"Invalid hexagram_id format: {data['hexagram_id']}")

    # Validate number matches
    expected_num = int(data['hexagram_id'].split('_')[1])
    if data['number'] != expected_num:
        return (False, f"Number mismatch: {data['number']} vs {expected_num}")

    # Validate binary length
    if len(data['binary']) != 6:
        return (False, f"Binary must be 6 digits: {data['binary']}")

    # Validate trigrams
    if 'upper' not in data['trigrams'] or 'lower' not in data['trigrams']:
        return (False, "Missing trigram data")

    # Validate canonical structure
    canonical = data['canonical']
    canonical_required = [
        'source_id', 'name', 'english_name', 'title',
        'judgment', 'image', 'lines', 'metadata'
    ]

    for field in canonical_required:
        if field not in canonical:
            return (False, f"Missing canonical field: {field}")

    # Validate lines (must have 1-6)
    lines = canonical['lines']
    for line_num in range(1, 7):
        line_key = str(line_num)
        if line_key not in lines:
            return (False, f"Missing line {line_num}")

        line_data = lines[line_key]
        if 'position' not in line_data:
            return (False, f"Line {line_num} missing position")
        if 'type' not in line_data:
            return (False, f"Line {line_num} missing type")
        if 'text' not in line_data:
            return (False, f"Line {line_num} missing text")

        # Validate line type
        if line_data['type'] not in ['six', 'nine']:
            return (False, f"Line {line_num} invalid type: {line_data['type']}")

    # Validate metadata
    metadata = canonical['metadata']
    if 'translator' not in metadata:
        return (False, "Missing translator in metadata")
    if 'year' not in metadata:
        return (False, "Missing year in metadata")

    return (True, None)


def validate_mappings(mappings_file):
    """Validate mappings.json structure."""
    try:
        with open(mappings_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return (False, f"Error reading mappings: {e}")

    required_sections = ['number_to_id', 'binary_to_id', 'trigram_pairs_to_id', 'trigrams']

    for section in required_sections:
        if section not in data:
            return (False, f"Missing section: {section}")

    # Validate trigrams
    required_trigrams = ['qian', 'kun', 'zhen', 'kan', 'gen', 'xun', 'li', 'dui']
    for trigram in required_trigrams:
        if trigram not in data['trigrams']:
            return (False, f"Missing trigram: {trigram}")

    return (True, None)


def validate_sources_metadata(sources_file):
    """Validate sources_metadata.json structure."""
    try:
        with open(sources_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return (False, f"Error reading sources metadata: {e}")

    if 'sources' not in data:
        return (False, "Missing 'sources' section")

    if 'source_priority' not in data:
        return (False, "Missing 'source_priority' section")

    # Validate canonical source exists
    canonical_found = False
    for source_id, source_data in data['sources'].items():
        if source_data.get('canonical', False):
            canonical_found = True
            if source_id != 'legge_1882':
                return (False, f"Unexpected canonical source: {source_id}")
            break

    if not canonical_found:
        return (False, "No canonical source found")

    return (True, None)


def main():
    """Run validation."""
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data'

    print("Validating pyChing JSON data structure...")
    print()

    # Validate mappings
    print("Validating mappings.json...")
    mappings_file = data_dir / 'mappings.json'
    is_valid, error = validate_mappings(mappings_file)
    if not is_valid:
        print(f"  ✗ FAILED: {error}")
        return 1
    print("  ✓ Valid")
    print()

    # Validate sources metadata
    print("Validating sources_metadata.json...")
    sources_file = data_dir / 'sources_metadata.json'
    is_valid, error = validate_sources_metadata(sources_file)
    if not is_valid:
        print(f"  ✗ FAILED: {error}")
        return 1
    print("  ✓ Valid")
    print()

    # Validate hexagram files
    hexagrams_dir = data_dir / 'hexagrams'
    hexagram_files = sorted(hexagrams_dir.glob('hexagram_*.json'))

    if not hexagram_files:
        print("  ✗ No hexagram files found")
        return 1

    print(f"Validating {len(hexagram_files)} hexagram files...")
    errors = []

    for hex_file in hexagram_files:
        is_valid, error = validate_hexagram(hex_file)
        if not is_valid:
            errors.append(f"{hex_file.name}: {error}")
        else:
            print(f"  ✓ {hex_file.name}")

    print()

    if errors:
        print("VALIDATION ERRORS:")
        for error in errors:
            print(f"  ✗ {error}")
        return 1

    print("=" * 60)
    print(f"✓ All {len(hexagram_files)} hexagram files validated successfully!")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
