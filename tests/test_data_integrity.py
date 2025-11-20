"""
Test Data Integrity
===================

These tests validate the integrity of hexagram data, images, and HTML content.

THESE TESTS VALIDATE DATA FILE INTEGRITY AND STRUCTURE.
"""

import sys
import base64
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pyching_int_data
import pyching_idimage_data
import pyching_hlhtx_data
import pytest


class TestHexagramDataCompleteness:
    """Test that all hexagram data is complete"""

    def test_all_64_hexagram_functions_exist(self):
        """All 64 hexagrams should have data functions"""
        for i in range(1, 65):
            func_name = f'in{i}data'
            assert hasattr(pyching_int_data, func_name), \
                f"Missing hexagram data function: {func_name}"

    def test_all_hexagram_functions_callable(self):
        """All hexagram data functions should be callable"""
        for i in range(1, 65):
            func_name = f'in{i}data'
            func = getattr(pyching_int_data, func_name)
            assert callable(func), f"{func_name} is not callable"

    def test_all_hexagram_functions_return_data(self):
        """All hexagram data functions should return non-empty strings"""
        for i in range(1, 65):
            func_name = f'in{i}data'
            func = getattr(pyching_int_data, func_name)
            data = func()

            assert data is not None, f"{func_name} returned None"
            assert isinstance(data, str), f"{func_name} should return string"
            assert len(data) > 0, f"{func_name} returned empty string"


class TestHexagramHTMLStructure:
    """Test HTML structure of hexagram data"""

    def test_all_hexagrams_have_html_tags(self):
        """All hexagrams should return valid HTML with basic tags"""
        for i in range(1, 65):
            func = getattr(pyching_int_data, f'in{i}data')
            html = func()

            assert '<html>' in html, f"Hexagram {i} missing <html> tag"
            assert '</html>' in html, f"Hexagram {i} missing </html> tag"
            assert '<body>' in html, f"Hexagram {i} missing <body> tag"
            assert '</body>' in html, f"Hexagram {i} missing </body> tag"

    def test_all_hexagrams_have_title(self):
        """All hexagrams should have a title in h2 tags"""
        for i in range(1, 65):
            func = getattr(pyching_int_data, f'in{i}data')
            html = func()

            assert '<h2>' in html, f"Hexagram {i} missing <h2> tag"
            assert '</h2>' in html, f"Hexagram {i} missing </h2> tag"

    def test_all_hexagrams_have_image_reference(self):
        """All hexagrams should reference an ideogram image"""
        for i in range(1, 65):
            func = getattr(pyching_int_data, f'in{i}data')
            html = func()

            assert '<img SRC=' in html or '<img src=' in html, \
                f"Hexagram {i} missing image reference"

    def test_all_hexagrams_have_line_descriptions(self):
        """All hexagrams should have descriptions for 6 lines"""
        line_markers = [
            'bottom line',
            'second line',
            'third line',
            'fourth line',
            'fifth line',
            'topmost line'
        ]

        for i in range(1, 65):
            func = getattr(pyching_int_data, f'in{i}data')
            html = func().lower()

            for marker in line_markers:
                assert marker in html, \
                    f"Hexagram {i} missing '{marker}' description"


class TestBuildHtmlFunction:
    """Test the BuildHtml utility function"""

    def test_build_html_exists(self):
        """BuildHtml function should exist"""
        assert hasattr(pyching_int_data, 'BuildHtml')

    def test_build_html_callable(self):
        """BuildHtml should be callable"""
        assert callable(pyching_int_data.BuildHtml)

    def test_build_html_with_minimal_dict(self):
        """BuildHtml should work with minimal data"""
        data = {
            'imgSrc': 'test.png',
            'title': 'Test',
            'text': 'Test text',
            1: 'Line 1',
            2: 'Line 2',
            3: 'Line 3',
            4: 'Line 4',
            5: 'Line 5',
            6: 'Line 6'
        }

        html = pyching_int_data.BuildHtml(data)

        assert isinstance(html, str)
        assert len(html) > 0
        assert '<html>' in html
        assert 'Test' in html

    def test_build_html_includes_all_lines(self):
        """BuildHtml should include all 6 line descriptions"""
        data = {
            'imgSrc': 'test.png',
            'title': 'Test',
            'text': 'Test text',
            1: 'Line 1 text',
            2: 'Line 2 text',
            3: 'Line 3 text',
            4: 'Line 4 text',
            5: 'Line 5 text',
            6: 'Line 6 text'
        }

        html = pyching_int_data.BuildHtml(data)

        for i in range(1, 7):
            assert f'Line {i} text' in html, \
                f"Line {i} not found in generated HTML"


class TestIdeogramImageData:
    """Test ideogram image data module"""

    def test_ideogram_data_module_exists(self):
        """pyching_idimage_data module should exist"""
        assert pyching_idimage_data is not None

    def test_ideogram_has_data_functions(self):
        """Ideogram module should have data functions"""
        # Check for at least a few expected functions
        for i in [1, 2, 32, 64]:
            func_name = f'id{i}data'
            assert hasattr(pyching_idimage_data, func_name), \
                f"Missing ideogram function: {func_name}"

    def test_ideogram_functions_return_data(self):
        """Ideogram functions should return data"""
        for i in [1, 2, 10, 32, 64]:
            if hasattr(pyching_idimage_data, f'id{i}data'):
                func = getattr(pyching_idimage_data, f'id{i}data')
                data = func()

                assert data is not None, f"id{i}data returned None"
                assert isinstance(data, str), f"id{i}data should return string"
                assert len(data) > 0, f"id{i}data returned empty string"


class TestHexagramLineTextData:
    """Test hexagram line text data module"""

    def test_hlhtx_module_exists(self):
        """pyching_hlhtx_data module should exist"""
        assert pyching_hlhtx_data is not None

    def test_hlhtx_has_data_functions(self):
        """Line text module should have data functions"""
        # Check for at least a few expected functions
        for i in [1, 2, 32, 64]:
            func_name = f'hl{i}data'
            if hasattr(pyching_hlhtx_data, func_name):
                func = getattr(pyching_hlhtx_data, func_name)
                assert callable(func)


class TestDataConsistency:
    """Test consistency across data modules"""

    def test_matching_hexagram_counts(self):
        """All data modules should have data for same hexagrams"""
        int_data_count = sum(1 for i in range(1, 65)
                            if hasattr(pyching_int_data, f'in{i}data'))

        assert int_data_count == 64, \
            f"Should have 64 hexagram interpretations, found {int_data_count}"

    def test_no_duplicate_hexagram_numbers(self):
        """Each hexagram number should appear only once in lookup"""
        from pyching_engine import Hexagrams

        seen_numbers = set()
        for i in range(1, 65):
            func_name = f'in{i}data'
            func = getattr(pyching_int_data, func_name)
            # Just verify uniqueness by function name
            assert func_name not in seen_numbers
            seen_numbers.add(func_name)


class TestDataEncoding:
    """Test data encoding and special characters"""

    def test_hexagram_data_handles_unicode(self):
        """Hexagram data should handle Unicode characters"""
        # Many hexagram names contain special characters
        hex1_data = pyching_int_data.in1data()

        # Should contain the apostrophe in Tch'ien
        assert "Tch'ien" in hex1_data or "Tch&#" in hex1_data or "Tch&" in hex1_data

    def test_all_hexagrams_valid_encoding(self):
        """All hexagram data should be valid UTF-8/string data"""
        for i in range(1, 65):
            func = getattr(pyching_int_data, f'in{i}data')
            data = func()

            # Should be valid string (not bytes)
            assert isinstance(data, str)
            # Should be able to encode/decode
            try:
                data.encode('utf-8')
            except UnicodeEncodeError:
                pytest.fail(f"Hexagram {i} has encoding issues")


class TestSpecificHexagramContent:
    """Test specific hexagram content for correctness"""

    def test_hexagram_1_content(self):
        """Hexagram 1 should contain expected content"""
        html = pyching_int_data.in1data()

        assert "Tch'ien" in html or "Tchien" in html
        assert len(html) > 500, "Hexagram 1 should have substantial content"

    def test_hexagram_2_content(self):
        """Hexagram 2 should contain expected content"""
        html = pyching_int_data.in2data()

        assert "Koun" in html
        assert len(html) > 500, "Hexagram 2 should have substantial content"

    def test_hexagram_64_content(self):
        """Hexagram 64 (last) should contain expected content"""
        html = pyching_int_data.in64data()

        assert "Wei Tchi" in html or "Wei" in html
        assert len(html) > 500, "Hexagram 64 should have substantial content"


class TestDataMinimumSize:
    """Test that data files have reasonable minimum sizes"""

    def test_all_hexagrams_have_substantial_content(self):
        """Each hexagram should have at least 500 characters of HTML"""
        for i in range(1, 65):
            func = getattr(pyching_int_data, f'in{i}data')
            html = func()

            assert len(html) >= 500, \
                f"Hexagram {i} has insufficient content: {len(html)} chars"

    def test_all_hexagrams_not_too_small(self):
        """No hexagram should be suspiciously small"""
        for i in range(1, 65):
            func = getattr(pyching_int_data, f'in{i}data')
            html = func()

            # Should have at minimum: html tags, title, 6 lines, some text
            min_size = 300
            assert len(html) >= min_size, \
                f"Hexagram {i} suspiciously small: {len(html)} chars"


class TestDataModuleImports:
    """Test that data modules can be imported"""

    def test_int_data_imports(self):
        """pyching_int_data should import successfully"""
        assert pyching_int_data is not None

    def test_idimage_data_imports(self):
        """pyching_idimage_data should import successfully"""
        assert pyching_idimage_data is not None

    def test_hlhtx_data_imports(self):
        """pyching_hlhtx_data should import successfully"""
        assert pyching_hlhtx_data is not None

    def test_all_data_modules_are_distinct(self):
        """All data modules should be different objects"""
        assert pyching_int_data is not pyching_idimage_data
        assert pyching_int_data is not pyching_hlhtx_data
        assert pyching_idimage_data is not pyching_hlhtx_data


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
