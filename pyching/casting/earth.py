"""
Earth Element casting method - Deterministic seeded PRNG.

Element: Earth (土)
Source: random module seeded with earth.txt + question
Characteristics: Reproducible, deterministic, contemplative, personal

THE PLANTING METAPHOR:
Your question is a seed, planted in your personal earth (foundation).
The reading grows from the combination of your accumulated wisdom
(earth.txt) and your specific inquiry (the question).

CONFIGURATION:
The Earth method uses a personal foundation file at:
    ~/.pyching/earth.txt

On first use, this file will be created automatically with traditional
I Ching content. You can customize it with your own philosophy, values,
or spiritual foundation. The same question will produce different
hexagrams for different people based on their unique earth.txt content.

The reading emerges from: earth.txt (soil) + question (seed) = hexagram (fruit)

CHARACTERISTICS:
- Same earth.txt + same question = same hexagram (reproducible)
- Different earth.txt = different hexagrams (personalized)
- Update your earth.txt as you grow = readings evolve with you
- No network required, works offline
"""

import random
from .base import CastingMethod, Element


class EarthMethod(CastingMethod):
    """
    Deterministic seeded PRNG method with personal foundation.

    Plants the user's question (seed) in their personal earth.txt
    (foundation/soil). The reading grows from combining accumulated
    wisdom with the specific inquiry.

    The same question produces the same hexagram for a given earth.txt,
    but different people with different foundations receive different
    readings. As you update your earth.txt, your readings evolve with you.

    This method uniquely connects the randomness to both the question
    AND your personal spiritual/philosophical foundation.
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
            "Plants your question (seed) in your personal earth.txt (foundation). "
            "The reading grows from combining your accumulated wisdom with your "
            "specific inquiry. Same earth.txt + same question = same hexagram. "
            "Different foundations produce different readings. As your earth.txt "
            "evolves, your readings evolve with you. Located at: ~/.pyching/earth.txt"
        )

    @property
    def requires_network(self) -> bool:
        return False

    def _get_earth_text(self) -> str:
        """
        Read earth.txt foundation file, create with default if doesn't exist.

        Returns:
            str: Content of earth.txt, or empty string on error
        """
        from pathlib import Path

        earth_path = Path.home() / '.pyching' / 'earth.txt'

        # Ensure .pyching directory exists
        earth_path.parent.mkdir(parents=True, exist_ok=True)

        # Create with default content if doesn't exist
        if not earth_path.exists():
            default_earth = """大哉乾元，萬物資始
Great is the Creative, the source of all things

The eight trigrams mark out the changes"""
            try:
                earth_path.write_text(default_earth, encoding='utf-8')
                return default_earth
            except Exception:
                return ""  # Fall back to empty on write error

        # Read existing earth.txt
        try:
            return earth_path.read_text(encoding='utf-8')
        except Exception:
            return ""  # Fall back to empty on read error

    def set_seed(self, seed: str) -> None:
        """
        Set the seed for deterministic generation.

        Plants the question (seed) in your personal earth.txt (foundation).
        The reading grows from combining your accumulated wisdom with your
        specific inquiry.

        If earth.txt doesn't exist, it will be created with traditional
        I Ching content. You can customize it at: ~/.pyching/earth.txt

        Args:
            seed: The question text (the seed to plant in your earth)
        """
        earth_text = self._get_earth_text()

        # Combine earth (soil) with question (seed) - Option A: Simple concatenation
        if earth_text:
            combined_seed = f"{earth_text}\n{seed}"
        else:
            # Empty or missing earth -> question-only (backward compatible)
            combined_seed = seed

        self._seed = combined_seed
        self._rng.seed(combined_seed)

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
