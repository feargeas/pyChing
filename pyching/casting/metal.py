"""
Metal Element casting method - Traditional coin method with OS entropy.

Element: Metal (金)
Source: os.urandom() - raw system entropy bytes
Characteristics: Highest quality local randomness, cryptographically secure

This is the traditional three-coin method, using low-level OS entropy
for maximum randomness quality. Preserves the original pyChing algorithm.
"""

import os
from .base import CastingMethod, Element


class MetalMethod(CastingMethod):
    """
    Traditional I Ching coin method using OS entropy.

    Uses os.urandom() to generate cryptographically secure random bytes,
    which are then converted to three coin values (each 2 or 3).

    This method provides the highest quality randomness available locally
    without requiring external services.
    """

    @property
    def element(self) -> Element:
        return Element.METAL

    @property
    def name(self) -> str:
        return "Traditional Coins (Metal Element 金)"

    @property
    def description(self) -> str:
        return (
            "The traditional three-coin method using raw OS entropy. "
            "Each of three coins is assigned yin (2) or yang (3) based on "
            "cryptographically secure random bytes from the operating system. "
            "This method provides the highest quality local randomness."
        )

    @property
    def requires_network(self) -> bool:
        return False

    def cast_line(self) -> int:
        """
        Cast a line using three virtual coins with OS entropy.

        Uses os.urandom() to get 3 random bytes, converts each byte
        to a coin value (2 or 3) using bit masking.

        Returns:
            int: Line value (6, 7, 8, or 9)
        """
        # Get 3 random bytes from OS
        random_bytes = os.urandom(3)

        # Convert each byte to coin value (2 or 3)
        # Use bit masking: if low bit is 0 → 2 (yin), if 1 → 3 (yang)
        coins = [(byte & 1) + 2 for byte in random_bytes]

        self._last_oracle_values = coins
        return self._traditional_coin_to_line(coins)
