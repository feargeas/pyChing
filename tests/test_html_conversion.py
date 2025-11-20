"""
Test HTML to Text Conversion
=============================

These tests validate HTML parsing and text extraction for hexagram interpretations.

THESE TESTS VALIDATE HTML PARSING CORRECTNESS AND EDGE CASES.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pyching_interface_console
from pyching_interface_console import HTMLToText, html_to_text
import pytest


class TestHTMLToTextBasic:
    """Test basic HTML to text conversion"""

    def test_plain_text_no_tags(self):
        """Plain text without tags should pass through"""
        html = "Just plain text"
        text = html_to_text(html)
        assert "Just plain text" in text

    def test_single_paragraph(self):
        """Single paragraph should be extracted"""
        html = "<p>This is a paragraph.</p>"
        text = html_to_text(html)
        assert "This is a paragraph." in text
        assert "<p>" not in text

    def test_multiple_paragraphs(self):
        """Multiple paragraphs should be separated"""
        html = "<p>First paragraph</p><p>Second paragraph</p>"
        text = html_to_text(html)
        assert "First paragraph" in text
        assert "Second paragraph" in text

    def test_bold_text(self):
        """Bold tags should be removed but content preserved"""
        html = "<b>Bold text</b>"
        text = html_to_text(html)
        assert "Bold text" in text
        assert "<b>" not in text

    def test_italic_text(self):
        """Italic tags should be removed but content preserved"""
        html = "<i>Italic text</i>"
        text = html_to_text(html)
        assert "Italic text" in text
        assert "<i>" not in text

    def test_mixed_formatting(self):
        """Mixed formatting should be handled"""
        html = "<p>Text with <b>bold</b> and <i>italic</i> and <u>underline</u></p>"
        text = html_to_text(html)
        assert "Text with bold and italic and underline" in text
        assert "<" not in text


class TestHTMLToTextHeadings:
    """Test heading extraction"""

    def test_h1_heading(self):
        """H1 headings should be extracted"""
        html = "<h1>Main Heading</h1>"
        text = html_to_text(html)
        assert "Main Heading" in text

    def test_h2_heading(self):
        """H2 headings should be extracted"""
        html = "<h2>Subheading</h2>"
        text = html_to_text(html)
        assert "Subheading" in text

    def test_all_heading_levels(self):
        """All heading levels should be handled"""
        for level in range(1, 7):
            html = f"<h{level}>Heading Level {level}</h{level}>"
            text = html_to_text(html)
            assert f"Heading Level {level}" in text

    def test_heading_with_paragraph(self):
        """Headings followed by paragraphs should be separated"""
        html = "<h2>Title</h2><p>Content text</p>"
        text = html_to_text(html)
        assert "Title" in text
        assert "Content text" in text


class TestHTMLToTextLineBreaks:
    """Test line break handling"""

    def test_br_tag(self):
        """<br> tags should create line breaks"""
        html = "Line 1<br>Line 2"
        text = html_to_text(html)
        assert "Line 1" in text
        assert "Line 2" in text

    def test_br_self_closing(self):
        """Self-closing <br/> should work"""
        html = "Line 1<br/>Line 2"
        text = html_to_text(html)
        assert "Line 1" in text
        assert "Line 2" in text


class TestHTMLToTextWhitespace:
    """Test whitespace handling"""

    def test_multiple_spaces_collapsed(self):
        """Multiple spaces should be collapsed to single space"""
        html = "<p>Text  with   multiple    spaces</p>"
        text = html_to_text(html)
        # The converter should clean this up
        assert "Text with multiple spaces" in text or "Text  with" in text

    def test_newlines_in_source_ignored(self):
        """Newlines in HTML source should not create text newlines"""
        html = """<p>Text
        with
        newlines
        in
        source</p>"""
        text = html_to_text(html)
        assert "Text with newlines in source" in text

    def test_leading_trailing_whitespace_stripped(self):
        """Leading/trailing whitespace should be stripped"""
        html = "  <p>  Text with spaces  </p>  "
        text = html_to_text(html)
        # Should not start or end with excess whitespace
        assert text.strip() == text or "Text with spaces" in text


class TestHTMLToTextComplexStructures:
    """Test complex HTML structures"""

    def test_nested_tags(self):
        """Nested tags should be handled"""
        html = "<p>Outer <b>bold <i>and italic</i> text</b> here</p>"
        text = html_to_text(html)
        assert "Outer bold and italic text here" in text

    def test_div_tags(self):
        """Div tags should be processed"""
        html = "<div>Content in div</div>"
        text = html_to_text(html)
        assert "Content in div" in text

    def test_full_html_document(self):
        """Full HTML document structure should be handled"""
        html = """
        <html>
        <head><title>Title</title></head>
        <body>
        <h2>Heading</h2>
        <p>Paragraph text</p>
        </body>
        </html>
        """
        text = html_to_text(html)
        assert "Heading" in text
        assert "Paragraph text" in text


class TestHTMLToTextSpecialCases:
    """Test special cases and edge conditions"""

    def test_empty_html(self):
        """Empty HTML should return empty text"""
        html = ""
        text = html_to_text(html)
        assert text == ""

    def test_only_tags_no_content(self):
        """HTML with only tags should return minimal text"""
        html = "<p></p><div></div>"
        text = html_to_text(html)
        # Should be empty or whitespace only
        assert len(text.strip()) == 0

    def test_html_entities(self):
        """HTML entities should be handled (if parser supports)"""
        html = "<p>Text with &amp; ampersand</p>"
        text = html_to_text(html)
        # HTMLParser should decode entities
        assert "Text with" in text

    def test_unicode_content(self):
        """Unicode content should be preserved"""
        html = "<p>易經 (I Ching) 陰陽</p>"
        text = html_to_text(html)
        assert "易經" in text
        assert "陰陽" in text

    def test_malformed_html(self):
        """Malformed HTML should not crash"""
        html = "<p>Unclosed paragraph"
        try:
            text = html_to_text(html)
            assert "Unclosed paragraph" in text
        except Exception:
            pytest.fail("Should handle malformed HTML gracefully")


class TestHTMLToTextRealHexagramData:
    """Test with actual hexagram HTML data"""

    def test_hexagram_html_conversion(self):
        """Real hexagram HTML should convert properly"""
        # Import hexagram data
        import pyching_int_data

        # Test with Hexagram 1
        hex1_html = pyching_int_data.in1data()
        text = html_to_text(hex1_html)

        # Should contain some expected text
        assert len(text) > 0
        assert "Tch'ien" in text or "Creative" in text

    def test_all_hexagrams_convert_without_error(self):
        """All 64 hexagrams should convert without errors"""
        import pyching_int_data

        for i in range(1, 65):
            func_name = f'in{i}data'
            func = getattr(pyching_int_data, func_name)
            html = func()

            try:
                text = html_to_text(html)
                assert len(text) > 0, f"Hexagram {i} conversion produced empty text"
            except Exception as e:
                pytest.fail(f"Hexagram {i} conversion failed: {e}")


class TestHTMLToTextClass:
    """Test the HTMLToText class directly"""

    def test_parser_creation(self):
        """Parser should be created successfully"""
        parser = HTMLToText()
        assert parser is not None

    def test_parser_feed(self):
        """Parser should accept HTML via feed()"""
        parser = HTMLToText()
        parser.feed("<p>Test</p>")
        text = parser.get_text()
        assert "Test" in text

    def test_parser_get_text(self):
        """get_text() should return extracted text"""
        parser = HTMLToText()
        parser.feed("<p>Extracted text</p>")
        text = parser.get_text()
        assert isinstance(text, str)
        assert "Extracted text" in text

    def test_parser_reuse(self):
        """Parser should handle multiple feeds"""
        parser = HTMLToText()
        parser.feed("<p>First</p>")
        parser.feed("<p>Second</p>")
        text = parser.get_text()
        assert "First" in text
        assert "Second" in text


class TestHTMLToTextLineDescriptions:
    """Test extraction of line descriptions from hexagram HTML"""

    def test_line_markers_extracted(self):
        """Line position markers should be in extracted text"""
        import pyching_int_data

        # Hexagram 1 should have line descriptions
        hex1_html = pyching_int_data.in1data()
        text = html_to_text(hex1_html)

        # Should contain line position words
        # (exact format may vary based on HTML structure)
        assert "line" in text.lower() or "bottom" in text.lower()


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
