"""
Test Hexagram Lookup Completeness
==================================

These tests ensure all 64 hexagrams are correctly identified by the lookup system.

THESE TESTS VALIDATE THE COMPLETE HEXAGRAM LOOKUP TABLE.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pyching_engine
import pytest


# Complete lookup table for all 64 hexagrams
# Format: (line_values, expected_number, expected_name)
ALL_HEXAGRAMS = [
    ([7,7,7,7,7,7], '1', "Tch'ien"),
    ([8,8,8,8,8,8], '2', "Koun"),
    ([7,8,8,8,7,8], '3', "T'oun"),
    ([8,7,8,8,8,7], '4', "Mong"),
    ([7,7,7,8,7,8], '5', "Hsu"),
    ([8,7,8,7,7,7], '6', "Song"),
    ([8,7,8,8,8,8], '7', "Cheu"),
    ([8,8,8,8,7,8], '8', "Pi"),
    ([7,7,7,8,7,7], '9', "Siao Tch'ou"),
    ([7,7,8,7,7,7], '10', "Li"),
    ([7,7,7,8,8,8], '11', "T'ai"),
    ([8,8,8,7,7,7], '12', "P'i"),
    ([7,8,7,7,7,7], '13', "Tong Jen"),
    ([7,7,7,7,8,7], '14', "Ta You"),
    ([8,8,7,8,8,8], '15', "Tchien"),
    ([8,8,8,7,8,8], '16', "Yu"),
    ([7,8,8,7,7,8], '17', "Souei"),
    ([8,7,7,8,8,7], '18', "Kou"),
    ([7,7,8,8,8,8], '19', "Lin"),
    ([8,8,8,8,7,7], '20', "Kouan"),
    ([7,8,8,7,8,7], '21', "Che Ho"),
    ([7,8,7,8,8,7], '22', "Pi"),
    ([8,8,8,8,8,7], '23', "Po"),
    ([7,8,8,8,8,8], '24', "Fou"),
    ([7,8,8,7,7,7], '25', "Wou Wang"),
    ([7,7,7,8,8,7], '26', "Ta Tch'ou"),
    ([7,8,8,8,8,7], '27', "I"),
    ([8,7,7,7,7,8], '28', "Ta Kouo"),
    ([8,7,8,8,7,8], '29', "K'an"),
    ([7,8,7,7,8,7], '30', "Li"),
    ([8,8,7,7,7,8], '31', "Hsien"),
    ([8,7,7,7,8,8], '32', "Hong"),
    ([8,8,7,7,7,7], '33', "Toun"),
    ([7,7,7,7,8,8], '34', "Ta Tch'ouang"),
    ([8,8,8,7,8,7], '35', "Tchin"),
    ([7,8,7,8,8,8], '36', "Ming Yi"),
    ([7,8,7,8,7,7], '37', "Tchia Jen"),
    ([7,7,8,7,8,7], '38', "K'ouei"),
    ([8,8,7,8,7,8], '39', "Tch'ien"),
    ([8,7,8,7,8,8], '40', "Tchieh"),
    ([7,7,8,8,8,7], '41', "Soun"),
    ([7,8,8,8,7,7], '42', "Yi"),
    ([7,7,7,7,7,8], '43', "Kouai"),
    ([8,7,7,7,7,7], '44', "Keou"),
    ([8,8,8,7,7,8], '45', "Ts'ouei"),
    ([8,7,7,8,8,8], '46', "Cheng"),
    ([8,7,8,7,7,8], '47', "K'oun"),
    ([8,7,7,8,7,8], '48', "Tsing"),
    ([7,8,7,7,7,8], '49', "Keu"),
    ([8,7,7,7,8,7], '50', "Ting"),
    ([7,8,8,7,8,8], '51', "Tchen"),
    ([8,8,7,8,8,7], '52', "Ken"),
    ([8,8,7,8,7,7], '53', "Tchien"),
    ([7,7,8,7,8,8], '54', "Kouei Mei"),
    ([7,8,7,7,8,8], '55', "Fong"),
    ([8,8,7,7,8,7], '56', "Lu"),
    ([8,7,7,8,7,7], '57', "Hsuan"),
    ([7,7,8,7,7,8], '58', "Touei"),
    ([8,7,8,8,7,7], '59', "Houan"),
    ([7,7,8,8,7,8], '60', "Tchieh"),
    ([7,7,8,8,7,7], '61', "Tchong Fou"),
    ([8,8,7,7,8,8], '62', "Siao Kouo"),
    ([7,8,7,8,7,8], '63', "Tchi Tchi"),
    ([8,7,8,7,8,7], '64', "Wei Tchi"),
]


class TestAllHexagramsLookup:
    """Test that all 64 hexagrams can be looked up correctly"""

    @pytest.mark.parametrize("line_values,expected_num,expected_name", ALL_HEXAGRAMS)
    def test_hexagram_lookup(self, line_values, expected_num, expected_name):
        """Test that each hexagram is identified correctly"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')

        # Set the line values and complete the hexagram
        hexagrams.hex1.lineValues = line_values.copy()
        hexagrams.currentLine = 6
        hexagrams.NewLine()

        # Verify correct identification
        assert hexagrams.hex1.number == expected_num, \
            f"Hexagram {expected_num} not identified correctly. " \
            f"Expected {expected_num}, got {hexagrams.hex1.number}"
        assert hexagrams.hex1.name == expected_name, \
            f"Hexagram {expected_num} name incorrect. " \
            f"Expected '{expected_name}', got '{hexagrams.hex1.name}'"

    def test_all_hexagrams_have_info_source(self):
        """Every hexagram should have an infoSource set"""
        for line_values, expected_num, _ in ALL_HEXAGRAMS:
            hexagrams = pyching_engine.Hexagrams(oracleType='coin')
            hexagrams.hex1.lineValues = line_values.copy()
            hexagrams.currentLine = 6
            hexagrams.NewLine()

            assert hexagrams.hex1.infoSource is not None, \
                f"Hexagram {expected_num} has no infoSource"
            assert f'in{expected_num}data()' in hexagrams.hex1.infoSource, \
                f"Hexagram {expected_num} infoSource incorrect: {hexagrams.hex1.infoSource}"


class TestHexagramLookupWithMovingLines:
    """Test hexagram lookup when moving lines (6 and 9) are present"""

    def test_all_moving_yang_still_identified_as_hexagram_1(self):
        """All moving yang (9s) should be identified as Hexagram 1"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.hex1.lineValues = [9, 9, 9, 9, 9, 9]
        hexagrams.currentLine = 6
        hexagrams.NewLine()

        assert hexagrams.hex1.number == '1', \
            f"All old yang should be Hexagram 1, got {hexagrams.hex1.number}"
        assert hexagrams.hex1.name == "Tch'ien", \
            f"Expected Tch'ien, got {hexagrams.hex1.name}"

    def test_all_moving_yin_still_identified_as_hexagram_2(self):
        """All moving yin (6s) should be identified as Hexagram 2"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.hex1.lineValues = [6, 6, 6, 6, 6, 6]
        hexagrams.currentLine = 6
        hexagrams.NewLine()

        assert hexagrams.hex1.number == '2', \
            f"All old yin should be Hexagram 2, got {hexagrams.hex1.number}"
        assert hexagrams.hex1.name == "Koun", \
            f"Expected Koun, got {hexagrams.hex1.name}"

    def test_mixed_moving_and_stable_lines_lookup(self):
        """Hexagrams with mix of moving and stable should still lookup correctly"""
        # Hexagram 1 with some moving lines: [9,7,9,7,9,7]
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.hex1.lineValues = [9, 7, 9, 7, 9, 7]
        hexagrams.currentLine = 6
        hexagrams.NewLine()

        # Should still be Hexagram 1 (all yang when stable)
        assert hexagrams.hex1.number == '1', \
            f"Mixed moving yang should be Hexagram 1, got {hexagrams.hex1.number}"

    @pytest.mark.parametrize("line_values,expected_num,expected_name", [
        # Hexagram 3 with moving lines
        ([9, 8, 8, 8, 7, 8], '3', "T'oun"),
        ([7, 6, 6, 6, 9, 8], '3', "T'oun"),
        # Hexagram 10 with moving lines
        ([9, 7, 6, 9, 7, 9], '10', "Li"),
        # Hexagram 63 with moving lines
        ([9, 6, 9, 6, 9, 6], '63', "Tchi Tchi"),
    ])
    def test_specific_hexagrams_with_moving_lines(self, line_values, expected_num, expected_name):
        """Test specific hexagrams with various moving line patterns"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.hex1.lineValues = line_values
        hexagrams.currentLine = 6
        hexagrams.NewLine()

        assert hexagrams.hex1.number == expected_num, \
            f"Expected hexagram {expected_num}, got {hexagrams.hex1.number}"
        assert hexagrams.hex1.name == expected_name, \
            f"Expected {expected_name}, got {hexagrams.hex1.name}"


class TestHexagramTransformations:
    """Test that moving lines create correct transformations"""

    def test_hexagram_1_to_2_all_moving(self):
        """All moving yang (Hex 1) should transform to all yin (Hex 2)"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.hex1.lineValues = [9, 9, 9, 9, 9, 9]
        hexagrams.currentLine = 6
        hexagrams.NewLine()

        assert hexagrams.hex1.number == '1'
        assert hexagrams.hex2.number == '2'
        assert hexagrams.hex2.lineValues == [8, 8, 8, 8, 8, 8]

    def test_hexagram_2_to_1_all_moving(self):
        """All moving yin (Hex 2) should transform to all yang (Hex 1)"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.hex1.lineValues = [6, 6, 6, 6, 6, 6]
        hexagrams.currentLine = 6
        hexagrams.NewLine()

        assert hexagrams.hex1.number == '2'
        assert hexagrams.hex2.number == '1'
        assert hexagrams.hex2.lineValues == [7, 7, 7, 7, 7, 7]

    def test_transformation_creates_valid_hexagram(self):
        """Any transformation should result in a valid hexagram"""
        # Test a few transformations
        test_cases = [
            [9, 7, 7, 7, 7, 7],  # Hex 1 with one moving line
            [6, 8, 8, 8, 8, 8],  # Hex 2 with one moving line
            [9, 6, 7, 8, 9, 6],  # Mixed moving lines
        ]

        for line_values in test_cases:
            hexagrams = pyching_engine.Hexagrams(oracleType='coin')
            hexagrams.hex1.lineValues = line_values
            hexagrams.currentLine = 6
            hexagrams.NewLine()

            # hex2 should be created and have a valid number
            if 6 in line_values or 9 in line_values:
                assert hexagrams.hex2.number != '', \
                    f"hex2 should exist for moving lines: {line_values}"
                assert hexagrams.hex2.number in [str(i) for i in range(1, 65)], \
                    f"hex2 number should be 1-64, got {hexagrams.hex2.number}"


class TestHexagramLookupEdgeCases:
    """Test edge cases in hexagram lookup"""

    def test_hexagram_without_completion_has_no_number(self):
        """Hexagram should not have number/name until all 6 lines are cast"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')
        hexagrams.hex1.lineValues = [7, 7, 7, 0, 0, 0]
        hexagrams.currentLine = 3

        # Don't call NewLine to complete it
        assert hexagrams.hex1.number == '', \
            "Incomplete hexagram should not have number"
        assert hexagrams.hex1.name == '', \
            "Incomplete hexagram should not have name"

    def test_no_duplicate_hexagram_numbers(self):
        """All 64 hexagrams should have unique numbers"""
        numbers = [num for _, num, _ in ALL_HEXAGRAMS]
        assert len(numbers) == 64, "Should have exactly 64 hexagrams"
        assert len(set(numbers)) == 64, "All hexagram numbers should be unique"
        assert set(numbers) == set(str(i) for i in range(1, 65)), \
            "Numbers should be 1-64"

    def test_no_duplicate_line_patterns(self):
        """All 64 hexagrams should have unique line patterns"""
        patterns = [tuple(lines) for lines, _, _ in ALL_HEXAGRAMS]
        assert len(patterns) == 64, "Should have exactly 64 patterns"
        assert len(set(patterns)) == 64, "All line patterns should be unique"


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
