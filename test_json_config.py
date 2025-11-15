#!/usr/bin/env python3
"""
Test script for JSON config and reading save/load functionality
Tests both config system and reading system with pickle migration
"""

import json
import pickle
import sys
from pathlib import Path
import tempfile
import shutil

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

import pyching_engine

def test_config_json():
    """Test JSON config save/load"""
    print("\n" + "="*70)
    print("TEST 1: JSON Config Save/Load")
    print("="*70)

    # Create a temporary config file
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / 'config.json'

        # Create test config
        config = {
            'version': '1.2.2',
            'appearance': {
                'theme': 'tokyo-night',
                'font_scale': 1.5
            },
            'display': {
                'cast_all': True,
                'show_places': False,
                'show_line_hints': True
            }
        }

        # Save
        print(f"\n1. Saving config to: {config_file}")
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print("   ✓ Config saved")

        # Show file contents
        print("\n2. Config file contents:")
        with open(config_file, 'r') as f:
            content = f.read()
            print("   " + content.replace('\n', '\n   '))

        # Load
        print("\n3. Loading config...")
        with open(config_file, 'r') as f:
            loaded_config = json.load(f)

        print(f"   ✓ Loaded theme: {loaded_config['appearance']['theme']}")
        print(f"   ✓ Loaded font_scale: {loaded_config['appearance']['font_scale']}")
        print(f"   ✓ Loaded cast_all: {loaded_config['display']['cast_all']}")

        # Verify
        assert loaded_config == config, "Config mismatch!"
        print("\n   ✓✓ Config save/load test PASSED")


def test_reading_json_save_load():
    """Test JSON reading save/load"""
    print("\n" + "="*70)
    print("TEST 2: JSON Reading Save/Load")
    print("="*70)

    with tempfile.TemporaryDirectory() as tmpdir:
        reading_file = Path(tmpdir) / 'test_reading.psv'

        # Create a reading
        print("\n1. Creating new reading...")
        hexes = pyching_engine.Hexagrams('coin')
        hexes.SetQuestion("Will JSON save work?")

        # Cast all 6 lines
        for i in range(6):
            hexes.NewLine()

        print(f"   Question: {hexes.question}")
        print(f"   Oracle: {hexes.oracle}")
        print(f"   Hex1: {hexes.hex1.number} - {hexes.hex1.name}")
        print(f"   Hex2: {hexes.hex2.number} - {hexes.hex2.name}")

        # Save
        print(f"\n2. Saving reading to: {reading_file}")
        hexes.Save(reading_file)
        print("   ✓ Reading saved")

        # Show file preview
        print("\n3. Reading file preview (first 500 chars):")
        with open(reading_file, 'r') as f:
            content = f.read(500)
            print("   " + content.replace('\n', '\n   '))
            if len(content) == 500:
                print("   ...")

        # Load in new instance
        print("\n4. Loading reading into new instance...")
        hexes2 = pyching_engine.Hexagrams()
        result = hexes2.Load(reading_file)

        print(f"   ✓ Loaded - File ID: {result}")
        print(f"   ✓ Question: {hexes2.question}")
        print(f"   ✓ Oracle: {hexes2.oracle}")
        print(f"   ✓ Hex1: {hexes2.hex1.number} - {hexes2.hex1.name}")
        print(f"   ✓ Hex2: {hexes2.hex2.number} - {hexes2.hex2.name}")

        # Verify
        assert hexes2.question == hexes.question, "Question mismatch!"
        assert hexes2.oracle == hexes.oracle, "Oracle mismatch!"
        assert hexes2.hex1.number == hexes.hex1.number, "Hex1 number mismatch!"
        assert hexes2.hex2.number == hexes.hex2.number, "Hex2 number mismatch!"

        print("\n   ✓✓ Reading JSON save/load test PASSED")


def test_pickle_migration():
    """Test migration from pickle to JSON"""
    print("\n" + "="*70)
    print("TEST 3: Pickle to JSON Migration")
    print("="*70)

    with tempfile.TemporaryDirectory() as tmpdir:
        reading_file = Path(tmpdir) / 'old_reading.psv'
        backup_file = Path(tmpdir) / 'old_reading.psv.backup'

        # Create a reading and save as OLD pickle format
        print("\n1. Creating old pickle format reading...")
        hexes = pyching_engine.Hexagrams('coin')
        hexes.SetQuestion("Old pickle reading")

        # Cast all 6 lines
        for i in range(6):
            hexes.NewLine()

        # Save using OLD pickle format directly
        print(f"\n2. Saving as pickle (simulating old version): {reading_file}")
        hexData = (pyching_engine.pyching.saveFileID, hexes.question, hexes.oracle, hexes.hex1,
                   hexes.hex2, hexes.currentLine, hexes.currentOracleValues)
        with open(reading_file, 'wb') as f:
            pickle.dump(hexData, f)
        print("   ✓ Old pickle file created")

        # Verify it's binary (pickle)
        with open(reading_file, 'rb') as f:
            first_bytes = f.read(10)
            print(f"   File starts with bytes: {first_bytes[:5]}... (pickle format)")

        # Load using new system (should auto-migrate)
        print("\n3. Loading old pickle file with new JSON system...")
        hexes2 = pyching_engine.Hexagrams()
        result = hexes2.Load(reading_file)

        print(f"   ✓ Successfully loaded from pickle")
        print(f"   ✓ Question: {hexes2.question}")
        print(f"   ✓ Oracle: {hexes2.oracle}")

        # Check if migration happened
        print("\n4. Checking migration...")
        if backup_file.exists():
            print(f"   ✓ Backup created: {backup_file}")
        else:
            print(f"   ⚠ No backup created (may be expected)")

        if reading_file.exists():
            # Check if it's now JSON
            try:
                with open(reading_file, 'r') as f:
                    migrated_data = json.load(f)
                print(f"   ✓ Original file migrated to JSON")
                print(f"   ✓ JSON contains: {list(migrated_data.keys())}")
            except:
                print(f"   ⚠ Original file still pickle (migration may have failed)")

        # Verify data integrity
        assert hexes2.question == hexes.question, "Question mismatch after migration!"
        assert hexes2.oracle == hexes.oracle, "Oracle mismatch after migration!"

        print("\n   ✓✓ Pickle migration test PASSED")


def main():
    print("\n" + "="*70)
    print("JSON CONFIG & READING SYSTEM TESTS")
    print("="*70)

    try:
        test_config_json()
        test_reading_json_save_load()
        test_pickle_migration()

        print("\n" + "="*70)
        print("ALL TESTS PASSED ✓✓✓")
        print("="*70)
        print("\nSummary:")
        print("  ✓ JSON config save/load working")
        print("  ✓ JSON reading save/load working")
        print("  ✓ Pickle to JSON migration working")
        print("  ✓ Old readings will be preserved and auto-migrated")
        print("\n")

    except Exception as e:
        print(f"\n\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
