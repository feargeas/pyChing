# Phase 6: Interface Updates - Plan

**Project:** pyChing Multi-Source I Ching Oracle Modernization
**Phase:** 6 of 6 - CLI and GUI Interface Updates
**Date:** 2025-11-18
**Status:** PLANNED (Implementation ready to proceed)

---

## Executive Summary

Phase 6 updates both the console (CLI) and graphical (GUI) interfaces to use the new HexagramEngine (Phase 4) with Five Elements casting methods (Phase 2) and multi-source interpretation access (Phase 3).

### Current Interfaces

**Console Interface** (`pyching_interface_console.py`):
- Uses old `pyching_engine.Hexagrams` class
- Coin method only (no element selection)
- Single source (Legge 1882 only)
- Text-based display
- Save/load via pickle

**Graphical Interface** (`pyching_interface_tkinter.py`):
- Uses old `pyching_engine.Hexagrams` class
- Tkinter-based GUI
- Coin method only
- Single source
- Visual hexagram display
- Save/load via pickle

### Target Updates

**CLI Enhancements:**
✓ Use `HexagramEngine` instead of old `Hexagrams`
✓ Add `--method` flag for element selection (wood, metal, fire, earth, air)
✓ Add `--source` flag for translation selection
✓ Add `--seed` flag for Earth method (deterministic readings)
✓ Add `--compare` flag for side-by-side source comparison
✓ Use JSON for save/load instead of pickle
✓ Preserve existing text-based display format

**GUI Enhancements:**
✓ Use `HexagramEngine` instead of old `Hexagrams`
✓ Add method dropdown (Five Elements)
✓ Add source dropdown (all translations)
✓ Add comparison view (side-by-side translations)
✓ Add seed input for Earth method
✓ Use JSON for save/load instead of pickle
✓ Update visual displays

---

## CLI Update Plan

### Current CLI Flow

```python
# Old code flow
hexes = pyching_engine.Hexagrams(oracleType='coin')
question = get_question()
hexes.SetQuestion(question)

for i in range(6):
    hexes.NewLine()  # Cast each line

display_reading(hexes)  # Show ASCII art
display_interpretation(hexes)  # Show text

# Save
hexes.Save("reading.psv")  # Pickle format
```

### New CLI Flow

```python
# New code flow
from pyching import HexagramEngine, Element

engine = HexagramEngine()

question = get_question()
method = get_method_choice()  # New: ask for element
source = get_source_choice()  # New: ask for translation

# Cast reading (all 6 lines automatically)
reading = engine.cast_reading(
    method=method,
    question=question,
    source=source,
    seed=args.seed if method == Element.EARTH else None
)

display_reading(reading)  # Use reading.as_text()
display_interpretation(reading)  # Access reading.primary.judgment, etc.

# Save
reading.save("reading.json")  # JSON format
```

### New CLI Arguments

```bash
# Basic usage (same as before)
python pyching_interface_console.py

# Specify casting method
python pyching_interface_console.py --method metal
python pyching_interface_console.py --method earth --seed "my question"

# Specify interpretation source
python pyching_interface_console.py --source wilhelm_baynes

# Compare multiple sources
python pyching_interface_console.py --compare canonical,wilhelm_baynes

# Combination
python pyching_interface_console.py --method fire --source canonical

# Non-interactive mode
python pyching_interface_console.py --question "What is my purpose?" --method wood
```

### Argument Parser Setup

```python
import argparse

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="pyChing - I Ching Oracle Console Interface"
    )

    parser.add_argument(
        '--method', '-m',
        choices=['wood', 'metal', 'fire', 'earth', 'air'],
        default='wood',
        help="Casting method (default: wood - original algorithm)"
    )

    parser.add_argument(
        '--source', '-s',
        default='canonical',
        help="Interpretation source (default: canonical/Legge 1882)"
    )

    parser.add_argument(
        '--seed',
        help="Seed for Earth method (deterministic casting)"
    )

    parser.add_argument(
        '--question', '-q',
        help="Question to ask (non-interactive mode)"
    )

    parser.add_argument(
        '--compare', '-c',
        help="Compare sources (comma-separated list)"
    )

    parser.add_argument(
        '--save',
        help="Save reading to JSON file"
    )

    parser.add_argument(
        '--load',
        help="Load reading from JSON file"
    )

    return parser.parse_args()
```

### Interactive Method Selection

```python
def get_method_choice():
    """Prompt user to select casting method."""
    print("\nSelect casting method:")
    print("  1. Wood  - Standard PRNG (original algorithm)")
    print("  2. Metal - OS Entropy (highest quality local randomness)")
    print("  3. Fire  - Cryptographic CSPRNG (unpredictable)")
    print("  4. Earth - Deterministic (same question = same answer)")
    print("  5. Air   - True RNG via RANDOM.ORG (requires network)")
    print()

    while True:
        choice = input("Method [1-5, default=1]: ").strip()

        if choice == '' or choice == '1':
            return Element.WOOD
        elif choice == '2':
            return Element.METAL
        elif choice == '3':
            return Element.FIRE
        elif choice == '4':
            return Element.EARTH
        elif choice == '5':
            # Check availability
            engine = HexagramEngine()
            available, error = engine.check_method_available(Element.AIR)
            if available:
                return Element.AIR
            else:
                print(f"Air method unavailable: {error}")
                print("Please choose another method.")
                continue
        else:
            print("Invalid choice. Please enter 1-5.")
```

### Source Comparison Display

```python
def display_source_comparison(hexagram_id, sources):
    """Display side-by-side comparison of sources."""
    from pyching.data import HexagramResolver

    resolver = HexagramResolver()

    print("\n" + "="*70)
    print("SOURCE COMPARISON")
    print("="*70)

    # Get judgment from each source
    comparison = resolver.compare_sources(
        hexagram_id,
        sources=sources,
        field="judgment"
    )

    for source_id, judgment in comparison.items():
        source_info = resolver.get_source_info(source_id)
        translator = source_info.get('translator', 'Unknown')
        year = source_info.get('year', '?')

        print(f"\n{source_id.upper()} ({translator}, {year}):")
        print("-" * 70)
        print(wrap_text(judgment, 70))
```

### Updated Display Functions

```python
def display_reading(reading):
    """Display reading in ASCII art (backward compatible)."""
    print("\n" + "="*70)
    print("YOUR READING")
    print("="*70)

    # Use new as_text() method (same format as original)
    reading_text = reading.as_text()
    print(reading_text)
    print("="*70 + "\n")


def display_interpretation(reading):
    """Display hexagram interpretations."""
    print("\n" + "="*70)
    print("INTERPRETATION")
    print("="*70 + "\n")

    # Primary hexagram
    print(f"\nHEXAGRAM {reading.primary.number}: {reading.primary.name}")
    print(f"{reading.primary.english_name}")
    print("-" * 70)

    print("\nJUDGMENT:")
    print(wrap_text(reading.primary.judgment, 70))

    print("\n\nIMAGE:")
    print(wrap_text(reading.primary.image, 70))

    # Moving lines
    if reading.has_moving_lines():
        print("\n\nMOVING LINES:")
        for line_num in reading.changing_lines:
            line_data = reading.primary.line_texts[str(line_num)]
            print(f"\nLine {line_num} ({line_data['position']}, {line_data['type']}):")
            print(wrap_text(line_data['text'], 70))

    # Relating hexagram
    if reading.relating:
        print(f"\n\nTRANSFORMATION TO HEXAGRAM {reading.relating.number}: {reading.relating.name}")
        print(f"{reading.relating.english_name}")
        print("-" * 70)

        print("\nJUDGMENT:")
        print(wrap_text(reading.relating.judgment, 70))

        print("\n\nIMAGE:")
        print(wrap_text(reading.relating.image, 70))
```

---

## GUI Update Plan

### Current GUI Structure

The Tkinter GUI (`pyching_interface_tkinter.py`) has:
- Main window with menu bar
- Cast reading interface
- Hexagram display canvas
- Interpretation text display
- Save/load dialogs

### New GUI Components

**1. Method Selection Dropdown**

Add to main casting interface:
```python
method_frame = ttk.LabelFrame(main_frame, text="Casting Method")
method_frame.pack(pady=10)

method_var = tk.StringVar(value="wood")
method_menu = ttk.Combobox(
    method_frame,
    textvariable=method_var,
    values=["wood", "metal", "fire", "earth", "air"],
    state="readonly"
)
method_menu.pack(padx=10, pady=5)

# Descriptions
method_descriptions = {
    "wood": "Standard PRNG (original algorithm)",
    "metal": "OS Entropy (highest quality)",
    "fire": "Cryptographic CSPRNG",
    "earth": "Deterministic (requires seed)",
    "air": "True RNG via RANDOM.ORG"
}

desc_label = ttk.Label(method_frame, text=method_descriptions["wood"])
desc_label.pack()

def on_method_change(event):
    desc_label.config(text=method_descriptions[method_var.get()])

method_menu.bind("<<ComboboxSelected>>", on_method_change)
```

**2. Seed Input (for Earth Method)**

```python
seed_frame = ttk.Frame(main_frame)
seed_frame.pack(pady=5)

seed_label = ttk.Label(seed_frame, text="Seed (Earth method only):")
seed_label.pack(side=tk.LEFT)

seed_entry = ttk.Entry(seed_frame, width=40)
seed_entry.pack(side=tk.LEFT, padx=5)

def on_method_change(event):
    # Enable/disable seed entry based on method
    if method_var.get() == "earth":
        seed_entry.config(state="normal")
    else:
        seed_entry.config(state="disabled")
```

**3. Source Selection Dropdown**

```python
source_frame = ttk.LabelFrame(main_frame, text="Interpretation Source")
source_frame.pack(pady=10)

# Get available sources
from pyching.data import HexagramResolver
resolver = HexagramResolver()
all_sources = resolver.list_all_sources()
source_ids = [s['id'] for s in all_sources]

source_var = tk.StringVar(value="canonical")
source_menu = ttk.Combobox(
    source_frame,
    textvariable=source_var,
    values=source_ids,
    state="readonly"
)
source_menu.pack(padx=10, pady=5)

# Display translator info
def on_source_change(event):
    source_info = resolver.get_source_info(source_var.get())
    translator = source_info.get('translator', 'Unknown')
    year = source_info.get('year', '?')
    info_label.config(text=f"{translator} ({year})")

source_menu.bind("<<ComboboxSelected>>", on_source_change)
```

**4. Comparison View**

New menu item: View → Compare Sources

```python
def show_comparison_dialog():
    """Show source comparison dialog."""
    comp_window = tk.Toplevel(root)
    comp_window.title("Compare Interpretations")
    comp_window.geometry("800x600")

    # Source selection checkboxes
    checkbox_frame = ttk.Frame(comp_window)
    checkbox_frame.pack(pady=10)

    ttk.Label(checkbox_frame, text="Select sources to compare:").pack()

    source_vars = {}
    for source_id in source_ids:
        var = tk.BooleanVar(value=(source_id == 'canonical'))
        source_vars[source_id] = var
        cb = ttk.Checkbutton(checkbox_frame, text=source_id, variable=var)
        cb.pack(anchor=tk.W)

    # Comparison display (notebook with tabs or side-by-side)
    comparison_notebook = ttk.Notebook(comp_window)
    comparison_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def update_comparison():
        # Get selected sources
        selected = [s for s, v in source_vars.items() if v.get()]

        # Clear existing tabs
        for tab in comparison_notebook.tabs():
            comparison_notebook.forget(tab)

        # Create tab for each source
        for source_id in selected:
            frame = ttk.Frame(comparison_notebook)
            comparison_notebook.add(frame, text=source_id)

            # Get hexagram with this source
            hex_data = current_reading.primary
            # (would need to re-resolve with different source)

            # Display in text widget
            text = tk.Text(frame, wrap=tk.WORD)
            text.pack(fill=tk.BOTH, expand=True)
            text.insert(tk.END, hex_data.judgment)
            text.config(state=tk.DISABLED)

    update_btn = ttk.Button(checkbox_frame, text="Compare", command=update_comparison)
    update_btn.pack(pady=10)
```

**5. Updated Cast Reading Function**

```python
def cast_reading():
    """Cast a new reading using new engine."""
    global current_reading

    # Get parameters
    question = question_entry.get()
    method = Element(method_var.get())
    source = source_var.get()
    seed = seed_entry.get() if method == Element.EARTH else None

    # Create engine and cast
    engine = HexagramEngine()

    # Check method availability
    available, error = engine.check_method_available(method)
    if not available:
        messagebox.showerror("Method Unavailable", error)
        return

    try:
        # Cast reading
        current_reading = engine.cast_reading(
            method=method,
            question=question,
            source=source,
            seed=seed
        )

        # Update display
        update_hexagram_display()
        update_interpretation_display()

        # Enable save menu
        file_menu.entryconfig("Save", state=tk.NORMAL)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to cast reading: {e}")
```

**6. Updated Save/Load Functions**

```python
def save_reading():
    """Save reading to JSON file."""
    filename = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )

    if filename:
        try:
            current_reading.save(filename)
            messagebox.showinfo("Success", "Reading saved successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")


def load_reading():
    """Load reading from JSON file."""
    global current_reading

    filename = filedialog.askopenfilename(
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )

    if filename:
        try:
            current_reading = Reading.load(filename)
            update_hexagram_display()
            update_interpretation_display()
            messagebox.showinfo("Success", "Reading loaded successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load: {e}")
```

---

## Migration Strategy

### Phase 1: CLI Update (2-4 hours)

1. **Add imports**: Import new engine classes
2. **Add argument parsing**: Support new flags
3. **Update main flow**: Replace old Hexagrams with HexagramEngine
4. **Test basic functionality**: Wood method, canonical source
5. **Test new features**: All methods, source selection
6. **Update help text**: Document new options

### Phase 2: GUI Update (4-6 hours)

1. **Add method dropdown**: Five element selection
2. **Add source dropdown**: Translation selection
3. **Update cast function**: Use HexagramEngine
4. **Test visual display**: Ensure hexagrams render correctly
5. **Add comparison view**: Side-by-side translations
6. **Update save/load**: JSON instead of pickle

### Phase 3: Testing (2-3 hours)

1. **Manual testing**: All methods, all features
2. **Edge cases**: Network errors (Air method), invalid seeds
3. **Integration testing**: CLI and GUI work together
4. **User acceptance**: Interface is intuitive

---

## Backward Compatibility

### For CLI Users

**Old command (still works):**
```bash
python pyching_interface_console.py
```
- Uses Wood method (original algorithm)
- Uses canonical source (Legge 1882)
- Same text output format

**New features (optional):**
```bash
python pyching_interface_console.py --method fire
python pyching_interface_console.py --source wilhelm_baynes
```

### For GUI Users

**Old workflow (still works):**
- Launch GUI
- Enter question
- Click "Cast"
- View interpretation

**New features (optional):**
- Select method from dropdown (defaults to Wood)
- Select source from dropdown (defaults to canonical)
- Click "Compare" to see multiple translations

### File Format Migration

**Automatic conversion tool:**
```python
#!/usr/bin/env python3
"""Convert old .psv (pickle) files to new .json format."""

import pickle
from pathlib import Path
from pyching import Reading, Hexagram

def convert_psv_to_json(psv_file):
    """Convert old pickle format to new JSON."""
    # Load old format
    with open(psv_file, 'rb') as f:
        old_data = pickle.load(f)

    # old_data = (saveFileID, question, oracle, hex1, hex2, currentLine, oracleValues)
    saveFileID, question, oracle, hex1, hex2, currentLine, oracleValues = old_data

    # Convert to new format
    primary = Hexagram.from_number(int(hex1.number))
    primary.lines = hex1.lineValues

    relating = None
    if hex2.number:
        relating = Hexagram.from_number(int(hex2.number))
        relating.lines = hex2.lineValues

    reading = Reading.from_hexagrams(
        primary=primary,
        relating=relating,
        question=question,
        method="wood",  # Old files always used coin/wood method
        oracle_values=oracleValues
    )

    # Save as JSON
    json_file = psv_file.replace('.psv', '.json')
    reading.save(json_file)
    print(f"Converted {psv_file} → {json_file}")

if __name__ == "__main__":
    import sys
    for psv_file in sys.argv[1:]:
        convert_psv_to_json(psv_file)
```

---

## Testing Plan

### CLI Tests

```bash
# Basic functionality
python pyching_interface_console.py

# All methods
python pyching_interface_console.py --method wood
python pyching_interface_console.py --method metal
python pyching_interface_console.py --method fire
python pyching_interface_console.py --method earth --seed "test"
python pyching_interface_console.py --method air

# Sources (when Phase 5 complete)
python pyching_interface_console.py --source canonical
python pyching_interface_console.py --source wilhelm_baynes

# Comparison
python pyching_interface_console.py --compare canonical,wilhelm_baynes

# Save/load
python pyching_interface_console.py --save my_reading.json
python pyching_interface_console.py --load my_reading.json

# Non-interactive
python pyching_interface_console.py --question "Test?" --method wood
```

### GUI Tests

1. Launch GUI
2. Select each method, verify descriptions update
3. Enter question and cast with each method
4. Verify hexagram displays correctly
5. Verify interpretation text displays
6. Select different sources (when available)
7. Test comparison view
8. Save reading to JSON
9. Load reading from JSON
10. Verify all menu items work

---

## Success Criteria

Phase 6 will be considered complete when:

✓ CLI uses new HexagramEngine
✓ CLI supports all five element methods
✓ CLI supports source selection (--source flag)
✓ CLI supports comparison mode (--compare flag)
✓ CLI uses JSON for save/load
✓ GUI uses new HexagramEngine
✓ GUI has method selection dropdown
✓ GUI has source selection dropdown
✓ GUI has comparison view
✓ GUI uses JSON for save/load
✓ Backward compatibility maintained
✓ All existing features still work
✓ Tests pass for both interfaces

---

## Implementation Status

**CLI**: ⏳ Planned (ready to implement)
**GUI**: ⏳ Planned (ready to implement)
**Testing**: ⏳ Planned

**Estimated Effort**: 8-12 hours
**Dependencies**: Phases 1-4 complete ✓

The infrastructure is complete and tested. Implementation is straightforward adaptation of existing interfaces to use new engine classes.

---

**End of Phase 6 Plan**
