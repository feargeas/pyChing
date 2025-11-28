#!/usr/bin/env python3
"""Verify Wilhelm YAML extraction against wilhelm.txt source."""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple


def extract_hexagram_from_txt(txt_content: str, hex_num: int) -> Dict[str, str]:
    """Extract a hexagram from wilhelm.txt for comparison."""
    lines = txt_content.split('\n')

    # Find hexagram start - look for pattern like "1. Ch'ien / The Creative"
    hex_pattern = rf"^{hex_num}\.\s+"
    start_idx = None
    for i, line in enumerate(lines):
        if re.match(hex_pattern, line):
            start_idx = i
            break

    if start_idx is None:
        return {}

    # Find next hexagram or end
    end_idx = len(lines)
    for i in range(start_idx + 1, len(lines)):
        if re.match(r"^\d+\.\s+\w", lines[i]):  # Next hexagram
            end_idx = i
            break

    hex_lines = lines[start_idx:end_idx]

    # Extract sections
    judgment = extract_txt_section(hex_lines, "THE JUDGMENT")
    image = extract_txt_section(hex_lines, "THE IMAGE")

    return {
        'judgment': judgment.strip() if judgment else "",
        'image': image.strip() if image else ""
    }


def extract_txt_section(hex_lines: List[str], section_name: str) -> str:
    """Extract a section from wilhelm.txt hexagram lines."""
    section_start = None
    for i, line in enumerate(hex_lines):
        if line.strip() == section_name or line.strip() == section_name + '.':
            section_start = i + 1
            break

    if section_start is None:
        return ""

    # Collect until next section
    text_lines = []
    for i in range(section_start, len(hex_lines)):
        line = hex_lines[i].strip()

        # Stop at next major section
        if line in ['THE JUDGMENT', 'THE IMAGE', 'THE IMAGE.', 'THE LINES']:
            break

        if line:
            text_lines.append(line)
        elif text_lines:
            text_lines.append('')

    # Join and normalize
    text = '\n'.join(text_lines).strip()
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text


def normalize_text(text: str) -> str:
    """Normalize text for comparison - remove extra whitespace, normalize quotes."""
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    # Normalize quotes
    text = text.replace("'", "'").replace("'", "'")
    text = text.replace(""", '"').replace(""", '"')
    return text.strip()


def compare_hexagrams(yaml_file: Path, txt_hex: Dict[str, str]) -> List[str]:
    """Compare YAML hexagram with txt source, return list of differences."""
    differences = []

    with open(yaml_file, 'r', encoding='utf-8') as f:
        yaml_data = yaml.safe_load(f)

    hex_num = yaml_data['metadata']['hexagram']

    # Compare judgment
    yaml_judgment = normalize_text(yaml_data.get('judgment', ''))
    txt_judgment = normalize_text(txt_hex.get('judgment', ''))

    if yaml_judgment != txt_judgment:
        # Check if it's just minor differences
        yaml_words = set(yaml_judgment.split())
        txt_words = set(txt_judgment.split())

        if yaml_words != txt_words:
            missing_in_yaml = txt_words - yaml_words
            extra_in_yaml = yaml_words - txt_words

            if missing_in_yaml or extra_in_yaml:
                differences.append(f"  JUDGMENT differs:")
                if missing_in_yaml:
                    differences.append(f"    Missing in YAML: {missing_in_yaml}")
                if extra_in_yaml:
                    differences.append(f"    Extra in YAML: {extra_in_yaml}")

                # Show length difference
                differences.append(f"    Length: YAML={len(yaml_judgment)} chars, TXT={len(txt_judgment)} chars")

    # Compare image
    yaml_image = normalize_text(yaml_data.get('image', ''))
    txt_image = normalize_text(txt_hex.get('image', ''))

    if yaml_image != txt_image:
        yaml_words = set(yaml_image.split())
        txt_words = set(txt_image.split())

        if yaml_words != txt_words:
            missing_in_yaml = txt_words - yaml_words
            extra_in_yaml = yaml_words - txt_words

            if missing_in_yaml or extra_in_yaml:
                differences.append(f"  IMAGE differs:")
                if missing_in_yaml:
                    differences.append(f"    Missing in YAML: {missing_in_yaml}")
                if extra_in_yaml:
                    differences.append(f"    Extra in YAML: {extra_in_yaml}")

                differences.append(f"    Length: YAML={len(yaml_image)} chars, TXT={len(txt_image)} chars")

    return differences


def main():
    """Main verification function."""
    base_dir = Path(__file__).parent.parent
    txt_file = base_dir / 'data' / 'sources' / 'wilhelm' / 'wilhelm.txt'
    yaml_dir = base_dir / 'data' / 'interpretations' / 'wilhelm'

    # Read wilhelm.txt
    print("Reading wilhelm.txt...")
    with open(txt_file, 'r', encoding='utf-8') as f:
        txt_content = f.read()

    print("Verifying all 64 hexagrams against wilhelm.txt...\n")

    all_good = True
    for hex_num in range(1, 65):
        yaml_file = yaml_dir / f'hexagram_{hex_num:02d}.yaml'

        if not yaml_file.exists():
            print(f"✗ Hexagram {hex_num:02d}: YAML file not found")
            all_good = False
            continue

        # Extract from txt
        txt_hex = extract_hexagram_from_txt(txt_content, hex_num)

        if not txt_hex.get('judgment') or not txt_hex.get('image'):
            print(f"⚠ Hexagram {hex_num:02d}: Could not extract from TXT (judgment={bool(txt_hex.get('judgment'))}, image={bool(txt_hex.get('image'))})")
            continue

        # Compare
        differences = compare_hexagrams(yaml_file, txt_hex)

        if differences:
            print(f"⚠ Hexagram {hex_num:02d}: Differences found")
            for diff in differences:
                print(diff)
            print()
            all_good = False
        else:
            print(f"✓ Hexagram {hex_num:02d}: Matches wilhelm.txt")

    if all_good:
        print("\n✓ All hexagrams match wilhelm.txt source!")
    else:
        print("\n⚠ Some differences found - review above")


if __name__ == '__main__':
    main()
