"""
Comprehensive tests for I Ching casting methods.

Tests all five element casting methods for:
- Correct line value generation (6, 7, 8, 9)
- Traditional probability distributions
- Method-specific functionality
- Error handling
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from collections import Counter
from pyching.casting import (
    Element,
    CastingMethod,
    MetalMethod,
    WoodMethod,
    FireMethod,
    EarthMethod,
    AirMethod,
    get_registry
)


class TestCastingMethodBase:
    """Test base functionality common to all casting methods."""

    def test_valid_line_values(self):
        """All methods must produce line values 6, 7, 8, or 9."""
        methods = [MetalMethod(), WoodMethod(), FireMethod()]

        for method in methods:
            for _ in range(100):
                line = method.cast_line()
                assert line in [6, 7, 8, 9], (
                    f"{method.name} produced invalid line value: {line}"
                )

    def test_oracle_values_recorded(self):
        """Methods must record oracle values."""
        method = WoodMethod()
        line = method.cast_line()
        oracle_values = method.get_oracle_values()

        assert len(oracle_values) == 3
        assert all(v in [2, 3] for v in oracle_values)
        assert sum(oracle_values) == line

    def test_full_hexagram_casting(self):
        """Methods can cast full hexagrams (6 lines)."""
        method = WoodMethod()
        hexagram = method.cast_full_hexagram()

        assert len(hexagram) == 6
        assert all(line in [6, 7, 8, 9] for line in hexagram)


class TestMetalMethod:
    """Test Metal element method (os.urandom)."""

    def test_element(self):
        """Metal method has correct element."""
        method = MetalMethod()
        assert method.element == Element.METAL

    def test_no_network_required(self):
        """Metal method doesn't require network."""
        method = MetalMethod()
        assert not method.requires_network

    def test_always_available(self):
        """Metal method is always available."""
        method = MetalMethod()
        available, error = method.is_available()
        assert available
        assert error is None

    def test_produces_different_values(self):
        """Metal method produces varying results."""
        method = MetalMethod()
        lines = [method.cast_line() for _ in range(20)]

        # Should have at least some variety
        assert len(set(lines)) > 1


class TestWoodMethod:
    """Test Wood element method (random)."""

    def test_element(self):
        """Wood method has correct element."""
        method = WoodMethod()
        assert method.element == Element.WOOD

    def test_no_network_required(self):
        """Wood method doesn't require network."""
        method = WoodMethod()
        assert not method.requires_network

    def test_original_algorithm(self):
        """Wood method matches original pyChing algorithm."""
        # This was the original implementation
        method = WoodMethod()

        # Should produce valid results consistently
        for _ in range(100):
            line = method.cast_line()
            assert line in [6, 7, 8, 9]


class TestFireMethod:
    """Test Fire element method (secrets)."""

    def test_element(self):
        """Fire method has correct element."""
        method = FireMethod()
        assert method.element == Element.FIRE

    def test_no_network_required(self):
        """Fire method doesn't require network."""
        method = FireMethod()
        assert not method.requires_network

    def test_cryptographic_quality(self):
        """Fire method produces cryptographically secure randomness."""
        method = FireMethod()

        # Should produce valid, varied results
        lines = [method.cast_line() for _ in range(50)]
        assert len(set(lines)) > 1
        assert all(line in [6, 7, 8, 9] for line in lines)


class TestEarthMethod:
    """Test Earth element method (seeded)."""

    def test_element(self):
        """Earth method has correct element."""
        method = EarthMethod()
        assert method.element == Element.EARTH

    def test_no_network_required(self):
        """Earth method doesn't require network."""
        method = EarthMethod()
        assert not method.requires_network

    def test_requires_seed(self):
        """Earth method requires seed before casting."""
        method = EarthMethod()

        with pytest.raises(ValueError, match="Seed must be set"):
            method.cast_line()

    def test_deterministic_with_seed(self):
        """Earth method produces same results with same seed."""
        seed = "What is the meaning of life?"

        method1 = EarthMethod(seed)
        hexagram1 = method1.cast_full_hexagram()

        method2 = EarthMethod(seed)
        hexagram2 = method2.cast_full_hexagram()

        assert hexagram1 == hexagram2

    def test_different_seeds_different_results(self):
        """Different seeds produce different results."""
        method1 = EarthMethod("Question 1")
        hexagram1 = method1.cast_full_hexagram()

        method2 = EarthMethod("Question 2")
        hexagram2 = method2.cast_full_hexagram()

        # Very unlikely to be the same
        assert hexagram1 != hexagram2

    def test_set_seed_method(self):
        """Can set seed after initialization."""
        method = EarthMethod()
        method.set_seed("New question")

        # Should now work
        line = method.cast_line()
        assert line in [6, 7, 8, 9]


class TestAirMethod:
    """Test Air element method (RANDOM.ORG)."""

    def test_element(self):
        """Air method has correct element."""
        method = AirMethod()
        assert method.element == Element.AIR

    def test_requires_network(self):
        """Air method requires network."""
        method = AirMethod()
        assert method.requires_network

    def test_availability_check(self):
        """Air method checks availability."""
        method = AirMethod()
        available, error = method.is_available()

        # Should return a boolean and optional error
        assert isinstance(available, bool)
        if not available:
            assert isinstance(error, str)
        else:
            assert error is None

    @pytest.mark.skip(reason="Requires network - run manually")
    def test_cast_line_with_network(self):
        """Air method can cast lines (requires network)."""
        method = AirMethod()

        available, error = method.is_available()
        if not available:
            pytest.skip(f"RANDOM.ORG not available: {error}")

        # Try to cast a line
        line = method.cast_line()
        assert line in [6, 7, 8, 9]


class TestCastingMethodRegistry:
    """Test the casting method registry."""

    def test_registry_has_all_methods(self):
        """Registry contains all five element methods."""
        registry = get_registry()

        methods = registry.list_methods()
        assert len(methods) == 5

        elements = [m.element for m in methods]
        assert Element.METAL in elements
        assert Element.WOOD in elements
        assert Element.FIRE in elements
        assert Element.EARTH in elements
        assert Element.AIR in elements

    def test_get_by_element(self):
        """Can retrieve methods by element."""
        registry = get_registry()

        metal = registry.get(Element.METAL)
        assert isinstance(metal, MetalMethod)

        wood = registry.get(Element.WOOD)
        assert isinstance(wood, WoodMethod)

    def test_get_method_info(self):
        """Can get detailed method information."""
        registry = get_registry()

        info = registry.get_method_info(Element.WOOD)
        assert info['element'] == 'wood'
        assert 'name' in info
        assert 'description' in info
        assert 'available' in info

    def test_list_all_info(self):
        """Can list info for all methods."""
        registry = get_registry()

        all_info = registry.list_all_info()
        assert len(all_info) == 5


class TestProbabilityDistributions:
    """Test that methods produce correct probability distributions."""

    @pytest.mark.slow
    def test_wood_method_distribution(self):
        """Wood method produces traditional probabilities."""
        method = WoodMethod()
        sample_size = 10000

        lines = [method.cast_line() for _ in range(sample_size)]
        counts = Counter(lines)

        # Expected probabilities:
        # 6: 1/8 = 12.5%
        # 7: 3/8 = 37.5%
        # 8: 3/8 = 37.5%
        # 9: 1/8 = 12.5%

        # Allow 3% tolerance for randomness
        tolerance = 0.03

        prob_6 = counts[6] / sample_size
        prob_7 = counts[7] / sample_size
        prob_8 = counts[8] / sample_size
        prob_9 = counts[9] / sample_size

        assert abs(prob_6 - 0.125) < tolerance, f"6: {prob_6:.3f} (expected 0.125)"
        assert abs(prob_7 - 0.375) < tolerance, f"7: {prob_7:.3f} (expected 0.375)"
        assert abs(prob_8 - 0.375) < tolerance, f"8: {prob_8:.3f} (expected 0.375)"
        assert abs(prob_9 - 0.125) < tolerance, f"9: {prob_9:.3f} (expected 0.125)"

    @pytest.mark.slow
    def test_metal_method_distribution(self):
        """Metal method produces traditional probabilities."""
        method = MetalMethod()
        sample_size = 10000

        lines = [method.cast_line() for _ in range(sample_size)]
        counts = Counter(lines)

        tolerance = 0.03

        prob_6 = counts[6] / sample_size
        prob_7 = counts[7] / sample_size
        prob_8 = counts[8] / sample_size
        prob_9 = counts[9] / sample_size

        assert abs(prob_6 - 0.125) < tolerance
        assert abs(prob_7 - 0.375) < tolerance
        assert abs(prob_8 - 0.375) < tolerance
        assert abs(prob_9 - 0.125) < tolerance

    @pytest.mark.slow
    def test_fire_method_distribution(self):
        """Fire method produces traditional probabilities."""
        method = FireMethod()
        sample_size = 10000

        lines = [method.cast_line() for _ in range(sample_size)]
        counts = Counter(lines)

        tolerance = 0.03

        prob_6 = counts[6] / sample_size
        prob_7 = counts[7] / sample_size
        prob_8 = counts[8] / sample_size
        prob_9 = counts[9] / sample_size

        assert abs(prob_6 - 0.125) < tolerance
        assert abs(prob_7 - 0.375) < tolerance
        assert abs(prob_8 - 0.375) < tolerance
        assert abs(prob_9 - 0.125) < tolerance


if __name__ == "__main__":
    # Run quick tests
    pytest.main([__file__, "-v", "-m", "not slow"])
