#!/usr/bin/env python3
"""
Fix inappropriate backslashes in Wilhelm YAML files.

Removes:
1. Trailing backslashes at line continuations
2. Escaped single quotes (\\' -> ')
"""

import re
from pathlib import Path


def fix_yaml_backslashes(yaml_path: Path) -> bool:
    """
    Fix backslash issues in a YAML file.

    Args:
        yaml_path: Path to YAML file

    Returns:
        True if changes were made, False otherwise
    """
    with open(yaml_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Fix 1: Remove trailing backslashes followed by newline
    # Pattern: backslash at end of line (before newline)
    content = re.sub(r'\\\n', '\n', content)

    # Fix 2: Replace escaped quotes with regular quotes
    # Pattern: \' -> ' and \" -> "
    content = content.replace("\\'", "'")
    content = content.replace('\\"', '"')

    # Fix 3: Replace escaped brackets
    # Pattern: \[ -> [ and \] -> ]
    content = content.replace('\\[', '[')
    content = content.replace('\\]', ']')

    # Check if changes were made
    if content != original_content:
        with open(yaml_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    return False


def main():
    """Process all Wilhelm YAML files."""
    yaml_dir = Path('data/interpretations/wilhelm')

    if not yaml_dir.exists():
        print(f"Error: Directory not found: {yaml_dir}")
        return 1

    yaml_files = sorted(yaml_dir.glob('hexagram_*.yaml'))

    if not yaml_files:
        print(f"Error: No YAML files found in {yaml_dir}")
        return 1

    print(f"Processing {len(yaml_files)} YAML files...")
    print("-" * 70)

    fixed_count = 0
    for yaml_file in yaml_files:
        if fix_yaml_backslashes(yaml_file):
            print(f"✓ Fixed: {yaml_file.name}")
            fixed_count += 1
        else:
            print(f"  No changes: {yaml_file.name}")

    print("-" * 70)
    print(f"✓ Fixed {fixed_count}/{len(yaml_files)} files")

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
