#!/usr/bin/env python3
"""
pyChing - Modern CLI Interface

Console/terminal interface for pyChing using the new HexagramEngine.
Supports all five casting methods and multi-source interpretations.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

from pyching import HexagramEngine, Element, Reading


def print_banner() -> None:
    """Display the pyChing console banner."""
    print("\n" + "="*70)
    print(f"  pyChing - I Ching Oracle - Modern Console Interface")
    print(f"  Version 2.0.0-alpha")
    print("="*70)
    print("\nWelcome to the I Ching oracle.")
    print("This ancient Chinese divination system uses randomness methods")
    print("to generate hexagrams that provide wisdom and guidance.\n")


def wrap_text(text: str, width: int = 70) -> str:
    """Wrap text to specified width."""
    words = text.split()
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        word_length = len(word)
        if current_length + word_length + len(current_line) <= width:
            current_line.append(word)
            current_length += word_length
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_length = word_length

    if current_line:
        lines.append(' '.join(current_line))

    return '\n'.join(lines)


def get_question() -> Optional[str]:
    """Prompt user for their question."""
    print("What question do you wish to ask the oracle?")
    print("(Maximum 70 characters, or press Ctrl+C to cancel)")
    print()
    while True:
        try:
            question = input("Question: ").strip()
            if len(question) == 0:
                print("Please enter a question.")
                continue
            if len(question) > 70:
                print(f"Question too long ({len(question)} characters). Please limit to 70.")
                continue
            return question
        except (EOFError, KeyboardInterrupt):
            print("\n\nCancelled.")
            return None


def get_method_choice(engine: HexagramEngine) -> Optional[Element]:
    """Prompt user to select casting method."""
    print("\nSelect casting method:")
    print("  1. Wood  - Standard PRNG (original algorithm)")
    print("  2. Metal - OS Entropy (highest quality local randomness)")
    print("  3. Fire  - Cryptographic CSPRNG (unpredictable)")
    print("  4. Earth - Deterministic (same question = same answer)")
    print("  5. Air   - True RNG via RANDOM.ORG (requires network)")
    print()

    while True:
        try:
            choice = input("Method [1-5, default=1]: ").strip()

            if choice == '' or choice == '1':
                return Element.WOOD
            elif choice == '2':
                return Element.METAL
            elif choice == '3':
                return Element.FIRE
            elif choice == '4':
                return Element.EARTH
            elif choice == '5':
                # Check availability
                available, error = engine.check_method_available(Element.AIR)
                if available:
                    return Element.AIR
                else:
                    print(f"\n⚠ Air method unavailable: {error}")
                    print("Suggestion: Use Fire method for high-quality randomness")
                    print("Please choose another method.\n")
                    continue
            else:
                print("Invalid choice. Please enter 1-5.")
        except (EOFError, KeyboardInterrupt):
            print("\n\nCancelled.")
            return None


def get_seed_for_earth() -> Optional[str]:
    """Prompt for seed when using Earth method."""
    print("\nEarth method requires a seed for deterministic casting.")
    print("Suggestion: Use your question as the seed.")
    print("(Press Enter to use question as seed, or provide custom seed)")
    print()

    try:
        seed = input("Seed [press Enter for question]: ").strip()
        return seed if seed else None  # None means use question
    except (EOFError, KeyboardInterrupt):
        print("\n\nCancelled.")
        return None


def display_reading(reading: Reading) -> None:
    """Display the complete reading in ASCII art."""
    print("\n" + "="*70)
    print("YOUR READING")
    print("="*70)

    # Use the Reading's as_text() method (backward compatible)
    reading_text = reading.as_text()
    print(reading_text)
    print("="*70 + "\n")


def display_interpretation(reading: Reading, verbose: bool = True) -> None:
    """Display the hexagram interpretation(s)."""
    print("\n" + "="*70)
    print("INTERPRETATION")
    print("="*70 + "\n")

    # Primary hexagram
    print(f"HEXAGRAM {reading.primary.number}: {reading.primary.name}")
    print(f"{reading.primary.english_name}")
    print("-" * 70)

    # Source attribution
    translator = reading.primary.metadata.get('translator', 'Unknown')
    year = reading.primary.metadata.get('year', '?')
    print(f"Source: {translator} ({year})")
    print()

    # Judgment
    print("JUDGMENT:")
    print(wrap_text(reading.primary.judgment, 70))

    # Image
    if verbose:
        print("\n\nIMAGE:")
        print(wrap_text(reading.primary.image, 70))

    # Moving lines
    if reading.has_moving_lines() and verbose:
        print("\n\nMOVING LINES:")
        for line_num in reading.changing_lines:
            line_data = reading.primary.line_texts[str(line_num)]
            print(f"\nLine {line_num} ({line_data['position']}, {line_data['type']}):")
            print(wrap_text(line_data['text'], 70))

    # Relating hexagram
    if reading.relating:
        print(f"\n\n{'='*70}")
        print(f"TRANSFORMATION TO HEXAGRAM {reading.relating.number}: {reading.relating.name}")
        print(f"{reading.relating.english_name}")
        print("-" * 70)

        print("\nJUDGMENT:")
        print(wrap_text(reading.relating.judgment, 70))

        if verbose:
            print("\n\nIMAGE:")
            print(wrap_text(reading.relating.image, 70))


def display_source_comparison(reading: Reading, sources: list[str]) -> None:
    """Display side-by-side comparison of sources."""
    from pyching.data import HexagramResolver

    resolver = HexagramResolver()

    print("\n" + "="*70)
    print("SOURCE COMPARISON - JUDGMENT")
    print("="*70)

    # Get hexagram with each source
    for source_id in sources:
        try:
            from pyching import Hexagram
            hex_data = Hexagram.from_number(reading.primary.number, source=source_id)

            source_info = resolver.get_source_info(source_id)
            translator = source_info.get('translator', 'Unknown') if source_info else 'Unknown'
            year = source_info.get('year', '?') if source_info else '?'

            print(f"\n{source_id.upper()} ({translator}, {year}):")
            print("-" * 70)
            print(wrap_text(hex_data.judgment, 70))

        except Exception as e:
            print(f"\n{source_id.upper()}: Error loading - {e}")


def interactive_mode(args: argparse.Namespace) -> int:
    """Run in interactive mode."""
    print_banner()

    engine = HexagramEngine()

    # Get question
    question = get_question()
    if question is None:
        return 1

    # Get method
    method = get_method_choice(engine)
    if method is None:
        return 1

    # Get seed if Earth method
    seed = None
    if method == Element.EARTH:
        seed_input = get_seed_for_earth()
        if seed_input is None:
            return 1
        seed = seed_input if seed_input else question  # Use question if no custom seed

    # Cast reading
    print("\n" + "-"*70)
    print(f"Casting with {method.value.upper()} method...")
    if seed:
        print(f"Seed: {seed}")
    print("-"*70 + "\n")

    try:
        reading = engine.cast_reading(
            method=method,
            question=question,
            source=args.source,
            seed=seed
        )
    except Exception as e:
        print(f"\n✗ Error casting reading: {e}\n")
        return 1

    # Display results
    display_reading(reading)
    display_interpretation(reading, verbose=not args.brief)

    # Source comparison if requested
    if args.compare:
        sources_to_compare = args.compare.split(',')
        display_source_comparison(reading, sources_to_compare)

    # Save if requested
    if args.save:
        try:
            reading.save(args.save)
            print(f"\n✓ Reading saved to {args.save}\n")
        except Exception as e:
            print(f"\n✗ Error saving reading: {e}\n")
            return 1

    return 0


def non_interactive_mode(args: argparse.Namespace) -> int:
    """Run in non-interactive mode with question provided."""
    engine = HexagramEngine()

    # Determine method
    method = Element(args.method)

    # Determine seed
    seed = None
    if method == Element.EARTH:
        seed = args.seed if args.seed else args.question

    # Cast reading
    try:
        reading = engine.cast_reading(
            method=method,
            question=args.question,
            source=args.source,
            seed=seed
        )
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1

    # Display results
    if not args.quiet:
        display_reading(reading)
        display_interpretation(reading, verbose=not args.brief)

        # Source comparison if requested
        if args.compare:
            sources_to_compare = args.compare.split(',')
            display_source_comparison(reading, sources_to_compare)

    # Save if requested
    if args.save:
        try:
            reading.save(args.save)
            if not args.quiet:
                print(f"\n✓ Reading saved to {args.save}\n")
        except Exception as e:
            print(f"✗ Error saving: {e}", file=sys.stderr)
            return 1

    return 0


def load_mode(args: argparse.Namespace) -> int:
    """Load and display a saved reading."""
    try:
        reading = Reading.load(args.load)

        if not args.quiet:
            print_banner()
            print(f"Loaded reading from {args.load}")
            print(f"Cast on: {reading.timestamp}")
            print(f"Method: {reading.method}")

            display_reading(reading)
            display_interpretation(reading, verbose=not args.brief)

        return 0

    except Exception as e:
        print(f"✗ Error loading reading: {e}", file=sys.stderr)
        return 1


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="pyChing - I Ching Oracle Console Interface",
        epilog="Examples:\n"
               "  %(prog)s                              # Interactive mode\n"
               "  %(prog)s -q 'What is my purpose?'     # Non-interactive\n"
               "  %(prog)s -m fire -q 'Question?'       # Fire method\n"
               "  %(prog)s -m earth --seed 'my seed'    # Deterministic\n"
               "  %(prog)s --compare canonical,wilhelm  # Compare sources\n"
               "  %(prog)s --load reading.json          # Load saved\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--method', '-m',
        choices=['wood', 'metal', 'fire', 'earth', 'air'],
        default='wood',
        help="Casting method (default: wood - original algorithm)"
    )

    parser.add_argument(
        '--source', '-s',
        default='canonical',
        help="Interpretation source (default: canonical/Legge 1882)"
    )

    parser.add_argument(
        '--seed',
        help="Seed for Earth method (defaults to question if not provided)"
    )

    parser.add_argument(
        '--question', '-q',
        help="Question to ask (enables non-interactive mode)"
    )

    parser.add_argument(
        '--compare', '-c',
        help="Compare sources (comma-separated list, e.g., canonical,wilhelm)"
    )

    parser.add_argument(
        '--save',
        help="Save reading to JSON file"
    )

    parser.add_argument(
        '--load', '-l',
        help="Load reading from JSON file"
    )

    parser.add_argument(
        '--brief', '-b',
        action='store_true',
        help="Brief output (judgment only, no image or line texts)"
    )

    parser.add_argument(
        '--quiet',
        action='store_true',
        help="Quiet mode (minimal output)"
    )

    parser.add_argument(
        '--version', '-v',
        action='version',
        version='pyChing 2.0.0-alpha'
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()

    # Load mode
    if args.load:
        return load_mode(args)

    # Non-interactive mode
    if args.question:
        return non_interactive_mode(args)

    # Interactive mode (default)
    return interactive_mode(args)


if __name__ == "__main__":
    sys.exit(main())
