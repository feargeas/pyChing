"""
Hexagram data loader.

Loads hexagram data from YAML files with caching for performance.
"""

import json
import yaml
from pathlib import Path
from typing import Optional, Dict, Any


class HexagramDataLoader:
    """
    Loads hexagram data from YAML files.

    Provides efficient loading with caching and multiple lookup methods:
    - By hexagram number (1-64)
    - By binary pattern (e.g., "111111")
    - By line values (e.g., [7, 7, 7, 7, 7, 7])
    - By trigram pair (e.g., "qian_qian")
    """

    def __init__(self, data_dir: Path = None, source: str = 'legge'):
        """
        Initialize the loader.

        Args:
            data_dir: Path to data directory. If None, uses default
                     (project_root/data)
            source: Default/canonical source to use (default: 'legge')
        """
        if data_dir is None:
            # Default to data/ directory relative to project root
            # pyching/data/loader.py -> pyching -> project_root -> data
            data_dir = Path(__file__).parent.parent.parent / 'data'

        self.data_dir = Path(data_dir)
        self.source = source
        self.interpretations_dir = self.data_dir / 'interpretations'
        self.mappings_path = self.data_dir / 'mappings.json'
        self.sources_path = self.data_dir / 'sources_metadata.json'

        # Caches
        self._hexagram_cache: Dict[str, Dict[str, Any]] = {}
        self._mappings: Optional[Dict[str, Any]] = None
        self._sources: Optional[Dict[str, Any]] = None

    def load_hexagram(self, hexagram_id: str) -> Dict[str, Any]:
        """
        Load a hexagram by ID from all available sources.

        Args:
            hexagram_id: Hexagram identifier (e.g., "hexagram_01")

        Returns:
            dict: Complete hexagram data with canonical and all available sources

        Raises:
            FileNotFoundError: If hexagram file doesn't exist in any source
            yaml.YAMLError: If file contains invalid YAML
        """
        # Check cache first
        if hexagram_id in self._hexagram_cache:
            return self._hexagram_cache[hexagram_id]

        # Load canonical source (default)
        canonical_file = self.interpretations_dir / self.source / f"{hexagram_id}.yaml"

        if not canonical_file.exists():
            raise FileNotFoundError(
                f"Hexagram file not found: {canonical_file}. "
                f"Expected hexagram_id format: 'hexagram_NN' where NN is 01-64"
            )

        with open(canonical_file, 'r', encoding='utf-8') as f:
            canonical_yaml = yaml.safe_load(f)

        # Build base structure from canonical source
        data = {
            'hexagram_id': hexagram_id,
            'number': canonical_yaml['metadata']['hexagram'],
            'king_wen_sequence': canonical_yaml['metadata']['king_wen_sequence'],
            'fu_xi_sequence': canonical_yaml['metadata']['fu_xi_sequence'],
            'binary': canonical_yaml['metadata']['binary'],
            'trigrams': canonical_yaml['trigrams'],
            'canonical': {
                'source_id': canonical_yaml['metadata']['source'],
                'name': canonical_yaml['name'],
                'english_name': canonical_yaml['english_name'],
                'title': canonical_yaml['title'],
                'judgment': canonical_yaml['judgment'],
                'image': canonical_yaml['image'],
                'lines': canonical_yaml['lines'],
                'metadata': {
                    'translator': canonical_yaml['metadata']['translator'],
                    'year': canonical_yaml['metadata']['year'],
                    'language': canonical_yaml['metadata']['language'],
                    'verified': canonical_yaml['metadata']['verified']
                }
            },
            'sources': {}
        }

        # Load all other available sources
        if self.interpretations_dir.exists():
            for source_dir in self.interpretations_dir.iterdir():
                if not source_dir.is_dir():
                    continue

                source_name = source_dir.name

                # Skip canonical source (already loaded)
                if source_name == self.source:
                    continue

                source_file = source_dir / f"{hexagram_id}.yaml"
                if source_file.exists():
                    try:
                        with open(source_file, 'r', encoding='utf-8') as f:
                            source_yaml = yaml.safe_load(f)

                        # Map source directory name to source_id from metadata
                        source_id = source_yaml['metadata']['source']

                        data['sources'][source_id] = {
                            'source_id': source_id,
                            'name': source_yaml['name'],
                            'english_name': source_yaml['english_name'],
                            'title': source_yaml['title'],
                            'judgment': source_yaml['judgment'],
                            'image': source_yaml['image'],
                            'lines': source_yaml['lines'],
                            'metadata': {
                                'translator': source_yaml['metadata']['translator'],
                                'year': source_yaml['metadata']['year'],
                                'language': source_yaml['metadata']['language'],
                                'verified': source_yaml['metadata']['verified']
                            }
                        }
                    except (yaml.YAMLError, KeyError) as e:
                        # Skip malformed source files
                        print(f"Warning: Could not load source {source_name} for {hexagram_id}: {e}")
                        continue

        # Cache and return
        self._hexagram_cache[hexagram_id] = data
        return data

    def load_mappings(self) -> Dict[str, Any]:
        """
        Load mapping tables (number, binary, trigrams, etc.).

        Returns:
            dict: Mapping tables

        Raises:
            FileNotFoundError: If mappings file doesn't exist
        """
        if self._mappings is not None:
            return self._mappings

        with open(self.mappings_path, 'r', encoding='utf-8') as f:
            self._mappings = json.load(f)

        return self._mappings

    def load_sources_metadata(self) -> Dict[str, Any]:
        """
        Load source metadata (translator info, URLs, etc.).

        Returns:
            dict: Source metadata

        Raises:
            FileNotFoundError: If sources file doesn't exist
        """
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

        Raises:
            ValueError: If number is out of range
            KeyError: If number not in mappings
        """
        if not 1 <= number <= 64:
            raise ValueError(f"Hexagram number must be 1-64, got {number}")

        mappings = self.load_mappings()
        hexagram_id = mappings['number_to_id'][str(number)]
        return self.load_hexagram(hexagram_id)

    def get_hexagram_by_binary(self, binary: str) -> Dict[str, Any]:
        """
        Get hexagram by binary pattern.

        Args:
            binary: 6-character binary string (e.g., "111111")
                   1 = yang (line value 7)
                   0 = yin (line value 8)

        Returns:
            dict: Hexagram data

        Raises:
            ValueError: If binary string invalid
            KeyError: If binary pattern not found
        """
        if len(binary) != 6:
            raise ValueError(f"Binary pattern must be 6 characters, got {len(binary)}")

        if not all(c in '01' for c in binary):
            raise ValueError(f"Binary pattern must contain only 0 and 1, got {binary}")

        mappings = self.load_mappings()
        hexagram_id = mappings['binary_to_id'][binary]
        return self.load_hexagram(hexagram_id)

    def get_hexagram_by_lines(self, lines: list[int]) -> Dict[str, Any]:
        """
        Get hexagram by line values.

        Moving lines (6, 9) are converted to stable form (8, 7) for lookup.

        Args:
            lines: List of 6 line values (6, 7, 8, or 9)

        Returns:
            dict: Hexagram data

        Raises:
            ValueError: If lines list invalid
        """
        if len(lines) != 6:
            raise ValueError(f"Must provide 6 line values, got {len(lines)}")

        # Convert to stable form (moving lines -> stable)
        stable_lines = []
        for line in lines:
            if line not in [6, 7, 8, 9]:
                raise ValueError(f"Line values must be 6, 7, 8, or 9, got {line}")

            if line == 6:  # old yin -> yin
                stable_lines.append(8)
            elif line == 9:  # old yang -> yang
                stable_lines.append(7)
            else:  # already stable
                stable_lines.append(line)

        # Convert to binary
        # 7 (yang) = 1, 8 (yin) = 0
        binary = ''.join('1' if line == 7 else '0' for line in reversed(stable_lines))

        return self.get_hexagram_by_binary(binary)

    def get_hexagram_by_trigrams(self, upper: str, lower: str) -> Dict[str, Any]:
        """
        Get hexagram by trigram pair.

        Args:
            upper: Upper trigram name (e.g., "qian")
            lower: Lower trigram name (e.g., "kun")

        Returns:
            dict: Hexagram data

        Raises:
            KeyError: If trigram pair not found
        """
        mappings = self.load_mappings()
        trigram_key = f"{upper}_{lower}"
        hexagram_id = mappings['trigram_pairs_to_id'][trigram_key]
        return self.load_hexagram(hexagram_id)

    def get_hexagram_by_name(self, name: str) -> Dict[str, Any]:
        """
        Get hexagram by name variant.

        Args:
            name: Hexagram name (e.g., "Tch'ien", "Ch'ien", "Qian")

        Returns:
            dict: Hexagram data

        Raises:
            KeyError: If name not found in variants
        """
        mappings = self.load_mappings()
        name_info = mappings['name_variants'][name]
        hexagram_id = name_info['hexagram_id']
        return self.load_hexagram(hexagram_id)

    def clear_cache(self) -> None:
        """Clear all caches (useful for testing or memory management)."""
        self._hexagram_cache.clear()
        self._mappings = None
        self._sources = None

    def get_cache_stats(self) -> Dict[str, int]:
        """
        Get cache statistics.

        Returns:
            dict: Cache statistics (cached hexagrams, mappings loaded, etc.)
        """
        return {
            'hexagrams_cached': len(self._hexagram_cache),
            'mappings_loaded': self._mappings is not None,
            'sources_loaded': self._sources is not None,
        }
