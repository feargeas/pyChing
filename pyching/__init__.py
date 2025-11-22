"""
pyChing - Modern I Ching oracle with multi-source translations and five elements casting.

This package provides a complete I Ching divination system with:
- Multiple translation sources (Legge, Wilhelm, etc.)
- Five element casting methods (Metal, Wood, Fire, Earth, Water)
- Modern Python architecture with type hints and dataclasses
- JSON-based data storage for easy maintenance and extension

Cultural respect and authenticity are core principles.

Quick Start:
    >>> from pyching import HexagramEngine, Element
    >>> engine = HexagramEngine()
    >>> reading = engine.cast_reading(Element.WOOD, "What is my purpose?")
    >>> print(reading.as_text())
"""

__version__ = "2.0.0-alpha"
__author__ = "Stephen M. Gava (original), modernized by Claude"
__license__ = "GPL v2+"

# Core engine and dataclasses (Phase 4)
from pyching.core.engine import HexagramEngine
from pyching.core.hexagram import Hexagram
from pyching.core.reading import Reading

# Casting methods (Phase 2)
from pyching.casting.base import Element, CastingMethod
from pyching.casting.wood import WoodMethod
from pyching.casting.metal import MetalMethod
from pyching.casting.fire import FireMethod
from pyching.casting.earth import EarthMethod
from pyching.casting.water import WaterMethod
from pyching.casting.registry import CastingMethodRegistry

# Data access layer (Phase 3)
from pyching.data.loader import HexagramDataLoader
from pyching.data.resolver import HexagramResolver

__all__ = [
    # Version info
    '__version__',
    '__author__',
    '__license__',

    # Main API (most users will only need these)
    'HexagramEngine',
    'Hexagram',
    'Reading',
    'Element',

    # Casting methods (for advanced usage)
    'CastingMethod',
    'WoodMethod',
    'MetalMethod',
    'FireMethod',
    'EarthMethod',
    'WaterMethod',
    'CastingMethodRegistry',

    # Data access (for advanced usage or custom sources)
    'HexagramDataLoader',
    'HexagramResolver',
]
