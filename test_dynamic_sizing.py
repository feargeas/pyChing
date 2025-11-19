#!/usr/bin/env python3
"""
Test script to verify dynamic window sizing
Launches GUI and reports the calculated minimum size
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Set verbose mode to see sizing information
import pyching_interface_tkinter
pyching_interface_tkinter.VERBOSE = True
pyching_interface_tkinter.DEBUG = True

def test_dynamic_sizing():
    """Test that window calculates its minimum size dynamically"""
    print("\n" + "="*70)
    print("DYNAMIC WINDOW SIZING TEST")
    print("="*70)
    print("\nThis test will:")
    print("  1. Launch the GUI")
    print("  2. Calculate natural window size based on content")
    print("  3. Set that as the minimum size")
    print("  4. Report the calculated dimensions")
    print("\nWatch for 'Set dynamic minsize' message in verbose output...")
    print("\n" + "="*70 + "\n")

    # Import tkinter and launch
    from tkinter import Tk
    import pyching_engine

    root = Tk()

    # Create main window (will calculate dynamic size)
    window = pyching_interface_tkinter.WindowMain(root)

    # Get the calculated minimum size
    min_width = root.winfo_reqwidth()
    min_height = root.winfo_reqheight()

    print("\n" + "="*70)
    print("SIZING RESULTS")
    print("="*70)
    print(f"Calculated minimum width:  {min_width}px")
    print(f"Calculated minimum height: {min_height}px")
    print(f"\nWindow will:")
    print(f"  - Start at exactly {min_width}x{min_height}")
    print(f"  - Cannot be shrunk below this size")
    print(f"  - Can be resized larger by user")
    print(f"\nOld hardcoded size was: 600x500")

    if min_width < 600:
        print(f"  → Width optimized: saved {600 - min_width}px horizontal space")
    elif min_width > 600:
        print(f"  → Width expanded: needed {min_width - 600}px more horizontal space")
    else:
        print(f"  → Width unchanged")

    if min_height < 500:
        print(f"  → Height optimized: saved {500 - min_height}px vertical space")
    elif min_height > 500:
        print(f"  → Height expanded: needed {min_height - 500}px more vertical space")
    else:
        print(f"  → Height unchanged")

    print("\n" + "="*70)
    print("TEST COMPLETE")
    print("="*70)
    print("\nClose the window to exit test...")

    # Run briefly to show the window
    root.after(100, lambda: None)  # Small delay to show window
    root.mainloop()

if __name__ == '__main__':
    test_dynamic_sizing()
