"""
Test Reading Persistence and Question Handling
==============================================

These tests ensure that readings can be saved, loaded, and include questions.

THESE TESTS MUST PASS AFTER PYTHON 3 MIGRATION.
"""

import sys
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pyching_engine


class TestQuestionHandling:
    """Test that questions are properly stored and retrieved"""

    def test_set_question(self):
        """Questions should be stored correctly"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')

        question = "What should I do about my current situation?"
        hexagrams.SetQuestion(question)

        assert hexagrams.question == question, \
            f"Question should be '{question}', got '{hexagrams.question}'"

    def test_empty_question(self):
        """Empty questions should be allowed"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')

        hexagrams.SetQuestion("")
        assert hexagrams.question == "", \
            "Empty question should be allowed"

    def test_unicode_question(self):
        """Questions with Unicode characters should be supported"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')

        question = "What about 易經 (I Ching)?"
        hexagrams.SetQuestion(question)

        assert hexagrams.question == question, \
            f"Unicode question should be preserved"


class TestReadingSaveLoad:
    """Test that readings can be saved and loaded"""

    def test_save_and_load_complete_reading(self):
        """A complete reading should save and load correctly"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')

        # Create a complete reading
        hexagrams.SetQuestion("Test question")
        for _ in range(6):
            hexagrams.NewLine()

        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.psv') as f:
            temp_file = f.name

        try:
            # Save the reading
            hexagrams.Save(temp_file)

            # Create a new instance and load
            loaded_hexagrams = pyching_engine.Hexagrams(oracleType='coin')
            version = loaded_hexagrams.Load(temp_file)

            # Verify data matches
            assert loaded_hexagrams.question == hexagrams.question, \
                "Question should match after load"
            assert loaded_hexagrams.hex1.lineValues == hexagrams.hex1.lineValues, \
                "Hex1 line values should match after load"
            assert loaded_hexagrams.hex1.number == hexagrams.hex1.number, \
                "Hex1 number should match after load"
            assert loaded_hexagrams.hex1.name == hexagrams.hex1.name, \
                "Hex1 name should match after load"

            if hexagrams.hex2.number != '':
                assert loaded_hexagrams.hex2.lineValues == hexagrams.hex2.lineValues, \
                    "Hex2 line values should match after load"
                assert loaded_hexagrams.hex2.number == hexagrams.hex2.number, \
                    "Hex2 number should match after load"

        finally:
            # Clean up temp file
            temp_path = Path(temp_file)
            if temp_path.exists():
                temp_path.unlink()

    def test_save_and_load_partial_reading(self):
        """A partial reading should save and load correctly"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')

        # Create a partial reading (3 lines)
        hexagrams.SetQuestion("Partial test")
        for _ in range(3):
            hexagrams.NewLine()

        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.psv') as f:
            temp_file = f.name

        try:
            hexagrams.Save(temp_file)

            # Load it back
            loaded_hexagrams = pyching_engine.Hexagrams(oracleType='coin')
            loaded_hexagrams.Load(temp_file)

            # Verify
            assert loaded_hexagrams.question == "Partial test"
            assert loaded_hexagrams.currentLine == 3, \
                "Should have 3 lines"
            assert loaded_hexagrams.hex1.lineValues[:3] == hexagrams.hex1.lineValues[:3], \
                "First 3 lines should match"

        finally:
            temp_path = Path(temp_file)
            if temp_path.exists():
                temp_path.unlink()

    def test_load_returns_version(self):
        """Loading should return the save file version"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')

        hexagrams.SetQuestion("Version test")
        for _ in range(6):
            hexagrams.NewLine()

        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.psv') as f:
            temp_file = f.name

        try:
            hexagrams.Save(temp_file)

            # Load and check version
            loaded_hexagrams = pyching_engine.Hexagrams(oracleType='coin')
            version = loaded_hexagrams.Load(temp_file)

            assert version is not None, "Load should return version info"
            assert isinstance(version, tuple), "Version should be a tuple"

        finally:
            temp_path = Path(temp_file)
            if temp_path.exists():
                temp_path.unlink()


class TestReadingAsText:
    """Test that readings can be converted to text representation"""

    def test_reading_as_text_format(self):
        """Text representation should include hexagram info and question"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')

        hexagrams.SetQuestion("Test question for text output")
        hexagrams.hex1.lineValues = [7, 7, 7, 7, 7, 7]
        hexagrams.currentLine = 6
        hexagrams.NewLine()

        text = hexagrams.ReadingAsText()

        # Should contain the question
        assert "Test question for text output" in text, \
            "Text should contain the question"

        # Should contain hexagram number and name
        assert hexagrams.hex1.number in text, \
            "Text should contain hex1 number"
        assert hexagrams.hex1.name in text, \
            "Text should contain hex1 name"

        # Should contain line representations
        assert '-------' in text, \
            "Text should contain line representations"

    def test_reading_with_moving_lines_shows_transformation(self):
        """Text with moving lines should show 'becomes'"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')

        hexagrams.SetQuestion("Moving lines test")
        hexagrams.hex1.lineValues = [9, 7, 7, 7, 7, 7]  # One moving line
        hexagrams.currentLine = 6
        hexagrams.NewLine()

        text = hexagrams.ReadingAsText()

        # Should indicate transformation
        assert 'becomes' in text, \
            "Text should contain 'becomes' for moving lines"

        # Should show both hexagrams
        assert hexagrams.hex1.number in text and hexagrams.hex2.number in text, \
            "Text should show both hexagram numbers"

    def test_reading_without_moving_lines_shows_no_change(self):
        """Text without moving lines should indicate no transformation"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')

        hexagrams.SetQuestion("No moving lines test")
        hexagrams.hex1.lineValues = [7, 7, 7, 8, 8, 8]  # No moving lines
        hexagrams.currentLine = 6
        hexagrams.NewLine()

        text = hexagrams.ReadingAsText()

        # Should indicate no moving lines
        assert 'no moving lines' in text, \
            "Text should contain 'no moving lines' when there are none"


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
