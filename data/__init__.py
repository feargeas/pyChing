"""
I Ching Hexagram Data Package

Provides lookup and visualization tools for the 64 hexagrams of the I Ching.
"""

from .hexagram_lookup import (
    HexagramData,
    lookup,
    get_hexagram_unicode,
    binary_to_hexagram,
    trigrams_to_hexagram,
    get_data
)

from .hexagram_svg import (
    HexagramSVG,
    create_trigram_svg,
    generate_trigram_svgs
)

__version__ = "1.0.0"

__all__ = [
    'HexagramData',
    'lookup',
    'get_hexagram_unicode',
    'binary_to_hexagram',
    'trigrams_to_hexagram',
    'get_data',
    'HexagramSVG',
    'create_trigram_svg',
    'generate_trigram_svgs',
]
