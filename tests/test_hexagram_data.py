"""
Test Hexagram Data Functions
=============================

These tests ensure all 64 hexagram data functions are accessible and return valid HTML data.

The hexagram data is based on James Legge's 1882 translation of the I Ching.
This translation must be preserved exactly.

THESE TESTS MUST PASS AFTER PYTHON 3 MIGRATION.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pyching_int_data


class TestAllHexagramsExist:
    """Test that all 64 hexagrams have data functions"""

    def test_all_64_hexagrams_have_functions(self):
        """Each hexagram from 1-64 must have a data function that returns HTML"""
        for i in range(1, 65):
            func_name = f'in{i}data'
            assert hasattr(pyching_int_data, func_name), \
                f"Missing data function: {func_name}"

            # Call the function to ensure it works
            func = getattr(pyching_int_data, func_name)
            html_data = func()

            assert html_data is not None, \
                f"Function {func_name} returned None"
            assert isinstance(html_data, str), \
                f"Function {func_name} should return HTML string, got {type(html_data)}"
            assert len(html_data) > 0, \
                f"Function {func_name} returned empty string"


class TestHexagramHTMLStructure:
    """Test that hexagram HTML has the correct structure"""

    def test_hexagram_html_is_valid(self):
        """Each hexagram HTML should contain basic HTML tags"""
        for i in range(1, 65):
            func_name = f'in{i}data'
            func = getattr(pyching_int_data, func_name)
            html = func()

            assert '<html>' in html, \
                f"Hexagram {i} HTML should contain <html> tag"
            assert '</html>' in html, \
                f"Hexagram {i} HTML should contain </html> tag"
            assert '<body>' in html, \
                f"Hexagram {i} HTML should contain <body> tag"
            assert '</body>' in html, \
                f"Hexagram {i} HTML should contain </body> tag"

    def test_hexagram_html_contains_title(self):
        """Each hexagram HTML should contain a title in h2 tags"""
        for i in range(1, 65):
            func_name = f'in{i}data'
            func = getattr(pyching_int_data, func_name)
            html = func()

            assert '<h2>' in html, \
                f"Hexagram {i} HTML should contain <h2> tag for title"
            assert '</h2>' in html, \
                f"Hexagram {i} HTML should contain </h2> closing tag"

    def test_hexagram_html_contains_line_descriptions(self):
        """Each hexagram HTML should contain descriptions for all 6 lines"""
        line_markers = [
            '<b>The bottom line</b>',
            '<b>The second line</b>',
            '<b>The third line</b>',
            '<b>The fourth line</b>',
            '<b>The fifth line</b>',
            '<b>The topmost line</b>'
        ]

        for i in range(1, 65):
            func_name = f'in{i}data'
            func = getattr(pyching_int_data, func_name)
            html = func()

            for line_marker in line_markers:
                assert line_marker in html, \
                    f"Hexagram {i} HTML should contain '{line_marker}'"

    def test_hexagram_html_contains_image_reference(self):
        """Each hexagram HTML should reference an ideogram image"""
        for i in range(1, 65):
            func_name = f'in{i}data'
            func = getattr(pyching_int_data, func_name)
            html = func()

            assert '<img SRC=' in html, \
                f"Hexagram {i} HTML should contain image reference"
            assert 'pyching_idimage_data' in html, \
                f"Hexagram {i} HTML should reference pyching_idimage_data"


class TestSpecificHexagrams:
    """Test specific hexagrams to ensure correct data"""

    def test_hexagram_1_tch_ien(self):
        """Test Hexagram 1 - Tch'ien (The Creative)"""
        html = pyching_int_data.in1data()

        assert "Tch'ien" in html, "Should contain Tch'ien"
        assert "Creative" in html, "Should contain 'Creative'"
        assert len(html) > 100, "Should have substantial content"

    def test_hexagram_2_koun(self):
        """Test Hexagram 2 - Koun (The Receptive)"""
        html = pyching_int_data.in2data()

        assert "Koun" in html, "Should contain Koun"
        assert "Receptive" in html, "Should contain 'Receptive'"
        assert len(html) > 100, "Should have substantial content"

    def test_hexagram_64_wei_tchi(self):
        """Test Hexagram 64 - Wei Tchi (Before Completion/Achievement)"""
        html = pyching_int_data.in64data()

        assert "Wei Tchi" in html, "Should contain Wei Tchi"
        assert len(html) > 100, "Should have substantial content"


class TestBuildHtmlFunction:
    """Test the BuildHtml utility function"""

    def test_build_html_function_exists(self):
        """BuildHtml function should exist and be callable"""
        assert hasattr(pyching_int_data, 'BuildHtml'), \
            "BuildHtml function should exist"
        assert callable(pyching_int_data.BuildHtml), \
            "BuildHtml should be callable"

    def test_build_html_creates_valid_html(self):
        """BuildHtml should create valid HTML from a dict"""
        test_dict = {
            'imgSrc': 'test.png',
            'title': 'Test Title',
            'text': 'Test text content',
            1: 'Line 1',
            2: 'Line 2',
            3: 'Line 3',
            4: 'Line 4',
            5: 'Line 5',
            6: 'Line 6'
        }

        html = pyching_int_data.BuildHtml(test_dict)

        assert '<html>' in html
        assert 'Test Title' in html
        assert 'Test text content' in html
        assert 'Line 1' in html
        assert 'Line 6' in html


if __name__ == '__main__':
    # Simple test runner for manual testing
    import pytest
    pytest.main([__file__, '-v'])
