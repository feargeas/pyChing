#!/usr/bin/env python3
"""
Migrate existing JSON hexagram data to YAML format

Input:  data/hexagrams/hexagram_NN.json (64 files)
Output: data/interpretations/legge/hexagram_NN.yaml (64 files)

Preserves exact data content, changes format only to cleaner YAML structure.
"""

import json
import yaml
from pathlib import Path


def migrate_all_hexagrams(json_dir='data/hexagrams',
                          yaml_dir='data/interpretations/legge'):
    """Convert all 64 hexagrams from JSON to YAML"""

    json_dir = Path(json_dir)
    yaml_dir = Path(yaml_dir)
    yaml_dir.mkdir(parents=True, exist_ok=True)

    # Process each hexagram
    print("Migrating all 64 hexagrams from JSON to YAML...")
    for i in range(1, 65):
        migrate_single_hexagram(i, json_dir, yaml_dir)

    print(f"\n✓ Migration complete: {yaml_dir}")


def migrate_single_hexagram(number,
                            json_dir='data/hexagrams',
                            yaml_dir='data/interpretations/legge'):
    """Migrate a single hexagram (for testing)"""

    json_dir = Path(json_dir)
    yaml_dir = Path(yaml_dir)
    yaml_dir.mkdir(parents=True, exist_ok=True)

    json_file = json_dir / f'hexagram_{number:02d}.json'
    yaml_file = yaml_dir / f'hexagram_{number:02d}.yaml'

    # Load JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Restructure for cleaner YAML
    clean_data = restructure_for_yaml(data)

    # Write YAML with clean formatting
    with open(yaml_file, 'w', encoding='utf-8') as f:
        yaml.dump(clean_data, f,
                 allow_unicode=True,
                 default_flow_style=False,
                 sort_keys=False,
                 width=80)

    print(f"✓ Migrated hexagram {number:02d}: {data['canonical']['name']}")
    return yaml_file


def restructure_for_yaml(json_data):
    """
    Restructure JSON data for cleaner YAML format.

    Flattens canonical section to top level for better readability.
    Preserves all data content exactly.
    """

    return {
        'metadata': {
            'hexagram': json_data['number'],
            'king_wen_sequence': json_data['king_wen_sequence'],
            'fu_xi_sequence': json_data['fu_xi_sequence'],
            'binary': json_data['binary'],
            'source': json_data['canonical']['source_id'],
            'translator': json_data['canonical']['metadata']['translator'],
            'year': json_data['canonical']['metadata']['year'],
            'language': json_data['canonical']['metadata']['language'],
            'verified': json_data['canonical']['metadata']['verified']
        },

        'name': json_data['canonical']['name'],
        'english_name': json_data['canonical']['english_name'],
        'title': json_data['canonical']['title'],

        'trigrams': json_data['trigrams'],

        'judgment': json_data['canonical']['judgment'],
        'image': json_data['canonical']['image'],

        'lines': {
            i: {
                'position': line['position'],
                'type': line['type'],
                'text': line['text']
            }
            for i, line in json_data['canonical']['lines'].items()
        }
    }


def verify_migration(json_dir='data/hexagrams',
                    yaml_dir='data/interpretations/legge'):
    """Verify JSON and YAML contain same data"""

    json_dir = Path(json_dir)
    yaml_dir = Path(yaml_dir)

    errors = []

    print("\nVerifying migration...")
    for i in range(1, 65):
        json_file = json_dir / f'hexagram_{i:02d}.json'
        yaml_file = yaml_dir / f'hexagram_{i:02d}.yaml'

        if not yaml_file.exists():
            errors.append(f"Hexagram {i:02d}: YAML file missing")
            continue

        with open(json_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        with open(yaml_file, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)

        # Compare critical fields
        hex_errors = verify_hexagram(json_data, yaml_data, i)
        if hex_errors:
            errors.extend(hex_errors)

    if errors:
        print("\n✗ ERRORS FOUND:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✓ All 64 hexagrams verified - data preserved correctly")
        return True


def verify_hexagram(json_data, yaml_data, number):
    """Verify single hexagram migration - return list of errors"""

    errors = []

    # Check hexagram number
    if json_data['number'] != yaml_data['metadata']['hexagram']:
        errors.append(f"Hexagram {number:02d}: number mismatch")

    # Check name
    if json_data['canonical']['name'] != yaml_data['name']:
        errors.append(f"Hexagram {number:02d}: name mismatch")

    # Check judgment
    if json_data['canonical']['judgment'] != yaml_data['judgment']:
        errors.append(f"Hexagram {number:02d}: judgment text differs")

    # Check image
    if json_data['canonical']['image'] != yaml_data['image']:
        errors.append(f"Hexagram {number:02d}: image text differs")

    # Check all 6 lines present
    if len(yaml_data['lines']) != 6:
        errors.append(f"Hexagram {number:02d}: expected 6 lines, got {len(yaml_data['lines'])}")

    # Check each line text matches
    for i in range(1, 7):
        json_line = json_data['canonical']['lines'][str(i)]['text']
        yaml_line = yaml_data['lines'][str(i)]['text']
        if json_line != yaml_line:
            errors.append(f"Hexagram {number:02d}: line {i} text differs")

    return errors


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Migrate hexagram data from JSON to YAML format'
    )
    parser.add_argument('--verify', action='store_true',
                       help='Verify migration instead of running it')
    parser.add_argument('--single', type=int, metavar='N',
                       help='Migrate only single hexagram N (for testing)')
    args = parser.parse_args()

    if args.verify:
        success = verify_migration()
        exit(0 if success else 1)
    elif args.single:
        # Test on single hexagram first
        if not 1 <= args.single <= 64:
            print(f"Error: hexagram number must be 1-64, got {args.single}")
            exit(1)

        migrate_single_hexagram(args.single)
        print(f"\n✓ Test migration complete for hexagram {args.single}")
        print(f"  Check: data/interpretations/legge/hexagram_{args.single:02d}.yaml")
    else:
        migrate_all_hexagrams()
        verify_migration()
