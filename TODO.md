# TODO - Known Issues and Planned Work

## Current Branch: devnew

This is a **clean slate** branch created from dev, with all legacy code removed. Look to branch dev for missing files.


**Context:** This TODO tracks current objectives. For overall aims and vision, see `project_notes.txt`.

**Philosophy:** Growing pyChing organically from the seed of v1.2.2 - steady, thoughtful growth.

---

## Immediate

Work is needed to improve the gui. The option to 'Cast each line separately' was removed for simplicity in development, and 
must be reinstated. Look in branch dev for missing resources. 

### 1. Restore the coin animation in the gui

**Status:** ✅ **Complete**

The coin animation has been restored as a separate module (`pyching_coin_animation.py`) with the following features:
- Progressive hexagram line drawing (builds from bottom to top as coins are cast)
- Toggle option in Settings menu ('Show Coin Animation')
- Element-specific animation speeds reflecting each method's character:
  - Earth: Slow and grounded
  - Wood: Natural growth pace (baseline)
  - Metal: Sharp and precise
  - Fire: Quick and energetic
  - Water: Extreme variation (cognitive dissonance - slow buildups, sudden breaks)
- Settings persist across sessions
- Clean architecture - no legacy code reintroduced

### 2. Fix Help Menus

**Status:** ✅ **Complete**

All help menu items are now fully functional:
- Restored `pyching_hlhtx_data.py` from dev branch with HTML help content
- "Using pyChing" and "Introduction to the I Ching" menus now display correctly
- "Browse Hexagram Information" modernized to use HexagramInfoWindow with number prompt
- Fixed import issues (added tkSimpleDialog) and corrected Hexagram instantiation method

### 3. Themes Need Attention

**Status:** GUI theming requires improvement and consistency. Some elements currently are not themed,
and selecting 'System Default' does not work properly.

### 4. Fonts Need Attention

**Status:** Font usage and display needs refinement across the GUI.

### 5. Issue: gui will clear  when 'Cast New Hexagram' is selected

**Needed:** When a reading has been cast but not saved, and the user selects 'Cast New Hexagram', the user
will be given the option to save; after which the gui will clear but the session settings will not change.

### 6. Issue: Settings dropdown 

***Add Feature*** In addition to 'Save Settings' there will be 'Default Settings' 'Load Settings' and 'Save Settings As...' options.
Users may name and store settings, On startup, the last used settings will be used. Initially there will be 'default' and 'user' as available
settings to load (and of course they will be the same until 'Save Settings' is selected). settings will include the 'Method' and  'Source' choices.

---

## High Priority

### 1. Integrate Additional Translation Sources (When Ready)

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


### 2. Include Notetaking Functionality

The user will have tha ability to save text notes, for reflections and research, which are associated with a particular reading. Additionally, there will be utility for notes to be stored which are for general, long term reference, and the opportunity to journal. now, <vibe=on| consider the user: understand the context, make it easy and all-joined-up (by whatver means, with the overrides of beauty and simplicity) for someone with no technical nous to be able to  say what they mean in-the-moment, perhaps make general remarks, future notes, look up a few web sources, whatever: make it easy for these folk to be able to come back later and 'follow the breadcrumbs' of that experience, perhaps to rationalise it, blog about it, follow it through and extend the process - and... |vibe=off> #rem we know 'pebkac', make this a feature, not a bug. [note: a webui ie access to this software through a browser via localhost is coming quite soon (but not now) which may inform design decisions,]



---

## Low Priority / Future Enhancements [some things below are a bit sketchy, have a rake through see what you think]

### 5. Package for PyPI

- Create proper package distribution
- Upload to PyPI
- Users can `pip install pyching`

### 4. Documentation Website

- Convert documentation to static site (MkDocs, Sphinx, etc.)
- Host on GitHub Pages

### 3 Yarrow Stalk Method

- Implement traditional yarrow stalk casting
- Different probability distribution than 3-coin method

### 1. Reading Journal

- SQLite database for storing readings
- Search and analyze reading history
- Export to various formats (PDF, HTML, Markdown)

### 2. Web Interface

- Flask/FastAPI backend
- Browser-based GUI
- Mobile-friendly design

---

## Testing Gaps

### Missing test coverage:
- GUI functionality (manual testing needed after update)
- CLI argument parsing edge cases
- Error handling for network failures (Water method)
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

No account so far about how Mac users might incorporate this software. This is important, do not want to exclude anybody. Sorry, BSD* but ifyouwantityoucanhaveitDIY.

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

- ✅ **Phase 2: Code Modernization** - Complete
  - Type hints ✅
  - Dataclasses ✅
  - Modern patterns (pathlib, f-strings, context managers) ✅
  - JSON data structure ✅
  - Package structure ✅
  - Five Elements casting methods ✅
  - Modern CLI ✅
  - GUI modernization ✅

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
