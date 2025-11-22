# TODO - Known Issues and Planned Work

## Current Branch: devnew

This is a **clean slate** branch created from dev, with all legacy code removed.
Only modern `pyching/` package code remains.

**Context:** This TODO tracks current objectives. For overall aims and vision, see `project_notes.txt`.

**Philosophy:** Growing pyChing organically from the seed of v1.2.2 - steady, thoughtful growth.

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

### 2. Integrate Additional Translation Sources (When Ready)

**Status:** Infrastructure complete and ready. Sources available but deliberately held back.

**Philosophy:** Staying with Legge (1882) for now keeps things simple and provides solid basis.
Additional sources will be integrated when GUI is stable and system is proven.

**What we have:**
- Multi-source JSON structure already implemented
- HexagramResolver can handle multiple translations
- Source comparison functionality built-in
- Various sources ready in different formats (PDF, text, web scrapes, .doc files)

**What's needed when time comes:**
- Convert source materials to JSON format (regardless of input format)
- Integrate into `data/hexagrams/*.json` structure (add to "sources" key)
- Update `data/sources_metadata.json` with new source info
- Verify all 64 hexagrams present and complete
- Test with both CLI and GUI

**Estimated effort:** 4-8 hours per source (infrastructure already built)

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

## Eventually / Future Vision

See `project_notes.txt` for long-term aspirational goals (Phases 4-5):

**Phase 4: Universal Access**
- Internationalization (multiple languages)
- Accessibility features (WCAG compliance, screen readers, keyboard navigation)
- Alternative interfaces (web interface, TUI with Rich/Textual)
- RTL language support

**Phase 5: Distribution & Community**
- Distribution (Docker, PyPI, Flatpak, Homebrew, Windows installer)
- Documentation website (Sphinx, ReadTheDocs)
- Community building (code of conduct, contributor guidelines)
- Scholar consultation and collaboration

These remain on the horizon. The plant grows from strong roots.

---

## Current Phase Status

We are completing **Phase 2** (Code Modernization) and beginning **Phase 3** (Enhanced Features):

- ✅ **Phase 1: Foundation & Preservation** - Complete
  - Python 2 → 3 migration done
  - Tests comprehensive
  - Oracle authenticity preserved

- 🔄 **Phase 2: Code Modernization** - ~95% complete
  - Type hints ✅
  - Dataclasses ✅
  - Modern patterns (pathlib, f-strings, context managers) ✅
  - JSON data structure ✅
  - Package structure ✅
  - Five Elements casting methods ✅
  - Modern CLI ✅
  - GUI update remaining ⏳

- 🌱 **Phase 3: Enhanced Features** - Ready to begin
  - Multiple translation sources (infrastructure ready, sources available)
  - Reading journal (planned)
  - Yarrow stalk method (planned)
  - Educational content (future)

---

## Notes

- All legacy code removed from devnew - clean foundation
- Growing organically: GUI first, then sources, then enhancements
- Infrastructure built to adapt to different input formats
- Staying simple with Legge until system proven stable

**Philosophy:** Working modern codebase with clear direction. Plant grows from strong roots, not rushed.
