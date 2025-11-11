#!/usr/bin/env python3
"""
Script to extract hexagram data from pyching_int_data.py and convert to JSON
"""

import json
import re
from pathlib import Path

def extract_hexagram_data(file_path):
    """Extract all hexagram data from the pyching_int_data.py file"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    hexagrams = []

    # Find all functions in1data() through in64data()
    for i in range(1, 65):
        # Find the function definition
        func_pattern = rf"def in{i}data\(\):\s*return BuildHtml\(\s*\{{"
        match = re.search(func_pattern, content)

        if not match:
            print(f"Warning: Could not find function in{i}data()")
            continue

        # Find the start of the dictionary
        dict_start = content.find('{', match.end() - 1)

        # Extract the dictionary by finding matching braces
        brace_count = 0
        pos = dict_start
        in_triple_quote = False
        triple_quote_char = None

        while pos < len(content):
            # Check for triple quotes
            if pos + 2 < len(content):
                three_char = content[pos:pos+3]
                if three_char in ['"""', "'''"]:
                    if not in_triple_quote:
                        in_triple_quote = True
                        triple_quote_char = three_char
                        pos += 3
                        continue
                    elif three_char == triple_quote_char:
                        in_triple_quote = False
                        triple_quote_char = None
                        pos += 3
                        continue

            if in_triple_quote:
                pos += 1
                continue

            char = content[pos]

            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    # Found the end of the dictionary
                    dict_text = content[dict_start:pos+1]
                    hexagram_data = parse_dict_text(dict_text, i)
                    if hexagram_data:
                        hexagrams.append(hexagram_data)
                    break

            pos += 1

    return hexagrams

def parse_dict_text(dict_text, hexagram_num):
    """Parse the dictionary text and extract values"""

    hexagram = {
        'number': hexagram_num,
        'imgSrc': '',
        'title': '',
        'text': '',
        'lines': {}
    }

    # Extract imgSrc
    imgSrc_match = re.search(r"'imgSrc'\s*:\s*\"([^\"]+)\"", dict_text)
    if imgSrc_match:
        hexagram['imgSrc'] = imgSrc_match.group(1)

    # Extract title (triple quoted)
    title_match = re.search(r"'title'\s*:\s*\"\"\"([^\"]+)\"\"\"", dict_text)
    if title_match:
        hexagram['title'] = title_match.group(1)

    # Extract text (triple quoted, multiline)
    text_match = re.search(r"'text'\s*:\s*\"\"\"(.*?)\"\"\"", dict_text, re.DOTALL)
    if text_match:
        hexagram['text'] = text_match.group(1)

    # Extract the six lines
    for line_num in range(1, 7):
        line_pattern = rf"{line_num}\s*:\s*\"\"\"(.*?)\"\"\""
        line_match = re.search(line_pattern, dict_text, re.DOTALL)
        if line_match:
            hexagram['lines'][str(line_num)] = line_match.group(1)

    return hexagram

def main():
    input_file = Path('/home/user/pyChing/pyching_int_data.py')
    output_file = Path('/home/user/pyChing/data/hexagrams.json')

    # Create data directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)

    print(f"Extracting hexagram data from {input_file}...")
    hexagrams = extract_hexagram_data(input_file)

    print(f"Extracted {len(hexagrams)} hexagrams")

    # Sort by hexagram number to ensure they're in order
    hexagrams.sort(key=lambda x: x['number'])

    # Write to JSON file with nice formatting
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(hexagrams, f, indent=2, ensure_ascii=False)

    print(f"Successfully wrote hexagram data to {output_file}")

    # Print summary
    print(f"\nSummary:")
    print(f"  Total hexagrams extracted: {len(hexagrams)}")
    print(f"  Output file: {output_file}")
    print(f"  File size: {output_file.stat().st_size} bytes")

    # Verify a couple of hexagrams
    if hexagrams:
        print(f"\nVerification:")
        hex1 = next((h for h in hexagrams if h['number'] == 1), None)
        if hex1:
            print(f"  Hexagram 1 title: {hex1['title']}")
        hex64 = next((h for h in hexagrams if h['number'] == 64), None)
        if hex64:
            print(f"  Hexagram 64 title: {hex64['title']}")

if __name__ == '__main__':
    main()
