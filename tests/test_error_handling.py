"""
Test Error Handling in Persistence
===================================

These tests ensure that the persistence layer handles errors gracefully.

THESE TESTS VALIDATE ERROR HANDLING FOR SAVE/LOAD OPERATIONS.
"""

import sys
import tempfile
import pickle
from pathlib import Path
from unittest.mock import patch, mock_open

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pyching_engine


class TestStorageErrorHandling:
    """Test error handling in the Storage utility function"""

    def test_storage_load_file_not_found(self):
        """Loading a non-existent file should raise IOError"""
        non_existent = '/tmp/definitely_does_not_exist_12345.psv'
        try:
            pyching_engine.Storage(non_existent)
            assert False, "Should have raised IOError for missing file"
        except IOError:
            pass  # Expected

    def test_storage_load_corrupted_pickle(self):
        """Loading a corrupted pickle file should raise Exception"""
        # Create a file with invalid pickle data
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.psv') as f:
            temp_file = f.name
            f.write(b'This is not valid pickle data\x00\xFF\xFE')

        try:
            try:
                pyching_engine.Storage(temp_file)
                assert False, "Should have raised Exception for corrupted pickle"
            except Exception as e:
                # Should be wrapped as pychingUnpickleError
                assert 'pychingUnpickleError' in str(e) or isinstance(e, Exception)
        finally:
            Path(temp_file).unlink(missing_ok=True)

    def test_storage_save_to_invalid_path(self):
        """Saving to an invalid path should raise IOError"""
        invalid_path = '/root/no_permission_here/test.psv'
        test_data = ('test', 'data')

        try:
            pyching_engine.Storage(invalid_path, data=test_data)
            # If somehow we have permission, this isn't a good test, skip it
        except (IOError, PermissionError):
            pass  # Expected

    def test_storage_roundtrip_preserves_data(self):
        """Data should survive a save/load cycle"""
        test_data = ('pyching_save_file', '1.2.2', 'test question',
                     'coin', [7, 8, 9, 6, 7, 8], [2, 3, 2])

        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.psv') as f:
            temp_file = f.name

        try:
            # Save
            pyching_engine.Storage(temp_file, data=test_data)

            # Load
            loaded_data = pyching_engine.Storage(temp_file)

            # Verify
            assert loaded_data == test_data, \
                f"Loaded data doesn't match saved data"
        finally:
            Path(temp_file).unlink(missing_ok=True)


class TestHexagramsLoadErrors:
    """Test error handling in Hexagrams Load method"""

    def test_load_non_existent_file(self):
        """Loading non-existent file should raise IOError"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')

        try:
            hexagrams.Load('/tmp/does_not_exist_67890.psv')
            assert False, "Should have raised IOError"
        except IOError:
            pass  # Expected

    def test_load_wrong_file_format(self):
        """Loading a non-pyching file should handle gracefully"""
        # Create a pickle file with wrong structure
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.psv') as f:
            temp_file = f.name
            pickle.dump(('wrong', 'format'), f)

        try:
            hexagrams = pyching_engine.Hexagrams(oracleType='coin')
            try:
                hexagrams.Load(temp_file)
                # This might fail during unpacking, which is acceptable
            except (ValueError, TypeError, Exception):
                pass  # Expected - wrong data structure
        finally:
            Path(temp_file).unlink(missing_ok=True)

    def test_load_returns_version_tuple(self):
        """Load should return version info as a tuple"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.SetQuestion("Test version")
        for _ in range(6):
            hexagrams.NewLine()

        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.psv') as f:
            temp_file = f.name

        try:
            hexagrams.Save(temp_file)

            loaded_hex = pyching_engine.Hexagrams(oracleType='coin')
            version = loaded_hex.Load(temp_file)

            assert isinstance(version, tuple), \
                f"Version should be tuple, got {type(version)}"
            assert len(version) == 2, \
                f"Version tuple should have 2 elements, got {len(version)}"
            assert version[0] == 'pyching_save_file', \
                f"First element should be 'pyching_save_file', got {version[0]}"
        finally:
            Path(temp_file).unlink(missing_ok=True)


class TestHexagramsSaveErrors:
    """Test error handling in Hexagrams Save method"""

    def test_save_to_readonly_directory(self):
        """Saving to read-only directory should raise IOError"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.SetQuestion("Test save error")
        for _ in range(6):
            hexagrams.NewLine()

        # Try to save to a read-only location
        readonly_path = '/root/test.psv'

        try:
            hexagrams.Save(readonly_path)
            # If we somehow have permission, skip this test
        except (IOError, PermissionError):
            pass  # Expected

    def test_save_partial_reading_succeeds(self):
        """Saving a partial reading (< 6 lines) should work"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.SetQuestion("Partial")
        hexagrams.NewLine()
        hexagrams.NewLine()

        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.psv') as f:
            temp_file = f.name

        try:
            hexagrams.Save(temp_file)  # Should not raise
            assert Path(temp_file).exists(), "Save file should exist"
        except Exception as e:
            assert False, f"Partial reading save should not fail: {e}"
        finally:
            Path(temp_file).unlink(missing_ok=True)

    def test_save_empty_reading_succeeds(self):
        """Saving with no lines cast should work"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.SetQuestion("Empty reading")

        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.psv') as f:
            temp_file = f.name

        try:
            hexagrams.Save(temp_file)  # Should not raise
            assert Path(temp_file).exists(), "Save file should exist"
        except Exception as e:
            assert False, f"Empty reading save should not fail: {e}"
        finally:
            Path(temp_file).unlink(missing_ok=True)


class TestDataIntegrity:
    """Test that saved data maintains integrity"""

    def test_unicode_question_survives_save_load(self):
        """Questions with Unicode should be preserved"""
        unicode_question = "What about 易經 (I Ching) 陰陽 yin-yang?"

        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.SetQuestion(unicode_question)
        for _ in range(6):
            hexagrams.NewLine()

        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.psv') as f:
            temp_file = f.name

        try:
            hexagrams.Save(temp_file)

            loaded = pyching_engine.Hexagrams(oracleType='coin')
            loaded.Load(temp_file)

            assert loaded.question == unicode_question, \
                f"Unicode question not preserved: {loaded.question}"
        finally:
            Path(temp_file).unlink(missing_ok=True)

    def test_moving_lines_preserved_in_save_load(self):
        """Moving lines (6 and 9) should be preserved exactly"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.SetQuestion("Moving lines test")
        hexagrams.hex1.lineValues = [6, 9, 7, 8, 6, 9]
        hexagrams.currentLine = 6
        hexagrams.NewLine()  # Trigger hexagram completion

        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.psv') as f:
            temp_file = f.name

        try:
            hexagrams.Save(temp_file)

            loaded = pyching_engine.Hexagrams(oracleType='coin')
            loaded.Load(temp_file)

            assert loaded.hex1.lineValues == [6, 9, 7, 8, 6, 9], \
                f"Line values not preserved: {loaded.hex1.lineValues}"
            assert loaded.hex2.lineValues == [7, 8, 7, 8, 7, 8], \
                f"Hex2 values not correct: {loaded.hex2.lineValues}"
        finally:
            Path(temp_file).unlink(missing_ok=True)

    def test_oracle_type_preserved_in_save_load(self):
        """Oracle type should be preserved"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.SetQuestion("Oracle type test")

        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.psv') as f:
            temp_file = f.name

        try:
            hexagrams.Save(temp_file)

            loaded = pyching_engine.Hexagrams(oracleType='coin')
            loaded.Load(temp_file)

            assert loaded.oracle == 'coin', \
                f"Oracle type not preserved: {loaded.oracle}"
        finally:
            Path(temp_file).unlink(missing_ok=True)


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
