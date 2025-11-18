"""
Earth Element casting method - Deterministic seeded PRNG.

Element: Earth (土)
Source: random module with user-provided seed (question text)
Characteristics: Reproducible, deterministic, contemplative

Produces reproducible results based on the user's question.
The same question will always produce the same hexagram,
allowing for consistent readings and reflection over time.
"""

import random
from .base import CastingMethod, Element


class EarthMethod(CastingMethod):
    """
    Deterministic seeded PRNG method.

    Uses the user's question as a seed for deterministic random
    number generation. The same question will always produce the
    same hexagram, allowing for reproducible readings and
    contemplation of how understanding evolves over time.

    This method is unique in that it connects the randomness
    directly to the question itself.
    """

    def __init__(self, seed: str = None):
        super().__init__()
        self._seed = seed
        self._rng = random.Random()
        if seed:
            self._rng.seed(seed)

    @property
    def element(self) -> Element:
        return Element.EARTH

    @property
    def name(self) -> str:
        return "Seeded/Deterministic (Earth Element 土)"

    @property
    def description(self) -> str:
        return (
            "Uses the user's question as a seed for deterministic random "
            "number generation. The same question will always produce the "
            "same hexagram, allowing for reproducible readings and "
            "contemplation of how understanding evolves over time. "
            "This method connects the randomness to the question itself."
        )

    @property
    def requires_network(self) -> bool:
        return False

    def set_seed(self, seed: str) -> None:
        """
        Set the seed for deterministic generation.

        Args:
            seed: String to use as seed (typically the question text)
        """
        self._seed = seed
        self._rng.seed(seed)

    def cast_line(self) -> int:
        """
        Cast a line using seeded PRNG.

        Uses the seeded Random instance for deterministic coin selection.

        Returns:
            int: Line value (6, 7, 8, or 9)

        Raises:
            ValueError: If seed has not been set
        """
        if self._seed is None:
            raise ValueError(
                "Seed must be set before casting (use set_seed() method)"
            )

        # Use seeded RNG instance
        coins = [self._rng.choice([2, 3]) for _ in range(3)]

        self._last_oracle_values = coins
        return self._traditional_coin_to_line(coins)
