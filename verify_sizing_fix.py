#!/usr/bin/env python3
"""
Verify that window sizing properly accommodates all content including info buttons
This test verifies the fix for info buttons not being in initial layout
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

print("\n" + "="*70)
print("VERIFICATION: Dynamic Sizing with Info Buttons Fix")
print("="*70)
print("\nThis test verifies:")
print("  1. Initial minimum size is set based on visible content")
print("  2. When first reading is cast, info buttons appear")
print("  3. Minimum size is recalculated to include info buttons")
print("  4. Window is always sized correctly for all active elements")
print("="*70)

from tkinter import Tk
import pyching_interface_tkinter as pyt
import pyching_engine

# Enable verbose output
pyt.VERBOSE = True
pyt.DEBUG = True

root = Tk()
root.withdraw()  # Hide for automated testing

print("\n" + "-"*70)
print("PHASE 1: Initial window creation (no reading)")
print("-"*70)

window = pyt.WindowMain(root)

root.update_idletasks()
init_min = root.minsize()
print(f"Initial minimum set to: {init_min[0]}x{init_min[1]}")
print(f"Flag _minsize_recalc_needed: {window._minsize_recalc_needed}")

print("\n" + "-"*70)
print("PHASE 2: Cast first reading (info buttons will appear)")
print("-"*70)

# Create and display a reading
window.hexes = pyching_engine.Hexagrams('coin')
window.hexes.SetQuestion("Testing window sizing with full content")

# Cast all 6 lines
for i in range(6):
    window.hexes.NewLine()

print(f"Created: Hex1={window.hexes.hex1.number} - {window.hexes.hex1.name}")
print(f"         Hex2={window.hexes.hex2.number} - {window.hexes.hex2.name}")

# Show info buttons (this should trigger minsize recalculation)
print("\nCalling ShowInfoButtons()...")
window.ShowInfoButtons()

root.update_idletasks()
after_min = root.minsize()
print(f"\nAfter showing info buttons:")
print(f"  Minimum size: {after_min[0]}x{after_min[1]}")
print(f"  Flag _minsize_recalc_needed: {window._minsize_recalc_needed}")

print("\n" + "-"*70)
print("PHASE 3: Verification")
print("-"*70)

# Verify the fix worked
if after_min != init_min:
    width_change = after_min[0] - init_min[0]
    height_change = after_min[1] - init_min[1]
    print(f"✓ Minimum size was recalculated (as expected)")
    if width_change > 0:
        print(f"  Width increased by {width_change}px to accommodate info buttons")
    if height_change > 0:
        print(f"  Height increased by {height_change}px")
else:
    print(f"⚠ Minimum size unchanged (info buttons may have fit already)")

# Verify flag was cleared
if not window._minsize_recalc_needed:
    print(f"✓ Flag cleared - won't recalculate on subsequent readings")
else:
    print(f"✗ Flag not cleared - may recalculate unnecessarily")

# Check that current size can fit all content
root.update_idletasks()
req_width = root.winfo_reqwidth()
req_height = root.winfo_reqheight()

print(f"\nFinal check:")
print(f"  Required size: {req_width}x{req_height}")
print(f"  Minimum size:  {after_min[0]}x{after_min[1]}")

if req_width <= after_min[0] and req_height <= after_min[1]:
    print(f"  ✓ All content fits within minimum size")
    result = "PASS"
else:
    print(f"  ✗ Content exceeds minimum size!")
    if req_width > after_min[0]:
        print(f"    Width shortage: {req_width - after_min[0]}px")
    if req_height > after_min[1]:
        print(f"    Height shortage: {req_height - after_min[1]}px")
    result = "FAIL"

print("\n" + "="*70)
print(f"TEST RESULT: {result}")
print("="*70)

if result == "PASS":
    print("\n✓ Window sizing fix is working correctly!")
    print("  - Initial size is compact")
    print("  - Expands when info buttons appear")
    print("  - All content always fits")
else:
    print("\n✗ Window sizing still has issues")
    print("  - Further fixes needed")

root.destroy()
sys.exit(0 if result == "PASS" else 1)
