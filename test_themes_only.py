#!/usr/bin/env python3
"""
Test script to verify theme system

Tests that all themes can be loaded and have correct attributes.
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

import pyching_themes


def test_all_themes_load():
    """Test that all themes can be instantiated"""
    print("Testing all themes can be loaded...")
    print()

    for theme_name, theme_class in pyching_themes.THEMES.items():
        try:
            theme = theme_class()
            print(f"✓ {theme_name:20} → {theme.name}")
            print(f"  Description: {theme.description}")
            print(f"  Line style:  {theme.line_style} (width={theme.line_width}, rounded={theme.line_rounded_corners})")

            # Verify all required attributes exist
            required_attrs = [
                'bgReading', 'bgLabelHint', 'fgLabelHint', 'fgLabelPlaces',
                'fgLabelHexTitles', 'fgLabelLines', 'fgMessageQuestion',
                'colorLineBody', 'colorLineHighlight', 'colorLineShadow',
                'line_style', 'line_width', 'line_rounded_corners',
                'name', 'description'
            ]

            missing_attrs = []
            for attr in required_attrs:
                if not hasattr(theme, attr):
                    missing_attrs.append(attr)

            if missing_attrs:
                print(f"  ✗ Missing attributes: {', '.join(missing_attrs)}")
                return False

            # Show sample colors
            print(f"  Colors: bg={theme.bgReading}, lines={theme.colorLineBody}")
            print()

        except Exception as e:
            print(f"✗ {theme_name}: Error - {e}")
            import traceback
            traceback.print_exc()
            return False

    print("All themes loaded successfully!")
    print()
    return True


def test_get_theme_function():
    """Test the get_theme() helper function"""
    print("Testing get_theme() function...")
    print()

    # Test valid theme names
    for theme_name in pyching_themes.THEMES.keys():
        theme = pyching_themes.get_theme(theme_name)
        if not theme:
            print(f"  ✗ get_theme('{theme_name}') returned None")
            return False
        print(f"  ✓ get_theme('{theme_name}') → {theme.name}")

    # Test invalid theme name (should return default)
    theme = pyching_themes.get_theme('nonexistent-theme')
    if theme.name != "Default (Classic)":
        print(f"  ✗ get_theme('nonexistent') should return default theme")
        return False
    print(f"  ✓ get_theme('nonexistent') → {theme.name} (fallback to default)")

    print()
    print("get_theme() function works correctly!")
    print()
    return True


def test_theme_inheritance():
    """Test that child themes properly inherit from base Theme"""
    print("Testing theme inheritance...")
    print()

    base_theme = pyching_themes.Theme()

    for theme_name, theme_class in pyching_themes.THEMES.items():
        if theme_name == 'default':
            continue  # Skip base theme

        theme = theme_class()

        # Check that theme has all base attributes
        base_attrs = [attr for attr in dir(base_theme) if not attr.startswith('_')]
        for attr in base_attrs:
            if not hasattr(theme, attr):
                print(f"  ✗ {theme_name} missing inherited attribute: {attr}")
                return False

    print("  ✓ All themes properly inherit from base Theme")
    print()
    return True


def main():
    """Run all tests"""
    print("=" * 70)
    print("pyChing Theme System Tests")
    print("=" * 70)
    print()

    all_passed = True

    # Test 1: All themes load
    if not test_all_themes_load():
        all_passed = False

    # Test 2: get_theme() function
    if not test_get_theme_function():
        all_passed = False

    # Test 3: Theme inheritance
    if not test_theme_inheritance():
        all_passed = False

    print("=" * 70)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print()
        print(f"Total themes: {len(pyching_themes.THEMES)}")
        print("Theme names:", ', '.join(pyching_themes.THEMES.keys()))
    else:
        print("✗ SOME TESTS FAILED")

    print("=" * 70)
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
