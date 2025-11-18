"""
Air Element casting method - True RNG via RANDOM.ORG API.

Element: Air (風/氣)
Source: RANDOM.ORG - atmospheric noise-based true RNG
Characteristics: True physical randomness, requires internet

Uses physical atmospheric noise measurements to generate
true random numbers. This is the only method that provides
genuine physical randomness rather than algorithmic pseudo-randomness.
"""

from typing import Optional
from .base import CastingMethod, Element


class AirMethod(CastingMethod):
    """
    True random number generation via RANDOM.ORG API.

    Uses RANDOM.ORG's true random number generator, which is based
    on atmospheric noise measurements. Provides genuine physical
    randomness rather than algorithmic pseudo-randomness.

    Requires internet connection. Falls back gracefully if unavailable.
    """

    API_URL = "https://www.random.org/integers/"
    TIMEOUT = 5  # seconds

    @property
    def element(self) -> Element:
        return Element.AIR

    @property
    def name(self) -> str:
        return "True RNG via RANDOM.ORG (Air Element 風/氣)"

    @property
    def description(self) -> str:
        return (
            "Uses RANDOM.ORG's true random number generator, which is based "
            "on atmospheric noise measurements. Provides genuine physical "
            "randomness rather than algorithmic pseudo-randomness. "
            "Requires internet connection."
        )

    @property
    def requires_network(self) -> bool:
        return True

    def is_available(self) -> tuple[bool, Optional[str]]:
        """
        Check if RANDOM.ORG API is accessible.

        Returns:
            tuple[bool, Optional[str]]: (available, error_message)
        """
        try:
            import requests
        except ImportError:
            return (
                False,
                "requests library not installed. Install with: pip install requests"
            )

        try:
            # Simple connectivity check
            import requests
            response = requests.head(self.API_URL, timeout=2)
            return (True, None)
        except requests.RequestException as e:
            return (False, f"Cannot reach RANDOM.ORG: {str(e)}")

    def cast_line(self) -> int:
        """
        Cast a line using RANDOM.ORG API.

        Makes an HTTP request to RANDOM.ORG to get three truly random
        numbers (each 2 or 3), then converts to line value.

        Returns:
            int: Line value (6, 7, 8, or 9)

        Raises:
            ImportError: If requests library is not installed
            ConnectionError: If API is unavailable
            ValueError: If API response is invalid
        """
        try:
            import requests
        except ImportError:
            raise ImportError(
                "requests library required for Air method. "
                "Install with: pip install requests"
            )

        try:
            # Request 3 random integers (2 or 3)
            params = {
                'num': 3,          # 3 coins
                'min': 2,          # minimum value (yin)
                'max': 3,          # maximum value (yang)
                'col': 1,          # single column
                'base': 10,        # decimal
                'format': 'plain', # plain text
                'rnd': 'new'       # new randomization
            }

            response = requests.get(
                self.API_URL,
                params=params,
                timeout=self.TIMEOUT
            )
            response.raise_for_status()

            # Parse response (three integers, one per line)
            lines = response.text.strip().split('\n')
            coins = [int(line.strip()) for line in lines]

            if len(coins) != 3:
                raise ValueError(f"Expected 3 values, got {len(coins)}")

            if not all(c in [2, 3] for c in coins):
                raise ValueError(f"Invalid coin values: {coins}")

            self._last_oracle_values = coins
            return self._traditional_coin_to_line(coins)

        except requests.RequestException as e:
            raise ConnectionError(
                f"Failed to get random numbers from RANDOM.ORG: {str(e)}. "
                f"Consider using Fire method (cryptographic) as alternative."
            ) from e
        except (ValueError, IndexError) as e:
            raise ValueError(
                f"Invalid response from RANDOM.ORG: {str(e)}"
            ) from e
