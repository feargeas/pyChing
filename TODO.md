# TODO - Known Issues and Planned Work

## Current Branch: devnew

This is a **clean slate** branch created from dev, with all legacy code removed.
Only modern `pyching/` package code remains.

---

## High Priority

### 1. Update GUI to Use Modern Engine

**File:** `pyching_interface_tkinter.py` (2,311 lines)

**Status:** GUI currently imports BOTH old (removed) and new engines. Needs complete update.

**What's needed:**
- Remove all old `pyching_engine` imports (will break initially - that's OK)
- Use `from pyching import HexagramEngine, Element, Reading, Hexagram`
- Add UI elements for:
  - Method selection (Wood/Metal/Fire/Earth/Air dropdown)
  - Source selection (when multi-source available)
  - Seed input (for Earth method)
- Update casting logic to use `HexagramEngine.cast_reading()`
- Replace pickle save/load with JSON
- Add source comparison view (optional)

**Estimated effort:** 10-15 hours

**Benefits:**
- GUI users can access all five casting methods
- JSON save/load (safer than pickle)
- Consistent with CLI behavior
- Enables multi-source translations when available

---

## Medium Priority

### 2. Extract Additional Translation Sources

**Status:** Infrastructure complete, actual text extraction pending

**Target sources:**
1. **Wilhelm/Baynes** (1950) - Most requested, influential Western translation
2. **Simplified Legge** (TwoDreams, 2020) - Modern language
3. **DeKorne's Gnostic Book of Changes** - Alternative interpretation
4. **Hermetica I Ching** - Hermetic perspective

**What's needed:**
- Web scraping / PDF extraction scripts
- Manual verification of extracted text
- Update JSON hexagram files with new source data

**Estimated effort:** 8-12 hours per source (Wilhelm first priority)

---

## Low Priority / Future Enhancements

### 3. Package for PyPI

- Create proper package distribution
- Upload to PyPI
- Users can `pip install pyching`

### 4. Documentation Website

- Convert documentation to static site (MkDocs, Sphinx, etc.)
- Host on GitHub Pages

### 5. Yarrow Stalk Method

- Implement traditional yarrow stalk casting
- Different probability distribution than 3-coin method

### 6. Reading Journal

- SQLite database for storing readings
- Search and analyze reading history
- Export to various formats (PDF, HTML, Markdown)

### 7. Web Interface

- Flask/FastAPI backend
- Browser-based GUI
- Mobile-friendly design

---

## Testing Gaps

### Missing test coverage:
- GUI functionality (manual testing needed after update)
- CLI argument parsing edge cases
- Error handling for network failures (Air method)
- Large-scale data integrity checks

---

## Documentation Needed

Once GUI is updated and objectives are clarified:

1. **User Guide** - Comprehensive usage documentation
2. **API Reference** - Python API documentation
3. **Developer Guide** - Contributing guidelines, architecture overview
4. **Translation Guide** - How to add new I Ching sources

---

## Technical Debt

### Minor issues:
- Some docstrings need updating
- Type hints could be more comprehensive
- Could add more integration tests
- Performance profiling not done yet

---

## Notes

- All legacy code has been removed from devnew
- Focus is on completing GUI update first
- Then extract additional translation sources
- Then package and distribute

**Philosophy:** Working modern codebase with clear direction, even if some features temporarily broken.
