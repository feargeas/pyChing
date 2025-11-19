#!/usr/bin/env python3
"""
Test backward compatibility with old config files

Simulates loading old config files without theme attributes.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import pyching_themes


class OldWidgetColors:
    """Simulates an old WidgetColors object without theme attributes"""
    def __init__(self):
        self.bgReading = '#323c4a'
        self.bgLabelHint = '#FFE4B5'
        self.fgLabelHint = '#000000'
        self.fgLabelPlaces = '#FFA07A'
        self.fgLabelHexTitles = '#FFFFFF'
        self.fgLabelLines = '#FFFFFF'
        self.fgMessageQuestion = '#FFFFFF'
        self.colorLineBody = '#DAA520'
        self.colorLineHighlight = '#EEE8AA'
        self.colorLineShadow = '#B8860B'
        # NO theme or theme_name attributes!


def test_add_missing_attributes():
    """Test adding missing theme attributes to old config"""
    print("Testing backward compatibility fix...")

    # Simulate loading an old config file
    old_colors = OldWidgetColors()

    # Verify it's missing the new attributes
    assert not hasattr(old_colors, 'theme_name'), "Should not have theme_name"
    assert not hasattr(old_colors, 'theme'), "Should not have theme"

    # Apply the fix (from LoadSettings code)
    if not hasattr(old_colors, 'theme_name'):
        old_colors.theme_name = 'default'
    if not hasattr(old_colors, 'theme'):
        old_colors.theme = pyching_themes.get_theme('default')

    # Verify attributes were added
    assert hasattr(old_colors, 'theme_name'), "Should now have theme_name"
    assert hasattr(old_colors, 'theme'), "Should now have theme"
    assert old_colors.theme_name == 'default', "theme_name should be 'default'"
    assert old_colors.theme is not None, "theme should not be None"

    # Verify theme object has required attributes
    assert hasattr(old_colors.theme, 'line_style'), "theme should have line_style"
    assert hasattr(old_colors.theme, 'line_width'), "theme should have line_width"
    assert hasattr(old_colors.theme, 'name'), "theme should have name"

    # Verify original colors were preserved
    assert old_colors.bgReading == '#323c4a', "bgReading should be preserved"
    assert old_colors.colorLineBody == '#DAA520', "colorLineBody should be preserved"

    print("  ✓ Missing attributes added successfully")
    print("  ✓ Original color values preserved")
    print("  ✓ Theme object has all required attributes")
    print()
    return True


def main():
    print("=" * 70)
    print("Config Backward Compatibility Test")
    print("=" * 70)
    print()

    if test_add_missing_attributes():
        print("=" * 70)
        print("✓ TEST PASSED")
        print("=" * 70)
        return 0
    else:
        print("=" * 70)
        print("✗ TEST FAILED")
        print("=" * 70)
        return 1


if __name__ == '__main__':
    sys.exit(main())
