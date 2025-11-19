"""
Wood Element casting method - Standard PRNG (Mersenne Twister).

Element: Wood (木)
Source: random module - fast, general-purpose PRNG
Characteristics: Fast, deterministic but high-quality distribution

Uses Python's default random number generator, which is based on the
Mersenne Twister algorithm. This was the algorithm used in the original
pyChing implementation.
"""

import random
from .base import CastingMethod, Element


class WoodMethod(CastingMethod):
    """
    Standard PRNG method using Mersenne Twister.

    Uses Python's random module (Mersenne Twister algorithm) for
    fast, high-quality pseudo-random number generation.

    This matches the original pyChing implementation and is suitable
    for divination purposes where cryptographic security is not required.
    """

    @property
    def element(self) -> Element:
        return Element.WOOD

    @property
    def name(self) -> str:
        return "Mersenne Twister (Wood Element 木)"

    @property
    def description(self) -> str:
        return (
            "Uses Python's standard random module (Mersenne Twister algorithm). "
            "Fast, general-purpose random number generation suitable for "
            "divination purposes. Deterministic but high-quality distribution. "
            "This was the method used in the original pyChing implementation."
        )

    @property
    def requires_network(self) -> bool:
        return False

    def cast_line(self) -> int:
        """
        Cast a line using Mersenne Twister PRNG.

        Uses random.choice() for each of three coins, matching
        the original pyChing algorithm exactly.

        Returns:
            int: Line value (6, 7, 8, or 9)
        """
        # Use random.choice for each coin (matches original pyChing)
        coins = [random.choice([2, 3]) for _ in range(3)]

        self._last_oracle_values = coins
        return self._traditional_coin_to_line(coins)
