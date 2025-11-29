#!/usr/bin/env python3
"""
Base extractor classes for I Ching source extraction.

This module provides the abstract base class and common utilities for
extracting hexagram data from various sources (HTML, Markdown, DOC, PDF, etc.)
and converting them to the standardized YAML format.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import yaml


# Custom YAML representer to use literal block scalars for multi-line strings
class LiteralString(str):
    """String that should be dumped as literal block scalar."""
    pass


def literal_string_representer(dumper, data):
    """Represent strings with newlines as literal block scalars."""
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)


yaml.add_representer(LiteralString, literal_string_representer)


@dataclass
class SourceMetadata:
    """Metadata for an I Ching source."""
    source_id: str
    name: str
    translator: str
    year: int
    language: str = 'en'
    original_translator: Optional[str] = None
    source_url: Optional[str] = None
    description: Optional[str] = None
    license: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class HexagramData:
    """Extracted hexagram data (format-agnostic)."""
    hexagram_number: int
    chinese_name: str
    english_name: str
    judgment: str
    image: str
    lines: Dict[str, Dict[str, str]]  # {line_num: {position, type, text}}
    all_lines_changing: Optional[str] = None
    additional_sections: Optional[Dict[str, str]] = None


class BaseExtractor(ABC):
    """
    Abstract base class for source extractors.

    Each source format (HTML, Markdown, DOC, PDF) should implement
    this interface to provide a consistent extraction pipeline.

    Usage:
        extractor = WilhelmMarkdownExtractor(source_dir='data/sources/wilhelm')
        hex_data = extractor.extract_hexagram(1)
        extractor.save_to_yaml(hex_data, 'data/interpretations/wilhelm')
    """

    def __init__(self, source_dir: Path, metadata: SourceMetadata):
        """
        Initialize the extractor.

        Args:
            source_dir: Path to directory containing source files
            metadata: Source metadata (translator, year, etc.)
        """
        self.source_dir = Path(source_dir)
        self.metadata = metadata

        if not self.source_dir.exists():
            raise FileNotFoundError(f"Source directory not found: {source_dir}")

    @abstractmethod
    def extract_hexagram(self, hexagram_number: int) -> Optional[HexagramData]:
        """
        Extract data for a single hexagram.

        Args:
            hexagram_number: Hexagram number (1-64)

        Returns:
            HexagramData object or None if extraction failed
        """
        pass

    def extract_all_hexagrams(self) -> List[HexagramData]:
        """
        Extract all 64 hexagrams.

        Returns:
            List of successfully extracted HexagramData objects
        """
        results = []
        for i in range(1, 65):
            try:
                hex_data = self.extract_hexagram(i)
                if hex_data:
                    results.append(hex_data)
                    print(f"✓ Hexagram {i:02d}: {hex_data.chinese_name}")
                else:
                    print(f"✗ Hexagram {i:02d}: Extraction failed")
            except Exception as e:
                print(f"✗ Hexagram {i:02d}: Error - {e}")

        return results

    def convert_to_yaml_dict(self, hex_data: HexagramData) -> Dict[str, Any]:
        """
        Convert HexagramData to YAML-compatible dictionary.

        Args:
            hex_data: Extracted hexagram data

        Returns:
            Dictionary in standardized YAML format
        """
        # Get trigrams and binary from reference mappings
        from pyching.data import HexagramDataLoader
        loader = HexagramDataLoader(source='legge')
        ref_data = loader.get_hexagram_by_number(hex_data.hexagram_number)

        # Wrap multi-line strings in LiteralString for proper YAML formatting
        lines_formatted = {}
        for line_num, line_data in hex_data.lines.items():
            lines_formatted[line_num] = {
                'position': line_data['position'],
                'type': line_data['type'],
                'text': LiteralString(line_data['text'])
            }

        result = {
            'metadata': {
                'hexagram': hex_data.hexagram_number,
                'king_wen_sequence': hex_data.hexagram_number,
                'fu_xi_sequence': hex_data.hexagram_number,
                'binary': ref_data['binary'],
                'source': self.metadata.source_id,
                'translator': self.metadata.translator,
                'year': self.metadata.year,
                'language': self.metadata.language,
                'verified': False  # Must be manually verified
            },
            'name': hex_data.chinese_name,
            'english_name': hex_data.english_name,
            'title': f"{hex_data.hexagram_number}. {hex_data.chinese_name} / {hex_data.english_name}",
            'trigrams': ref_data['trigrams'],
            'judgment': LiteralString(hex_data.judgment),
            'image': LiteralString(hex_data.image),
            'lines': lines_formatted
        }

        # Add optional fields
        if hex_data.all_lines_changing:
            result['all_lines_changing'] = LiteralString(hex_data.all_lines_changing)

        if hex_data.additional_sections:
            result['additional_sections'] = {
                k: LiteralString(v) for k, v in hex_data.additional_sections.items()
            }

        return result

    def save_to_yaml(self,
                     hex_data: HexagramData,
                     output_dir: Path,
                     overwrite: bool = False) -> bool:
        """
        Save extracted hexagram data to YAML file.

        Args:
            hex_data: Extracted hexagram data
            output_dir: Directory to save YAML files
            overwrite: Whether to overwrite existing files

        Returns:
            True if saved successfully, False otherwise
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        yaml_file = output_path / f'hexagram_{hex_data.hexagram_number:02d}.yaml'

        # Check if file exists
        if yaml_file.exists() and not overwrite:
            print(f"⚠ Skipping hexagram {hex_data.hexagram_number:02d}: File exists (use --overwrite to replace)")
            return False

        # Convert to YAML format
        yaml_data = self.convert_to_yaml_dict(hex_data)

        # Write to file
        with open(yaml_file, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_data, f,
                     allow_unicode=True,
                     default_flow_style=False,
                     sort_keys=False)

        return True

    def extract_and_save_all(self,
                            output_dir: Path,
                            overwrite: bool = False) -> int:
        """
        Extract all hexagrams and save to YAML files.

        Args:
            output_dir: Directory to save YAML files
            overwrite: Whether to overwrite existing files

        Returns:
            Number of successfully extracted and saved hexagrams
        """
        print(f"Extracting all hexagrams from {self.metadata.name}...")
        print(f"Source: {self.source_dir}")
        print(f"Output: {output_dir}")
        print("-" * 70)

        extracted = self.extract_all_hexagrams()

        saved_count = 0
        for hex_data in extracted:
            if self.save_to_yaml(hex_data, output_dir, overwrite):
                saved_count += 1

        print("-" * 70)
        print(f"✓ Extracted and saved {saved_count}/{len(extracted)} hexagrams")

        return saved_count

    @abstractmethod
    def validate_source_files(self) -> bool:
        """
        Validate that required source files exist.

        Returns:
            True if all required files are present
        """
        pass

    def get_position_name(self, line_num: int) -> str:
        """Get standardized position name for line number."""
        positions = {
            1: 'bottom',
            2: 'second',
            3: 'third',
            4: 'fourth',
            5: 'fifth',
            6: 'topmost'
        }
        return positions.get(line_num, 'unknown')
