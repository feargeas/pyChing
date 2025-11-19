"""
SVG Generator for I Ching Hexagrams

Generates SVG representations of hexagrams with customizable styling.
"""

from typing import Optional, Tuple
from pathlib import Path
import json


class HexagramSVG:
    """Generate SVG images for I Ching hexagrams."""

    def __init__(self,
                 line_width: int = 100,
                 line_height: int = 8,
                 line_gap: int = 12,
                 broken_gap: int = 20,
                 stroke_color: str = "#000000",
                 stroke_width: int = 2,
                 background: str = "transparent"):
        """
        Initialize SVG generator with styling parameters.

        Args:
            line_width: Width of each line in pixels
            line_height: Height of each line in pixels
            line_gap: Vertical gap between lines in pixels
            broken_gap: Gap in the middle of broken lines in pixels
            stroke_color: Color of lines (hex or named color)
            stroke_width: Width of line stroke
            background: Background color or 'transparent'
        """
        self.line_width = line_width
        self.line_height = line_height
        self.line_gap = line_gap
        self.broken_gap = broken_gap
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self.background = background

    def binary_to_svg(self, binary: str, title: Optional[str] = None) -> str:
        """
        Generate SVG from binary representation.

        Args:
            binary: 6-character binary string (e.g., '111111')
            title: Optional title for the SVG

        Returns:
            SVG string
        """
        if len(binary) != 6 or not all(c in '01' for c in binary):
            raise ValueError("Binary must be 6 characters of 0s and 1s")

        # Calculate dimensions
        height = 6 * self.line_height + 5 * self.line_gap
        width = self.line_width

        # Start SVG
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}">'
        ]

        if title:
            svg_parts.append(f'  <title>{title}</title>')

        # Add background if not transparent
        if self.background != "transparent":
            svg_parts.append(
                f'  <rect width="{width}" height="{height}" '
                f'fill="{self.background}"/>'
            )

        # Draw lines from bottom to top (index 0 is bottom line)
        for i, bit in enumerate(reversed(binary)):
            y = i * (self.line_height + self.line_gap)

            if bit == '1':
                # Solid line (yang)
                svg_parts.append(
                    f'  <rect x="0" y="{y}" '
                    f'width="{self.line_width}" height="{self.line_height}" '
                    f'fill="{self.stroke_color}" '
                    f'stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>'
                )
            else:
                # Broken line (yin)
                segment_width = (self.line_width - self.broken_gap) / 2
                # Left segment
                svg_parts.append(
                    f'  <rect x="0" y="{y}" '
                    f'width="{segment_width}" height="{self.line_height}" '
                    f'fill="{self.stroke_color}" '
                    f'stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>'
                )
                # Right segment
                svg_parts.append(
                    f'  <rect x="{segment_width + self.broken_gap}" y="{y}" '
                    f'width="{segment_width}" height="{self.line_height}" '
                    f'fill="{self.stroke_color}" '
                    f'stroke="{self.stroke_color}" stroke-width="{self.stroke_width}"/>'
                )

        svg_parts.append('</svg>')
        return '\n'.join(svg_parts)

    def hexagram_to_svg(self, hexagram_dict: dict) -> str:
        """
        Generate SVG from hexagram dictionary.

        Args:
            hexagram_dict: Hexagram dictionary from hexagrams.json

        Returns:
            SVG string
        """
        title = f"{hexagram_dict['number']}. {hexagram_dict['english']}"
        return self.binary_to_svg(hexagram_dict['binary'], title)

    def number_to_svg(self, number: int) -> str:
        """
        Generate SVG for hexagram by King Wen number.

        Args:
            number: Hexagram number (1-64)

        Returns:
            SVG string
        """
        from .hexagram_lookup import lookup
        hexagram = lookup(number)
        if not hexagram:
            raise ValueError(f"Invalid hexagram number: {number}")
        return self.hexagram_to_svg(hexagram)

    def save_svg(self, svg_content: str, filepath: Path):
        """Save SVG content to file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg_content)

    def generate_all(self, output_dir: Path):
        """
        Generate SVG files for all 64 hexagrams.

        Args:
            output_dir: Directory to save SVG files
        """
        from .hexagram_lookup import HexagramData

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        data = HexagramData()

        for hexagram in data.get_all():
            svg = self.hexagram_to_svg(hexagram)
            filename = f"hexagram_{hexagram['number']:02d}.svg"
            filepath = output_dir / filename
            self.save_svg(svg, filepath)
            print(f"Generated: {filename}")


def create_trigram_svg(trigram_binary: str,
                      width: int = 100,
                      height: int = 50) -> str:
    """
    Create SVG for a single trigram.

    Args:
        trigram_binary: 3-character binary string
        width: SVG width
        height: SVG height

    Returns:
        SVG string
    """
    generator = HexagramSVG(
        line_width=width,
        line_height=8,
        line_gap=8,
        broken_gap=20
    )

    # Pad to 6 characters to use existing generator
    # But calculate height for 3 lines only
    actual_height = 3 * generator.line_height + 2 * generator.line_gap

    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{actual_height}" viewBox="0 0 {width} {actual_height}">'

    for i, bit in enumerate(reversed(trigram_binary)):
        y = i * (generator.line_height + generator.line_gap)

        if bit == '1':
            # Solid line
            svg += f'<rect x="0" y="{y}" width="{width}" height="{generator.line_height}" fill="{generator.stroke_color}"/>'
        else:
            # Broken line
            segment_width = (width - generator.broken_gap) / 2
            svg += f'<rect x="0" y="{y}" width="{segment_width}" height="{generator.line_height}" fill="{generator.stroke_color}"/>'
            svg += f'<rect x="{segment_width + generator.broken_gap}" y="{y}" width="{segment_width}" height="{generator.line_height}" fill="{generator.stroke_color}"/>'

    svg += '</svg>'
    return svg


def generate_trigram_svgs(output_dir: Path):
    """Generate SVG files for all 8 trigrams."""
    from .hexagram_lookup import HexagramData

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    data = HexagramData()

    for name, trigram in data.trigrams.items():
        svg = create_trigram_svg(trigram['binary'])
        filename = f"trigram_{name}.svg"
        filepath = output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg)

        print(f"Generated: {filename}")


if __name__ == '__main__':
    import sys

    # Generate all hexagram SVGs
    output_dir = Path(__file__).parent / "svg"

    print("Generating hexagram SVGs...")
    generator = HexagramSVG()
    generator.generate_all(output_dir)

    print("\nGenerating trigram SVGs...")
    generate_trigram_svgs(output_dir)

    print(f"\nAll SVGs generated in: {output_dir}")
