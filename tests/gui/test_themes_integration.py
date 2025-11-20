#!/usr/bin/env python3
"""
Test script to verify theme system integration

Tests that themes can be loaded and WidgetColors works correctly.
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

import pyching_themes
from pyching_interface_tkinter import WidgetColors


def test_all_themes_load():
    """Test that all themes can be instantiated"""
    print("Testing all themes can be loaded...")

    for theme_name, theme_class in pyching_themes.THEMES.items():
        try:
            theme = theme_class()
            print(f"  ✓ {theme_name}: {theme.name}")

            # Verify all required attributes exist
            required_attrs = [
                'bgReading', 'bgLabelHint', 'fgLabelHint', 'fgLabelPlaces',
                'fgLabelHexTitles', 'fgLabelLines', 'fgMessageQuestion',
                'colorLineBody', 'colorLineHighlight', 'colorLineShadow',
                'line_style', 'line_width', 'line_rounded_corners',
                'name', 'description'
            ]

            for attr in required_attrs:
                if not hasattr(theme, attr):
                    print(f"    ✗ Missing attribute: {attr}")
                    return False

        except Exception as e:
            print(f"  ✗ {theme_name}: Error - {e}")
            return False

    print("  All themes loaded successfully!\n")
    return True


def test_widget_colors_integration():
    """Test that WidgetColors can load themes"""
    print("Testing WidgetColors integration...")

    for theme_name in pyching_themes.THEMES.keys():
        try:
            colors = WidgetColors(theme_name)

            # Verify colors has theme object
            if not hasattr(colors, 'theme'):
                print(f"  ✗ {theme_name}: WidgetColors missing 'theme' attribute")
                return False

            # Verify all color attributes are copied
            if colors.bgReading != colors.theme.bgReading:
                print(f"  ✗ {theme_name}: bgReading not copied correctly")
                return False

            if colors.colorLineBody != colors.theme.colorLineBody:
                print(f"  ✗ {theme_name}: colorLineBody not copied correctly")
                return False

            print(f"  ✓ {theme_name}: WidgetColors loaded correctly")

        except Exception as e:
            print(f"  ✗ {theme_name}: Error - {e}")
            import traceback
            traceback.print_exc()
            return False

    print("  WidgetColors integration successful!\n")
    return True


def test_theme_properties():
    """Test that themes have correct line_style settings"""
    print("Testing theme line_style properties...")

    expected_styles = {
        'default': 'beveled',
        'system': 'flat',
        'solarized-dark': 'flat',
        'solarized-light': 'flat',
        'tokyo-night': 'flat',
        'tokyo-night-storm': 'flat',
        'nord': 'flat',
        'dracula': 'flat',
        'gruvbox-dark': 'flat',
    }

    for theme_name, expected_style in expected_styles.items():
        theme = pyching_themes.get_theme(theme_name)
        if theme.line_style != expected_style:
            print(f"  ✗ {theme_name}: Expected line_style '{expected_style}', got '{theme.line_style}'")
            return False
        else:
            print(f"  ✓ {theme_name}: line_style = '{theme.line_style}'")

    print("  Theme properties correct!\n")
    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("Theme System Integration Tests")
    print("=" * 60)
    print()

    all_passed = True

    # Test 1: All themes load
    if not test_all_themes_load():
        all_passed = False

    # Test 2: WidgetColors integration
    if not test_widget_colors_integration():
        all_passed = False

    # Test 3: Theme properties
    if not test_theme_properties():
        all_passed = False

    print("=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print("=" * 60)
        return 1


if __name__ == '__main__':
    sys.exit(main())
