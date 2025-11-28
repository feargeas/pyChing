#!/usr/bin/env python3
"""
Extract Wilhelm/Baynes translation from markdown to YAML

Input:  data/sources/wilhelm/wilhelm.md
Output: data/interpretations/wilhelm/hexagram_NN.yaml

Much simpler than HTML parsing since we have clean markdown!
"""

import re
import sys
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def extract_hexagram_from_md(md_content: str, hex_num: int) -> Optional[Dict[str, Any]]:
    """
    Extract a single hexagram from Wilhelm markdown.

    Args:
        md_content: Full markdown content
        hex_num: Hexagram number (1-64)

    Returns:
        Hexagram data dict or None if not found
    """
    # Find the hexagram heading: ## 1. Ch'ien / The Creative
    pattern = rf"^## {hex_num}\. (.+?) / (.+?)$"

    # Split into lines for processing
    lines = md_content.split('\n')

    # Find start of this hexagram
    start_idx = None
    chinese_name = None
    english_name = None

    for i, line in enumerate(lines):
        match = re.match(pattern, line)
        if match:
            start_idx = i
            chinese_name = match.group(1).strip().replace("\\'", "'")
            english_name = match.group(2).strip()
            break

    if start_idx is None:
        return None

    # Find end (next hexagram or end of file)
    end_idx = len(lines)
    for i in range(start_idx + 1, len(lines)):
        if re.match(r"^## \d+\.", lines[i]):
            end_idx = i
            break

    # Extract hexagram section
    hex_lines = lines[start_idx:end_idx]

    # Now parse sections
    judgment = extract_section(hex_lines, "THE JUDGMENT")
    image = extract_section(hex_lines, "THE IMAGE")
    line_texts = extract_lines(hex_lines)

    if not judgment or not image or len(line_texts) != 6:
        print(f"⚠ Hexagram {hex_num}: incomplete data (judgment={bool(judgment)}, image={bool(image)}, lines={len(line_texts)})")
        return None

    return {
        'chinese_name': chinese_name,
        'english_name': english_name,
        'judgment': judgment.strip(),
        'image': image.strip(),
        'lines': line_texts
    }


def extract_section(hex_lines: list[str], section_name: str) -> Optional[str]:
    """Extract text from a named section like THE JUDGMENT or THE IMAGE."""

    # Find section start
    section_start = None
    for i, line in enumerate(hex_lines):
        if line.strip() == section_name:
            section_start = i + 1
            break

    if section_start is None:
        return None

    # Collect lines until next section or end
    text_lines = []
    for i in range(section_start, len(hex_lines)):
        line = hex_lines[i].strip()

        # Stop at next major section
        if line in ['THE JUDGMENT', 'THE IMAGE', 'THE LINES']:
            break

        # Skip empty lines at start
        if not text_lines and not line:
            continue

        # Add line
        if line:
            text_lines.append(line)
        elif text_lines:  # Empty line after we've started collecting
            text_lines.append('')  # Preserve paragraph breaks

    # Join and clean up
    text = '\n'.join(text_lines).strip()

    # Remove excessive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text


def extract_lines(hex_lines: list[str]) -> Dict[str, Dict[str, str]]:
    """Extract the 6 line interpretations."""

    # Find THE LINES section
    lines_start = None
    for i, line in enumerate(hex_lines):
        if line.strip() == 'THE LINES':
            lines_start = i + 1
            break

    if lines_start is None:
        return {}

    # Line patterns
    line_patterns = [
        (r"^(Nine|Six) at the beginning means:", 1),
        (r"^(Nine|Six) in the second place means:", 2),
        (r"^(Nine|Six) in the third place means:", 3),
        (r"^(Nine|Six) in the fourth place means:", 4),
        (r"^(Nine|Six) in the fifth place means:", 5),
        (r"^(Nine|Six) at the top means:", 6),
    ]

    line_texts = {}
    current_line_num = None
    current_text = []

    for i in range(lines_start, len(hex_lines)):
        line = hex_lines[i].strip()

        # Skip markdown navigation artifacts
        if line in ['[index](#index)', ''] or re.match(r'^\[\]\{#\d+\}', line):
            continue

        # Check if this is a new line marker
        matched_new_line = False
        for pattern, line_num in line_patterns:
            if re.match(pattern, line):
                # Save previous line if any
                if current_line_num is not None:
                    text = '\n'.join(current_text[1:]).strip()
                    # Clean markdown artifacts from text
                    text = clean_markdown_artifacts(text)
                    line_texts[str(current_line_num)] = {
                        'position': get_position_name(current_line_num),
                        'type': 'nine' if current_text[0].startswith('Nine') else 'six',
                        'text': text
                    }

                # Start new line
                current_line_num = line_num
                current_text = [line]
                matched_new_line = True
                break

        if not matched_new_line and current_line_num is not None:
            # Continue collecting text for current line
            if line:
                current_text.append(line)

    # Save last line
    if current_line_num is not None:
        text = '\n'.join(current_text[1:]).strip()
        # Clean markdown artifacts from text
        text = clean_markdown_artifacts(text)
        line_texts[str(current_line_num)] = {
            'position': get_position_name(current_line_num),
            'type': 'nine' if current_text[0].startswith('Nine') else 'six',
            'text': text
        }

    return line_texts


def clean_markdown_artifacts(text: str) -> str:
    """Remove markdown navigation artifacts from text."""
    # Remove [index](#index) links
    text = re.sub(r'\[index\]\(#index\)', '', text)
    # Remove empty anchor tags like []{#2}
    text = re.sub(r'\[\]\{#\d+\}', '', text)
    # Clean up excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def get_position_name(line_num: int) -> str:
    """Get position name for line number."""
    positions = {
        1: 'bottom',
        2: 'second',
        3: 'third',
        4: 'fourth',
        5: 'fifth',
        6: 'topmost'
    }
    return positions.get(line_num, 'unknown')


def convert_to_yaml(hex_data: Dict[str, Any], hex_num: int) -> Dict[str, Any]:
    """Convert extracted data to YAML format (same structure as Legge)."""

    # Load mappings to get trigrams and binary
    from pyching.data import HexagramDataLoader
    loader = HexagramDataLoader(source='legge')
    ref_data = loader.get_hexagram_by_number(hex_num)

    return {
        'metadata': {
            'hexagram': hex_num,
            'king_wen_sequence': hex_num,
            'fu_xi_sequence': hex_num,  # Simplified
            'binary': ref_data['binary'],
            'source': 'wilhelm_baynes',
            'translator': 'Richard Wilhelm / Cary F. Baynes',
            'year': 1950,
            'language': 'en',
            'verified': True
        },
        'name': hex_data['chinese_name'],
        'english_name': hex_data['english_name'],
        'title': f"{hex_num}. {hex_data['chinese_name']} / {hex_data['english_name']}",
        'trigrams': ref_data['trigrams'],
        'judgment': hex_data['judgment'],
        'image': hex_data['image'],
        'lines': hex_data['lines']
    }


def extract_single_hexagram(hex_num: int,
                            md_file: str = 'data/sources/wilhelm/wilhelm.md',
                            output_dir: str = 'data/interpretations/wilhelm'):
    """Extract and save a single hexagram."""

    md_path = Path(md_file)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Read markdown
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Extract
    hex_data = extract_hexagram_from_md(md_content, hex_num)
    if not hex_data:
        print(f"✗ Failed to extract hexagram {hex_num}")
        return False

    # Convert to YAML format
    yaml_data = convert_to_yaml(hex_data, hex_num)

    # Write YAML
    yaml_file = output_path / f'hexagram_{hex_num:02d}.yaml'
    with open(yaml_file, 'w', encoding='utf-8') as f:
        yaml.dump(yaml_data, f,
                 allow_unicode=True,
                 default_flow_style=False,
                 sort_keys=False,
                 width=80)

    print(f"✓ Extracted hexagram {hex_num:02d}: {hex_data['chinese_name']}")
    return True


def extract_all_hexagrams():
    """Extract all 64 hexagrams from Wilhelm markdown."""

    print("Extracting all 64 hexagrams from Wilhelm/Baynes markdown...")

    success_count = 0
    for i in range(1, 65):
        if extract_single_hexagram(i):
            success_count += 1

    print(f"\n✓ Extracted {success_count}/64 hexagrams")
    return success_count == 64


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Extract Wilhelm/Baynes translation from markdown to YAML'
    )
    parser.add_argument('--single', type=int, metavar='N',
                       help='Extract only hexagram N (for testing)')
    parser.add_argument('--all', action='store_true',
                       help='Extract all 64 hexagrams')

    args = parser.parse_args()

    if args.single:
        if not 1 <= args.single <= 64:
            print(f"Error: hexagram number must be 1-64, got {args.single}")
            exit(1)
        success = extract_single_hexagram(args.single)
        exit(0 if success else 1)
    elif args.all:
        success = extract_all_hexagrams()
        exit(0 if success else 1)
    else:
        print("Use --single N to test on one hexagram, or --all for all 64")
        exit(1)
