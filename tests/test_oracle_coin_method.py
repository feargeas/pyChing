"""
Test Oracle Coin Method Logic
==============================

These tests ensure the authentic I Ching 3-coin oracle method is preserved.

The traditional 3-coin method:
- Each coin has two sides: heads (value 3) and tails (value 2)
- Three coins are tossed
- The sum of the three coins determines the line value:
  - 6 (2+2+2) = old yin (moving yin) → transforms to yang (7)
  - 7 (2+2+3, 2+3+2, 3+2+2) = yang (stable)
  - 8 (2+3+3, 3+2+3, 3+3+2) = yin (stable)
  - 9 (3+3+3) = old yang (moving yang) → transforms to yin (8)

THESE TESTS MUST PASS AFTER PYTHON 3 MIGRATION.
"""

import sys
from pathlib import Path

# Add parent directory to path to import pyching_engine
sys.path.insert(0, str(Path(__file__).parent.parent))

import pyching_engine


class TestOracleCoinValues:
    """Test that coin oracle produces valid line values"""

    def test_coin_values_are_valid(self):
        """Each coin toss must produce either 2 or 3"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')

        # Generate many lines to test randomness produces valid values
        for _ in range(100):
            hexagrams.currentLine = 0  # Reset
            hexagrams.hex1.lineValues = [0, 0, 0, 0, 0, 0]
            hexagrams.NewLine()

            # Check that oracle values are 2 or 3
            assert len(hexagrams.currentOracleValues) == 3, \
                "Must toss exactly 3 coins"
            for coin_value in hexagrams.currentOracleValues:
                assert coin_value in [2, 3], \
                    f"Each coin must be 2 or 3, got {coin_value}"

    def test_line_values_are_valid(self):
        """Line values must be 6, 7, 8, or 9 (sum of three coins)"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')

        # Generate many lines to test all possible values appear
        line_values_seen = set()
        for _ in range(1000):
            hexagrams.currentLine = 0  # Reset
            hexagrams.hex1.lineValues = [0, 0, 0, 0, 0, 0]
            hexagrams.NewLine()

            line_value = hexagrams.hex1.lineValues[0]
            assert line_value in [6, 7, 8, 9], \
                f"Line value must be 6, 7, 8, or 9, got {line_value}"
            line_values_seen.add(line_value)

        # Statistically, with 1000 tosses, we should see all four values
        # (though this could theoretically fail with extremely bad luck)
        assert len(line_values_seen) >= 3, \
            f"Should see at least 3 different line values in 1000 tosses, saw {line_values_seen}"

    def test_line_value_sums_correctly(self):
        """Line value must equal sum of three coin values"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')

        for _ in range(100):
            hexagrams.currentLine = 0
            hexagrams.hex1.lineValues = [0, 0, 0, 0, 0, 0]
            hexagrams.NewLine()

            expected_sum = sum(hexagrams.currentOracleValues)
            actual_value = hexagrams.hex1.lineValues[0]

            assert actual_value == expected_sum, \
                f"Line value {actual_value} must equal sum of coins {hexagrams.currentOracleValues} = {expected_sum}"


class TestOracleProbabilities:
    """Test that coin oracle produces theoretically correct probabilities"""

    def test_line_value_frequencies(self):
        """
        Test that line values appear with correct relative frequencies.

        Theoretical probabilities for 3-coin method:
        - 6 (2+2+2): 1/8 = 12.5%
        - 7 (one 3, two 2s): 3/8 = 37.5%
        - 8 (two 3s, one 2): 3/8 = 37.5%
        - 9 (3+3+3): 1/8 = 12.5%
        """
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')

        # Generate a large sample
        sample_size = 10000
        counts = {6: 0, 7: 0, 8: 0, 9: 0}

        for _ in range(sample_size):
            hexagrams.currentLine = 0
            hexagrams.hex1.lineValues = [0, 0, 0, 0, 0, 0]
            hexagrams.NewLine()
            counts[hexagrams.hex1.lineValues[0]] += 1

        # Check frequencies are approximately correct (within reasonable tolerance)
        # Using loose bounds because this is probabilistic
        freq_6 = counts[6] / sample_size
        freq_7 = counts[7] / sample_size
        freq_8 = counts[8] / sample_size
        freq_9 = counts[9] / sample_size

        # 6 and 9 should each be around 12.5% (1/8)
        assert 0.08 < freq_6 < 0.18, \
            f"Frequency of 6 should be ~12.5%, got {freq_6*100:.1f}%"
        assert 0.08 < freq_9 < 0.18, \
            f"Frequency of 9 should be ~12.5%, got {freq_9*100:.1f}%"

        # 7 and 8 should each be around 37.5% (3/8)
        assert 0.32 < freq_7 < 0.43, \
            f"Frequency of 7 should be ~37.5%, got {freq_7*100:.1f}%"
        assert 0.32 < freq_8 < 0.43, \
            f"Frequency of 8 should be ~37.5%, got {freq_8*100:.1f}%"


class TestHexagramCompletion:
    """Test that hexagrams are properly completed after 6 lines"""

    def test_six_lines_complete_hexagram(self):
        """After 6 lines, hexagram should be complete with name and number"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')

        # Cast all 6 lines
        for i in range(6):
            assert hexagrams.currentLine == i, \
                f"Current line should be {i}, got {hexagrams.currentLine}"
            hexagrams.NewLine()

        # After 6 lines, hex1 should be complete
        assert hexagrams.currentLine == 6, "Should have 6 lines"
        assert hexagrams.hex1.number != '', "Hex1 should have a number"
        assert hexagrams.hex1.name != '', "Hex1 should have a name"
        assert hexagrams.hex1.infoSource is not None, "Hex1 should have infoSource"

    def test_no_moving_lines_means_no_hex2(self):
        """If no moving lines (6 or 9), hex2 should be empty"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')

        # Manually set stable lines (only 7 and 8, no 6 or 9)
        hexagrams.hex1.lineValues = [7, 7, 7, 7, 7, 7]
        hexagrams.currentLine = 6
        hexagrams.NewLine()

        # hex2 should be empty (no transformation)
        assert hexagrams.hex2.number == '', "Hex2 should be empty (no moving lines)"
        assert hexagrams.hex2.name == '', "Hex2 should be empty (no moving lines)"


class TestMovingLines:
    """Test that moving lines transform correctly"""

    def test_old_yin_transforms_to_yang(self):
        """Old yin (6) should transform to yang (7) in hex2"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')

        # Set hex1 with a 6 (old yin) in first position
        hexagrams.hex1.lineValues = [6, 7, 7, 7, 7, 7]
        hexagrams.currentLine = 6
        hexagrams.NewLine()

        # hex2 should have 7 (yang) in first position
        assert hexagrams.hex2.lineValues[0] == 7, \
            "Old yin (6) should transform to yang (7)"

    def test_old_yang_transforms_to_yin(self):
        """Old yang (9) should transform to yin (8) in hex2"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')

        # Set hex1 with a 9 (old yang) in first position
        hexagrams.hex1.lineValues = [9, 7, 7, 7, 7, 7]
        hexagrams.currentLine = 6
        hexagrams.NewLine()

        # hex2 should have 8 (yin) in first position
        assert hexagrams.hex2.lineValues[0] == 8, \
            "Old yang (9) should transform to yin (8)"

    def test_stable_lines_dont_transform(self):
        """Stable lines (7 and 8) should stay the same in hex2"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')

        # Set hex1 with stable lines and one moving line
        hexagrams.hex1.lineValues = [7, 8, 7, 8, 6, 7]
        hexagrams.currentLine = 6
        hexagrams.NewLine()

        # Check stable lines remain unchanged
        assert hexagrams.hex2.lineValues[0] == 7, "Yang (7) should stay yang"
        assert hexagrams.hex2.lineValues[1] == 8, "Yin (8) should stay yin"
        assert hexagrams.hex2.lineValues[2] == 7, "Yang (7) should stay yang"
        assert hexagrams.hex2.lineValues[3] == 8, "Yin (8) should stay yin"
        # Check moving line transformed
        assert hexagrams.hex2.lineValues[4] == 7, "Old yin (6) should become yang (7)"
        assert hexagrams.hex2.lineValues[5] == 7, "Yang (7) should stay yang"

    def test_all_moving_lines_transform(self):
        """All moving lines should transform in hex2"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')

        # Set hex1 with all moving lines
        hexagrams.hex1.lineValues = [6, 9, 6, 9, 6, 9]
        hexagrams.currentLine = 6
        hexagrams.NewLine()

        # All should transform: 6→7, 9→8
        expected = [7, 8, 7, 8, 7, 8]
        assert hexagrams.hex2.lineValues == expected, \
            f"All moving lines should transform: 6→7, 9→8. Got {hexagrams.hex2.lineValues}"


class TestHexagramLookup:
    """Test that hexagrams are correctly identified"""

    def test_hexagram_1_tch_ien(self):
        """Hexagram 1 (all yang) should be identified correctly"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')

        hexagrams.hex1.lineValues = [7, 7, 7, 7, 7, 7]
        hexagrams.currentLine = 6
        hexagrams.NewLine()

        assert hexagrams.hex1.number == '1', \
            f"All yang should be Hexagram 1, got {hexagrams.hex1.number}"
        assert hexagrams.hex1.name == "Tch'ien", \
            f"Hexagram 1 should be Tch'ien, got {hexagrams.hex1.name}"

    def test_hexagram_2_koun(self):
        """Hexagram 2 (all yin) should be identified correctly"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')

        hexagrams.hex1.lineValues = [8, 8, 8, 8, 8, 8]
        hexagrams.currentLine = 6
        hexagrams.NewLine()

        assert hexagrams.hex1.number == '2', \
            f"All yin should be Hexagram 2, got {hexagrams.hex1.number}"
        assert hexagrams.hex1.name == "Koun", \
            f"Hexagram 2 should be Koun, got {hexagrams.hex1.name}"

    def test_moving_lines_use_stable_form_for_lookup(self):
        """Hexagram lookup should use stable line values (6→8, 9→7)"""
        hexagrams = pyching_engine.Hexagrams(oracleType='coin')

        # Hexagram 1 with all moving yang (9s)
        hexagrams.hex1.lineValues = [9, 9, 9, 9, 9, 9]
        hexagrams.currentLine = 6
        hexagrams.NewLine()

        # Should still be identified as Hexagram 1 (all yang)
        assert hexagrams.hex1.number == '1', \
            f"All old yang should be Hexagram 1, got {hexagrams.hex1.number}"

        # And should transform to Hexagram 2 (all yin)
        assert hexagrams.hex2.number == '2', \
            f"All old yang should transform to Hexagram 2, got {hexagrams.hex2.number}"


if __name__ == '__main__':
    # Simple test runner for manual testing
    import pytest
    pytest.main([__file__, '-v'])
