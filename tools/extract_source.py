#!/usr/bin/env python3
"""
Unified source extraction tool.

Extract hexagram data from any registered source and convert to YAML format.

Usage:
    # Extract all hexagrams from Wilhelm source
    ./extract_source.py wilhelm --all

    # Extract single hexagram
    ./extract_source.py wilhelm --hexagram 1

    # List available sources
    ./extract_source.py --list

    # Validate extracted YAML files
    ./extract_source.py wilhelm --validate

    # Extract with overwrite
    ./extract_source.py wilhelm --all --overwrite
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import extractors (this triggers registration)
from tools.extractors import ExtractorRegistry, YAMLValidator
from tools.extractors.wilhelm import WilhelmMarkdownExtractor  # noqa


def list_sources():
    """List all registered source extractors."""
    extractors = ExtractorRegistry.list_extractors()

    if not extractors:
        print("No extractors registered.")
        return

    print("=" * 70)
    print("Available Source Extractors")
    print("=" * 70)

    for source_id, metadata in extractors.items():
        print(f"\n{source_id}:")
        print(f"  Name: {metadata.name}")
        print(f"  Translator: {metadata.translator}")
        print(f"  Year: {metadata.year}")
        if metadata.source_url:
            print(f"  URL: {metadata.source_url}")
        if metadata.description:
            print(f"  Description: {metadata.description}")

    print()


def extract_hexagram(source_id: str, hexagram_num: int, output_dir: Path, overwrite: bool):
    """Extract a single hexagram."""
    try:
        extractor = ExtractorRegistry.get_extractor(source_id)
    except KeyError as e:
        print(f"Error: {e}")
        return False

    print(f"Extracting hexagram {hexagram_num} from {extractor.metadata.name}...")

    try:
        hex_data = extractor.extract_hexagram(hexagram_num)
        if not hex_data:
            print(f"✗ Failed to extract hexagram {hexagram_num}")
            return False

        if extractor.save_to_yaml(hex_data, output_dir, overwrite):
            print(f"✓ Saved hexagram {hexagram_num:02d}: {hex_data.chinese_name}")
            return True
        else:
            return False

    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def extract_all(source_id: str, output_dir: Path, overwrite: bool):
    """Extract all hexagrams from a source."""
    try:
        extractor = ExtractorRegistry.get_extractor(source_id)
    except KeyError as e:
        print(f"Error: {e}")
        return False

    # Validate source files exist
    if not extractor.validate_source_files():
        print(f"✗ Source files validation failed for {source_id}")
        return False

    # Extract and save all
    count = extractor.extract_and_save_all(output_dir, overwrite)

    return count == 64


def validate_yaml(source_id: str, strict: bool = False):
    """Validate extracted YAML files."""
    output_dir = Path('data/interpretations') / source_id

    if not output_dir.exists():
        print(f"✗ Directory not found: {output_dir}")
        return False

    validator = YAMLValidator(strict=strict)
    results = validator.validate_directory(output_dir)

    return validator.print_validation_report(results)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Extract I Ching hexagram data from various sources',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List available sources
  %(prog)s --list

  # Extract all hexagrams from Wilhelm
  %(prog)s wilhelm --all

  # Extract single hexagram
  %(prog)s wilhelm --hexagram 1

  # Validate extracted data
  %(prog)s wilhelm --validate

  # Extract with overwrite
  %(prog)s wilhelm --all --overwrite
        """
    )

    parser.add_argument(
        'source',
        nargs='?',
        help='Source ID (e.g., wilhelm, dekorne)'
    )

    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List all available source extractors'
    )

    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Extract all 64 hexagrams'
    )

    parser.add_argument(
        '--hexagram', '-n',
        type=int,
        metavar='N',
        help='Extract single hexagram (1-64)'
    )

    parser.add_argument(
        '--validate', '-v',
        action='store_true',
        help='Validate extracted YAML files'
    )

    parser.add_argument(
        '--output', '-o',
        type=Path,
        metavar='DIR',
        help='Output directory (default: data/interpretations/{source})'
    )

    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite existing files'
    )

    parser.add_argument(
        '--strict',
        action='store_true',
        help='Strict validation (warnings treated as errors)'
    )

    args = parser.parse_args()

    # List sources
    if args.list:
        list_sources()
        return 0

    # Validate source argument
    if not args.source:
        parser.error('source is required (unless using --list)')

    # Default output directory
    if args.output is None:
        args.output = Path('data/interpretations') / args.source

    # Validation mode
    if args.validate:
        success = validate_yaml(args.source, strict=args.strict)
        return 0 if success else 1

    # Extract single hexagram
    if args.hexagram:
        if not 1 <= args.hexagram <= 64:
            parser.error(f'hexagram must be 1-64, got {args.hexagram}')

        success = extract_hexagram(args.source, args.hexagram, args.output, args.overwrite)
        return 0 if success else 1

    # Extract all hexagrams
    if args.all:
        success = extract_all(args.source, args.output, args.overwrite)
        return 0 if success else 1

    # No action specified
    parser.error('specify --all, --hexagram, --validate, or --list')


if __name__ == '__main__':
    sys.exit(main())
