"""
Hexagram source resolver.

Resolves hexagram data from multiple sources with fallback logic.
Supports source comparison for scholarly study.
"""

from typing import Optional, Dict, Any, List
from .loader import HexagramDataLoader


class HexagramResolver:
    """
    Resolves hexagram data from multiple sources with fallback.

    Handles multi-source resolution:
    - Returns canonical source by default
    - Falls back to canonical if requested source unavailable
    - Merges incomplete sources with canonical
    - Supports side-by-side comparison
    """

    def __init__(self, loader: HexagramDataLoader = None):
        """
        Initialize the resolver.

        Args:
            loader: HexagramDataLoader instance. If None, creates default loader.
        """
        self.loader = loader or HexagramDataLoader()
        self._sources_metadata = None

    def _get_sources_metadata(self) -> Dict[str, Any]:
        """Lazy-load sources metadata."""
        if self._sources_metadata is None:
            self._sources_metadata = self.loader.load_sources_metadata()
        return self._sources_metadata

    def resolve(self,
                hexagram_id: str,
                source: str = 'canonical') -> Dict[str, Any]:
        """
        Resolve hexagram data from specified source.

        Args:
            hexagram_id: Hexagram identifier (e.g., "hexagram_01")
            source: Source ID (defaults to 'canonical')
                   For canonical, uses 'canonical' directly
                   For others, looks in sources dict

        Returns:
            dict: Resolved hexagram data formatted for display

        Raises:
            FileNotFoundError: If hexagram file doesn't exist
        """
        hex_data = self.loader.load_hexagram(hexagram_id)

        # If requesting canonical or source not available, return canonical
        if source == 'canonical' or source not in hex_data.get('sources', {}):
            return self._format_for_display(hex_data['canonical'], hex_data, source_id='canonical')

        # Get requested source
        source_data = hex_data['sources'][source]

        # Merge with canonical for missing fields
        merged = self._merge_with_canonical(source_data, hex_data['canonical'])

        return self._format_for_display(merged, hex_data, source_id=source)

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
                 Sources that don't exist are omitted
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
            list: Available source IDs (always includes 'canonical')
        """
        hex_data = self.loader.load_hexagram(hexagram_id)
        sources = ['canonical']
        sources.extend(hex_data.get('sources', {}).keys())
        return sources

    def get_source_info(self, source_id: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata about a source.

        Args:
            source_id: Source identifier

        Returns:
            dict: Source metadata (translator, year, URL, etc.)
            None: If source doesn't exist
        """
        metadata = self._get_sources_metadata()
        return metadata['sources'].get(source_id)

    def list_all_sources(self) -> List[Dict[str, Any]]:
        """
        List all registered sources.

        Returns:
            list: Source metadata dicts
        """
        metadata = self._get_sources_metadata()
        return list(metadata['sources'].values())

    def get_source_priority(self) -> List[str]:
        """
        Get default source priority order.

        Returns:
            list: Source IDs in priority order
        """
        metadata = self._get_sources_metadata()
        return metadata.get('source_priority', ['canonical'])

    def compare_sources(self,
                       hexagram_id: str,
                       sources: Optional[List[str]] = None,
                       field: Optional[str] = None) -> Dict[str, Any]:
        """
        Compare specific field across sources.

        Args:
            hexagram_id: Hexagram identifier
            sources: Sources to compare (None = all available)
            field: Specific field to compare (None = all fields)
                  Options: 'judgment', 'image', 'lines', 'name', etc.

        Returns:
            dict: Comparison results
                 If field specified: {source_id: field_value, ...}
                 If field None: {source_id: full_data, ...}
        """
        if sources is None:
            sources = self.get_available_sources(hexagram_id)

        # Resolve all sources
        resolved = self.resolve_multiple(hexagram_id, sources)

        if field is None:
            return resolved

        # Extract specific field
        comparison = {}
        for source_id, data in resolved.items():
            if field in data:
                comparison[source_id] = data[field]
            elif field == 'lines':
                # Lines is nested, return all lines
                comparison[source_id] = data.get('lines', {})

        return comparison

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
        # Start with canonical as base
        merged = canonical_data.copy()

        # Override with source-specific data where available
        for key in ['name', 'english_name', 'title', 'judgment', 'image', 'lines']:
            if key in source_data and source_data[key]:
                merged[key] = source_data[key]

        # Always include source metadata (not canonical's)
        if 'metadata' in source_data:
            merged['metadata'] = source_data['metadata']

        return merged

    def _format_for_display(self,
                           source_data: Dict[str, Any],
                           hex_data: Dict[str, Any],
                           source_id: str = None) -> Dict[str, Any]:
        """
        Format hexagram data for display, adding contextual information.

        Args:
            source_data: Resolved source data
            hex_data: Full hexagram data (for context like number, trigrams)
            source_id: Override source_id (if None, uses source_data's source_id)

        Returns:
            dict: Formatted data with context
        """
        if source_id is None:
            source_id = source_data.get('source_id', 'canonical')

        return {
            'hexagram_id': hex_data['hexagram_id'],
            'number': hex_data['number'],
            'binary': hex_data['binary'],
            'trigrams': hex_data['trigrams'],
            'name': source_data.get('name', ''),
            'english_name': source_data.get('english_name', ''),
            'title': source_data.get('title', ''),
            'judgment': source_data.get('judgment', ''),
            'image': source_data.get('image', ''),
            'lines': source_data.get('lines', {}),
            'metadata': source_data.get('metadata', {}),
            'source_id': source_id
        }

    def validate_source_completeness(self, hexagram_id: str, source_id: str) -> Dict[str, bool]:
        """
        Check completeness of a source for a hexagram.

        Args:
            hexagram_id: Hexagram identifier
            source_id: Source to validate

        Returns:
            dict: Completeness check results
                 {field_name: is_present, ...}
        """
        data = self.resolve(hexagram_id, source_id)

        required_fields = [
            'name', 'english_name', 'judgment', 'image',
            'lines'  # Lines dict should have all 6 lines
        ]

        completeness = {}
        for field in required_fields:
            if field == 'lines':
                # Check if all 6 lines present
                lines = data.get('lines', {})
                completeness['lines'] = all(
                    str(i) in lines for i in range(1, 7)
                )
            else:
                completeness[field] = bool(data.get(field))

        return completeness
