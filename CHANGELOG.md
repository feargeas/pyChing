# Changelog

All notable changes to pyChing will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased] - devnew branch

### Major Refactoring
- Created clean `devnew` branch from dev
- Removed all legacy Python 2 code
- Removed historical planning documentation (PHASE*.md, etc.)
- Established clear modern codebase without conflicts

### Removed
- `pyching.py` - Old entry point (replaced by pyching_cli.py)
- `pyching_engine.py` - Legacy engine (replaced by pyching/core/)
- `pyching_interface_console.py` - Old console interface (replaced by pyching_cli.py)
- `pyching_*_data.py` (3 files) - Old Python dict data (replaced by data/hexagrams/*.json)
- 22 test files using old code
- 17+ historical documentation files
- Test utility scripts and backup files

### Changed
- Entry point now `pyching_cli:main` in pyproject.toml
- Tests reorganized: modern tests in tests/, GUI tests in tests/gui/
- .gitignore updated for Emacs backup files

### Added
- requirements.txt for runtime dependencies
- pytest and pytest-cov as dev dependencies
- Optional `air` extras for Air method (requests library)
- Fresh README.md, TODO.md, CHANGELOG.md

### Known Issues
- GUI (pyching_interface_tkinter.py) needs updating to use modern engine
- Only one translation source available (Legge 1882)

---

## [2.0.0-alpha] - 2025-11-20 (dev branch)

### Added - Modern Architecture (Phases 1-4)
- Modern `pyching/` package structure
- Five element casting methods (Wood, Metal, Fire, Earth, Air)
- JSON-based data storage (64 hexagram files)
- HexagramEngine orchestration layer
- Hexagram and Reading dataclasses
- Multi-source translation infrastructure
- pyching_cli.py - Modern command-line interface
- Comprehensive test suite
- Type hints throughout codebase

### Changed
- Python 2 → Python 3.10+ migration
- Procedural code → dataclasses and modern patterns
- Pickle persistence → JSON
- Single random source → five element methods
- Hardcoded data → JSON data files

### Technical Details
- ~2,230 lines of production code
- ~1,730 lines of test code
- 64 JSON data files
- 100% test pass rate on modern code
- Preserves original algorithm exactly (Wood method)

---

## [1.2.2] - 2006-02-27 (original pyChing)

Last release by Stephen M. Gava.

### Original Features
- Tkinter GUI interface
- Console interface
- 3-coin oracle method
- James Legge 1882 translation
- Pickle-based save/load
- Python 2 compatible
- Configuration system
- Hexagram lookup tables

---

## Legend

- `Added` - New features
- `Changed` - Changes to existing functionality
- `Deprecated` - Soon-to-be removed features
- `Removed` - Removed features
- `Fixed` - Bug fixes
- `Security` - Security fixes
