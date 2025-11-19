#!/usr/bin/env python3
"""
Non-interactive sizing check
"""
import sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

# Suppress Tk display requirement
os.environ['DISPLAY'] = ':99' if 'DISPLAY' not in os.environ else os.environ['DISPLAY']

try:
    from tkinter import Tk
    import pyching_interface_tkinter as pyt
    import pyching_engine

    print("\n" + "="*70)
    print("Window Sizing Check (info buttons are key)")
    print("="*70)

    root = Tk()
    root.withdraw()  # Hide window
    window = pyt.WindowMain(root)

    # Get initial minimum
    root.update_idletasks()
    init_min = root.minsize()
    print(f"\n1. Initial minimum: {init_min[0]}x{init_min[1]}")

    # Check if info buttons are in the layout
    info_button_text = 'View information on:  12. Standstill (example long name)'
    window.buttonViewHex1Info.configure(text=info_button_text, state='normal')
    window.buttonViewHex1Info.grid(column=0, row=0, pady=15)
    window.frameInfoButtons.grid(column=1, row=0, columnspan=3, sticky='nw', pady=5)

    root.update_idletasks()
    with_buttons_w = root.winfo_reqwidth()
    with_buttons_h = root.winfo_reqheight()

    print(f"2. With info buttons shown: {with_buttons_w}x{with_buttons_h}")

    if with_buttons_w > init_min[0]:
        print(f"\n⚠ ISSUE: Info buttons add {with_buttons_w - init_min[0]}px width")
        print(f"   Initial minimum is too small!")
        print(f"   Need to fix: include info buttons in initial sizing calculation")
    else:
        print(f"\n✓ OK: Info buttons fit within initial minimum")

    root.destroy()

except Exception as e:
    print(f"Cannot run GUI test: {e}")
    print("This is expected if no display is available")
