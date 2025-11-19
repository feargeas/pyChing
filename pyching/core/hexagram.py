"""
Hexagram dataclass - modern representation of an I Ching hexagram.

Uses Phase 3 data access layer for multi-source content retrieval.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

from pyching.data import HexagramDataLoader, HexagramResolver


@dataclass
class Hexagram:
    """
    Represents a single I Ching hexagram with its associated data.

    This modern dataclass replaces the old Hexagram class, integrating
    with the Phase 3 data access layer for flexible source selection.
    """

    number: int
    """Hexagram number (1-64) in King Wen sequence"""

    name: str
    """Chinese romanized name (e.g., "Tch'ien", "Koun")"""

    english_name: str
    """English name (e.g., "The Creative", "The Receptive")"""

    binary: str
    """Six-digit binary pattern (e.g., "111111" for qian)"""

    trigrams: Dict[str, str]
    """Upper and lower trigrams (e.g., {"upper": "qian", "lower": "qian"})"""

    lines: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0, 0])
    """Line values (6, 7, 8, or 9). 0 means not yet set."""

    judgment: str = ""
    """Judgment text from selected source"""

    image: str = ""
    """Image text from selected source"""

    line_texts: Dict[str, Dict[str, str]] = field(default_factory=dict)
    """Line interpretation texts"""

    source_id: str = "canonical"
    """Source ID for the hexagram data"""

    metadata: Dict[str, Any] = field(default_factory=dict)
    """Additional metadata (translator, year, etc.)"""

    _full_data: Optional[Dict[str, Any]] = field(default=None, repr=False)
    """Full hexagram data from resolver (private)"""

    @classmethod
    def from_number(cls,
                   number: int,
                   source: str = "canonical",
                   lines: Optional[List[int]] = None) -> 'Hexagram':
        """
        Create hexagram from King Wen number.

        Args:
            number: Hexagram number (1-64)
            source: Source ID for interpretation (default: canonical)
            lines: Optional line values to set

        Returns:
            Hexagram instance

        Example:
            >>> hex1 = Hexagram.from_number(1)
            >>> print(hex1.english_name)
            'The Creative'
        """
        loader = HexagramDataLoader()
        resolver = HexagramResolver(loader)

        # Get hexagram data from specified source
        hex_data = resolver.resolve(f"hexagram_{number:02d}", source=source)

        return cls._from_resolved_data(hex_data, lines)

    @classmethod
    def from_lines(cls,
                  lines: List[int],
                  source: str = "canonical") -> 'Hexagram':
        """
        Create hexagram from line values.

        Moving lines (6, 9) are automatically converted to stable form
        for hexagram identification.

        Args:
            lines: List of 6 line values (6, 7, 8, or 9)
            source: Source ID for interpretation

        Returns:
            Hexagram instance

        Example:
            >>> hex1 = Hexagram.from_lines([7, 7, 7, 7, 7, 7])
            >>> print(hex1.number)
            1
        """
        if len(lines) != 6:
            raise ValueError(f"Must provide 6 line values, got {len(lines)}")

        loader = HexagramDataLoader()
        resolver = HexagramResolver(loader)

        # Loader handles moving line conversion automatically
        hex_data_raw = loader.get_hexagram_by_lines(lines)
        hex_data = resolver.resolve(hex_data_raw['hexagram_id'], source=source)

        return cls._from_resolved_data(hex_data, lines)

    @classmethod
    def from_binary(cls,
                   binary: str,
                   source: str = "canonical",
                   lines: Optional[List[int]] = None) -> 'Hexagram':
        """
        Create hexagram from binary pattern.

        Args:
            binary: 6-digit binary string (e.g., "111111")
            source: Source ID for interpretation
            lines: Optional line values to set

        Returns:
            Hexagram instance
        """
        loader = HexagramDataLoader()
        resolver = HexagramResolver(loader)

        hex_data_raw = loader.get_hexagram_by_binary(binary)
        hex_data = resolver.resolve(hex_data_raw['hexagram_id'], source=source)

        return cls._from_resolved_data(hex_data, lines)

    @classmethod
    def from_trigrams(cls,
                     upper: str,
                     lower: str,
                     source: str = "canonical",
                     lines: Optional[List[int]] = None) -> 'Hexagram':
        """
        Create hexagram from trigram pair.

        Args:
            upper: Upper trigram name (qian, kun, zhen, kan, gen, xun, li, dui)
            lower: Lower trigram name
            source: Source ID for interpretation
            lines: Optional line values to set

        Returns:
            Hexagram instance
        """
        loader = HexagramDataLoader()
        resolver = HexagramResolver(loader)

        hex_data_raw = loader.get_hexagram_by_trigrams(upper, lower)
        hex_data = resolver.resolve(hex_data_raw['hexagram_id'], source=source)

        return cls._from_resolved_data(hex_data, lines)

    @classmethod
    def _from_resolved_data(cls,
                           hex_data: Dict[str, Any],
                           lines: Optional[List[int]] = None) -> 'Hexagram':
        """
        Create hexagram from resolved data (internal helper).

        Args:
            hex_data: Resolved hexagram data from HexagramResolver
            lines: Optional line values to set

        Returns:
            Hexagram instance
        """
        # Extract line texts
        line_texts = hex_data.get('lines', {})

        # Set lines if provided, otherwise leave as zeros
        if lines is None:
            lines = [0, 0, 0, 0, 0, 0]

        return cls(
            number=hex_data['number'],
            name=hex_data.get('name', ''),
            english_name=hex_data.get('english_name', ''),
            binary=hex_data['binary'],
            trigrams=hex_data['trigrams'],
            lines=lines.copy() if lines else [0, 0, 0, 0, 0, 0],
            judgment=hex_data.get('judgment', ''),
            image=hex_data.get('image', ''),
            line_texts=line_texts,
            source_id=hex_data['source_id'],
            metadata=hex_data.get('metadata', {}),
            _full_data=hex_data
        )

    def has_moving_lines(self) -> bool:
        """
        Check if hexagram has any moving lines (6 or 9).

        Returns:
            True if any lines are moving (6 or 9)
        """
        return any(line in [6, 9] for line in self.lines)

    def get_moving_lines(self) -> List[int]:
        """
        Get list of moving line positions (1-6, bottom to top).

        Returns:
            List of line positions (1-indexed) that are moving

        Example:
            >>> hex1 = Hexagram.from_lines([7, 9, 8, 7, 6, 7])
            >>> hex1.get_moving_lines()
            [2, 5]
        """
        return [i + 1 for i, line in enumerate(self.lines) if line in [6, 9]]

    def to_stable_lines(self) -> List[int]:
        """
        Convert line values to stable form (6→8, 9→7).

        Used for hexagram identification.

        Returns:
            List of stable line values
        """
        stable = []
        for line in self.lines:
            if line == 6:
                stable.append(8)
            elif line == 9:
                stable.append(7)
            else:
                stable.append(line)
        return stable

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert hexagram to dictionary for serialization.

        Returns:
            Dictionary representation
        """
        return {
            'number': self.number,
            'name': self.name,
            'english_name': self.english_name,
            'binary': self.binary,
            'trigrams': self.trigrams,
            'lines': self.lines,
            'judgment': self.judgment,
            'image': self.image,
            'line_texts': self.line_texts,
            'source_id': self.source_id,
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Hexagram':
        """
        Create hexagram from dictionary (deserialization).

        Args:
            data: Dictionary representation

        Returns:
            Hexagram instance
        """
        return cls(
            number=data['number'],
            name=data['name'],
            english_name=data['english_name'],
            binary=data['binary'],
            trigrams=data['trigrams'],
            lines=data.get('lines', [0, 0, 0, 0, 0, 0]),
            judgment=data.get('judgment', ''),
            image=data.get('image', ''),
            line_texts=data.get('line_texts', {}),
            source_id=data.get('source_id', 'canonical'),
            metadata=data.get('metadata', {})
        )

    def __str__(self) -> str:
        """String representation for display."""
        return f"Hexagram {self.number}: {self.english_name}"

    def __repr__(self) -> str:
        """Developer representation."""
        return (f"Hexagram(number={self.number}, english_name='{self.english_name}', "
                f"binary='{self.binary}', source='{self.source_id}')")
