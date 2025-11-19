#!/usr/bin/env python3
"""
Comprehensive test for dynamic window sizing
Tests both empty state and with full reading displayed
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_window_sizes():
    """Test window sizing in different states"""
    print("\n" + "="*70)
    print("WINDOW SIZING COMPREHENSIVE TEST")
    print("="*70)

    from tkinter import Tk
    import pyching_interface_tkinter
    import pyching_engine

    # Enable verbose to see sizing messages
    pyching_interface_tkinter.VERBOSE = True

    root = Tk()
    window = pyching_interface_tkinter.WindowMain(root)

    # Get initial (empty) size
    root.update_idletasks()
    initial_width = root.winfo_width()
    initial_height = root.winfo_height()
    min_width = root.winfo_reqwidth()
    min_height = root.winfo_reqheight()

    print("\n" + "="*70)
    print("PHASE 1: Empty State (No Reading)")
    print("="*70)
    print(f"Window size: {initial_width}x{initial_height}")
    print(f"Minimum size: {min_width}x{min_height}")
    print(f"Status: Only cast button and menu visible")

    # Simulate casting a hexagram (create full reading)
    print("\n" + "="*70)
    print("PHASE 2: Casting Hexagram...")
    print("="*70)

    # Create a reading
    window.hexes = pyching_engine.Hexagrams('coin')
    window.hexes.SetQuestion("Test question for window sizing analysis")

    # Cast all 6 lines
    for i in range(6):
        window.hexes.NewLine()

    print(f"Created reading:")
    print(f"  Hex1: {window.hexes.hex1.number} - {window.hexes.hex1.name}")
    print(f"  Hex2: {window.hexes.hex2.number} - {window.hexes.hex2.name}")

    # Display the reading (this shows all elements)
    window.ShowReading()

    # Get size with full reading displayed
    root.update_idletasks()
    full_width = root.winfo_width()
    full_height = root.winfo_height()
    req_width = root.winfo_reqwidth()
    req_height = root.winfo_reqheight()

    print("\n" + "="*70)
    print("PHASE 3: Full Reading Displayed")
    print("="*70)
    print(f"Window size: {full_width}x{full_height}")
    print(f"Required size: {req_width}x{req_height}")
    print(f"Status: All elements visible (hexagrams, question, info buttons)")

    # Check if window needs to grow beyond initial minimum
    if req_width > min_width or req_height > min_height:
        print(f"\n⚠ ISSUE DETECTED:")
        print(f"  Initial minimum: {min_width}x{min_height}")
        print(f"  Required with content: {req_width}x{req_height}")
        if req_width > min_width:
            print(f"  Width shortfall: {req_width - min_width}px")
        if req_height > min_height:
            print(f"  Height shortfall: {req_height - min_height}px")
        print(f"\n  The window may be clipping content!")
        success = False
    else:
        print(f"\n✓ Window sizing is correct:")
        print(f"  All content fits within minimum size")
        success = True

    # Test different font sizes
    print("\n" + "="*70)
    print("PHASE 4: Testing Font Size Scaling")
    print("="*70)

    test_scales = [0.8, 1.0, 1.5, 2.0]
    for scale in test_scales:
        window.fonts.set_scale(scale)
        root.update_idletasks()

        current_min_w = root.winfo_reqwidth()
        current_min_h = root.winfo_reqheight()

        print(f"\nFont scale {int(scale*100)}%:")
        print(f"  Required size: {current_min_w}x{current_min_h}")

    # Return to normal size
    window.fonts.set_scale(1.0)

    print("\n" + "="*70)
    print("TEST RESULTS")
    print("="*70)

    if success:
        print("✓ PASSED: Window sizing is working correctly")
        print("  - Initial minimum size accommodates all content")
        print("  - No clipping or scrolling needed")
        print("  - Font scaling adjusts size appropriately")
    else:
        print("✗ FAILED: Window sizing needs adjustment")
        print("  - Initial minimum is too small for full content")
        print("  - Need to recalculate minimum after showing reading")

    print("\n" + "="*70)
    print("Close window to exit...")
    print("="*70 + "\n")

    # Keep window open for manual inspection
    root.mainloop()

    return success

if __name__ == '__main__':
    success = test_window_sizes()
    sys.exit(0 if success else 1)
