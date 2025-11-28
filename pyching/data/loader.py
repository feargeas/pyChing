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
            source: Default source to load from (default: 'legge')
        """
        if data_dir is None:
            # Default to data/ directory relative to project root
            # pyching/data/loader.py -> pyching -> project_root -> data
            data_dir = Path(__file__).parent.parent.parent / 'data'

        self.data_dir = Path(data_dir)
        self.source = source
        self.interpretations_dir = self.data_dir / 'interpretations' / source
        self.mappings_path = self.data_dir / 'mappings.json'
        self.sources_path = self.data_dir / 'sources_metadata.json'

        # Caches
        self._hexagram_cache: Dict[str, Dict[str, Any]] = {}
        self._mappings: Optional[Dict[str, Any]] = None
        self._sources: Optional[Dict[str, Any]] = None

    def load_hexagram(self, hexagram_id: str) -> Dict[str, Any]:
        """
        Load a hexagram by ID.

        Args:
            hexagram_id: Hexagram identifier (e.g., "hexagram_01")

        Returns:
            dict: Complete hexagram data from YAML

        Raises:
            FileNotFoundError: If hexagram file doesn't exist
            yaml.YAMLError: If file contains invalid YAML
        """
        # Check cache first
        if hexagram_id in self._hexagram_cache:
            return self._hexagram_cache[hexagram_id]

        # Load from YAML file
        hex_file = self.interpretations_dir / f"{hexagram_id}.yaml"

        if not hex_file.exists():
            raise FileNotFoundError(
                f"Hexagram file not found: {hex_file}. "
                f"Expected hexagram_id format: 'hexagram_NN' where NN is 01-64"
            )

        with open(hex_file, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)

        # Transform YAML structure to match old JSON structure for backward compatibility
        # YAML is flattened, but existing code expects nested 'canonical' section
        data = {
            'hexagram_id': hexagram_id,
            'number': yaml_data['metadata']['hexagram'],
            'king_wen_sequence': yaml_data['metadata']['king_wen_sequence'],
            'fu_xi_sequence': yaml_data['metadata']['fu_xi_sequence'],
            'binary': yaml_data['metadata']['binary'],
            'trigrams': yaml_data['trigrams'],
            'canonical': {
                'source_id': yaml_data['metadata']['source'],
                'name': yaml_data['name'],
                'english_name': yaml_data['english_name'],
                'title': yaml_data['title'],
                'judgment': yaml_data['judgment'],
                'image': yaml_data['image'],
                'lines': yaml_data['lines'],
                'metadata': {
                    'translator': yaml_data['metadata']['translator'],
                    'year': yaml_data['metadata']['year'],
                    'language': yaml_data['metadata']['language'],
                    'verified': yaml_data['metadata']['verified']
                }
            },
            'sources': {}  # Placeholder for future multi-source support
        }

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
