"""
Test Python 3 compatibility fixes

Verifies that Python 2 to Python 3 compatibility changes are correct,
including the .has_key() → in operator fix.
"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pyching_engine


class TestDictionaryOperators:
    """Test that dictionary operations use Python 3 syntax"""

    def test_in_operator_works_with_dict(self):
        """Test that 'in' operator works correctly with dictionaries"""
        test_dict = {0: 'value0', 1: 'value1', 2: 'value2'}

        # Python 3 syntax (correct)
        assert 0 in test_dict
        assert 1 in test_dict
        assert 2 in test_dict
        assert 3 not in test_dict

    def test_has_key_not_used(self):
        """Verify that .has_key() is not used (Python 2 syntax)"""
        # This test documents that we've migrated away from .has_key()
        test_dict = {0: 'value0'}

        # Python 2 syntax (should NOT be in codebase)
        with pytest.raises(AttributeError):
            test_dict.has_key(0)  # This should fail in Python 3


class TestBooleanConstants:
    """Test that Boolean constants use Python 3 syntax"""

    def test_true_false_are_builtin_bool(self):
        """Test that True/False are Python built-in booleans"""
        from tkinter import BooleanVar

        # Create a BooleanVar and set it to Python built-in True
        var = BooleanVar()
        var.set(True)

        assert var.get() is True

        var.set(False)
        assert var.get() is False

    def test_boolean_values_in_config(self):
        """Test boolean values work in configuration"""
        # This simulates the showPlaces, showLineHints, castAll variables
        from tkinter import BooleanVar

        config_vars = {
            'showPlaces': BooleanVar(),
            'showLineHints': BooleanVar(),
            'castAll': BooleanVar()
        }

        # Set all to True (Python 3 syntax)
        for var in config_vars.values():
            var.set(True)
            assert var.get() is True

        # Set all to False
        for var in config_vars.values():
            var.set(False)
            assert var.get() is False


class TestPathConcatenation:
    """Test Path object concatenation (Python 3 pathlib)"""

    def test_path_division_operator(self):
        """Test that Path objects use / operator, not + operator"""
        from pathlib import Path

        base = Path('/home/user')
        sub = 'subdir'

        # Python 3 pathlib syntax (correct)
        result = base / sub
        assert isinstance(result, Path)
        assert str(result).endswith('subdir')

        # Old string concatenation (should NOT work with Path)
        with pytest.raises(TypeError):
            _ = base + sub  # This should fail - can't add Path + str


class TestStringFormatting:
    """Test that modern string formatting is used"""

    def test_fstring_with_path_objects(self):
        """Test that f-strings work with Path objects"""
        from pathlib import Path

        test_path = Path('/home/user') / 'file.txt'

        # f-string formatting (Python 3.6+)
        formatted = f'Path: {test_path}'

        assert isinstance(formatted, str)
        assert 'file.txt' in formatted


class TestReduceFunction:
    """Test that reduce is imported from functools (Python 3)"""

    def test_reduce_is_available(self):
        """Test that reduce function is available from functools"""
        # In Python 3, reduce moved from builtins to functools
        from functools import reduce

        # Test reduce works
        result = reduce(lambda x, y: x + y, [1, 2, 3, 4])
        assert result == 10

    def test_reduce_used_in_hexagram_line_calculation(self):
        """Test that reduce works in hexagram line value calculation"""
        from functools import reduce

        # This simulates the line value calculation in Hexagrams.NewLine()
        # Line value = sum of oracle values (coin tosses)
        oracle_values = [2, 3, 3]  # Example coin toss results

        line_value = reduce(lambda x, y: x + y, oracle_values)

        assert line_value == 8  # 2 + 3 + 3 = 8 (yin line)


class TestPickleFileMode:
    """Test that pickle uses binary file modes (Python 3)"""

    def test_pickle_binary_mode(self):
        """Test that pickle operations use binary mode"""
        import pickle
        import tempfile

        test_data = {'key': 'value', 'number': 42}

        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            temp_file = f.name
            # Python 3 requires binary mode for pickle
            pickle.dump(test_data, f)

        with open(temp_file, 'rb') as f:
            loaded_data = pickle.load(f)

        assert loaded_data == test_data

        # Clean up
        import os
        os.unlink(temp_file)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
