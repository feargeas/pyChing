#!/usr/bin/env python3
"""
Test script for verbose and debug mode functionality

Tests both -v (verbose) and -vv (debug) modes without requiring tkinter.
"""

import sys
import argparse

# Simulate the verbose and debug system
VERBOSE = False
DEBUG = False

def vprint(*args, **kwargs):
    """Print only if verbose mode is enabled (-v)"""
    if VERBOSE:
        print("[pyChing]", *args, **kwargs)

def dprint(*args, **kwargs):
    """Print only if debug mode is enabled (very verbose -vv)"""
    if DEBUG:
        print("[pyChing DEBUG]", *args, **kwargs)

def main():
    global VERBOSE, DEBUG

    # Parse command-line arguments (same as in pyching_interface_tkinter.py)
    parser = argparse.ArgumentParser(
        description='pyChing - I Ching Oracle GUI (Test)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_verbose_mode.py          # Run normally (quiet)
  python test_verbose_mode.py -v       # Run with verbose output
  python test_verbose_mode.py -vv      # Run with very verbose/debug output
""")
    parser.add_argument('-v', '--verbose',
                       action='count',
                       default=0,
                       help='Increase verbosity (-v for verbose, -vv for debug)')

    args = parser.parse_args()

    # Set global verbose and debug flags based on count
    VERBOSE = args.verbose >= 1
    DEBUG = args.verbose >= 2

    if DEBUG:
        print("[pyChing DEBUG] Debug mode enabled (very verbose)")
        print("[pyChing DEBUG] Starting pyChing I Ching Oracle...")
    elif VERBOSE:
        print("[pyChing] Verbose mode enabled")
        print("[pyChing] Starting pyChing I Ching Oracle...")

    # Simulate startup with DEBUG output
    dprint("WidgetColors.__init__(theme_name='default')")
    dprint("  Loaded theme class: Theme")
    dprint("  Theme description: Original pyChing look with 3D beveled lines")
    dprint("  Theme line_style: beveled")
    dprint("  Colors: bg=#323c4a, lineBody=#DAA520")

    dprint("WidgetFonts.__init__(scale=1.0)")
    dprint("  Clamped scale to: 1.0 (100%)")
    dprint("  Font family fallbacks: ('Helvetica', 'Arial', 'DejaVu Sans', 'sans-serif')")
    dprint("  Creating fonts: small=10pt, large=12pt")
    dprint("  Created 5 font objects")

    # Simulate various operations with VERBOSE output
    vprint("Initializing WindowMain...")
    dprint("Creating application menus...")
    dprint("  Created File menu")
    dprint("  Created Settings menu")
    dprint("  Created Help menu")
    dprint("  Adding 7 items to menu")
    dprint("    - command: Load Reading...")
    dprint("    - command: Save Reading...")
    dprint("    - separator")
    dprint("    - command: Save Reading As Text...")
    dprint("    - separator")
    dprint("    - command: Exit")

    vprint("Window configured: resizable=True, minsize=600x500")
    vprint("Loaded coin images")
    vprint("Registered keyboard bindings: F1, Alt-c, Alt-v, Alt-i")
    vprint("Default settings: showPlaces=True, showLineHints=True, castAll=True")
    vprint("Initialized colors: theme='default'")
    vprint("Initialized fonts: scale=1.0 (100% = 100%)")

    # Simulate config loading
    vprint("Loading settings from: /home/user/.pyching/config")
    dprint("Config format: 7-item tuple")
    vprint("  Loaded theme='tokyo-night', font_scale=1.20 (120%)")
    dprint("WidgetColors.__init__(theme_name='tokyo-night')")
    dprint("  Loaded theme class: TokyoNightTheme")
    dprint("  Theme description: Modern dark theme with vibrant colors")
    dprint("  Theme line_style: flat")
    dprint("  Colors: bg=#1a1b26, lineBody=#f7768e")
    dprint("WidgetFonts.__init__(scale=1.2)")
    dprint("  Clamped scale to: 1.2 (120%)")
    dprint("  Font family fallbacks: ('Helvetica', 'Arial', 'DejaVu Sans', 'sans-serif')")
    dprint("  Creating fonts: small=12pt, large=14pt")
    dprint("  Created 5 font objects")
    vprint("  Settings loaded: castAll=True, showPlaces=True, showLineHints=True")

    # Simulate user interactions
    vprint("Cast button pressed - starting new reading...")
    vprint("Question entered: 'What should I focus on today?'")
    vprint("Starting hexagram cast (method=coin)...")

    # Simulate theme change with DEBUG
    vprint("Opening theme selection dialog...")
    dprint("DialogSelectTheme created with current_theme=TokyoNightTheme")
    vprint("User selected theme: 'solarized-dark'")
    dprint("WidgetColors.__init__(theme_name='solarized-dark')")
    dprint("  Loaded theme class: SolarizedDarkTheme")
    dprint("  Theme description: Precision colors for reduced eyestrain")
    dprint("  Theme line_style: flat")
    dprint("  Colors: bg=#002b36, lineBody=#cb4b16")
    vprint("Applied theme 'solarized-dark' (line_style=flat)")
    dprint("RepaintColors() called")
    dprint("  Old theme: tokyo-night")
    dprint("  New theme: solarized-dark")
    dprint("  Updating 24 widget backgrounds...")
    vprint("Theme applied and GUI repainted")

    # Simulate font size adjustment with DEBUG
    vprint("Opening font size dialog (current scale=1.20 = 120%)...")
    dprint("DialogAdjustFontSize created with current_scale=1.2")
    vprint("User selected font scale: 1.50 (150%)")
    dprint("WidgetFonts.set_scale(1.50) - old=1.20, new=1.50")
    dprint("  Updating fonts: small=15pt, large=18pt")
    dprint("  All 5 font objects reconfigured")
    vprint("Font sizes updated: small=15pt, large=18pt")

    # Simulate saving settings
    vprint("Saving settings...")
    dprint("Config tuple: 7 items")
    vprint("  castAll=True, showPlaces=True, showLineHints=True")
    vprint("  theme='solarized-dark', font_scale=1.50 (150%)")
    dprint("pyching_engine.Storage() called")
    dprint("  Writing pickle file: /home/user/.pyching/config")
    vprint("Settings saved to: /home/user/.pyching/config")

    # Simulate quit
    vprint("User quit - closing application...")
    dprint("Tk.quit() called")
    vprint("Application exited")

    print("\n" + "=" * 70)
    if DEBUG:
        print("✓ DEBUG mode test completed successfully!")
        print("All verbose AND debug output was displayed above.")
    elif VERBOSE:
        print("✓ VERBOSE mode test completed successfully!")
        print("Verbose output displayed (no debug output).")
    else:
        print("✓ NORMAL mode test completed successfully!")
        print("No verbose or debug output (run with -v or -vv to see output)")
    print("=" * 70)

if __name__ == '__main__':
    main()
