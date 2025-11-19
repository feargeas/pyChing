#!/usr/bin/env python3
"""
Simple test to check if window size is adequate for full reading
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

print("\n" + "="*70)
print("Testing window sizing with and without reading content...")
print("="*70)

from tkinter import Tk
import pyching_interface_tkinter as pyt
import pyching_engine

# Create window
root = Tk()
pyt.VERBOSE = True
window = pyt.WindowMain(root)

# Get initial size
root.update_idletasks()
init_req_w = root.winfo_reqwidth()
init_req_h = root.winfo_reqheight()
init_min_w, init_min_h = root.minsize()

print(f"\n1. INITIAL STATE (empty, just cast button):")
print(f"   Required: {init_req_w}x{init_req_h}")
print(f"   Minimum:  {init_min_w}x{init_min_h}")

# Now simulate showing a complete reading
# Create hexagrams
window.hexes = pyching_engine.Hexagrams('coin')
window.hexes.SetQuestion("What is the meaning of life, the universe, and everything?")

# Cast all 6 lines
for i in range(6):
    window.hexes.NewLine()

print(f"\n2. Created reading:")
print(f"   Hex1: {window.hexes.hex1.number} - {window.hexes.hex1.name}")
print(f"   Hex2: {window.hexes.hex2.number} - {window.hexes.hex2.name}")

# Show the reading components manually (simulate what CastAllLines does)
# Show question
window.messageQuestion.configure(width=window.frameQuestion.winfo_width(),
                                 text=window.hexes.question)

# Show hex1 title
window.labelH1Title.configure(text=window.hexes.hex1.number+'.  '+window.hexes.hex1.name)

# Draw hex1 lines
for i, line in enumerate(window.hexLines[0]):
    line.Draw(window.hexes.hex1.lineValues[i])

# Show hex2 if there are moving lines
if window.hexes.hex2.lineValues[0] != 0:
    window.labelBecomes.configure(fg=window.colors.fgLabelLines)
    window.labelH2Title.configure(text=window.hexes.hex2.number+'.  '+window.hexes.hex2.name)
    for i, line in enumerate(window.hexLines[1]):
        line.Draw(window.hexes.hex2.lineValues[i])
else:
    # Show "no moving lines" message
    for i in [3, 4, 5]:
        window.labelsNoMovingLines[i].tkraise()

# Show info buttons (this is KEY - these might not be in initial size calc)
textStub = 'View information on:  '
if window.hexes.hex2.lineValues[0] != 0:
    window.buttonViewHex2Info.configure(
        text=textStub+window.hexes.hex2.number+'. '+window.hexes.hex2.name,
        state='normal')
    window.buttonViewHex2Info.grid(column=0, row=1)
    button1Pad = 5
else:
    button1Pad = 15

window.buttonViewHex1Info.configure(
    text=textStub+window.hexes.hex1.number+'. '+window.hexes.hex1.name,
    state='normal')
window.buttonViewHex1Info.grid(column=0, row=0, pady=button1Pad)
window.frameInfoButtons.grid(column=1, row=0, columnspan=3, sticky='nw', pady=5)

# NOW check the required size with everything visible
root.update_idletasks()
full_req_w = root.winfo_reqwidth()
full_req_h = root.winfo_reqheight()

print(f"\n3. FULL READING DISPLAYED (all elements visible):")
print(f"   Required: {full_req_w}x{full_req_h}")
print(f"   Minimum:  {init_min_w}x{init_min_h} (from initial calc)")

# Check if there's a problem
print(f"\n4. ANALYSIS:")
width_diff = full_req_w - init_min_w
height_diff = full_req_h - init_min_h

if width_diff > 0 or height_diff > 0:
    print(f"   ⚠ PROBLEM DETECTED!")
    print(f"   Initial minimum is TOO SMALL for full content:")
    if width_diff > 0:
        print(f"      Width shortage: {width_diff}px (window needs to be {width_diff}px wider)")
    if height_diff > 0:
        print(f"      Height shortage: {height_diff}px (window needs to be {height_diff}px taller)")
    print(f"\n   FIX NEEDED: Recalculate minsize after showing first reading,")
    print(f"               or include info buttons in initial calculation")
    result = "FAIL"
else:
    print(f"   ✓ Initial minimum size is adequate")
    print(f"   All content fits without needing window to grow")
    result = "PASS"

print(f"\n" + "="*70)
print(f"TEST RESULT: {result}")
print("="*70)

# Show window for visual verification
print(f"\nWindow is displayed - you can verify visually that all content is visible.")
print("Close the window to exit...")

root.mainloop()

sys.exit(0 if result == "PASS" else 1)
