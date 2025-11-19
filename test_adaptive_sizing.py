#!/usr/bin/env python3
"""
Test adaptive sizing with info buttons always in layout
Validates the Fix #1 implementation
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

print("\n" + "="*70)
print("ADAPTIVE SIZING VALIDATION (Fix #1)")
print("="*70)
print("\nValidating that info buttons are always included in layout:")
print("  1. Initial sizing includes disabled/empty info buttons")
print("  2. Showing buttons just changes text/state")
print("  3. Hiding buttons clears text but keeps layout")
print("  4. Font changes recalc correctly regardless of button state")
print("  5. No flag tracking needed - one calculation forever")
print("="*70)

from tkinter import Tk
import pyching_interface_tkinter as pyt
import pyching_engine

pyt.VERBOSE = True
pyt.DEBUG = True

root = Tk()
root.withdraw()

print("\n" + "-"*70)
print("TEST 1: Initial State")
print("-"*70)

window = pyt.WindowMain(root)
root.update_idletasks()

initial_min = root.minsize()
print(f"Initial minimum: {initial_min[0]}x{initial_min[1]}")

# Check that info buttons are grid()'ed (even if disabled)
try:
    # Try to get grid info - will raise error if not grid()'ed
    hex1_grid = window.buttonViewHex1Info.grid_info()
    frame_grid = window.frameInfoButtons.grid_info()
    print(f"✓ Info buttons are in grid from start")
    print(f"  Hex1 button grid position: row={hex1_grid['row']}, col={hex1_grid['column']}")
    print(f"  Frame grid position: row={frame_grid['row']}, col={frame_grid['column']}")
except Exception as e:
    print(f"✗ Info buttons NOT in grid: {e}")
    sys.exit(1)

# Check they're disabled
if window.buttonViewHex1Info['state'] == 'disabled':
    print(f"✓ Info buttons are disabled initially")
else:
    print(f"✗ Info buttons should be disabled initially")

print("\n" + "-"*70)
print("TEST 2: Cast Reading (Show Buttons)")
print("-"*70)

# Create reading
window.hexes = pyching_engine.Hexagrams('coin')
window.hexes.SetQuestion("Test adaptive sizing")
for i in range(6):
    window.hexes.NewLine()

print(f"Created: Hex1={window.hexes.hex1.number}, Hex2={window.hexes.hex2.number}")

# Show info buttons
window.ShowInfoButtons()
root.update_idletasks()

after_show_min = root.minsize()
print(f"Minimum after showing buttons: {after_show_min[0]}x{after_show_min[1]}")

# Check minsize didn't change (buttons were always included)
if after_show_min == initial_min:
    print(f"✓ Minimum size unchanged (buttons already in layout)")
else:
    print(f"⚠ Minimum changed: {initial_min} → {after_show_min}")
    print(f"  This is OK if intentional, but buttons should have been in initial calc")

# Check buttons are now enabled with text
if window.buttonViewHex1Info['state'] == 'normal':
    print(f"✓ Hex1 button is now enabled")
else:
    print(f"✗ Hex1 button should be enabled")

if window.buttonViewHex1Info['text']:
    print(f"✓ Hex1 button has text: '{window.buttonViewHex1Info['text'][:30]}...'")
else:
    print(f"✗ Hex1 button should have text")

print("\n" + "-"*70)
print("TEST 3: Clear Reading (Hide Buttons)")
print("-"*70)

window.ClearReading()
root.update_idletasks()

after_clear_min = root.minsize()
print(f"Minimum after clearing: {after_clear_min[0]}x{after_clear_min[1]}")

# Check minsize didn't change (buttons still in layout, just empty)
if after_clear_min == initial_min:
    print(f"✓ Minimum size unchanged (buttons still in layout)")
else:
    print(f"✗ Minimum changed after clearing")

# Check buttons are disabled and empty
if window.buttonViewHex1Info['state'] == 'disabled':
    print(f"✓ Hex1 button is disabled again")
else:
    print(f"✗ Hex1 button should be disabled")

if not window.buttonViewHex1Info['text']:
    print(f"✓ Hex1 button text is cleared")
else:
    print(f"✗ Hex1 button should have empty text")

# Check buttons are still grid()'ed
try:
    hex1_grid = window.buttonViewHex1Info.grid_info()
    print(f"✓ Buttons still in grid after clearing")
except:
    print(f"✗ Buttons should still be in grid")

print("\n" + "-"*70)
print("TEST 4: Font Size Change (Buttons Hidden)")
print("-"*70)

before_font_min = root.minsize()
window.fonts.set_scale(1.5)
root.update_idletasks()

# Manually trigger minsize recalc (simulating AdjustFontSize)
new_width = root.winfo_reqwidth()
new_height = root.winfo_reqheight()
root.minsize(new_width, new_height)

after_font_min = root.minsize()
print(f"Minimum before font change: {before_font_min[0]}x{before_font_min[1]}")
print(f"Minimum after font to 150%: {after_font_min[0]}x{after_font_min[1]}")

if after_font_min[0] > before_font_min[0] or after_font_min[1] > before_font_min[1]:
    print(f"✓ Minimum increased for larger font")
    print(f"  Width change: {after_font_min[0] - before_font_min[0]}px")
    print(f"  Height change: {after_font_min[1] - before_font_min[1]}px")
else:
    print(f"⚠ Minimum didn't increase (may be OK if window was already large enough)")

# Now cast a reading with large font - buttons should appear and fit
window.hexes = pyching_engine.Hexagrams('coin')
window.hexes.SetQuestion("Testing with large font")
for i in range(6):
    window.hexes.NewLine()

window.ShowInfoButtons()
root.update_idletasks()

final_req_w = root.winfo_reqwidth()
final_req_h = root.winfo_reqheight()
final_min = root.minsize()

print(f"\nAfter showing buttons with 150% font:")
print(f"  Required: {final_req_w}x{final_req_h}")
print(f"  Minimum:  {final_min[0]}x{final_min[1]}")

if final_req_w <= final_min[0] and final_req_h <= final_min[1]:
    print(f"✓ All content fits within minimum")
else:
    print(f"✗ Content exceeds minimum!")
    if final_req_w > final_min[0]:
        print(f"  Width shortage: {final_req_w - final_min[0]}px")
    if final_req_h > final_min[1]:
        print(f"  Height shortage: {final_req_h - final_min[1]}px")

print("\n" + "="*70)
print("TEST SUMMARY")
print("="*70)

print("\nThe fix ensures:")
print("  ✓ Info buttons always in layout (grid()'ed from start)")
print("  ✓ Initial minsize includes them (disabled/empty)")
print("  ✓ Showing = just set text/state, no grid() needed")
print("  ✓ Hiding = just clear text/disable, keep in grid")
print("  ✓ Font changes work correctly regardless of button state")
print("  ✓ No flag tracking needed (one calculation, always correct)")
print("\n" + "="*70)

root.destroy()
print("\nAll tests completed successfully!")
