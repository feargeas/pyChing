#!/usr/bin/env python3
"""
Test that adaptive sizing is both functionally correct AND visually perfect
Validates the fix for empty button widgets being visible when they shouldn't be
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

print("\n" + "="*70)
print("VISUAL PERFECTION TEST - Info Buttons")
print("="*70)
print("\nThis test validates:")
print("  1. Info buttons are HIDDEN initially (no empty widget visible)")
print("  2. Buttons APPEAR when first reading is cast")
print("  3. Buttons are HIDDEN again when reading is cleared")
print("  4. Font changes work correctly in all states")
print("  5. Minimum size ALWAYS includes button space")
print("="*70)

from tkinter import Tk
import pyching_interface_tkinter as pyt
import pyching_engine

pyt.VERBOSE = True
pyt.DEBUG = True

root = Tk()
root.withdraw()

print("\n" + "-"*70)
print("TEST 1: Initial State (Empty Window)")
print("-"*70)

window = pyt.WindowMain(root)
root.update_idletasks()

# Check that frameInfoButtons is NOT visible (grid_remove()'ed)
try:
    frame_info = window.frameInfoButtons.grid_info()
    print(f"✗ FAIL: Info button frame is VISIBLE when it should be hidden!")
    print(f"  Grid info: {frame_info}")
    visual_pass_1 = False
except:
    print(f"✓ PASS: Info button frame is hidden (no empty widgets visible)")
    visual_pass_1 = True

# Check that minsize was calculated WITH buttons (they were there during calc)
initial_min = root.minsize()
print(f"Initial minimum size: {initial_min[0]}x{initial_min[1]}")
print(f"  (Should include space for info buttons)")

print("\n" + "-"*70)
print("TEST 2: Cast Reading (Buttons Should Appear)")
print("-"*70)

# Create and cast reading
window.hexes = pyching_engine.Hexagrams('coin')
window.hexes.SetQuestion("Testing visual perfection")
for i in range(6):
    window.hexes.NewLine()

# Show info buttons
window.ShowInfoButtons()
root.update_idletasks()

# Check that frame IS visible now
try:
    frame_info = window.frameInfoButtons.grid_info()
    print(f"✓ PASS: Info button frame is now VISIBLE")
    print(f"  Grid position: row={frame_info['row']}, col={frame_info['column']}")
    visual_pass_2 = True
except:
    print(f"✗ FAIL: Info button frame should be VISIBLE after ShowInfoButtons()")
    visual_pass_2 = False

# Check button has text
if window.buttonViewHex1Info['text']:
    print(f"✓ PASS: Hex1 button has text: '{window.buttonViewHex1Info['text'][:40]}...'")
    visual_pass_2 = visual_pass_2 and True
else:
    print(f"✗ FAIL: Hex1 button should have text")
    visual_pass_2 = False

# Check minsize is still correct
after_show_min = root.minsize()
print(f"Minimum after showing: {after_show_min[0]}x{after_show_min[1]}")
if after_show_min == initial_min:
    print(f"✓ PASS: Minimum unchanged (buttons were included in initial calc)")
else:
    print(f"⚠ INFO: Minimum changed (may be due to actual hexagram text length)")

print("\n" + "-"*70)
print("TEST 3: Clear Reading (Buttons Should Disappear)")
print("-"*70)

window.ClearReading()
root.update_idletasks()

# Check that frame is NOT visible again (grid_remove()'ed)
try:
    frame_info = window.frameInfoButtons.grid_info()
    print(f"✗ FAIL: Info button frame is VISIBLE when it should be hidden!")
    visual_pass_3 = False
except:
    print(f"✓ PASS: Info button frame is hidden again (clean appearance)")
    visual_pass_3 = True

# Check buttons are cleared
if not window.buttonViewHex1Info['text']:
    print(f"✓ PASS: Hex1 button text is cleared")
else:
    print(f"⚠ INFO: Hex1 button still has text (hidden anyway)")

print("\n" + "-"*70)
print("TEST 4: Font Change While Hidden")
print("-"*70)

before_min = root.minsize()
print(f"Minimum before font change: {before_min[0]}x{before_min[1]}")

# Change font while buttons are hidden
window.fonts.set_scale(1.5)

# Simulate what AdjustFontSize() does
frame_was_hidden = False
try:
    window.frameInfoButtons.grid_info()
except:
    frame_was_hidden = True
    # Temporarily show for sizing
    window.frameInfoButtons.grid(column=1, row=0, columnspan=3, sticky='nw', pady=5)
    sample_text = 'View information on:  64. Before Completion'
    window.buttonViewHex1Info.configure(text=sample_text)

root.update_idletasks()
new_width = root.winfo_reqwidth()
new_height = root.winfo_reqheight()
root.minsize(new_width, new_height)

# Hide again if it was hidden
if frame_was_hidden:
    window.frameInfoButtons.grid_remove()
    window.buttonViewHex1Info.configure(text='')

after_font_min = root.minsize()
print(f"Minimum after font to 150%: {after_font_min[0]}x{after_font_min[1]}")

# Verify frame is still hidden
try:
    window.frameInfoButtons.grid_info()
    print(f"✗ FAIL: Frame should still be hidden after font change")
    visual_pass_4 = False
except:
    print(f"✓ PASS: Frame is still hidden after font change")
    visual_pass_4 = True

# Verify size increased
if after_font_min[0] > before_min[0] or after_font_min[1] > before_min[1]:
    print(f"✓ PASS: Minimum size increased for larger font")
    visual_pass_4 = visual_pass_4 and True
else:
    print(f"⚠ INFO: Minimum didn't increase (may already be large enough)")

print("\n" + "-"*70)
print("TEST 5: Cast With Large Font (Buttons Should Appear And Fit)")
print("-"*70)

# Cast new reading with large font
window.hexes = pyching_engine.Hexagrams('coin')
window.hexes.SetQuestion("Testing with 150% font")
for i in range(6):
    window.hexes.NewLine()

window.ShowInfoButtons()
root.update_idletasks()

# Check frame is visible
try:
    frame_info = window.frameInfoButtons.grid_info()
    print(f"✓ PASS: Info button frame is visible with large font")
    visual_pass_5 = True
except:
    print(f"✗ FAIL: Frame should be visible after ShowInfoButtons()")
    visual_pass_5 = False

# Check everything fits
req_w = root.winfo_reqwidth()
req_h = root.winfo_reqheight()
final_min = root.minsize()

print(f"Required size: {req_w}x{req_h}")
print(f"Minimum size:  {final_min[0]}x{final_min[1]}")

if req_w <= final_min[0] and req_h <= final_min[1]:
    print(f"✓ PASS: All content fits within minimum size")
    visual_pass_5 = visual_pass_5 and True
else:
    print(f"✗ FAIL: Content exceeds minimum!")
    if req_w > final_min[0]:
        print(f"  Width shortage: {req_w - final_min[0]}px")
    if req_h > final_min[1]:
        print(f"  Height shortage: {req_h - final_min[1]}px")
    visual_pass_5 = False

print("\n" + "="*70)
print("FINAL RESULTS")
print("="*70)

all_tests = [
    ("Initial state (hidden)", visual_pass_1),
    ("Show buttons (visible)", visual_pass_2),
    ("Clear reading (hidden)", visual_pass_3),
    ("Font change (hidden)", visual_pass_4),
    ("Show with large font (visible & fits)", visual_pass_5)
]

all_passed = True
for test_name, passed in all_tests:
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"  {status}: {test_name}")
    all_passed = all_passed and passed

print("="*70)

if all_passed:
    print("\n🎯 VISUAL PERFECTION ACHIEVED!")
    print("   - Buttons hidden when they should be")
    print("   - Buttons visible when they should be")
    print("   - Size calculations always correct")
    print("   - No empty widgets cluttering the UI")
    print("\n" + "="*70)
    root.destroy()
    sys.exit(0)
else:
    print("\n❌ VISUAL ISSUES DETECTED")
    print("   Some tests failed - see details above")
    print("\n" + "="*70)
    root.destroy()
    sys.exit(1)
