#!/usr/bin/env python3
"""
Convert legacy pyching_int_data.py to modern JSON format.

This tool extracts hexagram data from the original Python functions
and converts them to structured JSON files.
"""

import sys
import json
import re
import argparse
from pathlib import Path

# Add parent directory to path to import legacy modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import pyching_int_data


# Trigram data for mapping
TRIGRAMS = {
    "qian": {"name": "Heaven", "binary": "111", "attribute": "Creative"},
    "kun": {"name": "Earth", "binary": "000", "attribute": "Receptive"},
    "zhen": {"name": "Thunder", "binary": "001", "attribute": "Arousing"},
    "kan": {"name": "Water", "binary": "010", "attribute": "Abysmal"},
    "gen": {"name": "Mountain", "binary": "100", "attribute": "Keeping Still"},
    "xun": {"name": "Wind", "binary": "110", "attribute": "Gentle"},
    "li": {"name": "Fire", "binary": "101", "attribute": "Clinging"},
    "dui": {"name": "Lake", "binary": "011", "attribute": "Joyous"},
}

# Hexagram to trigram mapping (King Wen sequence)
# Format: hexagram_number: (upper_trigram, lower_trigram)
HEXAGRAM_TRIGRAMS = {
    1: ("qian", "qian"),
    2: ("kun", "kun"),
    3: ("kan", "zhen"),
    4: ("gen", "kan"),
    5: ("kan", "qian"),
    6: ("qian", "kan"),
    7: ("kun", "kan"),
    8: ("kan", "kun"),
    9: ("xun", "qian"),
    10: ("qian", "dui"),
    11: ("kun", "qian"),
    12: ("qian", "kun"),
    13: ("qian", "li"),
    14: ("li", "qian"),
    15: ("kun", "gen"),
    16: ("zhen", "kun"),
    17: ("dui", "zhen"),
    18: ("gen", "xun"),
    19: ("kun", "dui"),
    20: ("xun", "kun"),
    21: ("li", "zhen"),
    22: ("gen", "li"),
    23: ("gen", "kun"),
    24: ("kun", "zhen"),
    25: ("qian", "zhen"),
    26: ("gen", "qian"),
    27: ("gen", "zhen"),
    28: ("dui", "xun"),
    29: ("kan", "kan"),
    30: ("li", "li"),
    31: ("dui", "gen"),
    32: ("zhen", "xun"),
    33: ("qian", "gen"),
    34: ("zhen", "qian"),
    35: ("li", "kun"),
    36: ("kun", "li"),
    37: ("xun", "li"),
    38: ("li", "dui"),
    39: ("kan", "gen"),
    40: ("zhen", "kan"),
    41: ("gen", "dui"),
    42: ("xun", "zhen"),
    43: ("dui", "qian"),
    44: ("qian", "xun"),
    45: ("dui", "kun"),
    46: ("kun", "xun"),
    47: ("dui", "kan"),
    48: ("kan", "xun"),
    49: ("dui", "li"),
    50: ("li", "xun"),
    51: ("zhen", "zhen"),
    52: ("gen", "gen"),
    53: ("xun", "gen"),
    54: ("zhen", "dui"),
    55: ("zhen", "li"),
    56: ("li", "gen"),
    57: ("xun", "xun"),
    58: ("dui", "dui"),
    59: ("xun", "kan"),
    60: ("kan", "dui"),
    61: ("xun", "dui"),
    62: ("zhen", "gen"),
    63: ("kan", "li"),
    64: ("li", "kan"),
}


def parse_title(title_str):
    """
    Parse title string to extract number, name, and English name.

    Example: " 1. Tch'ien / The Creative" -> (1, "Tch'ien", "The Creative")
    """
    # Remove leading/trailing whitespace
    title_str = title_str.strip()

    # Pattern: number. name / english_name
    match = re.match(r'(\d+)\.\s+([^/]+)\s*/\s*(.+)', title_str)

    if not match:
        raise ValueError(f"Could not parse title: {title_str}")

    number = int(match.group(1))
    name = match.group(2).strip()
    english_name = match.group(3).strip()

    return number, name, english_name


def extract_hexagram_data(hex_num):
    """
    Extract data for a single hexagram from legacy format.

    Args:
        hex_num: Hexagram number (1-64)

    Returns:
        dict: Structured hexagram data
    """
    # Get the function name
    func_name = f"in{hex_num}data"

    # Get the function from the module
    if not hasattr(pyching_int_data, func_name):
        raise ValueError(f"Function {func_name} not found in pyching_int_data")

    func = getattr(pyching_int_data, func_name)

    # Call the function to get HTML (we'll parse the raw dict instead)
    # We need to access the dict before BuildHtml processes it
    # Let's extract it by temporarily modifying BuildHtml

    # Actually, easier to just extract from source - but for now,
    # let's parse the HTML output
    html_output = func()

    # For proof of concept, let's manually create the structure
    # In production, we'd parse the HTML or modify BuildHtml temporarily

    # For now, call the function and extract via introspection
    # We'll need to get the raw dict data

    # Alternative: Read the source directly
    # But for PoC, let's hardcode the extraction for hexagrams 1, 2, 64

    raise NotImplementedError("Need to extract dict data from function source")


def extract_from_source(hex_num):
    """
    Extract hexagram data by parsing the source code directly.

    This is more reliable than trying to intercept BuildHtml.
    """
    import inspect
    import ast

    func_name = f"in{hex_num}data"
    func = getattr(pyching_int_data, func_name)

    # Get source code
    source = inspect.getsource(func)

    # Parse the AST
    tree = ast.parse(source)

    # Find the dict literal in the return statement
    for node in ast.walk(tree):
        if isinstance(node, ast.Return):
            if isinstance(node.value, ast.Call):
                if len(node.value.args) > 0:
                    dict_node = node.value.args[0]
                    if isinstance(dict_node, ast.Dict):
                        # Extract dict data
                        data = {}
                        for key, value in zip(dict_node.keys, dict_node.values):
                            if isinstance(key, ast.Constant):
                                key_val = key.value
                            elif isinstance(key, ast.Num):  # Python < 3.8
                                key_val = key.n
                            else:
                                continue

                            if isinstance(value, ast.Constant):
                                val = value.value
                            elif isinstance(value, ast.Str):  # Python < 3.8
                                val = value.s
                            else:
                                continue

                            data[key_val] = val

                        return data

    raise ValueError(f"Could not extract dict from {func_name}")


def convert_to_json_structure(hex_num, data_dict):
    """
    Convert legacy dict structure to new JSON format.

    Args:
        hex_num: Hexagram number
        data_dict: Dict extracted from legacy function

    Returns:
        dict: JSON-formatted hexagram data
    """
    # Parse title
    number, name, english_name = parse_title(data_dict['title'])

    # Get trigrams
    upper_trigram, lower_trigram = HEXAGRAM_TRIGRAMS[hex_num]

    # Calculate binary pattern
    upper_bin = TRIGRAMS[upper_trigram]['binary']
    lower_bin = TRIGRAMS[lower_trigram]['binary']
    binary = upper_bin + lower_bin

    # Split the text field into judgment and image
    # The text usually has two paragraphs separated by blank line
    text_parts = data_dict['text'].strip().split('\n\n')

    if len(text_parts) >= 2:
        image = text_parts[0].strip()
        judgment = text_parts[1].strip()
    else:
        # Fallback if format is different
        image = ""
        judgment = text_parts[0].strip() if text_parts else ""

    # Extract line data
    lines = {}
    position_names = {
        1: "bottom",
        2: "second",
        3: "third",
        4: "fourth",
        5: "fifth",
        6: "topmost"
    }

    for line_num in range(1, 7):
        line_text = data_dict[line_num].strip()

        # Extract line type (six, nine) from beginning
        line_type = "nine"  # default
        if line_text.startswith("six:"):
            line_type = "six"
            line_text = line_text[4:].strip()
        elif line_text.startswith("nine:"):
            line_type = "nine"
            line_text = line_text[5:].strip()

        lines[str(line_num)] = {
            "position": position_names[line_num],
            "type": line_type,
            "text": line_text
        }

    # Build the JSON structure
    json_data = {
        "hexagram_id": f"hexagram_{hex_num:02d}",
        "number": hex_num,
        "king_wen_sequence": hex_num,
        "fu_xi_sequence": hex_num,  # TODO: Add proper Fu Xi mapping
        "binary": binary,
        "trigrams": {
            "upper": upper_trigram,
            "lower": lower_trigram
        },
        "canonical": {
            "source_id": "legge_1882",
            "name": name,
            "english_name": english_name,
            "title": data_dict['title'].strip(),
            "judgment": judgment,
            "image": image,
            "lines": lines,
            "metadata": {
                "translator": "James Legge",
                "year": 1882,
                "language": "en",
                "verified": True,
                "notes": "Original translation preserved from pyChing v1.2.2"
            }
        },
        "sources": {}
    }

    return json_data


def convert_hexagram(hex_num, output_dir):
    """
    Convert a single hexagram to JSON.

    Args:
        hex_num: Hexagram number (1-64)
        output_dir: Output directory path
    """
    print(f"Converting hexagram {hex_num}...")

    # Extract data
    data_dict = extract_from_source(hex_num)

    # Convert to JSON structure
    json_data = convert_to_json_structure(hex_num, data_dict)

    # Write to file
    output_file = output_dir / f"hexagram_{hex_num:02d}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    print(f"  -> Saved to {output_file}")

    return json_data


def main():
    """Main conversion function."""
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Convert legacy pyChing hexagram data to JSON format"
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Convert all 64 hexagrams (default: convert 1, 2, 64 as proof of concept)'
    )
    parser.add_argument(
        '--hexagrams',
        type=int,
        nargs='+',
        metavar='N',
        help='Specific hexagrams to convert (e.g., --hexagrams 1 2 3)'
    )
    args = parser.parse_args()

    # Setup paths
    project_root = Path(__file__).parent.parent
    output_dir = project_root / 'data' / 'hexagrams'
    output_dir.mkdir(parents=True, exist_ok=True)

    # Determine which hexagrams to convert
    if args.hexagrams:
        hexagrams_to_convert = args.hexagrams
        mode = "custom"
    elif args.all:
        hexagrams_to_convert = list(range(1, 65))  # All 64 hexagrams
        mode = "all"
    else:
        hexagrams_to_convert = [1, 2, 64]  # Proof of concept
        mode = "poc"

    print("Converting legacy hexagram data to JSON...")
    print(f"Mode: {mode}")
    print(f"Hexagrams to convert: {len(hexagrams_to_convert)}")
    print(f"Output directory: {output_dir}")
    print()

    converted = []
    failed = []

    for hex_num in hexagrams_to_convert:
        try:
            json_data = convert_hexagram(hex_num, output_dir)
            converted.append(hex_num)
        except Exception as e:
            print(f"  ERROR converting hexagram {hex_num}: {e}")
            failed.append(hex_num)
            if mode != "all":  # Show traceback for non-batch conversions
                import traceback
                traceback.print_exc()

    print()
    print(f"Successfully converted {len(converted)} hexagrams")

    if failed:
        print(f"Failed to convert {len(failed)} hexagrams: {failed}")

    if mode == "all" and len(converted) == 64:
        print("\n" + "=" * 60)
        print("✓ ALL 64 HEXAGRAMS CONVERTED SUCCESSFULLY!")
        print("=" * 60)
        return 0
    elif mode == "poc" and len(converted) == len(hexagrams_to_convert):
        print("\n✓ Proof of concept complete!")
        print("  Review the generated JSON files, then run with --all to convert all 64 hexagrams")
        return 0
    elif len(converted) == len(hexagrams_to_convert):
        print("\n✓ All requested hexagrams converted successfully!")
        return 0
    else:
        print("\n✗ Some conversions failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
