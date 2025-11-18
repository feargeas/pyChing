# pyChing Multi-Source Data & Five Elements Casting System
## Design Document

**Version:** 1.0
**Date:** 2025-11-18
**Branch:** `claude/testing-markdown-updates-01Knt8MmG1b4jNE82h2YXmcB`
**Status:** Design Proposal

---

## Executive Summary

This document outlines the architectural design for extending pyChing to support:
1. **Multiple translation/interpretation sources** (Wilhelm, Legge variants, Hermetica, DeKorne, etc.)
2. **Five distinct casting methods** mapped to the Five Elements (Wood, Fire, Earth, Metal, Water/Air)
3. **Source comparison capabilities** for scholarly and educational use
4. **Harmonious integration** with canonical source (Legge 1882) as reference point

### Core Principles
- **Preserve the Original**: Legge 1882 remains canonical and always available
- **Harmonious Integration**: New sources map to canonical structure
- **Five Elements Framework**: Each casting method corresponds to Chinese phenomenology
- **Extensibility**: Easy addition of new sources and methods
- **Cultural Respect**: Maintain authenticity and scholarly rigor

---

## 1. Requirements

### 1.1 Multi-Source Data Requirements

**Primary Sources to Integrate:**
1. **Canonical**: James Legge 1882 (current, preserved)
2. **Wilhelm/Baynes**: Richard Wilhelm translation via http://www2.unipr.it/~deyoung/I_Ching_Wilhelm_Translation.html
3. **Simplified Legge**: https://twodreams.us/blog/a-simplified-version-of-james-legges-translation-of-the-i-ching
4. **Hermetica**: https://www.hermetica.info/Yijing1+2.pdf
5. **DeKorne**: https://jamesdekorne.com/GBCh/GBCh.htm
6. **GitHub Sources**: Additional community sources as identified

**Data Requirements:**
- Each source must map to canonical hexagram numbering (King Wen sequence)
- Preserve original text, translator attribution, and source URL
- Support comparison view (side-by-side or sequential)
- Maintain metadata: translator, year, verification status, provenance
- Handle name variants (e.g., "Tch'ien" vs "Ch'ien" vs "Qian")

### 1.2 Casting Method Requirements

**Five Elements Casting System:**

| Element | Python Module/Method | Source Type | Key Characteristic |
|---------|---------------------|-------------|-------------------|
| **Air** | `requests` to RANDOM.ORG API | True RNG (External API) | Based on physical atmospheric noise; requires network access |
| **Wood** | `random` module (Mersenne Twister) | PRNG (Standard Library) | Default, fast, general-purpose deterministic algorithm |
| **Fire** | `secrets` module or `SystemRandom` | CSPRNG (OS Entropy Pool) | Cryptographically secure; uses high-quality OS-provided randomness |
| **Earth** | `random` with `random.seed(user_string)` | Deterministic PRNG (Seeded) | Reproducible results based on user's question as seed |
| **Metal** | `os.urandom()` | Raw Bytes (OS Entropy Pool) | Low-level access to raw system entropy bytes |

**Functional Requirements:**
- All methods must produce line values 6, 7, 8, or 9 with traditional probabilities
- Each method tracked in reading metadata
- Original coin method (Metal element) preserved exactly
- Support for offline use (fallback when Air method unavailable)
- Reproducible readings when using Earth method (seeded)

### 1.3 Resolution & Mapping Requirements

**Core Capabilities:**
- Map all sources to canonical hexagram IDs
- Resolve by: hexagram number, binary pattern, trigram pairs, name variants
- Graceful fallback to canonical when source incomplete
- Merge incomplete sources with canonical data
- Source priority configuration
- Comparison mode: display multiple sources simultaneously

### 1.4 Backward Compatibility

**Status:** Not required (per user)
- Old `.psv` save files can be deprecated
- New format: JSON (user preference)
- Migration tools optional but recommended for historical readings

---

## 2. Current State Analysis

### 2.1 Existing Data Structure

**Current Implementation:**
```python
# pyching_int_data.py (1,082 lines)
def in1data():
    return BuildHtml({
        'imgSrc': "pyching_idimage_data.id1data()",
        'title': " 1. Tch'ien / The Creative",
        'text': "Heaven, in its motion...",
        1: "nine: we see the dragon lying hidden...",
        2: "nine: we see the dragon appearing...",
        # ... lines 3-6
    })
# ... 64 functions total
```

**Limitations:**
- Single source (Legge 1882) hardcoded in Python
- No metadata or provenance tracking
- Difficult to add alternative translations
- HTML formatting mixed with content
- No comparison capabilities

### 2.2 Existing Casting Implementation

**Current Implementation:**
```python
# pyching_engine.py lines 226-230
if self.oracle == 'coin':
    rc = random.choice
    self.currentOracleValues = [rc([2,3]), rc([2,3]), rc([2,3])]
    self.hex1.lineValues[self.currentLine] = reduce(lambda x,y: x+y,
                                                     self.currentOracleValues)
```

**Limitations:**
- Only coin method implemented
- Yarrow stalks mentioned but not implemented
- No extensibility framework
- Hardcoded random source

### 2.3 Migration Status

**Phase 1 Complete** (per MIGRATION_NOTES.md):
- ✅ Python 3.10+ migration complete
- ✅ 32 tests passing (100% oracle authenticity preserved)
- ✅ Legge 1882 translation intact
- ✅ All 64 hexagram functions verified

**Current Branch:**
- `claude/testing-markdown-updates-01Knt8MmG1b4jNE82h2YXmcB`

**Unmerged Branches:**
- `claude/claude-md-mi4wu1qr60yf763g-015qFMdA265azJ2jWpsh8oM2`

---

## 3. Proposed Architecture

### 3.1 Multi-Source Data Structure

#### 3.1.1 JSON Schema for Hexagrams

**File:** `data/hexagrams/hexagram_01.json`

```json
{
  "hexagram_id": "hexagram_01",
  "number": 1,
  "king_wen_sequence": 1,
  "fu_xi_sequence": 1,
  "binary": "111111",
  "trigrams": {
    "upper": "qian",
    "lower": "qian"
  },

  "canonical": {
    "source_id": "legge_1882",
    "name": "Tch'ien",
    "english_name": "The Creative",
    "title": "1. Tch'ien / The Creative",
    "judgment": "Tch'ien represents what is great and originating, penetrating, advantageous, correct and firm.",
    "image": "Heaven, in its motion, gives the idea of strength. The superior person, in accordance with this, will nerve their being to ceaseless activity.",
    "lines": {
      "1": {
        "position": "bottom",
        "type": "nine",
        "text": "we see the dragon lying hidden in the deep. It is not the time for active doing."
      },
      "2": {
        "position": "second",
        "type": "nine",
        "text": "we see the dragon appearing in the field. It will be advantageous to meet with the great person."
      },
      "3": {
        "position": "third",
        "type": "nine",
        "text": "we see the superior person active and vigilant all the day, and in the evening still careful and apprehensive. The position is dangerous, but there will be no mistake."
      },
      "4": {
        "position": "fourth",
        "type": "nine",
        "text": "we see the dragon looking as if they were leaping up, but still in the deep. There will be no mistake."
      },
      "5": {
        "position": "fifth",
        "type": "nine",
        "text": "we see the dragon on the wing in the sky. It will be advantageous to meet with the great person."
      },
      "6": {
        "position": "topmost",
        "type": "nine",
        "text": "we see the dragon exceeding the proper limits. There will be occasion for repentance."
      }
    },
    "metadata": {
      "translator": "James Legge",
      "year": 1882,
      "language": "en",
      "verified": true,
      "notes": "Original translation preserved from pyChing v1.2.2"
    }
  },

  "sources": {
    "wilhelm_baynes": {
      "source_id": "wilhelm_baynes",
      "name": "Ch'ien",
      "english_name": "The Creative",
      "title": "1. Ch'ien / The Creative",
      "judgment": "The Creative works sublime success, Furthering through perseverance.",
      "image": "The movement of heaven is full of power. Thus the superior man makes himself strong and untiring.",
      "lines": {
        "1": {
          "position": "bottom",
          "type": "nine",
          "text": "Hidden dragon. Do not act."
        },
        "2": {
          "position": "second",
          "type": "nine",
          "text": "Dragon appearing in the field. It furthers one to see the great man."
        },
        "3": {
          "position": "third",
          "type": "nine",
          "text": "All day long the superior man is creatively active. At nightfall his mind is still beset with cares. Danger. No blame."
        },
        "4": {
          "position": "fourth",
          "type": "nine",
          "text": "Wavering flight over the depths. No blame."
        },
        "5": {
          "position": "fifth",
          "type": "nine",
          "text": "Flying dragon in the heavens. It furthers one to see the great man."
        },
        "6": {
          "position": "topmost",
          "type": "nine",
          "text": "Arrogant dragon will have cause to repent."
        }
      },
      "metadata": {
        "translator": "Richard Wilhelm / Cary F. Baynes",
        "year": 1950,
        "source_url": "http://www2.unipr.it/~deyoung/I_Ching_Wilhelm_Translation.html",
        "language": "en",
        "verified": false,
        "notes": "Translation from German to English"
      }
    },

    "legge_simplified": {
      "source_id": "legge_simplified",
      "name": "Qian",
      "english_name": "The Creative",
      "title": "1. Qian / The Creative",
      "judgment": "...",
      "metadata": {
        "translator": "Simplified by TwoDreams.us",
        "original_translator": "James Legge",
        "year": 1882,
        "simplified_year": 2020,
        "source_url": "https://twodreams.us/blog/a-simplified-version-of-james-legges-translation-of-the-i-ching",
        "language": "en",
        "verified": false
      }
    },

    "hermetica": {
      "source_id": "hermetica",
      "metadata": {
        "source_url": "https://www.hermetica.info/Yijing1+2.pdf",
        "verified": false,
        "notes": "PDF source - requires extraction"
      }
    },

    "dekorne": {
      "source_id": "dekorne",
      "metadata": {
        "author": "James DeKorne",
        "source_url": "https://jamesdekorne.com/GBCh/GBCh.htm",
        "verified": false,
        "notes": "Gnostic Book of Changes interpretation"
      }
    }
  }
}
```

#### 3.1.2 Source Metadata Registry

**File:** `data/sources_metadata.json`

```json
{
  "sources": {
    "legge_1882": {
      "id": "legge_1882",
      "name": "James Legge Translation (1882)",
      "translator": "James Legge",
      "year": 1882,
      "language": "en",
      "canonical": true,
      "description": "Original translation preserved from pyChing v1.2.2",
      "license": "Public Domain",
      "completeness": 100,
      "verified": true
    },
    "wilhelm_baynes": {
      "id": "wilhelm_baynes",
      "name": "Wilhelm/Baynes Translation",
      "translator": "Richard Wilhelm / Cary F. Baynes",
      "year": 1950,
      "language": "en",
      "canonical": false,
      "description": "German to English translation, widely regarded",
      "source_url": "http://www2.unipr.it/~deyoung/I_Ching_Wilhelm_Translation.html",
      "completeness": 0,
      "verified": false,
      "notes": "Requires extraction and formatting"
    },
    "legge_simplified": {
      "id": "legge_simplified",
      "name": "Simplified Legge (TwoDreams)",
      "translator": "Simplified by TwoDreams.us",
      "original_translator": "James Legge",
      "year": 2020,
      "language": "en",
      "canonical": false,
      "source_url": "https://twodreams.us/blog/a-simplified-version-of-james-legges-translation-of-the-i-ching",
      "completeness": 0,
      "verified": false
    },
    "hermetica": {
      "id": "hermetica",
      "name": "Hermetica I Ching",
      "source_url": "https://www.hermetica.info/Yijing1+2.pdf",
      "completeness": 0,
      "verified": false,
      "format": "PDF"
    },
    "dekorne": {
      "id": "dekorne",
      "name": "Gnostic Book of Changes",
      "author": "James DeKorne",
      "source_url": "https://jamesdekorne.com/GBCh/GBCh.htm",
      "completeness": 0,
      "verified": false
    }
  },

  "source_priority": [
    "canonical",
    "wilhelm_baynes",
    "legge_simplified",
    "hermetica",
    "dekorne"
  ]
}
```

#### 3.1.3 Mapping Tables

**File:** `data/mappings.json`

```json
{
  "number_to_id": {
    "1": "hexagram_01",
    "2": "hexagram_02",
    "...": "...",
    "64": "hexagram_64"
  },

  "binary_to_id": {
    "111111": "hexagram_01",
    "000000": "hexagram_02",
    "100010": "hexagram_03",
    "...": "..."
  },

  "trigram_pairs_to_id": {
    "qian_qian": "hexagram_01",
    "kun_kun": "hexagram_02",
    "kan_zhen": "hexagram_03",
    "...": "..."
  },

  "name_variants": {
    "Tch'ien": {
      "hexagram_id": "hexagram_01",
      "source": "legge_1882"
    },
    "Ch'ien": {
      "hexagram_id": "hexagram_01",
      "source": "wilhelm_baynes"
    },
    "Qian": {
      "hexagram_id": "hexagram_01",
      "source": "pinyin"
    },
    "Koun": {
      "hexagram_id": "hexagram_02",
      "source": "legge_1882"
    },
    "K'un": {
      "hexagram_id": "hexagram_02",
      "source": "wilhelm_baynes"
    },
    "Kun": {
      "hexagram_id": "hexagram_02",
      "source": "pinyin"
    }
  },

  "trigrams": {
    "qian": {
      "name": "Heaven",
      "attribute": "Creative",
      "binary": "111",
      "element": "Metal",
      "direction": "Northwest",
      "family": "Father"
    },
    "kun": {
      "name": "Earth",
      "attribute": "Receptive",
      "binary": "000",
      "element": "Earth",
      "direction": "Southwest",
      "family": "Mother"
    },
    "zhen": {
      "name": "Thunder",
      "attribute": "Arousing",
      "binary": "001",
      "element": "Wood",
      "direction": "East",
      "family": "Eldest Son"
    },
    "kan": {
      "name": "Water",
      "attribute": "Abysmal",
      "binary": "010",
      "element": "Water",
      "direction": "North",
      "family": "Middle Son"
    },
    "gen": {
      "name": "Mountain",
      "attribute": "Keeping Still",
      "binary": "100",
      "element": "Earth",
      "direction": "Northeast",
      "family": "Youngest Son"
    },
    "xun": {
      "name": "Wind",
      "attribute": "Gentle",
      "binary": "110",
      "element": "Wood",
      "direction": "Southeast",
      "family": "Eldest Daughter"
    },
    "li": {
      "name": "Fire",
      "attribute": "Clinging",
      "binary": "101",
      "element": "Fire",
      "direction": "South",
      "family": "Middle Daughter"
    },
    "dui": {
      "name": "Lake",
      "attribute": "Joyous",
      "binary": "011",
      "element": "Metal",
      "direction": "West",
      "family": "Youngest Daughter"
    }
  }
}
```

### 3.2 Five Elements Casting System

#### 3.2.1 Casting Method Base Class

**File:** `pyching/casting/base.py`

```python
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

class Element(Enum):
    """Five Elements of Chinese phenomenology"""
    AIR = "air"      # 風/氣 - True RNG via API
    WOOD = "wood"    # 木 - Standard PRNG
    FIRE = "fire"    # 火 - Cryptographic RNG
    EARTH = "earth"  # 土 - Seeded/Deterministic
    METAL = "metal"  # 金 - OS Entropy (Traditional Coin)

class CastingMethod(ABC):
    """
    Abstract base class for all I Ching casting methods.

    Each method must produce line values 6, 7, 8, or 9 with traditional
    probabilities:
    - 6 (old yin): 12.5% (1/8)
    - 7 (yang): 37.5% (3/8)
    - 8 (yin): 37.5% (3/8)
    - 9 (old yang): 12.5% (1/8)
    """

    def __init__(self):
        self._last_oracle_values: list[int] = []

    @property
    @abstractmethod
    def element(self) -> Element:
        """The element this method corresponds to"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name of this casting method"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Detailed description of this method"""
        pass

    @property
    @abstractmethod
    def requires_network(self) -> bool:
        """Whether this method requires network access"""
        pass

    @abstractmethod
    def cast_line(self) -> int:
        """
        Cast a single line.

        Returns:
            int: Line value (6, 7, 8, or 9)
        """
        pass

    def get_oracle_values(self) -> list[int]:
        """
        Get the raw oracle values from the last cast.

        Returns:
            list[int]: Raw values used to determine the line
        """
        return self._last_oracle_values.copy()

    def is_available(self) -> tuple[bool, Optional[str]]:
        """
        Check if this casting method is currently available.

        Returns:
            tuple[bool, Optional[str]]: (available, error_message)
        """
        return (True, None)

    def _traditional_coin_to_line(self, coins: list[int]) -> int:
        """
        Convert three coin values to a line value.

        Traditional mapping:
        - Each coin is 2 (yin) or 3 (yang)
        - Sum of 6 (2+2+2) = old yin
        - Sum of 7 (2+2+3) = yang
        - Sum of 8 (2+3+3) = yin
        - Sum of 9 (3+3+3) = old yang

        Args:
            coins: List of three coin values (each 2 or 3)

        Returns:
            int: Line value (6, 7, 8, or 9)
        """
        if len(coins) != 3:
            raise ValueError("Must provide exactly 3 coin values")
        if not all(c in [2, 3] for c in coins):
            raise ValueError("Each coin must be 2 or 3")

        return sum(coins)
```

#### 3.2.2 Metal Element (Traditional Coin Method)

**File:** `pyching/casting/metal.py`

```python
import os
from typing import Optional
from .base import CastingMethod, Element

class MetalMethod(CastingMethod):
    """
    Traditional I Ching coin method using OS entropy.

    Element: Metal (金)
    Source: os.urandom() - raw system entropy bytes

    This is the traditional three-coin method, implemented using
    low-level OS entropy for maximum randomness quality.
    """

    @property
    def element(self) -> Element:
        return Element.METAL

    @property
    def name(self) -> str:
        return "Traditional Coins (Metal Element)"

    @property
    def description(self) -> str:
        return (
            "The traditional three-coin method using raw OS entropy. "
            "Each of three coins is assigned yin (2) or yang (3) based on "
            "cryptographically secure random bytes from the operating system."
        )

    @property
    def requires_network(self) -> bool:
        return False

    def cast_line(self) -> int:
        """
        Cast a line using three virtual coins with OS entropy.

        Returns:
            int: Line value (6, 7, 8, or 9)
        """
        # Get 3 random bytes from OS
        random_bytes = os.urandom(3)

        # Convert each byte to coin value (2 or 3)
        # Use bit masking: if low bit is 0 → 2, if 1 → 3
        coins = [(byte & 1) + 2 for byte in random_bytes]

        self._last_oracle_values = coins
        return self._traditional_coin_to_line(coins)
```

#### 3.2.3 Wood Element (Standard PRNG)

**File:** `pyching/casting/wood.py`

```python
import random
from .base import CastingMethod, Element

class WoodMethod(CastingMethod):
    """
    Standard PRNG method (Mersenne Twister).

    Element: Wood (木)
    Source: random module - fast, general-purpose PRNG

    Uses Python's default random number generator, which is deterministic
    but high-quality for non-cryptographic purposes.
    """

    @property
    def element(self) -> Element:
        return Element.WOOD

    @property
    def name(self) -> str:
        return "Mersenne Twister (Wood Element)"

    @property
    def description(self) -> str:
        return (
            "Uses Python's standard random module (Mersenne Twister algorithm). "
            "Fast, general-purpose random number generation suitable for "
            "divination purposes. Deterministic but high-quality distribution."
        )

    @property
    def requires_network(self) -> bool:
        return False

    def cast_line(self) -> int:
        """
        Cast a line using Mersenne Twister PRNG.

        Returns:
            int: Line value (6, 7, 8, or 9)
        """
        # Use random.choice for each coin (matches original pyChing algorithm)
        coins = [random.choice([2, 3]) for _ in range(3)]

        self._last_oracle_values = coins
        return self._traditional_coin_to_line(coins)
```

#### 3.2.4 Fire Element (Cryptographic RNG)

**File:** `pyching/casting/fire.py`

```python
import secrets
from .base import CastingMethod, Element

class FireMethod(CastingMethod):
    """
    Cryptographically secure RNG method.

    Element: Fire (火)
    Source: secrets module - CSPRNG using OS entropy pool

    Uses cryptographically strong random number generation suitable
    for security-sensitive applications. Highest quality randomness
    available without external sources.
    """

    @property
    def element(self) -> Element:
        return Element.FIRE

    @property
    def name(self) -> str:
        return "Cryptographic (Fire Element)"

    @property
    def description(self) -> str:
        return (
            "Uses Python's secrets module for cryptographically secure "
            "random number generation. Draws from the OS entropy pool, "
            "providing the highest quality randomness available locally."
        )

    @property
    def requires_network(self) -> bool:
        return False

    def cast_line(self) -> int:
        """
        Cast a line using cryptographically secure RNG.

        Returns:
            int: Line value (6, 7, 8, or 9)
        """
        # Use secrets.choice for cryptographically secure selection
        coins = [secrets.choice([2, 3]) for _ in range(3)]

        self._last_oracle_values = coins
        return self._traditional_coin_to_line(coins)
```

#### 3.2.5 Earth Element (Seeded/Deterministic)

**File:** `pyching/casting/earth.py`

```python
import random
from .base import CastingMethod, Element

class EarthMethod(CastingMethod):
    """
    Deterministic seeded PRNG method.

    Element: Earth (土)
    Source: random module with user-provided seed (question text)

    Produces reproducible results based on the user's question.
    The same question will always produce the same hexagram,
    allowing for consistent readings and reflection over time.
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
        return "Seeded/Deterministic (Earth Element)"

    @property
    def description(self) -> str:
        return (
            "Uses the user's question as a seed for deterministic random "
            "number generation. The same question will always produce the "
            "same hexagram, allowing for reproducible readings and "
            "contemplation of how understanding evolves over time."
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

        Returns:
            int: Line value (6, 7, 8, or 9)
        """
        if self._seed is None:
            raise ValueError("Seed must be set before casting (use set_seed())")

        # Use seeded RNG instance
        coins = [self._rng.choice([2, 3]) for _ in range(3)]

        self._last_oracle_values = coins
        return self._traditional_coin_to_line(coins)
```

#### 3.2.6 Air Element (True RNG via API)

**File:** `pyching/casting/air.py`

```python
from typing import Optional
import requests
from .base import CastingMethod, Element

class AirMethod(CastingMethod):
    """
    True random number generation via RANDOM.ORG API.

    Element: Air (風/氣)
    Source: RANDOM.ORG - atmospheric noise-based true RNG

    Uses physical atmospheric noise measurements to generate
    true random numbers. Requires network access.
    """

    API_URL = "https://www.random.org/integers/"
    TIMEOUT = 5  # seconds

    @property
    def element(self) -> Element:
        return Element.AIR

    @property
    def name(self) -> str:
        return "True RNG via RANDOM.ORG (Air Element)"

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
            # Simple connectivity check
            response = requests.head(self.API_URL, timeout=2)
            return (True, None)
        except requests.RequestException as e:
            return (False, f"Cannot reach RANDOM.ORG: {str(e)}")

    def cast_line(self) -> int:
        """
        Cast a line using RANDOM.ORG API.

        Returns:
            int: Line value (6, 7, 8, or 9)

        Raises:
            ConnectionError: If API is unavailable
        """
        try:
            # Request 3 random integers (2 or 3)
            params = {
                'num': 3,      # 3 coins
                'min': 2,      # minimum value (yin)
                'max': 3,      # maximum value (yang)
                'col': 1,      # single column
                'base': 10,    # decimal
                'format': 'plain',  # plain text
                'rnd': 'new'   # new randomization
            }

            response = requests.get(
                self.API_URL,
                params=params,
                timeout=self.TIMEOUT
            )
            response.raise_for_status()

            # Parse response (three integers, one per line)
            coins = [int(line.strip()) for line in response.text.strip().split('\n')]

            if len(coins) != 3:
                raise ValueError(f"Expected 3 values, got {len(coins)}")

            self._last_oracle_values = coins
            return self._traditional_coin_to_line(coins)

        except requests.RequestException as e:
            raise ConnectionError(
                f"Failed to get random numbers from RANDOM.ORG: {str(e)}"
            ) from e
        except (ValueError, IndexError) as e:
            raise ValueError(
                f"Invalid response from RANDOM.ORG: {str(e)}"
            ) from e
```

#### 3.2.7 Casting Method Registry

**File:** `pyching/casting/__init__.py`

```python
from typing import Optional
from .base import CastingMethod, Element
from .metal import MetalMethod
from .wood import WoodMethod
from .fire import FireMethod
from .earth import EarthMethod
from .air import AirMethod

class CastingMethodRegistry:
    """
    Registry and factory for casting methods.

    Manages all available casting methods and provides
    lookup by element.
    """

    def __init__(self):
        self._methods: dict[Element, CastingMethod] = {}
        self._register_defaults()

    def _register_defaults(self):
        """Register the five element methods"""
        self.register(MetalMethod())
        self.register(WoodMethod())
        self.register(FireMethod())
        self.register(EarthMethod())
        self.register(AirMethod())

    def register(self, method: CastingMethod) -> None:
        """
        Register a new casting method.

        Args:
            method: CastingMethod instance to register
        """
        self._methods[method.element] = method

    def get(self, element: Element) -> Optional[CastingMethod]:
        """
        Get casting method by element.

        Args:
            element: Element enum value

        Returns:
            CastingMethod instance or None if not found
        """
        return self._methods.get(element)

    def list_methods(self) -> list[CastingMethod]:
        """
        List all registered methods.

        Returns:
            list: All registered CastingMethod instances
        """
        return list(self._methods.values())

    def get_available_methods(self) -> list[CastingMethod]:
        """
        List all currently available methods.

        Returns:
            list: CastingMethod instances that are currently available
        """
        available = []
        for method in self._methods.values():
            is_avail, _ = method.is_available()
            if is_avail:
                available.append(method)
        return available

# Singleton instance
_registry = CastingMethodRegistry()

def get_registry() -> CastingMethodRegistry:
    """Get the global casting method registry"""
    return _registry
```

### 3.3 Data Resolution System

#### 3.3.1 Hexagram Data Loader

**File:** `pyching/data/loader.py`

```python
import json
from pathlib import Path
from typing import Optional, Dict, Any

class HexagramDataLoader:
    """
    Loads hexagram data from JSON files.
    """

    def __init__(self, data_dir: Path = None):
        if data_dir is None:
            # Default to data/ directory relative to project root
            data_dir = Path(__file__).parent.parent.parent / 'data'

        self.data_dir = Path(data_dir)
        self.hexagrams_dir = self.data_dir / 'hexagrams'
        self.mappings_path = self.data_dir / 'mappings.json'
        self.sources_path = self.data_dir / 'sources_metadata.json'

        self._cache: Dict[str, Dict[str, Any]] = {}
        self._mappings: Optional[Dict[str, Any]] = None
        self._sources: Optional[Dict[str, Any]] = None

    def load_hexagram(self, hexagram_id: str) -> Dict[str, Any]:
        """
        Load a hexagram by ID.

        Args:
            hexagram_id: Hexagram identifier (e.g., "hexagram_01")

        Returns:
            dict: Hexagram data
        """
        if hexagram_id in self._cache:
            return self._cache[hexagram_id]

        hex_file = self.hexagrams_dir / f"{hexagram_id}.json"

        if not hex_file.exists():
            raise FileNotFoundError(f"Hexagram file not found: {hex_file}")

        with open(hex_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self._cache[hexagram_id] = data
        return data

    def load_mappings(self) -> Dict[str, Any]:
        """Load mapping tables"""
        if self._mappings is not None:
            return self._mappings

        with open(self.mappings_path, 'r', encoding='utf-8') as f:
            self._mappings = json.load(f)

        return self._mappings

    def load_sources_metadata(self) -> Dict[str, Any]:
        """Load source metadata"""
        if self._sources is not None:
            return self._sources

        with open(self.sources_path, 'r', encoding='utf-8') as f:
            self._sources = json.load(f)

        return self._sources

    def get_hexagram_by_number(self, number: int) -> Dict[str, Any]:
        """
        Get hexagram by King Wen number.

        Args:
            number: Hexagram number (1-64)

        Returns:
            dict: Hexagram data
        """
        mappings = self.load_mappings()
        hexagram_id = mappings['number_to_id'][str(number)]
        return self.load_hexagram(hexagram_id)

    def get_hexagram_by_binary(self, binary: str) -> Dict[str, Any]:
        """
        Get hexagram by binary pattern.

        Args:
            binary: 6-character binary string (e.g., "111111")

        Returns:
            dict: Hexagram data
        """
        mappings = self.load_mappings()
        hexagram_id = mappings['binary_to_id'][binary]
        return self.load_hexagram(hexagram_id)

    def get_hexagram_by_lines(self, lines: list[int]) -> Dict[str, Any]:
        """
        Get hexagram by line values.

        Args:
            lines: List of 6 line values (7 or 8, non-moving)

        Returns:
            dict: Hexagram data
        """
        # Convert line values to binary
        # 7 (yang) = 1, 8 (yin) = 0
        binary = ''.join('1' if line == 7 else '0' for line in lines)
        return self.get_hexagram_by_binary(binary)
```

#### 3.3.2 Source Resolver

**File:** `pyching/data/resolver.py`

```python
from typing import Optional, Dict, Any, List
from .loader import HexagramDataLoader

class HexagramResolver:
    """
    Resolves hexagram data from multiple sources with fallback logic.
    """

    def __init__(self, loader: HexagramDataLoader = None):
        self.loader = loader or HexagramDataLoader()
        self._sources_metadata = self.loader.load_sources_metadata()

    def resolve(self,
                hexagram_id: str,
                source: str = 'canonical') -> Dict[str, Any]:
        """
        Resolve hexagram data from specified source.

        Args:
            hexagram_id: Hexagram identifier
            source: Source ID (defaults to 'canonical')

        Returns:
            dict: Resolved hexagram data
        """
        hex_data = self.loader.load_hexagram(hexagram_id)

        if source == 'canonical' or source not in hex_data.get('sources', {}):
            # Return canonical
            return self._format_for_display(hex_data['canonical'], hex_data)

        # Get requested source
        source_data = hex_data['sources'][source]

        # Merge with canonical for missing fields
        merged = self._merge_with_canonical(source_data, hex_data['canonical'])

        return self._format_for_display(merged, hex_data)

    def resolve_multiple(self,
                        hexagram_id: str,
                        sources: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Resolve hexagram data from multiple sources for comparison.

        Args:
            hexagram_id: Hexagram identifier
            sources: List of source IDs to retrieve

        Returns:
            dict: Map of source_id -> hexagram data
        """
        result = {}

        for source in sources:
            try:
                result[source] = self.resolve(hexagram_id, source)
            except KeyError:
                # Source not available, skip
                continue

        return result

    def get_available_sources(self, hexagram_id: str) -> List[str]:
        """
        Get list of available sources for a hexagram.

        Args:
            hexagram_id: Hexagram identifier

        Returns:
            list: Available source IDs
        """
        hex_data = self.loader.load_hexagram(hexagram_id)
        sources = ['canonical']
        sources.extend(hex_data.get('sources', {}).keys())
        return sources

    def _merge_with_canonical(self,
                             source_data: Dict[str, Any],
                             canonical_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge source data with canonical, using canonical for missing fields.

        Args:
            source_data: Data from specific source
            canonical_data: Canonical reference data

        Returns:
            dict: Merged data
        """
        merged = canonical_data.copy()

        # Override with source-specific data where available
        for key in ['name', 'english_name', 'title', 'judgment', 'image', 'lines']:
            if key in source_data:
                merged[key] = source_data[key]

        # Always include source metadata
        merged['metadata'] = source_data.get('metadata', {})

        return merged

    def _format_for_display(self,
                           source_data: Dict[str, Any],
                           hex_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format hexagram data for display, adding contextual information.

        Args:
            source_data: Resolved source data
            hex_data: Full hexagram data (for context)

        Returns:
            dict: Formatted data
        """
        return {
            'hexagram_id': hex_data['hexagram_id'],
            'number': hex_data['number'],
            'binary': hex_data['binary'],
            'trigrams': hex_data['trigrams'],
            'name': source_data['name'],
            'english_name': source_data.get('english_name', ''),
            'title': source_data.get('title', ''),
            'judgment': source_data.get('judgment', ''),
            'image': source_data.get('image', ''),
            'lines': source_data.get('lines', {}),
            'metadata': source_data.get('metadata', {})
        }
```

### 3.4 Updated Hexagram Models

**File:** `pyching/models/hexagram.py`

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
from pyching.casting.base import Element

@dataclass
class Hexagram:
    """
    Enhanced hexagram data structure.
    """
    number: str = ''
    name: str = ''
    lineValues: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0, 0])
    source: str = 'canonical'  # Source ID for interpretation
    castingMethod: Optional[Element] = Element.METAL

    # Full hexagram data (loaded on demand)
    _data: Optional[Dict[str, Any]] = field(default=None, repr=False)

@dataclass
class Reading:
    """
    Complete I Ching reading data structure.
    """
    question: str = ''
    timestamp: datetime = field(default_factory=datetime.now)
    castingMethod: Element = Element.METAL
    preferredSource: str = 'canonical'

    hex1: Hexagram = field(default_factory=Hexagram)
    hex2: Optional[Hexagram] = None

    currentLine: int = 0
    oracleValuesPerLine: List[List[int]] = field(default_factory=list)

    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'question': self.question,
            'timestamp': self.timestamp.isoformat(),
            'castingMethod': self.castingMethod.value,
            'preferredSource': self.preferredSource,
            'hex1': {
                'number': self.hex1.number,
                'name': self.hex1.name,
                'lineValues': self.hex1.lineValues,
                'source': self.hex1.source
            },
            'hex2': {
                'number': self.hex2.number,
                'name': self.hex2.name,
                'lineValues': self.hex2.lineValues,
                'source': self.hex2.source
            } if self.hex2 else None,
            'oracleValuesPerLine': self.oracleValuesPerLine,
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Reading':
        """Load from dictionary (JSON deserialization)"""
        reading = cls(
            question=data['question'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            castingMethod=Element(data['castingMethod']),
            preferredSource=data['preferredSource'],
            currentLine=6,  # Reading is complete
            oracleValuesPerLine=data.get('oracleValuesPerLine', []),
            metadata=data.get('metadata', {})
        )

        # Restore hex1
        hex1_data = data['hex1']
        reading.hex1 = Hexagram(
            number=hex1_data['number'],
            name=hex1_data['name'],
            lineValues=hex1_data['lineValues'],
            source=hex1_data.get('source', 'canonical'),
            castingMethod=reading.castingMethod
        )

        # Restore hex2 if present
        if data.get('hex2'):
            hex2_data = data['hex2']
            reading.hex2 = Hexagram(
                number=hex2_data['number'],
                name=hex2_data['name'],
                lineValues=hex2_data['lineValues'],
                source=hex2_data.get('source', 'canonical'),
                castingMethod=reading.castingMethod
            )

        return reading

    def save_to_file(self, filepath: str) -> None:
        """Save reading to JSON file"""
        import json
        from pathlib import Path

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    @classmethod
    def load_from_file(cls, filepath: str) -> 'Reading':
        """Load reading from JSON file"""
        import json

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return cls.from_dict(data)
```

### 3.5 Updated Engine Class

**File:** `pyching/engine.py`

```python
from typing import Optional, List
from functools import reduce

from pyching.models.hexagram import Hexagram, Reading
from pyching.casting.base import Element
from pyching.casting import get_registry
from pyching.data.loader import HexagramDataLoader
from pyching.data.resolver import HexagramResolver

class HexagramEngine:
    """
    Core I Ching oracle engine with multi-source and multi-method support.
    """

    def __init__(self,
                 casting_method: Element = Element.METAL,
                 preferred_source: str = 'canonical',
                 seed: Optional[str] = None):
        """
        Initialize the engine.

        Args:
            casting_method: Element enum for casting method
            preferred_source: Source ID for interpretations
            seed: Seed string for Earth method (deterministic)
        """
        self.reading = Reading(
            castingMethod=casting_method,
            preferredSource=preferred_source
        )

        # Get casting method
        registry = get_registry()
        self._caster = registry.get(casting_method)

        if self._caster is None:
            raise ValueError(f"Casting method not found: {casting_method}")

        # Set seed for Earth method
        if casting_method == Element.EARTH and seed:
            self._caster.set_seed(seed)

        # Data resolver
        self._loader = HexagramDataLoader()
        self._resolver = HexagramResolver(self._loader)

    def set_question(self, question: str) -> None:
        """Set the question for this reading"""
        self.reading.question = question

        # If using Earth method, use question as seed
        if self.reading.castingMethod == Element.EARTH:
            self._caster.set_seed(question)

    def cast_line(self) -> bool:
        """
        Cast the next line.

        Returns:
            bool: True if reading is complete, False otherwise
        """
        if self.reading.currentLine >= 6:
            return True  # Already complete

        # Cast line
        line_value = self._caster.cast_line()
        oracle_values = self._caster.get_oracle_values()

        # Store in reading
        self.reading.hex1.lineValues[self.reading.currentLine] = line_value
        self.reading.oracleValuesPerLine.append(oracle_values)
        self.reading.currentLine += 1

        # Complete hexagrams if we've cast all 6 lines
        if self.reading.currentLine == 6:
            self._complete_hexagrams()
            return True

        return False

    def cast_all_lines(self) -> None:
        """Cast all 6 lines at once"""
        while not self.cast_line():
            pass

    def _complete_hexagrams(self) -> None:
        """
        Complete hexagram lookup and transformation.

        This preserves the original pyChing algorithm exactly.
        """
        # Get non-moving line values for lookup
        hex1_key = []
        for line_value in self.reading.hex1.lineValues:
            if line_value == 6:
                hex1_key.append(8)  # old yin → yin for lookup
            elif line_value == 9:
                hex1_key.append(7)  # old yang → yang for lookup
            else:
                hex1_key.append(line_value)

        # Lookup hexagram 1
        hex1_data = self._loader.get_hexagram_by_lines(hex1_key)
        self.reading.hex1.number = str(hex1_data['number'])
        self.reading.hex1.name = hex1_data['canonical']['name']
        self.reading.hex1.source = self.reading.preferredSource

        # Check for moving lines
        has_moving_lines = any(v in [6, 9] for v in self.reading.hex1.lineValues)

        if has_moving_lines:
            # Create hexagram 2 with transformed lines
            hex2_lines = []
            for line_value in self.reading.hex1.lineValues:
                if line_value == 6:
                    hex2_lines.append(7)  # old yin → yang
                elif line_value == 9:
                    hex2_lines.append(8)  # old yang → yin
                else:
                    hex2_lines.append(line_value)  # stable

            # Lookup hexagram 2
            hex2_data = self._loader.get_hexagram_by_lines(hex2_lines)

            self.reading.hex2 = Hexagram(
                number=str(hex2_data['number']),
                name=hex2_data['canonical']['name'],
                lineValues=hex2_lines,
                source=self.reading.preferredSource,
                castingMethod=self.reading.castingMethod
            )

    def get_interpretation(self,
                          hexagram_num: int,
                          source: Optional[str] = None) -> dict:
        """
        Get interpretation for a hexagram.

        Args:
            hexagram_num: Hexagram number (1 or 2)
            source: Source ID (uses preferred if not specified)

        Returns:
            dict: Hexagram interpretation data
        """
        if source is None:
            source = self.reading.preferredSource

        if hexagram_num == 1:
            hex_id = f"hexagram_{int(self.reading.hex1.number):02d}"
        elif hexagram_num == 2 and self.reading.hex2:
            hex_id = f"hexagram_{int(self.reading.hex2.number):02d}"
        else:
            raise ValueError(f"Invalid hexagram number: {hexagram_num}")

        return self._resolver.resolve(hex_id, source)

    def compare_sources(self,
                       hexagram_num: int,
                       sources: Optional[List[str]] = None) -> dict:
        """
        Get interpretations from multiple sources for comparison.

        Args:
            hexagram_num: Hexagram number (1 or 2)
            sources: List of source IDs (uses all available if not specified)

        Returns:
            dict: Map of source_id -> interpretation
        """
        if hexagram_num == 1:
            hex_id = f"hexagram_{int(self.reading.hex1.number):02d}"
        elif hexagram_num == 2 and self.reading.hex2:
            hex_id = f"hexagram_{int(self.reading.hex2.number):02d}"
        else:
            raise ValueError(f"Invalid hexagram number: {hexagram_num}")

        if sources is None:
            sources = self._resolver.get_available_sources(hex_id)

        return self._resolver.resolve_multiple(hex_id, sources)
```

---

## 4. File Structure

### 4.1 Proposed Directory Layout

```
pyChing/
├── data/                          # New: Structured data files
│   ├── hexagrams/
│   │   ├── hexagram_01.json      # Hexagram 1 (all sources)
│   │   ├── hexagram_02.json      # Hexagram 2
│   │   ├── ...
│   │   └── hexagram_64.json      # Hexagram 64
│   ├── mappings.json             # Mapping tables
│   └── sources_metadata.json     # Source registry
│
├── pyching/                       # New: Package structure
│   ├── __init__.py
│   ├── casting/                  # New: Casting methods
│   │   ├── __init__.py
│   │   ├── base.py              # CastingMethod ABC, Element enum
│   │   ├── metal.py             # Traditional coin (os.urandom)
│   │   ├── wood.py              # Standard PRNG (random)
│   │   ├── fire.py              # Cryptographic (secrets)
│   │   ├── earth.py             # Seeded (deterministic)
│   │   └── air.py               # True RNG (RANDOM.ORG)
│   ├── data/                     # New: Data access layer
│   │   ├── __init__.py
│   │   ├── loader.py            # JSON data loader
│   │   ├── resolver.py          # Multi-source resolver
│   │   └── legacy.py            # Legacy format support
│   ├── models/                   # New: Data models
│   │   ├── __init__.py
│   │   └── hexagram.py          # Hexagram, Reading dataclasses
│   ├── engine.py                 # New: Core engine (replaces pyching_engine.py)
│   └── utils/
│       ├── __init__.py
│       └── conversion.py         # Legacy conversion utilities
│
├── pyching_engine.py             # Legacy: Keep for reference
├── pyching_int_data.py           # Legacy: Keep for reference
├── pyching_hlhtx_data.py         # Legacy: Help text
├── pyching_idimage_data.py       # Legacy: Images
├── pyching_cimages.py            # Legacy: Coin images
├── pyching_interface_tkinter.py  # Legacy: GUI (to be updated)
├── pyching_interface_console.py  # Legacy: CLI (to be updated)
├── pyching.py                    # Legacy: Entry point (to be updated)
│
├── tests/                         # Enhanced test suite
│   ├── __init__.py
│   ├── test_casting_methods.py   # New: Test all 5 methods
│   ├── test_data_loader.py       # New: Test data loading
│   ├── test_resolver.py          # New: Test source resolution
│   ├── test_engine.py            # New: Test core engine
│   ├── test_comparison.py        # New: Test source comparison
│   ├── test_hexagram_data.py     # Existing
│   ├── test_oracle_coin_method.py # Existing
│   └── test_reading_persistence.py # Existing (update for JSON)
│
├── tools/                         # New: Utilities
│   ├── extract_sources.py        # Extract data from web sources
│   ├── convert_legacy_data.py    # Convert pyching_int_data.py → JSON
│   └── validate_sources.py       # Validate JSON schemas
│
├── docs/                          # Documentation
│   ├── casting_methods.md        # Five Elements methods guide
│   ├── data_sources.md           # Source attribution and info
│   └── api.md                    # API documentation
│
├── pyproject.toml                 # Existing: Project config
├── README.md                      # Existing: Project readme
├── MIGRATION_NOTES.md            # Existing: Phase 1 notes
├── DESIGN_MULTI_SOURCE_CASTING.md # This document
└── project_notes.txt             # Existing: Planning notes
```

---

## 5. Migration Strategy

### 5.1 Phase 1: Data Extraction (Current Focus)

**Goal:** Convert existing data to new JSON structure

**Tasks:**
1. ✅ Create JSON schema for hexagrams
2. ✅ Create mapping tables schema
3. ✅ Create source metadata schema
4. ⬜ Write conversion tool: `pyching_int_data.py` → JSON
5. ⬜ Extract Legge 1882 data to canonical format
6. ⬜ Validate all 64 hexagrams
7. ⬜ Create initial `mappings.json`
8. ⬜ Create initial `sources_metadata.json`

**Deliverables:**
- `data/hexagrams/hexagram_01.json` through `hexagram_64.json`
- `data/mappings.json`
- `data/sources_metadata.json`
- `tools/convert_legacy_data.py`

### 5.2 Phase 2: Casting Methods Implementation

**Goal:** Implement all five element casting methods

**Tasks:**
1. ✅ Design casting method architecture
2. ⬜ Implement base classes (`base.py`)
3. ⬜ Implement Metal method (preserve original exactly)
4. ⬜ Implement Wood method (Mersenne Twister)
5. ⬜ Implement Fire method (cryptographic)
6. ⬜ Implement Earth method (seeded)
7. ⬜ Implement Air method (RANDOM.ORG)
8. ⬜ Create casting method registry
9. ⬜ Write comprehensive tests for all methods
10. ⬜ Validate probability distributions

**Deliverables:**
- `pyching/casting/` module complete
- `tests/test_casting_methods.py`
- Documentation on each method

### 5.3 Phase 3: Data Access Layer

**Goal:** Implement multi-source data loading and resolution

**Tasks:**
1. ✅ Design resolver architecture
2. ⬜ Implement `HexagramDataLoader`
3. ⬜ Implement `HexagramResolver`
4. ⬜ Add source comparison functionality
5. ⬜ Create fallback/merge logic
6. ⬜ Write tests for resolution
7. ⬜ Write tests for source comparison

**Deliverables:**
- `pyching/data/loader.py`
- `pyching/data/resolver.py`
- `tests/test_data_loader.py`
- `tests/test_resolver.py`

### 5.4 Phase 4: Core Engine Update

**Goal:** Integrate new casting and data systems

**Tasks:**
1. ✅ Design new engine architecture
2. ⬜ Implement updated `Hexagram` dataclass
3. ⬜ Implement `Reading` dataclass with JSON serialization
4. ⬜ Implement `HexagramEngine` class
5. ⬜ Preserve original algorithm exactly
6. ⬜ Add multi-source support
7. ⬜ Add casting method selection
8. ⬜ Write comprehensive engine tests

**Deliverables:**
- `pyching/models/hexagram.py`
- `pyching/engine.py`
- `tests/test_engine.py`
- Reading JSON format specification

### 5.5 Phase 5: Additional Sources Integration

**Goal:** Add Wilhelm, simplified Legge, Hermetica, DeKorne sources

**Tasks:**
1. ⬜ Create web scraping tools for each source
2. ⬜ Extract Wilhelm/Baynes translation
3. ⬜ Extract simplified Legge
4. ⬜ Extract Hermetica content (PDF)
5. ⬜ Extract DeKorne content
6. ⬜ Map each source to canonical structure
7. ⬜ Validate completeness and accuracy
8. ⬜ Add attribution and metadata

**Deliverables:**
- `tools/extract_sources.py`
- Updated `data/hexagrams/*.json` with new sources
- Updated `data/sources_metadata.json`
- Source attribution documentation

### 5.6 Phase 6: Interface Updates

**Goal:** Update UI/CLI to support new features

**Tasks:**
1. ⬜ Add casting method selection to UI
2. ⬜ Add source selection to UI
3. ⬜ Implement source comparison view
4. ⬜ Update console interface
5. ⬜ Update Tkinter interface
6. ⬜ Add settings for defaults
7. ⬜ Update help text

**Deliverables:**
- Updated `pyching_interface_console.py`
- Updated `pyching_interface_tkinter.py`
- Updated help documentation

### 5.7 Phase 7: Testing & Documentation

**Goal:** Comprehensive testing and documentation

**Tasks:**
1. ⬜ Achieve 100% test coverage on oracle logic
2. ⬜ Validate all 5 casting methods
3. ⬜ Validate all sources
4. ⬜ Create comparison tests
5. ⬜ Write user documentation
6. ⬜ Write developer documentation
7. ⬜ Create examples and tutorials

**Deliverables:**
- Full test suite passing
- Complete documentation
- User guide
- Developer guide

---

## 6. Expected Outcomes

### 6.1 Functional Outcomes

**Multi-Source Support:**
- ✅ Users can select preferred interpretation source
- ✅ Users can compare multiple sources side-by-side
- ✅ Automatic fallback to canonical when source incomplete
- ✅ Clear attribution and provenance for each source
- ✅ Easy addition of new sources via JSON files

**Five Elements Casting:**
- ✅ Five distinct methods mapped to Chinese elements
- ✅ Each method uses different randomness source
- ✅ All methods produce authentic I Ching probabilities
- ✅ Earth method provides reproducible readings (seeded)
- ✅ Air method provides true physical randomness
- ✅ Traditional coin method preserved exactly

**Data Architecture:**
- ✅ Separation of data from code
- ✅ Human-readable JSON format
- ✅ Comprehensive metadata tracking
- ✅ Extensible schema for future additions
- ✅ Efficient caching and loading

**User Experience:**
- ✅ Choice of casting method with clear descriptions
- ✅ Choice of interpretation source
- ✅ Comparison view for scholarly study
- ✅ Reading persistence in JSON format
- ✅ Historical reading journal
- ✅ Rich metadata for each reading

### 6.2 Technical Outcomes

**Code Quality:**
- ✅ Modern Python 3.10+ patterns
- ✅ Type hints throughout
- ✅ Dataclasses for models
- ✅ Abstract base classes for extensibility
- ✅ Comprehensive test coverage
- ✅ Clear separation of concerns

**Maintainability:**
- ✅ Easy to add new sources (just add JSON)
- ✅ Easy to add new casting methods (inherit from base)
- ✅ Data validation and error handling
- ✅ Clear documentation
- ✅ Migration tools for data updates

**Cultural Respect:**
- ✅ Canonical source always preserved
- ✅ Full attribution for all translators
- ✅ Source URLs and provenance tracked
- ✅ Five Elements framework honored
- ✅ Traditional probabilities maintained

### 6.3 Success Criteria

**Essential:**
- ✅ All 5 casting methods working with correct probabilities
- ✅ Original Legge 1882 preserved as canonical
- ✅ At least 3 additional sources integrated
- ✅ Source comparison functionality working
- ✅ 100% test coverage on oracle logic
- ✅ JSON reading format working
- ✅ All 64 hexagrams validated

**Desired:**
- ✅ All 5 proposed sources integrated
- ✅ Comprehensive documentation
- ✅ Example readings and tutorials
- ✅ Migration tools for legacy data
- ✅ Performance benchmarks

**Stretch:**
- ⬜ Additional community sources from GitHub
- ⬜ Chinese language source
- ⬜ Automated source extraction tools
- ⬜ Web interface for source management

---

## 7. Design Decisions & Rationale

### 7.1 Why JSON Over YAML?

**Decision:** Use JSON for data files

**Rationale:**
- Standard library support (no dependencies)
- Universal compatibility
- Better tooling support
- User preference (stated)
- Slightly more verbose but clearer structure

### 7.2 Why Not Backward Compatible?

**Decision:** Deprecate `.psv` save format

**Rationale:**
- User indicated backward compatibility not required
- JSON format much more extensible
- Easier to add metadata
- Human-readable and editable
- Standard format for data exchange
- Migration tools can be provided if needed

### 7.3 Why Five Elements Framework?

**Decision:** Map casting methods to Wu Xing (Five Elements)

**Rationale:**
- Culturally appropriate for I Ching
- Clear conceptual framework
- User-specified requirement
- Each element represents different quality of randomness
- Educational value (teaches Chinese philosophy)

### 7.4 Why Canonical + Sources Structure?

**Decision:** Always maintain canonical (Legge 1882) with additional sources as overlay

**Rationale:**
- Preserves original (Phase 1 requirement)
- Clear reference point for all translations
- Enables meaningful comparison
- Graceful degradation (fallback to canonical)
- Scholarly rigor (traceable to original)
- Honors Stephen M. Gava's original work

### 7.5 Why Abstract Base Classes for Casting?

**Decision:** Use ABC pattern for casting methods

**Rationale:**
- Ensures consistent interface
- Easy to add new methods
- Type safety via static analysis
- Clear contract for implementers
- Testable independently
- Registry pattern works cleanly

### 7.6 Why Separate Loader and Resolver?

**Decision:** Split data loading from source resolution

**Rationale:**
- Single Responsibility Principle
- Loader handles files, Resolver handles logic
- Easier to test independently
- Can cache at loader level
- Can swap resolution strategies
- Cleaner architecture

---

## 8. Open Questions & Decisions Needed

### 8.1 Source Integration Priority

**Question:** Which sources should be integrated first after canonical?

**Options:**
1. Wilhelm/Baynes (most popular alternative)
2. Simplified Legge (easier to understand)
3. All simultaneously

**Recommendation:** Wilhelm/Baynes first (most widely used)

### 8.2 UI for Source Comparison

**Question:** How should source comparison be displayed?

**Options:**
1. Side-by-side columns
2. Tabbed interface
3. Sequential display with clear separation
4. Overlay with toggle

**Recommendation:** Start with tabbed, add side-by-side later

### 8.3 Default Casting Method

**Question:** What should be the default casting method?

**Options:**
1. Metal (traditional coin, original default)
2. Wood (standard PRNG, fastest)
3. Fire (cryptographic, highest quality local)
4. User choice on first run

**Recommendation:** Metal (maintains tradition and original behavior)

### 8.4 Offline Fallback for Air Method

**Question:** What should happen when Air method (RANDOM.ORG) is unavailable?

**Options:**
1. Fail with error, require user to choose different method
2. Automatic fallback to Fire (next highest quality)
3. Automatic fallback to Wood (standard)
4. Cache some values for offline use

**Recommendation:** Fail with helpful message suggesting Fire as alternative

### 8.5 Reading Journal Features

**Question:** Should we implement reading journal in this phase?

**Options:**
1. Yes, as part of JSON reading format
2. No, defer to Phase 3 (Enhanced Features)
3. Minimal version (just save/load)

**Recommendation:** Minimal version (just enhanced save/load with metadata)

---

## 9. Next Steps

### 9.1 Immediate Actions (This Sprint)

1. ✅ Complete this design document
2. ⬜ Get user approval on architecture
3. ⬜ Create `tools/convert_legacy_data.py`
4. ⬜ Convert all 64 hexagrams to JSON (canonical only)
5. ⬜ Validate JSON structure
6. ⬜ Commit to current branch

### 9.2 Phase 2 Kickoff (Next Sprint)

1. ⬜ Implement casting method base classes
2. ⬜ Implement all 5 element methods
3. ⬜ Write comprehensive tests
4. ⬜ Validate probability distributions

### 9.3 Documentation Needs

1. ⬜ Create `docs/casting_methods.md`
2. ⬜ Create `docs/data_sources.md`
3. ⬜ Create `docs/json_format.md`
4. ⬜ Update README.md with new features

---

## 10. Conclusion

This design provides a comprehensive, extensible architecture for:

1. **Multiple I Ching Translation Sources**
   - Canonical Legge 1882 preserved
   - Wilhelm, simplified Legge, Hermetica, DeKorne, and others
   - Easy addition of new sources
   - Source comparison for scholarship

2. **Five Elements Casting System**
   - Air: True RNG via RANDOM.ORG
   - Wood: Standard Mersenne Twister PRNG
   - Fire: Cryptographic CSPRNG
   - Earth: Deterministic seeded (reproducible)
   - Metal: Traditional coin with OS entropy

3. **Modern Data Architecture**
   - JSON-based, human-readable
   - Comprehensive metadata
   - Clear provenance tracking
   - Extensible schema

4. **Cultural Respect & Authenticity**
   - Original translation preserved
   - Traditional probabilities maintained
   - Five Elements framework
   - Full attribution

The architecture honors both the ancient wisdom of the I Ching and modern software engineering principles, creating a system that is respectful, extensible, and maintainable.

---

**Document End**

*For questions or clarifications, please refer to project notes or contact the development team.*
