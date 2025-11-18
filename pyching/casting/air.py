"""
Air Element casting method - True RNG via RANDOM.ORG API.

Element: Air (風/氣)
Source: RANDOM.ORG - atmospheric noise-based true RNG
Characteristics: True physical randomness, requires internet

Uses physical atmospheric noise measurements to generate
true random numbers. This is the only method that provides
genuine physical randomness rather than algorithmic pseudo-randomness.

CONFIGURATION:
To use this method, you need a free API key from RANDOM.ORG:
1. Visit https://api.random.org/dashboard
2. Create an account or log in
3. Choose "Developer" account type to get API access
4. Navigate to API Keys section and generate a key
5. Save your API key to: ~/.pyching/random_org_api_key
   (Just the key on a single line, nothing else)

Without an API key, this method will not work. Use Fire method instead
for high-quality cryptographic randomness.
"""

import os
from pathlib import Path
from typing import Optional
from .base import CastingMethod, Element


class AirMethod(CastingMethod):
    """
    True random number generation via RANDOM.ORG JSON-RPC API.

    Uses RANDOM.ORG's true random number generator, which is based
    on atmospheric noise measurements. Provides genuine physical
    randomness rather than algorithmic pseudo-randomness.

    Requires internet connection and API key. See module docstring
    for setup instructions.
    """

    # JSON-RPC API endpoint (more reliable than basic API)
    API_URL = "https://api.random.org/json-rpc/4/invoke"
    TIMEOUT = 10  # seconds

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

    def _get_api_key(self) -> Optional[str]:
        """
        Get RANDOM.ORG API key from config file.

        Returns:
            API key string, or None if not configured
        """
        # Try ~/.pyching/random_org_api_key
        key_file = Path.home() / '.pyching' / 'random_org_api_key'

        if key_file.exists():
            try:
                api_key = key_file.read_text().strip()
                if api_key:
                    return api_key
            except Exception:
                pass

        # Also check environment variable
        env_key = os.environ.get('RANDOM_ORG_API_KEY', '').strip()
        if env_key:
            return env_key

        return None

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

        # Check for API key
        api_key = self._get_api_key()
        if not api_key:
            return (
                False,
                "RANDOM.ORG API key not configured.\n\n"
                "To use the Air method:\n"
                "1. Visit: https://api.random.org/dashboard\n"
                "2. Create account and choose 'Developer' type\n"
                "3. Generate API key in API Keys section\n"
                "4. Save to: ~/.pyching/random_org_api_key\n"
                "   (or set RANDOM_ORG_API_KEY environment variable)\n\n"
                "Alternative: Use Fire method for cryptographic randomness."
            )

        try:
            # Quick connectivity check
            import requests
            response = requests.head("https://api.random.org", timeout=2)
            return (True, None)
        except requests.RequestException as e:
            return (False, f"Cannot reach RANDOM.ORG: {str(e)}")

    def cast_line(self) -> int:
        """
        Cast a line using RANDOM.ORG JSON-RPC API.

        Makes an HTTP request to RANDOM.ORG to get three truly random
        numbers (each 2 or 3), then converts to line value.

        Returns:
            int: Line value (6, 7, 8, or 9)

        Raises:
            ImportError: If requests library is not installed
            ConnectionError: If API is unavailable or API key invalid
            ValueError: If API response is invalid
        """
        try:
            import requests
        except ImportError:
            raise ImportError(
                "requests library required for Air method. "
                "Install with: pip install requests"
            )

        # Get API key
        api_key = self._get_api_key()
        if not api_key:
            raise ConnectionError(
                "RANDOM.ORG API key not configured. "
                "See module docstring for setup instructions."
            )

        try:
            import json

            # Construct JSON-RPC 4.0 request
            request_payload = {
                "jsonrpc": "2.0",
                "method": "generateIntegers",
                "params": {
                    "apiKey": api_key,
                    "n": 3,        # 3 coins
                    "min": 2,      # minimum value (yin)
                    "max": 3,      # maximum value (yang)
                    "replacement": True
                },
                "id": 1
            }

            response = requests.post(
                self.API_URL,
                json=request_payload,
                headers={"Content-Type": "application/json"},
                timeout=self.TIMEOUT
            )
            response.raise_for_status()

            # Parse JSON-RPC response
            result = response.json()

            # Check for JSON-RPC error
            if "error" in result:
                error_msg = result["error"].get("message", "Unknown error")
                error_code = result["error"].get("code", "")
                raise ConnectionError(
                    f"RANDOM.ORG API error ({error_code}): {error_msg}. "
                    f"Check your API key and quota at https://api.random.org/dashboard"
                )

            # Extract random data
            if "result" not in result or "random" not in result["result"]:
                raise ValueError("Invalid JSON-RPC response structure")

            coins = result["result"]["random"]["data"]

            if len(coins) != 3:
                raise ValueError(f"Expected 3 values, got {len(coins)}")

            if not all(c in [2, 3] for c in coins):
                raise ValueError(f"Invalid coin values: {coins}")

            self._last_oracle_values = coins
            return self._traditional_coin_to_line(coins)

        except requests.RequestException as e:
            raise ConnectionError(
                f"Failed to connect to RANDOM.ORG: {str(e)}. "
                f"Check internet connection or use Fire method (cryptographic) as alternative."
            ) from e
        except (ValueError, KeyError, json.JSONDecodeError) as e:
            raise ValueError(
                f"Invalid response from RANDOM.ORG: {str(e)}"
            ) from e
