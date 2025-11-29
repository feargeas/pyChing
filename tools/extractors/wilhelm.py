#!/usr/bin/env python3
"""
Wilhelm/Baynes Markdown extractor.

Extracts hexagram data from Wilhelm/Baynes translation in Markdown format.
"""

import re
from pathlib import Path
from typing import Dict, Any, Optional

from .base import BaseExtractor, SourceMetadata, HexagramData
from .registry import ExtractorRegistry


# Source metadata
WILHELM_METADATA = SourceMetadata(
    source_id='wilhelm_baynes',
    name='Wilhelm/Baynes Translation',
    translator='Richard Wilhelm / Cary F. Baynes',
    year=1950,
    language='en',
    description='Richard Wilhelm\'s German translation rendered into English by Cary F. Baynes',
    source_url='http://www2.unipr.it/~deyoung/I_Ching_Wilhelm_Translation.html',
    license='Public Domain',
    notes='Influential Western translation with introduction by Carl Jung'
)


@ExtractorRegistry.register('wilhelm', WILHELM_METADATA)
class WilhelmMarkdownExtractor(BaseExtractor):
    """
    Extractor for Wilhelm/Baynes translation from Markdown.

    Expects a markdown file at: {source_dir}/wilhelm.md

    Format:
        ## 1. Ch'ien / The Creative
        THE JUDGMENT
        [judgment text]

        THE IMAGE
        [image text]

        THE LINES
        Nine at the beginning means:
        [line 1 text]
        ...
    """

    def __init__(self, source_dir: Path, metadata: SourceMetadata = WILHELM_METADATA):
        super().__init__(source_dir, metadata)
        self.md_file = self.source_dir / 'wilhelm.md'

        # Load markdown content once
        if not self.md_file.exists():
            # Try alternative name
            self.md_file = self.source_dir / 'wilhelm.txt'
            if not self.md_file.exists():
                raise FileNotFoundError(
                    f"Wilhelm markdown not found in {source_dir}. "
                    f"Expected: wilhelm.md or wilhelm.txt"
                )

        with open(self.md_file, 'r', encoding='utf-8') as f:
            self.md_content = f.read()

    def extract_hexagram(self, hexagram_number: int) -> Optional[HexagramData]:
        """Extract a single hexagram from the markdown."""
        # Find hexagram section
        pattern = rf"^## {hexagram_number}\. (.+?) / (.+?)$"
        lines = self.md_content.split('\n')

        # Find start
        start_idx = None
        chinese_name = None
        english_name = None

        for i, line in enumerate(lines):
            match = re.match(pattern, line)
            if match:
                start_idx = i
                chinese_name = match.group(1).strip().replace("\\'", "'")
                english_name = match.group(2).strip()
                break

        if start_idx is None:
            return None

        # Find end (next hexagram or EOF)
        end_idx = len(lines)
        for i in range(start_idx + 1, len(lines)):
            if re.match(r"^## \d+\.", lines[i]):
                end_idx = i
                break

        hex_lines = lines[start_idx:end_idx]

        # Extract sections
        judgment = self._extract_section(hex_lines, "THE JUDGMENT")
        image = self._extract_section(hex_lines, "THE IMAGE")
        line_texts, all_lines_changing = self._extract_lines(hex_lines)

        if not judgment or not image or len(line_texts) != 6:
            return None

        return HexagramData(
            hexagram_number=hexagram_number,
            chinese_name=chinese_name,
            english_name=english_name,
            judgment=judgment.strip(),
            image=image.strip(),
            lines=line_texts,
            all_lines_changing=all_lines_changing
        )

    def _extract_section(self, hex_lines: list[str], section_name: str) -> Optional[str]:
        """Extract text from a named section."""
        section_start = None
        for i, line in enumerate(hex_lines):
            stripped = line.strip()
            if stripped == section_name or stripped == section_name + '.':
                section_start = i + 1
                break

        if section_start is None:
            return None

        text_lines = []
        for i in range(section_start, len(hex_lines)):
            line = hex_lines[i].strip()

            # Stop at next section
            if line in ['THE JUDGMENT', 'THE IMAGE', 'THE IMAGE.', 'THE LINES']:
                break

            if not text_lines and not line:
                continue

            if line:
                text_lines.append(line)
            elif text_lines:
                text_lines.append('')

        text = '\n'.join(text_lines).strip()
        text = re.sub(r'\n{3,}', '\n\n', text)

        return text

    def _extract_lines(self, hex_lines: list[str]) -> tuple[Dict[str, Dict[str, str]], Optional[str]]:
        """Extract the 6 line interpretations."""
        lines_start = None
        for i, line in enumerate(hex_lines):
            if line.strip() == 'THE LINES':
                lines_start = i + 1
                break

        if lines_start is None:
            return {}, None

        line_patterns = [
            (r"^(Nine|Six) (at|in) the beginning means:", 1),
            (r"^(Nine|Six) in the second place means:", 2),
            (r"^(Nine|Six) in the third place means:", 3),
            (r"^(Nine|Six) in the fourth place means:", 4),
            (r"^(Nine|Six) in the fifth place means:", 5),
            (r"^(Nine|Six) at the top means:", 6),
        ]

        line_texts = {}
        current_line_num = None
        current_text = []
        all_lines_changing = None

        for i in range(lines_start, len(hex_lines)):
            line = hex_lines[i].strip()

            # Skip navigation
            if line in ['[index](#index)', ''] or re.match(r'^\[\]\{#\d+\}', line):
                continue

            # Check for "all lines changing"
            if re.match(r'^When all the lines are (nines|sixes)', line):
                if current_line_num is not None:
                    text = '\n'.join(current_text[1:]).strip()
                    text = self._clean_markdown(text)
                    line_texts[str(current_line_num)] = {
                        'position': self.get_position_name(current_line_num),
                        'type': 'nine' if current_text[0].startswith('Nine') else 'six',
                        'text': text
                    }

                all_lines_text = [line]
                for j in range(i + 1, len(hex_lines)):
                    next_line = hex_lines[j].strip()
                    if next_line == '[index](#index)' or re.match(r'^\[\]\{#\d+\}', next_line):
                        break
                    all_lines_text.append(next_line)

                all_lines_changing = '\n'.join(all_lines_text).strip()
                all_lines_changing = self._clean_markdown(all_lines_changing)
                break

            # Check for new line marker
            matched = False
            for pattern, line_num in line_patterns:
                if re.match(pattern, line):
                    if current_line_num is not None:
                        text = '\n'.join(current_text[1:]).strip()
                        text = self._clean_markdown(text)
                        line_texts[str(current_line_num)] = {
                            'position': self.get_position_name(current_line_num),
                            'type': 'nine' if current_text[0].startswith('Nine') else 'six',
                            'text': text
                        }

                    current_line_num = line_num
                    current_text = [line]
                    matched = True
                    break

            if not matched and current_line_num is not None:
                if line:
                    current_text.append(line)

        # Save last line
        if current_line_num is not None and all_lines_changing is None:
            text = '\n'.join(current_text[1:]).strip()
            text = self._clean_markdown(text)
            line_texts[str(current_line_num)] = {
                'position': self.get_position_name(current_line_num),
                'type': 'nine' if current_text[0].startswith('Nine') else 'six',
                'text': text
            }

        return line_texts, all_lines_changing

    def _clean_markdown(self, text: str) -> str:
        """Remove markdown artifacts."""
        text = re.sub(r'\[index\]\(#index\)', '', text)
        text = re.sub(r'\[\]\{#\d+\}', '', text)
        text = re.sub(r'\[(\d+)\]\(#\d+\)', r'\1', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    def validate_source_files(self) -> bool:
        """Validate that required source files exist."""
        return self.md_file.exists()
