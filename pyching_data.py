##---------------------------------------------------------------------------##
##
## pyChing -- a Python program to cast and interpret I Ching hexagrams
##
## Copyright (C) 1999-2006 Stephen M. Gava
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be of some
## interest to somebody, but WITHOUT ANY WARRANTY; without even the
## implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
## See the GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING or COPYING.txt. If not,
##  write to the Free Software Foundation, Inc.,
## 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
## The license can also be found at the GNU/FSF website: http://www.gnu.org
##
## Stephen M. Gava
## <elguavas@users.sourceforge.net>
## http://pyching.sourgeforge.net
##
##---------------------------------------------------------------------------##
"""
Modern data access module for pyching.
Loads hexagram data from JSON and provides access methods.
"""
import json
from pathlib import Path
from typing import Dict, Optional

# Cache for hexagram data
_hexagram_data: Optional[Dict[int, dict]] = None


def _load_hexagram_data() -> Dict[int, dict]:
    """Load hexagram data from JSON file. Called once and cached."""
    global _hexagram_data

    if _hexagram_data is not None:
        return _hexagram_data

    # Find the data file relative to this module
    data_file = Path(__file__).parent / 'data' / 'hexagrams.json'

    with open(data_file, 'r', encoding='utf-8') as f:
        hexagrams_list = json.load(f)

    # Convert list to dictionary keyed by hexagram number
    _hexagram_data = {hex_data['number']: hex_data for hex_data in hexagrams_list}

    return _hexagram_data


def BuildHtml(hex_dict: dict) -> str:
    """
    Build an HTML hexagram info string from the passed in dict.

    Args:
        hex_dict: Dictionary containing hexagram data with keys:
                  'imgSrc', 'title', 'text', and 'lines' (dict with keys "1" through "6")

    Returns:
        HTML string representation of the hexagram data
    """
    # Put the <p>'s between the text paragraphs
    text_list = hex_dict['text'].splitlines(True)
    for i in range(len(text_list)):
        if text_list[i].strip() == '':
            text_list[i] = "<p>"
    text_html_str = '\n'.join(text_list)

    lines = hex_dict['lines']
    html_str = (
        f"""<html><body><p><h2><img SRC={hex_dict['imgSrc']}"""
        f"""> {hex_dict['title']}</h2><p>"""
        f"""{text_html_str}<p>"""
        f"""<b>The bottom line</b>, as {lines['1']}<p>"""
        f"""<b>The second line</b>, as {lines['2']}<p>"""
        f"""<b>The third line</b>, as {lines['3']}<p>"""
        f"""<b>The fourth line</b>, as {lines['4']}<p>"""
        f"""<b>The fifth line</b>, as {lines['5']}<p>"""
        f"""<b>The topmost line</b>, as {lines['6']}<p>"""
        f"""</body></html>"""
    )
    return html_str


def get_hexagram_html(hexagram_number: int) -> str:
    """
    Get HTML for a specific hexagram by number.

    Args:
        hexagram_number: Hexagram number (1-64)

    Returns:
        HTML string for the hexagram

    Raises:
        KeyError: If hexagram number is not in valid range (1-64)
    """
    data = _load_hexagram_data()

    if hexagram_number not in data:
        raise KeyError(f"Invalid hexagram number: {hexagram_number}. Must be 1-64.")

    return BuildHtml(data[hexagram_number])


# Backwards compatibility: create individual functions for each hexagram
# This allows old code using pyching_int_data.in1data() to work
def _create_hexagram_function(num: int):
    """Factory function to create hexagram data functions."""
    def hexagram_func():
        return get_hexagram_html(num)
    return hexagram_func


# Generate all 64 hexagram functions
for i in range(1, 65):
    globals()[f'in{i}data'] = _create_hexagram_function(i)
