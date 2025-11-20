"""
Test Invalid Input Handling
============================

These tests ensure the engine handles invalid inputs gracefully.

THESE TESTS VALIDATE INPUT VALIDATION AND ERROR HANDLING.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pyching_engine
import pytest


class TestHexagramsInitialization:
    """Test Hexagrams initialization with various inputs"""

    def test_default_oracle_type_is_coin(self):
        """Default oracle type should be 'coin'"""
        hexagrams = pyching_engine.Hexagrams()
        assert hexagrams.oracle == 'coin', \
            f"Default oracle should be 'coin', got {hexagrams.oracle}"

    def test_explicit_coin_oracle(self):
        """Explicitly setting coin oracle should work"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        assert hexagrams.oracle == 'coin'

    def test_yarrow_oracle_type_accepted(self):
        """Yarrow oracle type should be accepted (even if not implemented)"""
        hexagrams = pyching_engine.Hexagrams(oracleType='yarrow')
        assert hexagrams.oracle == 'yarrow'

    def test_invalid_oracle_type_accepted(self):
        """Invalid oracle types are accepted (no validation currently)"""
        # Note: This documents current behavior - may want to add validation
        hexagrams = pyching_engine.Hexagrams(oracleType='invalid')
        assert hexagrams.oracle == 'invalid'


class TestQuestionValidation:
    """Test question input handling"""

    def test_normal_question(self):
        """Normal questions should be accepted"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.SetQuestion("What is the meaning of life?")
        assert hexagrams.question == "What is the meaning of life?"

    def test_empty_question(self):
        """Empty questions should be allowed"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.SetQuestion("")
        assert hexagrams.question == ""

    def test_very_long_question(self):
        """Very long questions should be accepted by the engine"""
        long_question = "A" * 1000
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.SetQuestion(long_question)
        assert hexagrams.question == long_question

    def test_question_with_newlines(self):
        """Questions with newlines should be preserved"""
        question_with_newlines = "Line 1\nLine 2\nLine 3"
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.SetQuestion(question_with_newlines)
        assert hexagrams.question == question_with_newlines

    def test_question_with_special_characters(self):
        """Questions with special characters should be preserved"""
        special_question = "What about: <>?/\\|[]{}!@#$%^&*()"
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.SetQuestion(special_question)
        assert hexagrams.question == special_question

    def test_question_with_quotes(self):
        """Questions with quotes should be preserved"""
        quoted_question = 'He said "What?" and I said \'Why?\''
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.SetQuestion(quoted_question)
        assert hexagrams.question == quoted_question

    def test_none_question_accepted(self):
        """Setting None as question should work (converts to None)"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.SetQuestion(None)
        assert hexagrams.question is None


class TestNewLineEdgeCases:
    """Test edge cases when calling NewLine"""

    def test_calling_newline_more_than_6_times(self):
        """Calling NewLine more than 6 times should not break"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')

        for i in range(6):
            hexagrams.NewLine()

        # After 6 lines, currentLine should be 6
        assert hexagrams.currentLine == 6

        # Calling again should not break (but won't add lines)
        hexagrams.NewLine()
        assert hexagrams.currentLine == 6  # Should stay at 6

    def test_newline_without_question(self):
        """NewLine should work even without a question set"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.NewLine()  # Should not raise
        assert hexagrams.currentLine == 1

    def test_newline_produces_valid_values_every_time(self):
        """Every NewLine call should produce valid line values"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')

        for i in range(6):
            hexagrams.NewLine()
            line_value = hexagrams.hex1.lineValues[i]
            assert line_value in [6, 7, 8, 9], \
                f"Line {i+1} has invalid value {line_value}"


class TestHexagramDataStructure:
    """Test that hexagram data structures are properly initialized"""

    def test_initial_line_values_are_zero(self):
        """Initial line values should all be 0"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        assert hexagrams.hex1.lineValues == [0, 0, 0, 0, 0, 0]
        assert hexagrams.hex2.lineValues == [0, 0, 0, 0, 0, 0]

    def test_initial_number_is_empty_string(self):
        """Initial hexagram numbers should be empty strings"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        assert hexagrams.hex1.number == ''
        assert hexagrams.hex2.number == ''

    def test_initial_name_is_empty_string(self):
        """Initial hexagram names should be empty strings"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        assert hexagrams.hex1.name == ''
        assert hexagrams.hex2.name == ''

    def test_initial_info_source_is_none(self):
        """Initial infoSource should be None"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        assert hexagrams.hex1.infoSource is None
        assert hexagrams.hex2.infoSource is None

    def test_current_line_starts_at_zero(self):
        """Current line should start at 0"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        assert hexagrams.currentLine == 0

    def test_oracle_values_initially_empty(self):
        """Oracle values should be empty list initially"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        assert hexagrams.currentOracleValues == []


class TestReadingAsTextEdgeCases:
    """Test ReadingAsText with various edge cases"""

    def test_reading_as_text_with_no_lines(self):
        """ReadingAsText should work even with no lines cast"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.SetQuestion("Empty reading")

        text = hexagrams.ReadingAsText()
        assert isinstance(text, str)
        assert "Empty reading" in text

    def test_reading_as_text_with_partial_reading(self):
        """ReadingAsText should work with partial readings"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.SetQuestion("Partial")
        hexagrams.NewLine()
        hexagrams.NewLine()
        hexagrams.NewLine()

        text = hexagrams.ReadingAsText()
        assert isinstance(text, str)
        assert "Partial" in text

    def test_reading_as_text_with_empty_question(self):
        """ReadingAsText should work with empty question"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.SetQuestion("")
        for _ in range(6):
            hexagrams.NewLine()

        text = hexagrams.ReadingAsText()
        assert isinstance(text, str)

    def test_reading_as_text_returns_non_empty_string(self):
        """ReadingAsText should always return a non-empty string"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        text = hexagrams.ReadingAsText()
        assert len(text) > 0


class TestPychingAppDetails:
    """Test PychingAppDetails initialization"""

    def test_app_details_creation(self):
        """PychingAppDetails should create successfully"""
        app = pyching_engine.PychingAppDetails(createConfigDir=0)
        assert app is not None

    def test_app_has_required_attributes(self):
        """App details should have all required attributes"""
        app = pyching_engine.PychingAppDetails(createConfigDir=0)

        assert hasattr(app, 'title')
        assert hasattr(app, 'version')
        assert hasattr(app, 'os')
        assert hasattr(app, 'osType')
        assert hasattr(app, 'execPath')
        assert hasattr(app, 'configPath')
        assert hasattr(app, 'savePath')
        assert hasattr(app, 'configFile')
        assert hasattr(app, 'saveFileExt')
        assert hasattr(app, 'saveFileID')

    def test_version_is_string(self):
        """Version should be a string"""
        app = pyching_engine.PychingAppDetails(createConfigDir=0)
        assert isinstance(app.version, str)
        assert len(app.version) > 0

    def test_save_file_id_is_tuple(self):
        """Save file ID should be a tuple"""
        app = pyching_engine.PychingAppDetails(createConfigDir=0)
        assert isinstance(app.saveFileID, tuple)
        assert len(app.saveFileID) == 2

    def test_title_is_pyching(self):
        """Title should be pyChing"""
        app = pyching_engine.PychingAppDetails(createConfigDir=0)
        assert app.title == 'pyChing'


class TestTypeValidation:
    """Test that types are correct throughout"""

    def test_hexagram_number_is_string(self):
        """Hexagram numbers should be strings, not integers"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        for _ in range(6):
            hexagrams.NewLine()

        assert isinstance(hexagrams.hex1.number, str), \
            f"Hexagram number should be string, got {type(hexagrams.hex1.number)}"

    def test_line_values_are_integers(self):
        """Line values should be integers"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.NewLine()

        for val in hexagrams.hex1.lineValues:
            assert isinstance(val, int), \
                f"Line value should be int, got {type(val)}"

    def test_oracle_values_are_integers(self):
        """Oracle values (coin tosses) should be integers"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.NewLine()

        for val in hexagrams.currentOracleValues:
            assert isinstance(val, int), \
                f"Oracle value should be int, got {type(val)}"

    def test_current_line_is_integer(self):
        """Current line counter should be integer"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        assert isinstance(hexagrams.currentLine, int)


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
