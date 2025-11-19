"""
Reading dataclass - represents a complete I Ching divination reading.

Replaces the old Hexagrams class with modern JSON-serializable structure.
"""

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, Any, List, Optional

from pyching.core.hexagram import Hexagram


@dataclass
class Reading:
    """
    Represents a complete I Ching reading with primary and relating hexagrams.

    This modern dataclass replaces the old Hexagrams class, with support for:
    - JSON serialization for storage
    - Multiple casting methods (Five Elements)
    - Multiple interpretation sources
    - Question and timestamp tracking
    """

    primary: Hexagram
    """Primary hexagram (the present situation)"""

    relating: Optional[Hexagram] = None
    """Relating hexagram (future situation), None if no moving lines"""

    question: str = ""
    """The question asked (optional)"""

    timestamp: datetime = field(default_factory=datetime.now)
    """When the reading was cast"""

    method: str = "wood"
    """Casting method used (element name: wood, metal, fire, earth, air)"""

    source_id: str = "canonical"
    """Source used for interpretation"""

    changing_lines: List[int] = field(default_factory=list)
    """Positions of changing lines (1-6, bottom to top)"""

    oracle_values: List[List[int]] = field(default_factory=list)
    """Raw oracle values for each line (for reference/debugging)"""

    @classmethod
    def from_hexagrams(cls,
                      primary: Hexagram,
                      relating: Optional[Hexagram] = None,
                      question: str = "",
                      method: str = "wood",
                      oracle_values: Optional[List[List[int]]] = None) -> 'Reading':
        """
        Create reading from hexagram instances.

        Args:
            primary: Primary hexagram
            relating: Relating hexagram (optional)
            question: Question text
            method: Casting method name
            oracle_values: Raw oracle values from casting

        Returns:
            Reading instance
        """
        changing_lines = primary.get_moving_lines()

        return cls(
            primary=primary,
            relating=relating,
            question=question,
            timestamp=datetime.now(),
            method=method,
            source_id=primary.source_id,
            changing_lines=changing_lines,
            oracle_values=oracle_values or []
        )

    def has_moving_lines(self) -> bool:
        """
        Check if reading has any moving lines.

        Returns:
            True if there are moving lines
        """
        return len(self.changing_lines) > 0

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert reading to dictionary for serialization.

        Returns:
            Dictionary representation
        """
        return {
            'primary': self.primary.to_dict(),
            'relating': self.relating.to_dict() if self.relating else None,
            'question': self.question,
            'timestamp': self.timestamp.isoformat(),
            'method': self.method,
            'source_id': self.source_id,
            'changing_lines': self.changing_lines,
            'oracle_values': self.oracle_values
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Reading':
        """
        Create reading from dictionary (deserialization).

        Args:
            data: Dictionary representation

        Returns:
            Reading instance
        """
        primary = Hexagram.from_dict(data['primary'])
        relating = Hexagram.from_dict(data['relating']) if data.get('relating') else None

        return cls(
            primary=primary,
            relating=relating,
            question=data.get('question', ''),
            timestamp=datetime.fromisoformat(data['timestamp']),
            method=data.get('method', 'wood'),
            source_id=data.get('source_id', 'canonical'),
            changing_lines=data.get('changing_lines', []),
            oracle_values=data.get('oracle_values', [])
        )

    def to_json(self, indent: int = 2) -> str:
        """
        Serialize reading to JSON string.

        Args:
            indent: JSON indentation level (default: 2)

        Returns:
            JSON string

        Example:
            >>> reading = Reading(...)
            >>> json_str = reading.to_json()
            >>> with open('reading.json', 'w') as f:
            ...     f.write(json_str)
        """
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_json(cls, json_str: str) -> 'Reading':
        """
        Deserialize reading from JSON string.

        Args:
            json_str: JSON string

        Returns:
            Reading instance

        Example:
            >>> with open('reading.json', 'r') as f:
            ...     json_str = f.read()
            >>> reading = Reading.from_json(json_str)
        """
        data = json.loads(json_str)
        return cls.from_dict(data)

    def save(self, filename: str) -> None:
        """
        Save reading to JSON file.

        Args:
            filename: Path to output file

        Example:
            >>> reading.save('my_reading.json')
        """
        with open(filename, 'w') as f:
            f.write(self.to_json())

    @classmethod
    def load(cls, filename: str) -> 'Reading':
        """
        Load reading from JSON file.

        Args:
            filename: Path to input file

        Returns:
            Reading instance

        Example:
            >>> reading = Reading.load('my_reading.json')
        """
        with open(filename, 'r') as f:
            json_str = f.read()
        return cls.from_json(json_str)

    def as_text(self) -> str:
        """
        Create a multi-line text representation of the reading.

        This mimics the original ReadingAsText() format from the legacy code
        for backward compatibility with text-based interfaces.

        Returns:
            Formatted multi-line string

        Example output:
            1  The Creative                    No moving lines

              topmost   ------- (7 yang)
               fifth    ------- (7 yang)
              fourth    ------- (7 yang)
               third    ------- (7 yang)
              second    ------- (7 yang)
              bottom    ------- (7 yang)

            What is my purpose?
        """
        # Line representations
        line_strings = {
            6: '---X---',  # moving yin
            7: '-------',  # yang
            8: '--- ---',  # yin
            9: '---O---',  # moving yang
            0: ''  # empty (for relating hexagram when no moving lines)
        }

        line_positions = {
            1: 'bottom',
            2: 'second',
            3: 'third',
            4: 'fourth',
            5: 'fifth',
            6: 'topmost'
        }

        line_types = {
            6: '(6 moving yin)',
            7: '(7 yang)',
            8: '(8 yin)',
            9: '(9 moving yang)',
            0: ''
        }

        parts = []

        # Header line with hexagram numbers and names
        if self.relating:
            parts.append(f"\n              {str(self.primary.number).ljust(2)} "
                        f"{self.primary.english_name.ljust(30)} "
                        f"{str(self.relating.number).ljust(2)} {self.relating.english_name}\n\n")
        else:
            parts.append(f"\n              {str(self.primary.number).ljust(2)} "
                        f"{self.primary.english_name.ljust(30)} "
                        f"No moving lines\n\n")

        # Lines (from top to bottom for display)
        for i in range(5, -1, -1):
            # Add separator in middle
            if i == 3:
                if self.relating:
                    separator = '  becomes  '
                else:
                    separator = '           '
            else:
                separator = '           '

            # Primary hexagram line
            primary_line = self.primary.lines[i]
            line_str = (f" {line_positions[i + 1].rjust(9)}   "
                       f"{line_strings[primary_line]} "
                       f"{line_types[primary_line].ljust(15)}")

            # Relating hexagram line (if present)
            if self.relating:
                relating_line = self.relating.lines[i]
                line_str += (f"{separator}{line_strings[relating_line]} "
                           f"{line_types[relating_line]}")
            elif i == 3:  # Add "no moving lines" text in middle
                line_str += separator

            parts.append(line_str + '\n')

        # Question at bottom
        parts.append(f'\n {self.question}\n\n')

        return ''.join(parts)

    def __str__(self) -> str:
        """String representation for display."""
        if self.relating:
            return (f"Reading: Hexagram {self.primary.number} → "
                   f"{self.relating.number} ({len(self.changing_lines)} moving lines)")
        else:
            return f"Reading: Hexagram {self.primary.number} (no moving lines)"

    def __repr__(self) -> str:
        """Developer representation."""
        return (f"Reading(primary=Hexagram({self.primary.number}), "
                f"relating={f'Hexagram({self.relating.number})' if self.relating else None}, "
                f"method='{self.method}', source='{self.source_id}')")
