"""
Tests verifying the hexagram inversion bug fix.

The bug: loader.py was building binary strings without reversing the lines array,
causing hexagrams from casting to be inverted (upside-down).

Fix: Added reversed() at loader.py:196 and pyching_interface_tkinter.py:987
"""
import pytest
from pyching import Hexagram


def test_hexagram_44_from_lines():
    """Hex 44 has one yin at bottom."""
    lines = [8, 7, 7, 7, 7, 7]  # line 1-6
    hex = Hexagram.from_lines(lines)
    assert hex.number == 44
    assert hex.binary == "111110"  # top-to-bottom


def test_hexagram_1_from_lines():
    """Hex 1 is all yang."""
    lines = [7, 7, 7, 7, 7, 7]
    hex = Hexagram.from_lines(lines)
    assert hex.number == 1
    assert hex.binary == "111111"


def test_hexagram_2_from_lines():
    """Hex 2 is all yin."""
    lines = [8, 8, 8, 8, 8, 8]
    hex = Hexagram.from_lines(lines)
    assert hex.number == 2
    assert hex.binary == "000000"


def test_moving_lines_transform():
    """Moving lines should preserve position."""
    lines = [8, 9, 7, 6, 7, 8]  # Lines 2 and 4 moving
    hex1 = Hexagram.from_lines(lines)
    
    # Transform
    transformed = [8, 8, 7, 7, 7, 8]  # 9→8, 6→7
    hex2 = Hexagram.from_lines(transformed)
    
    # Should be different hexagrams
    assert hex1.number != hex2.number


def test_line_positions():
    """Verify line position interpretation."""
    lines = [6, 8, 8, 8, 8, 8]  # Only line 1 moving
    hex = Hexagram.from_lines(lines)
    moving = hex.get_moving_lines()
    assert moving == [1]  # Line 1, not line 6
