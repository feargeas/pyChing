#!/usr/bin/env python3
"""
Extract Wilhelm/Baynes I Ching Translation

Scrapes the Wilhelm/Baynes translation from web source and converts to JSON format
compatible with pyChing Phase 1 data structure.

Source: http://www2.unipr.it/~deyoung/I_Ching_Wilhelm_Translation.html
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from urllib.request import urlopen, Request
from html.parser import HTMLParser


# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


class WilhelmHTMLParser(HTMLParser):
    """Parse Wilhelm/Baynes HTML structure to extract hexagram data."""

    def __init__(self):
        super().__init__()
        self.hexagrams: Dict[int, Dict[str, Any]] = {}
        self.current_hexagram: Optional[int] = None
        self.current_section: Optional[str] = None
        self.current_line: Optional[int] = None
        self.text_buffer: list[str] = []
        self.in_relevant_tag = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        """Track when entering relevant tags."""
        # Implementation would depend on actual HTML structure
        pass

    def handle_endtag(self, tag: str) -> None:
        """Track when exiting relevant tags."""
        pass

    def handle_data(self, data: str) -> None:
        """Capture text data."""
        if self.in_relevant_tag:
            self.text_buffer.append(data.strip())


def fetch_wilhelm_html(url: str) -> str:
    """Fetch HTML content from Wilhelm/Baynes source.

    Args:
        url: Source URL

    Returns:
        HTML content as string

    Raises:
        Exception: If fetch fails
    """
    try:
        req = Request(url, headers={'User-Agent': 'pyChing/2.0 (Educational Project)'})
        with urlopen(req, timeout=30) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        raise Exception(f"Failed to fetch Wilhelm/Baynes HTML: {e}")


def parse_wilhelm_hexagram(html: str, hex_num: int) -> Optional[Dict[str, Any]]:
    """Parse a single hexagram from Wilhelm/Baynes HTML.

    Args:
        html: HTML content
        hex_num: Hexagram number (1-64)

    Returns:
        Hexagram data dict or None if not found
    """
    # This is a placeholder implementation
    # The actual implementation would need to:
    # 1. Find the section for this hexagram number
    # 2. Extract Chinese name
    # 3. Extract English name
    # 4. Extract Judgment section
    # 5. Extract Image section
    # 6. Extract line texts (6 lines)
    # 7. Structure according to Phase 1 JSON format

    # For now, return None to indicate manual extraction needed
    return None


def extract_wilhelm_hexagram(hex_num: int, html_content: str) -> Dict[str, Any]:
    """Extract Wilhelm/Baynes data for a single hexagram.

    Args:
        hex_num: Hexagram number (1-64)
        html_content: Full HTML content from source

    Returns:
        Wilhelm/Baynes source data dict
    """
    # Parse hexagram from HTML
    parsed = parse_wilhelm_hexagram(html_content, hex_num)

    if parsed is None:
        # Manual extraction required
        print(f"⚠ Hexagram {hex_num}: Manual extraction required")
        return create_placeholder_wilhelm(hex_num)

    # Convert to Phase 1 JSON structure
    return {
        "source_id": "wilhelm_baynes",
        "name": parsed.get('chinese_name', ''),
        "english_name": parsed.get('english_name', ''),
        "judgment": parsed.get('judgment', ''),
        "image": parsed.get('image', ''),
        "lines": {
            "1": {"position": "bottom", "type": "nine", "text": parsed.get('line_1', '')},
            "2": {"position": "second", "type": "nine", "text": parsed.get('line_2', '')},
            "3": {"position": "third", "type": "nine", "text": parsed.get('line_3', '')},
            "4": {"position": "fourth", "type": "nine", "text": parsed.get('line_4', '')},
            "5": {"position": "fifth", "type": "nine", "text": parsed.get('line_5', '')},
            "6": {"position": "top", "type": "nine", "text": parsed.get('line_6', '')}
        },
        "metadata": {
            "translator": "Richard Wilhelm / Cary F. Baynes",
            "year": 1950,
            "language": "en",
            "extraction_date": "2025-11-18",
            "verified": False,
            "url": "http://www2.unipr.it/~deyoung/I_Ching_Wilhelm_Translation.html"
        }
    }


def create_placeholder_wilhelm(hex_num: int) -> Dict[str, Any]:
    """Create placeholder entry for manual extraction.

    Args:
        hex_num: Hexagram number

    Returns:
        Placeholder data structure
    """
    return {
        "source_id": "wilhelm_baynes",
        "name": f"[Hexagram {hex_num} - Manual extraction needed]",
        "english_name": "[To be extracted]",
        "judgment": "[Wilhelm/Baynes judgment text to be extracted from source]",
        "image": "[Wilhelm/Baynes image text to be extracted from source]",
        "lines": {
            "1": {"position": "bottom", "type": "nine", "text": "[Line 1 to be extracted]"},
            "2": {"position": "second", "type": "nine", "text": "[Line 2 to be extracted]"},
            "3": {"position": "third", "type": "nine", "text": "[Line 3 to be extracted]"},
            "4": {"position": "fourth", "type": "nine", "text": "[Line 4 to be extracted]"},
            "5": {"position": "fifth", "type": "nine", "text": "[Line 5 to be extracted]"},
            "6": {"position": "top", "type": "nine", "text": "[Line 6 to be extracted]"}
        },
        "metadata": {
            "translator": "Richard Wilhelm / Cary F. Baynes",
            "year": 1950,
            "language": "en",
            "extraction_date": "2025-11-18",
            "verified": False,
            "manual_extraction_required": True,
            "url": "http://www2.unipr.it/~deyoung/I_Ching_Wilhelm_Translation.html"
        }
    }


def merge_wilhelm_source(hex_num: int, wilhelm_data: Dict[str, Any]) -> None:
    """Merge Wilhelm/Baynes data into existing hexagram JSON file.

    Args:
        hex_num: Hexagram number (1-64)
        wilhelm_data: Wilhelm/Baynes source data to merge
    """
    # Load existing hexagram file
    hex_file = Path(__file__).parent.parent / "data" / "hexagrams" / f"hexagram_{hex_num:02d}.json"

    if not hex_file.exists():
        raise FileNotFoundError(f"Hexagram file not found: {hex_file}")

    with open(hex_file, 'r', encoding='utf-8') as f:
        hex_data = json.load(f)

    # Add Wilhelm/Baynes to sources
    if "sources" not in hex_data:
        hex_data["sources"] = {}

    hex_data["sources"]["wilhelm_baynes"] = wilhelm_data

    # Write back
    with open(hex_file, 'w', encoding='utf-8') as f:
        json.dump(hex_data, f, indent=2, ensure_ascii=False)

    print(f"✓ Merged Wilhelm/Baynes data for Hexagram {hex_num}")


def extract_all_wilhelm(fetch_html: bool = False) -> None:
    """Extract all 64 Wilhelm/Baynes hexagrams.

    Args:
        fetch_html: If True, attempt to fetch from web. If False, create placeholders.
    """
    print("=" * 70)
    print("Wilhelm/Baynes Translation Extraction")
    print("=" * 70)
    print()

    html_content = None

    if fetch_html:
        print("Fetching HTML from source...")
        try:
            url = "http://www2.unipr.it/~deyoung/I_Ching_Wilhelm_Translation.html"
            html_content = fetch_wilhelm_html(url)
            print(f"✓ Fetched {len(html_content)} characters")
        except Exception as e:
            print(f"✗ Error fetching HTML: {e}")
            print("  Falling back to placeholder mode")
            html_content = None

    print()
    print("Extracting hexagrams...")
    print("-" * 70)

    extracted_count = 0
    placeholder_count = 0

    for hex_num in range(1, 65):
        try:
            # Extract Wilhelm/Baynes data
            wilhelm_data = extract_wilhelm_hexagram(hex_num, html_content or "")

            # Merge into existing JSON
            merge_wilhelm_source(hex_num, wilhelm_data)

            if wilhelm_data["metadata"].get("manual_extraction_required", False):
                placeholder_count += 1
            else:
                extracted_count += 1

        except Exception as e:
            print(f"✗ Hexagram {hex_num}: Error - {e}")

    print("-" * 70)
    print()
    print(f"Extraction complete:")
    print(f"  Extracted: {extracted_count}")
    print(f"  Placeholders: {placeholder_count}")
    print(f"  Total: {extracted_count + placeholder_count}")
    print()

    if placeholder_count > 0:
        print("⚠ Manual extraction required for placeholders")
        print("  Next steps:")
        print("  1. Visit the source URL")
        print("  2. Copy text for each hexagram")
        print("  3. Update JSON files manually or improve this script")
        print()


def validate_wilhelm_extraction() -> None:
    """Validate Wilhelm/Baynes extraction completeness and quality."""
    print("=" * 70)
    print("Validating Wilhelm/Baynes Extraction")
    print("=" * 70)
    print()

    data_dir = Path(__file__).parent.parent / "data" / "hexagrams"

    missing = []
    incomplete = []
    verified = []

    for hex_num in range(1, 65):
        hex_file = data_dir / f"hexagram_{hex_num:02d}.json"

        if not hex_file.exists():
            missing.append(hex_num)
            continue

        with open(hex_file, 'r', encoding='utf-8') as f:
            hex_data = json.load(f)

        if "sources" not in hex_data or "wilhelm_baynes" not in hex_data["sources"]:
            missing.append(hex_num)
            continue

        wilhelm = hex_data["sources"]["wilhelm_baynes"]

        # Check completeness
        if wilhelm["metadata"].get("manual_extraction_required", False):
            incomplete.append(hex_num)
        elif wilhelm["metadata"].get("verified", False):
            verified.append(hex_num)

    print(f"Wilhelm/Baynes Source Status:")
    print(f"  Missing: {len(missing)}")
    print(f"  Incomplete (placeholders): {len(incomplete)}")
    print(f"  Verified: {len(verified)}")
    print(f"  Total files: 64")
    print()

    if missing:
        print(f"⚠ Missing hexagrams: {missing}")
    if incomplete:
        print(f"⚠ Incomplete hexagrams: {incomplete[:10]}..." if len(incomplete) > 10 else f"⚠ Incomplete hexagrams: {incomplete}")
    if verified:
        print(f"✓ Verified hexagrams: {len(verified)}")
    print()


def main() -> int:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Extract Wilhelm/Baynes I Ching translation"
    )
    parser.add_argument(
        '--fetch',
        action='store_true',
        help="Attempt to fetch HTML from web (otherwise create placeholders)"
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        help="Validate existing extraction"
    )
    parser.add_argument(
        '--hexagram', '-n',
        type=int,
        choices=range(1, 65),
        help="Extract single hexagram (1-64)"
    )

    args = parser.parse_args()

    if args.validate:
        validate_wilhelm_extraction()
        return 0

    if args.hexagram:
        # Single hexagram extraction
        print(f"Extracting Hexagram {args.hexagram}...")
        try:
            html = fetch_wilhelm_html("http://www2.unipr.it/~deyoung/I_Ching_Wilhelm_Translation.html") if args.fetch else ""
            wilhelm_data = extract_wilhelm_hexagram(args.hexagram, html)
            merge_wilhelm_source(args.hexagram, wilhelm_data)
            print(f"✓ Complete")
        except Exception as e:
            print(f"✗ Error: {e}")
            return 1
    else:
        # All hexagrams
        extract_all_wilhelm(fetch_html=args.fetch)

    return 0


if __name__ == "__main__":
    sys.exit(main())
