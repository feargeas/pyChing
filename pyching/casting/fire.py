"""
Fire Element casting method - Cryptographically secure PRNG.

Element: Fire (火)
Source: secrets module - CSPRNG using OS entropy pool
Characteristics: Cryptographically secure, unpredictable

Uses Python's secrets module for cryptographically strong random
number generation, suitable for security-sensitive applications.
Provides the highest quality randomness available locally.
"""

import secrets
from .base import CastingMethod, Element


class FireMethod(CastingMethod):
    """
    Cryptographically secure RNG method.

    Uses Python's secrets module for cryptographically strong random
    number generation. Draws from the OS entropy pool, providing
    unpredictable, security-grade randomness.

    While cryptographic security is not strictly necessary for divination,
    this method ensures the absolute highest quality local randomness.
    """

    @property
    def element(self) -> Element:
        return Element.FIRE

    @property
    def name(self) -> str:
        return "Cryptographic CSPRNG (Fire Element 火)"

    @property
    def description(self) -> str:
        return (
            "Uses Python's secrets module for cryptographically secure "
            "random number generation. Draws from the OS entropy pool, "
            "providing the highest quality randomness available locally. "
            "Unpredictable and suitable for security-sensitive applications."
        )

    @property
    def requires_network(self) -> bool:
        return False

    def cast_line(self) -> int:
        """
        Cast a line using cryptographically secure RNG.

        Uses secrets.choice() for each coin, providing cryptographically
        strong random selection.

        Returns:
            int: Line value (6, 7, 8, or 9)
        """
        # Use secrets.choice for cryptographically secure selection
        coins = [secrets.choice([2, 3]) for _ in range(3)]

        self._last_oracle_values = coins
        return self._traditional_coin_to_line(coins)
