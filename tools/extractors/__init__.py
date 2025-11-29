"""
Source extractor framework for pyChing.

This package provides a flexible, extensible system for extracting
I Ching hexagram data from various sources and formats.

Usage:
    from tools.extractors import ExtractorRegistry

    # Get the appropriate extractor
    extractor = ExtractorRegistry.get_extractor('wilhelm')

    # Extract all hexagrams
    extractor.extract_and_save_all('data/interpretations/wilhelm')
"""

from .base import BaseExtractor, SourceMetadata, HexagramData
from .registry import ExtractorRegistry
from .validator import YAMLValidator

__all__ = [
    'BaseExtractor',
    'SourceMetadata',
    'HexagramData',
    'ExtractorRegistry',
    'YAMLValidator',
]
