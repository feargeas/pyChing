"""
Test Console Interface Functions
=================================

These tests validate the console interface input handling and display.

THESE TESTS VALIDATE THE CONSOLE INTERFACE USER INTERACTIONS.
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from io import StringIO

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pyching_interface_console
import pyching_engine
import pytest


class TestGetQuestion:
    """Test the get_question() function"""

    @patch('builtins.input', return_value='What is my purpose?')
    def test_get_question_normal(self, mock_input):
        """Normal question should be accepted"""
        question = pyching_interface_console.get_question()
        assert question == 'What is my purpose?'

    @patch('builtins.input', side_effect=['', '', 'Valid question'])
    def test_get_question_requires_non_empty(self, mock_input):
        """Empty questions should be rejected and re-prompted"""
        question = pyching_interface_console.get_question()
        assert question == 'Valid question'
        assert mock_input.call_count == 3

    @patch('builtins.input', side_effect=['A' * 71, 'A' * 70])
    def test_get_question_enforces_length_limit(self, mock_input):
        """Questions over 70 characters should be rejected"""
        question = pyching_interface_console.get_question()
        assert len(question) == 70
        assert mock_input.call_count == 2

    @patch('builtins.input', side_effect=KeyboardInterrupt())
    def test_get_question_handles_ctrl_c(self, mock_input):
        """Ctrl+C should return None"""
        question = pyching_interface_console.get_question()
        assert question is None

    @patch('builtins.input', side_effect=EOFError())
    def test_get_question_handles_eof(self, mock_input):
        """EOF should return None"""
        question = pyching_interface_console.get_question()
        assert question is None

    @patch('builtins.input', return_value='  spaces around  ')
    def test_get_question_strips_whitespace(self, mock_input):
        """Leading/trailing whitespace should be stripped"""
        question = pyching_interface_console.get_question()
        assert question == 'spaces around'

    @patch('builtins.input', return_value='What about 易經?')
    def test_get_question_accepts_unicode(self, mock_input):
        """Unicode characters should be accepted"""
        question = pyching_interface_console.get_question()
        assert question == 'What about 易經?'


class TestCastReading:
    """Test the cast_reading() function"""

    @patch('builtins.input', return_value='')
    def test_cast_reading_completes_all_six_lines(self, mock_input):
        """Casting should complete all 6 lines"""
        hexes = pyching_engine.Hexagrams(oracleType='coin')
        result = pyching_interface_console.cast_reading(hexes)

        assert result is True
        assert hexes.currentLine == 6
        assert mock_input.call_count == 6

    @patch('builtins.input', side_effect=KeyboardInterrupt())
    def test_cast_reading_handles_cancellation(self, mock_input):
        """Ctrl+C during casting should return False"""
        hexes = pyching_engine.Hexagrams(oracleType='coin')
        result = pyching_interface_console.cast_reading(hexes)

        assert result is False

    @patch('builtins.input', side_effect=EOFError())
    def test_cast_reading_handles_eof(self, mock_input):
        """EOF during casting should return False"""
        hexes = pyching_engine.Hexagrams(oracleType='coin')
        result = pyching_interface_console.cast_reading(hexes)

        assert result is False

    @patch('builtins.input', return_value='')
    def test_cast_reading_populates_oracle_values(self, mock_input):
        """Each line should have oracle values (coin tosses)"""
        hexes = pyching_engine.Hexagrams(oracleType='coin')
        pyching_interface_console.cast_reading(hexes)

        # After casting, currentOracleValues should be set
        assert len(hexes.currentOracleValues) == 3


class TestDisplayReading:
    """Test the display_reading() function"""

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_reading_shows_question(self, mock_stdout):
        """Display should include the question"""
        hexes = pyching_engine.Hexagrams(oracleType='coin')
        hexes.SetQuestion("Test question display")
        for _ in range(6):
            hexes.NewLine()

        pyching_interface_console.display_reading(hexes)
        output = mock_stdout.getvalue()

        assert "Test question display" in output

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_reading_shows_hexagram_info(self, mock_stdout):
        """Display should show hexagram number and name"""
        hexes = pyching_engine.Hexagrams(oracleType='coin')
        hexes.SetQuestion("Show hex info")
        hexes.hex1.lineValues = [7, 7, 7, 7, 7, 7]
        hexes.currentLine = 6
        hexes.NewLine()

        pyching_interface_console.display_reading(hexes)
        output = mock_stdout.getvalue()

        assert hexes.hex1.number in output
        assert hexes.hex1.name in output

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_reading_with_transformation(self, mock_stdout):
        """Display should show both hexagrams when there are moving lines"""
        hexes = pyching_engine.Hexagrams(oracleType='coin')
        hexes.SetQuestion("Moving lines")
        hexes.hex1.lineValues = [9, 7, 7, 7, 7, 7]
        hexes.currentLine = 6
        hexes.NewLine()

        pyching_interface_console.display_reading(hexes)
        output = mock_stdout.getvalue()

        assert "becomes" in output or hexes.hex2.number in output


class TestWrapText:
    """Test the wrap_text() function"""

    def test_wrap_text_short_text(self):
        """Short text should not be wrapped"""
        text = "Short text"
        wrapped = pyching_interface_console.wrap_text(text, 70)
        assert wrapped == "Short text"

    def test_wrap_text_at_width(self):
        """Text should wrap at specified width"""
        text = "A" * 100
        wrapped = pyching_interface_console.wrap_text(text, 50)
        lines = wrapped.split('\n')
        for line in lines:
            assert len(line) <= 50

    def test_wrap_text_preserves_words(self):
        """Wrapping should not break words"""
        text = "The quick brown fox jumps over the lazy dog"
        wrapped = pyching_interface_console.wrap_text(text, 20)
        lines = wrapped.split('\n')

        # Each word should be intact
        assert 'quick' in wrapped
        assert 'brown' in wrapped
        assert 'jumps' in wrapped

    def test_wrap_text_empty_string(self):
        """Empty string should return empty"""
        wrapped = pyching_interface_console.wrap_text("", 70)
        assert wrapped == ""

    def test_wrap_text_single_long_word(self):
        """Single word longer than width should be on its own line"""
        text = "A" * 100
        wrapped = pyching_interface_console.wrap_text(text, 50)
        lines = wrapped.split('\n')
        assert len(lines) >= 2


class TestHTMLToText:
    """Test the html_to_text() function"""

    def test_html_to_text_simple(self):
        """Simple HTML should be converted to text"""
        html = "<p>Simple paragraph</p>"
        text = pyching_interface_console.html_to_text(html)
        assert "Simple paragraph" in text

    def test_html_to_text_removes_tags(self):
        """HTML tags should be removed"""
        html = "<p>Text with <b>bold</b> and <i>italic</i></p>"
        text = pyching_interface_console.html_to_text(html)
        assert "<b>" not in text
        assert "<i>" not in text
        assert "bold" in text
        assert "italic" in text

    def test_html_to_text_headings(self):
        """Headings should be converted"""
        html = "<h2>Heading Text</h2><p>Body text</p>"
        text = pyching_interface_console.html_to_text(html)
        assert "Heading Text" in text
        assert "Body text" in text

    def test_html_to_text_line_breaks(self):
        """HTML line breaks should create text breaks"""
        html = "<p>Line 1</p><p>Line 2</p>"
        text = pyching_interface_console.html_to_text(html)
        assert "Line 1" in text
        assert "Line 2" in text

    def test_html_to_text_empty(self):
        """Empty HTML should return empty string"""
        html = ""
        text = pyching_interface_console.html_to_text(html)
        assert text == ""

    def test_html_to_text_complex(self):
        """Complex HTML structure should be handled"""
        html = """
        <html>
        <body>
        <h2>Title</h2>
        <p>First paragraph</p>
        <p>Second paragraph with <b>bold text</b></p>
        </body>
        </html>
        """
        text = pyching_interface_console.html_to_text(html)
        assert "Title" in text
        assert "First paragraph" in text
        assert "Second paragraph" in text
        assert "bold text" in text


class TestPrintBanner:
    """Test the print_banner() function"""

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_banner_displays_title(self, mock_stdout):
        """Banner should display pyChing title"""
        pyching_interface_console.print_banner()
        output = mock_stdout.getvalue()
        assert "pyChing" in output

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_banner_displays_version(self, mock_stdout):
        """Banner should display version"""
        pyching_interface_console.print_banner()
        output = mock_stdout.getvalue()
        assert "Version" in output


class TestDisplayInterpretation:
    """Test the display_interpretation() function"""

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_interpretation_shows_hexagram_1(self, mock_stdout):
        """Interpretation should display hex1 info"""
        hexes = pyching_engine.Hexagrams(oracleType='coin')
        hexes.hex1.lineValues = [7, 7, 7, 7, 7, 7]
        hexes.currentLine = 6
        hexes.NewLine()

        pyching_interface_console.display_interpretation(hexes)
        output = mock_stdout.getvalue()

        assert hexes.hex1.number in output
        assert hexes.hex1.name in output

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_interpretation_shows_hex2_when_present(self, mock_stdout):
        """Interpretation should display hex2 if moving lines exist"""
        hexes = pyching_engine.Hexagrams(oracleType='coin')
        hexes.hex1.lineValues = [9, 7, 7, 7, 7, 7]
        hexes.currentLine = 6
        hexes.NewLine()

        pyching_interface_console.display_interpretation(hexes)
        output = mock_stdout.getvalue()

        if hexes.hex2.number:
            assert hexes.hex2.number in output or "TRANSFORMATION" in output


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
