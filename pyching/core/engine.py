"""
HexagramEngine - integrates casting methods with data access layer.

This engine class ties together:
- Phase 2: Five Elements casting methods
- Phase 3: Multi-source data access layer
- Modern dataclasses (Hexagram, Reading)

Preserves the original pyChing casting algorithm exactly.
"""

from typing import Optional, List, Tuple

from pyching.casting.base import CastingMethod, Element
from pyching.casting.registry import CastingMethodRegistry
from pyching.core.hexagram import Hexagram
from pyching.core.reading import Reading


class HexagramEngine:
    """
    Core engine for casting I Ching readings.

    Integrates Five Elements casting methods with multi-source interpretation data.
    Preserves the original pyChing algorithm while adding modern features.
    """

    def __init__(self, registry: Optional[CastingMethodRegistry] = None):
        """
        Initialize engine.

        Args:
            registry: CastingMethodRegistry instance (default: creates new one with all methods)
        """
        if registry is None:
            # Create default registry with all five element methods
            from pyching.casting import (WoodMethod, MetalMethod, FireMethod,
                                        EarthMethod, AirMethod)

            registry = CastingMethodRegistry()
            registry.register(WoodMethod())  # Default/original method
            registry.register(MetalMethod())
            registry.register(FireMethod())
            registry.register(EarthMethod())
            registry.register(AirMethod())

        self.registry = registry

    def cast_reading(self,
                    method: Element | CastingMethod | str = Element.WOOD,
                    question: str = "",
                    source: str = "canonical",
                    seed: Optional[str] = None) -> Reading:
        """
        Cast a complete I Ching reading.

        This is the main interface for casting a reading. It handles:
        1. Selecting the casting method
        2. Casting all 6 lines
        3. Creating primary hexagram
        4. Creating relating hexagram (if moving lines)
        5. Packaging into Reading object

        Args:
            method: Casting method (Element enum, CastingMethod instance, or element name string)
            question: Question text (optional)
            source: Interpretation source ID (default: "canonical")
            seed: Seed string for Earth method (deterministic readings)

        Returns:
            Reading instance with primary and (if applicable) relating hexagrams

        Example:
            >>> engine = HexagramEngine()
            >>> reading = engine.cast_reading(Element.WOOD, "What is my purpose?")
            >>> print(reading.primary.english_name)
            >>> if reading.relating:
            ...     print(f"Becomes: {reading.relating.english_name}")
        """
        # Get the casting method instance
        casting_method = self._get_method(method, seed)

        # Cast all 6 lines
        lines, oracle_values = self._cast_all_lines(casting_method)

        # Create primary hexagram
        primary = Hexagram.from_lines(lines, source=source)

        # Create relating hexagram if there are moving lines
        relating = None
        if primary.has_moving_lines():
            relating_lines = self._transform_moving_lines(lines)
            relating = Hexagram.from_lines(relating_lines, source=source)

        # Get method name for recording
        method_name = self._get_method_name(method)

        # Create and return reading
        return Reading.from_hexagrams(
            primary=primary,
            relating=relating,
            question=question,
            method=method_name,
            oracle_values=oracle_values
        )

    def cast_hexagram(self,
                     method: Element | CastingMethod | str = Element.WOOD,
                     source: str = "canonical",
                     seed: Optional[str] = None) -> Tuple[Hexagram, List[List[int]]]:
        """
        Cast a single hexagram (without creating relating hexagram).

        Useful for testing or when you only need the primary hexagram.

        Args:
            method: Casting method
            source: Interpretation source ID
            seed: Seed string for Earth method

        Returns:
            Tuple of (Hexagram, oracle_values)
        """
        casting_method = self._get_method(method, seed)
        lines, oracle_values = self._cast_all_lines(casting_method)
        hexagram = Hexagram.from_lines(lines, source=source)

        return hexagram, oracle_values

    def _get_method(self,
                   method: Element | CastingMethod | str,
                   seed: Optional[str] = None) -> CastingMethod:
        """
        Get casting method instance from various input types.

        Args:
            method: Element enum, CastingMethod instance, or element name string
            seed: Seed string for Earth method

        Returns:
            CastingMethod instance

        Raises:
            ValueError: If method not found or invalid
        """
        # If already a CastingMethod instance, use it directly
        if isinstance(method, CastingMethod):
            # Set seed if Earth method
            if hasattr(method, 'set_seed') and seed:
                method.set_seed(seed)
            return method

        # Convert string to Element enum
        if isinstance(method, str):
            try:
                method = Element(method.lower())
            except ValueError:
                raise ValueError(f"Invalid method name: {method}. "
                               f"Valid options: {[e.value for e in Element]}")

        # Get method from registry
        casting_method = self.registry.get(method)
        if casting_method is None:
            raise ValueError(f"Method {method} not found in registry")

        # Set seed if Earth method
        if hasattr(casting_method, 'set_seed') and seed:
            casting_method.set_seed(seed)

        return casting_method

    def _get_method_name(self, method: Element | CastingMethod | str) -> str:
        """Get string name for method (for recording in Reading)."""
        if isinstance(method, str):
            return method.lower()
        elif isinstance(method, Element):
            return method.value
        elif isinstance(method, CastingMethod):
            return method.element.value
        else:
            return "unknown"

    def _cast_all_lines(self, casting_method: CastingMethod) -> Tuple[List[int], List[List[int]]]:
        """
        Cast all 6 lines using specified method.

        This preserves the original pyChing algorithm:
        - Cast from bottom to top (line 1 to line 6)
        - Each line gets its own oracle values
        - Line value is sum of oracle values (coin method)

        Args:
            casting_method: CastingMethod instance to use

        Returns:
            Tuple of (line_values, oracle_values)
            - line_values: List of 6 line values (6, 7, 8, or 9)
            - oracle_values: List of 6 lists of oracle values (for recording)
        """
        lines = []
        oracle_values_all = []

        for _ in range(6):
            line_value = casting_method.cast_line()
            lines.append(line_value)

            # Capture oracle values if available
            if hasattr(casting_method, '_last_oracle_values'):
                oracle_values_all.append(casting_method._last_oracle_values.copy())
            else:
                oracle_values_all.append([])

        return lines, oracle_values_all

    def _transform_moving_lines(self, lines: List[int]) -> List[int]:
        """
        Transform moving lines for relating hexagram.

        Moving lines transform as follows:
        - 6 (old yin) → 7 (yang)
        - 9 (old yang) → 8 (yin)
        - 7 (yang) → 7 (unchanged)
        - 8 (yin) → 8 (unchanged)

        This preserves the original algorithm from pyching_engine.py lines 247-250.

        Args:
            lines: Original line values with moving lines

        Returns:
            Transformed line values for relating hexagram
        """
        transformed = []
        for line in lines:
            if line == 6:  # old yin becomes yang
                transformed.append(7)
            elif line == 9:  # old yang becomes yin
                transformed.append(8)
            else:  # stable lines unchanged
                transformed.append(line)

        return transformed

    def get_available_methods(self) -> List[str]:
        """
        Get list of available casting method names.

        Returns:
            List of element names (e.g., ['wood', 'metal', 'fire', 'earth', 'air'])
        """
        methods = self.registry.get_available_methods()
        return [method.element.value for method in methods]

    def check_method_available(self, method: Element | str) -> Tuple[bool, Optional[str]]:
        """
        Check if a method is available and usable.

        Particularly useful for Air method which requires network.

        Args:
            method: Element enum or element name string

        Returns:
            Tuple of (is_available, error_message)
            - is_available: True if method can be used
            - error_message: None if available, error string if not

        Example:
            >>> engine = HexagramEngine()
            >>> available, error = engine.check_method_available(Element.AIR)
            >>> if not available:
            ...     print(f"Air method unavailable: {error}")
        """
        # Convert string to Element
        if isinstance(method, str):
            try:
                method = Element(method.lower())
            except ValueError:
                return False, f"Invalid method name: {method}"

        # Get method from registry
        casting_method = self.registry.get(method)
        if casting_method is None:
            return False, f"Method {method.value} not registered"

        # Check if method is available
        if hasattr(casting_method, 'is_available'):
            return casting_method.is_available()

        # No availability check, assume available
        return True, None
