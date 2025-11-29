#!/usr/bin/env python3
"""
Extractor registry for managing source extractors.

This module provides a central registry for all source extractors,
allowing for dynamic discovery and instantiation of extractors.
"""

from typing import Dict, Type, Optional
from pathlib import Path
from .base import BaseExtractor, SourceMetadata


class ExtractorRegistry:
    """
    Central registry for source extractors.

    New extractors are automatically registered when their module is imported.
    Use the @ExtractorRegistry.register decorator to add extractors.
    """

    _extractors: Dict[str, Type[BaseExtractor]] = {}
    _metadata: Dict[str, SourceMetadata] = {}

    @classmethod
    def register(cls,
                 source_id: str,
                 metadata: SourceMetadata):
        """
        Decorator to register an extractor class.

        Args:
            source_id: Unique identifier for this source
            metadata: Source metadata

        Usage:
            @ExtractorRegistry.register('wilhelm', metadata)
            class WilhelmExtractor(BaseExtractor):
                ...
        """
        def decorator(extractor_class: Type[BaseExtractor]):
            cls._extractors[source_id] = extractor_class
            cls._metadata[source_id] = metadata
            return extractor_class
        return decorator

    @classmethod
    def get_extractor(cls,
                     source_id: str,
                     source_dir: Optional[Path] = None) -> BaseExtractor:
        """
        Get an extractor instance for a source.

        Args:
            source_id: Source identifier
            source_dir: Override default source directory

        Returns:
            Configured extractor instance

        Raises:
            KeyError: If source_id not registered
        """
        if source_id not in cls._extractors:
            available = ', '.join(cls._extractors.keys())
            raise KeyError(
                f"Unknown source '{source_id}'. "
                f"Available extractors: {available}"
            )

        metadata = cls._metadata[source_id]
        extractor_class = cls._extractors[source_id]

        # Use default source directory if not specified
        if source_dir is None:
            source_dir = Path('data/sources') / source_id

        return extractor_class(source_dir, metadata)

    @classmethod
    def list_extractors(cls) -> Dict[str, SourceMetadata]:
        """
        List all registered extractors.

        Returns:
            Dictionary of source_id -> metadata
        """
        return cls._metadata.copy()

    @classmethod
    def is_registered(cls, source_id: str) -> bool:
        """Check if a source extractor is registered."""
        return source_id in cls._extractors
