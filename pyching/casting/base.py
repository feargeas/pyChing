"""
Base classes for I Ching casting methods.

Defines the Element enum and CastingMethod abstract base class that
all casting implementations must follow.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional


class Element(Enum):
    """
    Five Elements of Chinese phenomenology (Wu Xing).

    Each element corresponds to a different casting method with
    distinct randomness characteristics.
    """
    WATER = "water"  # 水 - True RNG via RANDOM.ORG API
    WOOD = "wood"    # 木 - Standard PRNG (Mersenne Twister)
    FIRE = "fire"    # 火 - Cryptographic CSPRNG
    EARTH = "earth"  # 土 - Seeded/Deterministic
    METAL = "metal"  # 金 - OS Entropy (Traditional Coin)


class CastingMethod(ABC):
    """
    Abstract base class for all I Ching casting methods.

    Each method must produce line values 6, 7, 8, or 9 with traditional
    probabilities:
    - 6 (old yin): 12.5% (1/8) → transforms to 7 (yang)
    - 7 (yang): 37.5% (3/8) → stable
    - 8 (yin): 37.5% (3/8) → stable
    - 9 (old yang): 12.5% (1/8) → transforms to 8 (yin)

    These probabilities are achieved through the traditional three-coin method,
    where each coin has value 2 (yin) or 3 (yang), and the sum determines
    the line value.
    """

    def __init__(self):
        self._last_oracle_values: list[int] = []

    @property
    @abstractmethod
    def element(self) -> Element:
        """The element this method corresponds to."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name of this casting method."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Detailed description of this method."""
        pass

    @property
    @abstractmethod
    def requires_network(self) -> bool:
        """Whether this method requires network access."""
        pass

    @abstractmethod
    def cast_line(self) -> int:
        """
        Cast a single line.

        Returns:
            int: Line value (6, 7, 8, or 9)

        Raises:
            Exception: If casting fails (e.g., network error for Water method)
        """
        pass

    def get_oracle_values(self) -> list[int]:
        """
        Get the raw oracle values from the last cast.

        For three-coin methods, this returns the three coin values.
        For other methods, returns whatever raw values were used.

        Returns:
            list[int]: Raw values used to determine the line
        """
        return self._last_oracle_values.copy()

    def is_available(self) -> tuple[bool, Optional[str]]:
        """
        Check if this casting method is currently available.

        For most methods this is always True. For methods requiring
        external resources (like Water/RANDOM.ORG), this checks connectivity.

        Returns:
            tuple[bool, Optional[str]]: (available, error_message)
                If available is True, error_message is None.
                If available is False, error_message explains why.
        """
        return (True, None)

    def _traditional_coin_to_line(self, coins: list[int]) -> int:
        """
        Convert three coin values to a line value.

        Traditional mapping:
        - Sum of 6 (2+2+2) = old yin (moving)
        - Sum of 7 (2+2+3) = yang (stable)
        - Sum of 8 (2+3+3) = yin (stable)
        - Sum of 9 (3+3+3) = old yang (moving)

        Args:
            coins: List of three coin values (each 2 or 3)

        Returns:
            int: Line value (6, 7, 8, or 9)

        Raises:
            ValueError: If coins list is invalid
        """
        if len(coins) != 3:
            raise ValueError("Must provide exactly 3 coin values")
        if not all(c in [2, 3] for c in coins):
            raise ValueError("Each coin must be 2 (yin) or 3 (yang)")

        return sum(coins)

    def cast_full_hexagram(self) -> list[int]:
        """
        Cast all six lines for a complete hexagram.

        Returns:
            list[int]: Six line values (from bottom to top)
        """
        return [self.cast_line() for _ in range(6)]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(element={self.element.value})"
