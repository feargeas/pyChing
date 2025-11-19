# Phase 5: Additional Source Integration - Plan

**Project:** pyChing Multi-Source I Ching Oracle Modernization
**Phase:** 5 of 6 - Additional Translation Sources
**Date:** 2025-11-18
**Status:** PLANNED (Implementation deferred - data extraction required)

---

## Executive Summary

Phase 5 involves extracting and integrating additional I Ching translation sources into the JSON data structure created in Phase 1. This expands the multi-source interpretation capability demonstrated in Phase 3.

### Target Sources

1. **Wilhelm/Baynes Translation** (1950) - Most influential Western translation
2. **Simplified Legge** (TwoDreams.us, 2020) - Modern language version
3. **Hermetica I Ching** (PDF) - Alternative interpretation
4. **DeKorne's Gnostic Book of Changes** - Esoteric perspective

### Current Status

**Phase 3 Infrastructure**: ✓ Complete and tested
- `HexagramResolver` can handle multiple sources
- Fallback to canonical source working
- Comparison functionality ready

**Data Structure**: ✓ Defined and validated
- JSON schema supports multiple sources
- Each hexagram JSON has "sources" key ready
- Metadata registry in place

**Sources Available**: ⚠ Data extraction needed
- Canonical (Legge 1882): ✓ Complete (Phase 1)
- Wilhelm/Baynes: ⏳ Needs web scraping
- Simplified Legge: ⏳ Needs web scraping
- Hermetica: ⏳ Needs PDF extraction
- DeKorne: ⏳ Needs HTML parsing

---

## Objectives

### Primary Goals

1. **Extract Wilhelm/Baynes**: Scrape complete translation from web source
2. **Extract Simplified Legge**: Parse modernized version from TwoDreams
3. **Extract Hermetica**: Convert PDF to structured data
4. **Extract DeKorne**: Parse HTML into JSON format
5. **Validate All Sources**: Ensure completeness and accuracy

### Quality Standards

- **Completeness**: All 64 hexagrams for each source
- **Accuracy**: Preserve original text exactly (no paraphrasing)
- **Attribution**: Proper metadata (translator, year, URL, license)
- **Verification**: Each source marked as verified after manual review
- **Formatting**: Consistent structure across all sources

---

## Data Sources

### Source 1: Wilhelm/Baynes Translation

**Details:**
- **Translator**: Richard Wilhelm (German) / Cary F. Baynes (English)
- **Year**: 1950 (German), 1967 (English)
- **URL**: http://www2.unipr.it/~deyoung/I_Ching_Wilhelm_Translation.html
- **Format**: HTML
- **License**: Public domain (?)
- **Completeness Target**: 100% (all 64 hexagrams)
- **Cultural Significance**: Most influential Western I Ching, Jung's introduction

**Extraction Method:**
1. Web scraping with Beautiful Soup or similar
2. Parse HTML structure to identify hexagrams
3. Extract hexagram name, judgment, image, line texts
4. Handle any special formatting (italics, footnotes)
5. Validate against original text

**JSON Structure:**
```json
{
  "hexagram_id": "hexagram_01",
  "sources": {
    "wilhelm_baynes": {
      "source_id": "wilhelm_baynes",
      "name": "Ch'ien",
      "english_name": "The Creative",
      "judgment": "THE CREATIVE works sublime success...",
      "image": "The movement of heaven is full of power...",
      "lines": {
        "1": {"position": "bottom", "type": "nine", "text": "..."},
        ...
      },
      "metadata": {
        "translator": "Richard Wilhelm / Cary F. Baynes",
        "year": 1950,
        "language": "en",
        "verified": true
      }
    }
  }
}
```

### Source 2: Simplified Legge (TwoDreams)

**Details:**
- **Translator**: Simplified by TwoDreams.us
- **Original**: James Legge (1882)
- **Year**: 2020
- **URL**: https://twodreams.us/blog/a-simplified-version-of-james-legges-translation-of-the-i-ching
- **Format**: HTML/Web
- **License**: TBD (need to verify)
- **Completeness Target**: 100%
- **Purpose**: Modernize Legge's archaic language for contemporary readers

**Extraction Method:**
1. Web scraping from TwoDreams blog/site
2. Parse simplified text for each hexagram
3. Map to original Legge structure
4. Preserve modernized language exactly
5. Compare with canonical Legge for verification

**Benefits:**
- Easier to read than Victorian English
- Maintains Legge's scholarly accuracy
- Appeals to modern users
- Good for comparing traditional vs. modern language

### Source 3: Hermetica I Ching

**Details:**
- **URL**: https://www.hermetica.info/Yijing1+2.pdf
- **Format**: PDF
- **License**: TBD
- **Completeness Target**: TBD (need to assess PDF content)
- **Purpose**: Hermetic/esoteric interpretation

**Extraction Method:**
1. PDF parsing with PyPDF2, pdfminer, or similar
2. Text extraction and structure identification
3. OCR if necessary for image-based PDF
4. Manual verification of extraction accuracy
5. Structure mapping to JSON format

**Challenges:**
- PDF formatting may be complex
- May require manual cleanup
- Verification of completeness needed
- License/permission verification

### Source 4: DeKorne's Gnostic Book of Changes

**Details:**
- **Author**: James DeKorne
- **URL**: https://jamesdekorne.com/GBCh/GBCh.htm
- **Format**: HTML
- **License**: TBD (need to verify)
- **Completeness Target**: 100%
- **Purpose**: Gnostic/alternative interpretation

**Extraction Method:**
1. HTML parsing from website
2. Navigate site structure to find all 64 hexagrams
3. Extract gnostic interpretation text
4. Preserve formatting and structure
5. Attribution and metadata

**Benefits:**
- Alternative philosophical perspective
- Unique interpretation approach
- Appeals to users interested in esoteric studies

---

## Implementation Plan

### Step 1: Source Assessment (1-2 hours)

**Actions:**
- Visit each source URL
- Assess structure and accessibility
- Determine best extraction method
- Verify licensing/permissions
- Estimate extraction effort

**Deliverables:**
- Assessment document for each source
- Extraction strategy for each
- Permission status

### Step 2: Tool Selection (1 hour)

**Web Scraping:**
- Beautiful Soup 4 (HTML parsing)
- Requests (HTTP)
- lxml (XML/HTML processing)

**PDF Extraction:**
- PyPDF2 or pdfplumber
- pdfminer.six
- OCR fallback (Tesseract) if needed

**Utilities:**
- JSON validation tools
- Text comparison tools
- Progress tracking

### Step 3: Extraction Scripts (4-8 hours)

Create extraction scripts for each source:

**`tools/extract_wilhelm.py`:**
```python
#!/usr/bin/env python3
"""Extract Wilhelm/Baynes translation from web source."""

import requests
from bs4 import BeautifulSoup
import json

def extract_wilhelm_hexagram(hex_num):
    """Extract single hexagram from Wilhelm/Baynes."""
    # Fetch HTML
    # Parse structure
    # Extract data
    # Return structured dict

def extract_all_wilhelm():
    """Extract all 64 hexagrams."""
    for i in range(1, 65):
        hex_data = extract_wilhelm_hexagram(i)
        # Merge with existing JSON file
        # Validate
```

**Similar scripts for:**
- `tools/extract_legge_simplified.py`
- `tools/extract_hermetica.py`
- `tools/extract_dekorne.py`

### Step 4: Data Validation (2-4 hours)

**Validation Checks:**
- All 64 hexagrams present
- All required fields populated
- Text quality (no garbled characters)
- Metadata complete
- JSON schema valid

**Script: `tools/validate_sources.py`:**
```python
def validate_source_completeness(source_id):
    """Validate a source has all required data."""
    for i in range(1, 65):
        hex_file = f"data/hexagrams/hexagram_{i:02d}.json"
        # Load JSON
        # Check source_id exists in sources
        # Validate required fields
        # Check text quality
```

### Step 5: Manual Verification (4-8 hours)

**Process:**
- Randomly sample 10-20 hexagrams per source
- Compare extracted text with original
- Check for extraction errors
- Verify special formatting preserved
- Mark source as "verified" in metadata

### Step 6: Integration Testing (2 hours)

**Tests:**
- Load hexagrams from each new source
- Test multi-source comparison
- Verify fallback logic
- Test GUI/CLI source selection (Phase 6)

---

## JSON Structure Updates

### Hexagram File Structure

Each hexagram JSON file (`data/hexagrams/hexagram_*.json`) will be updated:

```json
{
  "hexagram_id": "hexagram_01",
  "number": 1,
  "binary": "111111",
  "trigrams": {"upper": "qian", "lower": "qian"},

  "canonical": {
    "source_id": "legge_1882",
    "name": "Tch'ien",
    "english_name": "The Creative",
    "judgment": "...",
    "image": "...",
    "lines": {...},
    "metadata": {...}
  },

  "sources": {
    "wilhelm_baynes": {
      "source_id": "wilhelm_baynes",
      "name": "Ch'ien",
      "english_name": "The Creative",
      "judgment": "...",
      "image": "...",
      "lines": {...},
      "metadata": {
        "translator": "Richard Wilhelm / Cary F. Baynes",
        "year": 1950,
        "extraction_date": "2025-11-18",
        "verified": true
      }
    },
    "legge_simplified": {...},
    "hermetica": {...},
    "dekorne": {...}
  }
}
```

### Metadata Registry Update

`data/sources_metadata.json` already includes these sources with completeness=0. Will be updated to completeness=100 and verified=true as sources are added.

---

## Testing Strategy

### Unit Tests

Update existing tests to include new sources:

**`tests/test_data_resolver.py` additions:**
```python
def test_wilhelm_source():
    """Test Wilhelm/Baynes source access."""
    resolver = HexagramResolver()
    hex_data = resolver.resolve("hexagram_01", source="wilhelm_baynes")

    assert hex_data['source_id'] == "wilhelm_baynes"
    assert hex_data['metadata']['translator'] == "Richard Wilhelm / Cary F. Baynes"

def test_source_comparison():
    """Test comparing Legge vs Wilhelm interpretations."""
    resolver = HexagramResolver()

    comparison = resolver.compare_sources(
        "hexagram_01",
        sources=["canonical", "wilhelm_baynes"],
        field="judgment"
    )

    assert 'canonical' in comparison
    assert 'wilhelm_baynes' in comparison
    assert comparison['canonical'] != comparison['wilhelm_baynes']
```

### Integration Tests

**Test multi-source readings:**
```python
def test_reading_with_wilhelm():
    """Test casting reading with Wilhelm source."""
    engine = HexagramEngine()

    reading = engine.cast_reading(
        method=Element.WOOD,
        source="wilhelm_baynes"
    )

    assert reading.source_id == "wilhelm_baynes"
    assert "Wilhelm" in reading.primary.metadata['translator']
```

---

## Risks and Mitigations

### Risk 1: Copyright/Licensing Issues

**Risk**: Some sources may not allow redistribution
**Mitigation**:
- Verify license before extraction
- Contact rights holders if needed
- Only include public domain or openly licensed texts
- Provide attribution and source URLs

### Risk 2: Extraction Errors

**Risk**: Web scraping may miss or corrupt text
**Mitigation**:
- Manual verification of samples
- Automated quality checks
- Compare against original sources
- Version control allows rollback

### Risk 3: Source Availability

**Risk**: Web sources may move or become unavailable
**Mitigation**:
- Archive source HTML/PDF locally
- Document source URLs and access dates
- Provide fallback to canonical source

### Risk 4: Incomplete Sources

**Risk**: Some sources may not have all fields (e.g., no line texts)
**Mitigation**:
- Resolver merge logic (Phase 3) fills gaps with canonical
- Mark incompleteness in metadata
- Document what's missing

---

## Success Criteria

Phase 5 will be considered complete when:

✓ Wilhelm/Baynes translation extracted (all 64 hexagrams)
✓ Simplified Legge extracted (all 64 hexagrams)
✓ Hermetica extracted (or documented as incomplete)
✓ DeKorne extracted (all 64 hexagrams)
✓ All sources validated and verified
✓ Tests updated to include new sources
✓ Documentation updated with source details
✓ Source comparison working in GUI/CLI (Phase 6)

---

## Deferred to Future Work

Due to the data extraction effort required and time constraints, Phase 5 **implementation** is documented but **deferred**. The infrastructure is complete:

✓ JSON structure supports multiple sources
✓ HexagramResolver can access any source
✓ Comparison functionality works
✓ Tests validate multi-source logic

**What's needed**: Data extraction scripts and manual verification

**Estimated effort**: 20-30 hours
**Dependencies**: Web scraping, PDF parsing, manual verification

**Next developer** can use this plan to complete Phase 5 with:
1. The extraction scripts outlined above
2. The validation tools specified
3. The test updates described
4. Full integration with Phases 3 and 4 already working

---

## Alternative: Gradual Source Addition

Phase 5 can be completed incrementally:

1. **Start with Wilhelm** (most requested, well-structured)
2. **Add Simplified Legge** (easier than PDF sources)
3. **Add DeKorne** (HTML, straightforward)
4. **Add Hermetica** (PDF, most complex)

Each source can be added independently and tested immediately.

---

**End of Phase 5 Plan**
