"""
Core engine components for pyChing.

Provides modern dataclasses and engine logic that integrates:
- Phase 2: Five Elements casting methods
- Phase 3: Multi-source data access layer
- Backward compatibility with original algorithm
"""

from pyching.core.hexagram import Hexagram
from pyching.core.reading import Reading
from pyching.core.engine import HexagramEngine

__all__ = ['Hexagram', 'Reading', 'HexagramEngine']
