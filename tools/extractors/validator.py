#!/usr/bin/env python3
"""
YAML schema validator for hexagram data.

Ensures all extracted YAML files conform to the expected structure
and contain all required fields.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of YAML validation."""
    valid: bool
    errors: List[str]
    warnings: List[str]
    hexagram_number: int
    source_id: str


class YAMLValidator:
    """
    Validates hexagram YAML files against the expected schema.

    Checks for:
    - Required fields (metadata, name, judgment, image, lines)
    - Correct data types
    - Complete line data (all 6 lines)
    - Valid metadata fields
    - Text quality (no placeholders, reasonable length)
    """

    REQUIRED_FIELDS = {
        'metadata', 'name', 'english_name', 'title',
        'trigrams', 'judgment', 'image', 'lines'
    }

    REQUIRED_METADATA = {
        'hexagram', 'king_wen_sequence', 'binary', 'source',
        'translator', 'year', 'language', 'verified'
    }

    REQUIRED_LINE_FIELDS = {'position', 'type', 'text'}

    def __init__(self, strict: bool = False):
        """
        Initialize validator.

        Args:
            strict: If True, warnings are treated as errors
        """
        self.strict = strict

    def validate_file(self, yaml_file: Path) -> ValidationResult:
        """
        Validate a single YAML file.

        Args:
            yaml_file: Path to YAML file

        Returns:
            ValidationResult with details
        """
        errors = []
        warnings = []

        # Load YAML
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except Exception as e:
            return ValidationResult(
                valid=False,
                errors=[f"Failed to load YAML: {e}"],
                warnings=[],
                hexagram_number=0,
                source_id='unknown'
            )

        # Extract basic info
        hex_num = data.get('metadata', {}).get('hexagram', 0)
        source_id = data.get('metadata', {}).get('source', 'unknown')

        # Check required top-level fields
        missing_fields = self.REQUIRED_FIELDS - set(data.keys())
        if missing_fields:
            errors.append(f"Missing required fields: {missing_fields}")

        # Validate metadata
        metadata_errors = self._validate_metadata(data.get('metadata', {}))
        errors.extend(metadata_errors)

        # Validate lines
        line_errors, line_warnings = self._validate_lines(data.get('lines', {}))
        errors.extend(line_errors)
        warnings.extend(line_warnings)

        # Validate text content
        content_warnings = self._validate_content(data)
        warnings.extend(content_warnings)

        # Determine overall validity
        valid = len(errors) == 0
        if self.strict:
            valid = valid and len(warnings) == 0

        return ValidationResult(
            valid=valid,
            errors=errors,
            warnings=warnings,
            hexagram_number=hex_num,
            source_id=source_id
        )

    def validate_directory(self, directory: Path) -> List[ValidationResult]:
        """
        Validate all YAML files in a directory.

        Args:
            directory: Directory containing hexagram YAML files

        Returns:
            List of validation results
        """
        results = []

        yaml_files = sorted(Path(directory).glob('hexagram_*.yaml'))

        for yaml_file in yaml_files:
            result = self.validate_file(yaml_file)
            results.append(result)

        return results

    def print_validation_report(self, results: List[ValidationResult]) -> bool:
        """
        Print validation report to console.

        Args:
            results: List of validation results

        Returns:
            True if all files valid, False otherwise
        """
        total = len(results)
        valid = sum(1 for r in results if r.valid)
        invalid = total - valid

        print("=" * 70)
        print("YAML Validation Report")
        print("=" * 70)
        print(f"Total files: {total}")
        print(f"Valid: {valid}")
        print(f"Invalid: {invalid}")
        print()

        # Show details for invalid files
        if invalid > 0:
            print("Invalid Files:")
            print("-" * 70)
            for result in results:
                if not result.valid:
                    print(f"\nHexagram {result.hexagram_number:02d} ({result.source_id}):")
                    for error in result.errors:
                        print(f"  ✗ ERROR: {error}")
                    for warning in result.warnings:
                        print(f"  ⚠ WARNING: {warning}")

        # Show warnings for valid files if any
        valid_with_warnings = [r for r in results if r.valid and r.warnings]
        if valid_with_warnings:
            print("\nValid Files with Warnings:")
            print("-" * 70)
            for result in valid_with_warnings:
                print(f"\nHexagram {result.hexagram_number:02d} ({result.source_id}):")
                for warning in result.warnings:
                    print(f"  ⚠ {warning}")

        print("\n" + "=" * 70)
        return invalid == 0

    def _validate_metadata(self, metadata: Dict[str, Any]) -> List[str]:
        """Validate metadata section."""
        errors = []

        missing = self.REQUIRED_METADATA - set(metadata.keys())
        if missing:
            errors.append(f"Missing metadata fields: {missing}")

        # Type checks
        if 'hexagram' in metadata and not isinstance(metadata['hexagram'], int):
            errors.append("metadata.hexagram must be an integer")

        if 'hexagram' in metadata and not 1 <= metadata['hexagram'] <= 64:
            errors.append(f"metadata.hexagram must be 1-64, got {metadata['hexagram']}")

        if 'year' in metadata and not isinstance(metadata['year'], int):
            errors.append("metadata.year must be an integer")

        if 'verified' in metadata and not isinstance(metadata['verified'], bool):
            errors.append("metadata.verified must be a boolean")

        return errors

    def _validate_lines(self, lines: Dict[str, Any]) -> tuple[List[str], List[str]]:
        """Validate lines section."""
        errors = []
        warnings = []

        # Check all 6 lines present
        expected_lines = {'1', '2', '3', '4', '5', '6'}
        actual_lines = set(lines.keys())

        missing = expected_lines - actual_lines
        if missing:
            errors.append(f"Missing lines: {missing}")

        extra = actual_lines - expected_lines
        if extra:
            warnings.append(f"Extra line keys: {extra}")

        # Validate each line
        for line_num in expected_lines:
            if line_num not in lines:
                continue

            line_data = lines[line_num]

            if not isinstance(line_data, dict):
                errors.append(f"Line {line_num} must be a dict, got {type(line_data)}")
                continue

            # Check required fields
            missing_fields = self.REQUIRED_LINE_FIELDS - set(line_data.keys())
            if missing_fields:
                errors.append(f"Line {line_num} missing fields: {missing_fields}")

            # Check text length
            text = line_data.get('text', '')
            if len(text) < 10:
                warnings.append(f"Line {line_num} text suspiciously short ({len(text)} chars)")

        return errors, warnings

    def _validate_content(self, data: Dict[str, Any]) -> List[str]:
        """Validate text content quality."""
        warnings = []

        # Check for placeholder text
        placeholder_patterns = [
            'to be extracted',
            'manual extraction',
            'placeholder',
            '[...]',
            'TODO',
        ]

        for field in ['judgment', 'image', 'name', 'english_name']:
            text = str(data.get(field, '')).lower()
            for pattern in placeholder_patterns:
                if pattern.lower() in text:
                    warnings.append(f"Field '{field}' contains placeholder text: {pattern}")

        # Check minimum text lengths
        judgment = data.get('judgment', '')
        if len(judgment) < 50:
            warnings.append(f"Judgment text suspiciously short ({len(judgment)} chars)")

        image = data.get('image', '')
        if len(image) < 50:
            warnings.append(f"Image text suspiciously short ({len(image)} chars)")

        return warnings
