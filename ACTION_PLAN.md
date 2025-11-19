# pyChing Test Coverage - Action Plan

**Status:** Analysis Complete  
**Date:** 2025-11-15  
**Scope:** 12 source files, 3 test files, 309 recent Tkinter changes

---

## Phase 1: Critical Bug Fixes (1-2 days)

### Task 1.1: Fix TclError Import Bug #1
- [ ] Open `/home/user/pyChing/pyching_interface_tkinter.py`
- [ ] Find line 41-44 (tkinter imports section)
- [ ] Add: `from tkinter import TclError`
- [ ] Verify syntax with: `python -m py_compile pyching_interface_tkinter.py`
- [ ] Git commit with message: "Fix: Add missing TclError import to pyching_interface_tkinter.py"

**Files:** `pyching_interface_tkinter.py`  
**Time:** 5 minutes

---

### Task 1.2: Fix TclError Import Bug #2
- [ ] Open `/home/user/pyChing/smgHtmlView.py`
- [ ] Find line 38-40 (tkinter imports section)
- [ ] Add: `from tkinter import TclError`
- [ ] Verify syntax with: `python -m py_compile smgHtmlView.py`
- [ ] Git commit with message: "Fix: Add missing TclError import to smgHtmlView.py"

**Files:** `smgHtmlView.py`  
**Time:** 5 minutes

---

### Task 1.3: Improve TkVersion Import (Optional)
- [ ] Open `/home/user/pyChing/smgAbout.py`
- [ ] Find line 37 (tkinter imports)
- [ ] Replace wildcard with: `from tkinter import *` and add below:
  `from tkinter import TkVersion`
- [ ] Verify syntax: `python -m py_compile smgAbout.py`
- [ ] Git commit: "Refactor: Add explicit TkVersion import to smgAbout.py"

**Files:** `smgAbout.py`  
**Time:** 5 minutes  
**Priority:** LOW (code quality only)

---

## Phase 2: Test Infrastructure Setup (2-3 days)

### Task 2.1: Install Test Dependencies
```bash
pip install pytest pytest-cov pytest-mock
```
- [ ] Verify pytest installed: `pytest --version`
- [ ] Verify coverage installed: `pytest --cov`
- [ ] Create `requirements-dev.txt` with:
  - pytest>=7.0
  - pytest-cov>=3.0
  - pytest-mock>=3.0

**Time:** 30 minutes

---

### Task 2.2: Create conftest.py for Pytest
**File:** `/home/user/pyChing/tests/conftest.py`

```python
"""
Pytest configuration and fixtures for pyChing tests
"""
import pytest
import sys
from pathlib import Path

# Ensure parent directory is in path
sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture
def pyching_app():
    """Fixture providing PychingAppDetails instance"""
    import pyching_engine
    return pyching_engine.PychingAppDetails(createConfigDir=0)

@pytest.fixture
def temp_reading(tmp_path):
    """Fixture providing temporary reading file path"""
    return tmp_path / "test_reading.psv"

@pytest.fixture
def hexagrams(pyching_app):
    """Fixture providing Hexagrams instance"""
    import pyching_engine
    return pyching_engine.Hexagrams(oracleType='coin')
```

- [ ] Create file
- [ ] Test with: `pytest tests/ --collect-only`
- [ ] Verify fixtures load correctly

**Time:** 30 minutes

---

### Task 2.3: Verify Existing Tests Run
```bash
pytest tests/ -v --tb=short
```

- [ ] Run test suite
- [ ] Verify all 42 tests pass
- [ ] Note any failures or warnings
- [ ] Document results

**Time:** 10 minutes

---

## Phase 3: New Test Development (1 week)

### Task 3.1: Create test_engine_paths.py
**File:** `/home/user/pyChing/tests/test_engine_paths.py`

**Coverage:**
- Path resolution (GetProgramDir)
- Path concatenation
- File existence validation
- Config directory creation

**Lines:** ~50  
**Tests:** ~6-8

**Checklist:**
- [ ] Create file
- [ ] Write path concatenation tests
- [ ] Test all path operations work
- [ ] Run with: `pytest tests/test_engine_paths.py -v`
- [ ] Achieve 100% pass rate

**Time:** 2-3 hours

---

### Task 3.2: Create test_gui_constants.py
**File:** `/home/user/pyChing/tests/test_gui_constants.py`

**Coverage:**
- Tkinter constants application
- Widget state management
- Boolean values in BooleanVar
- Relief/anchor/justify values

**Lines:** ~80  
**Tests:** ~10-12

**Checklist:**
- [ ] Create file
- [ ] Test widget states work
- [ ] Test boolean assignments
- [ ] Test relief values
- [ ] Run with: `pytest tests/test_gui_constants.py -v`
- [ ] Achieve 100% pass rate

**Time:** 3-4 hours

---

### Task 3.3: Create test_console_interface.py
**File:** `/home/user/pyChing/tests/test_console_interface.py`

**Coverage:**
- Console output formatting
- User input prompts
- Input validation

**Lines:** ~60  
**Tests:** ~6-8

**Checklist:**
- [ ] Create file
- [ ] Test console formatting
- [ ] Test input handling
- [ ] Run with: `pytest tests/test_console_interface.py -v`
- [ ] Achieve 100% pass rate

**Time:** 2-3 hours

---

### Task 3.4: Create test_engine_path_resolution.py
**File:** `/home/user/pyChing/tests/test_engine_path_resolution.py`

**Coverage:**
- GetProgramDir() correctness
- GetUserCfgDir() directory creation
- Config file path resolution
- Home directory fallback

**Lines:** ~40  
**Tests:** ~4-6

**Checklist:**
- [ ] Create file
- [ ] Test path resolution
- [ ] Test directory creation
- [ ] Test home dir fallback
- [ ] Run with: `pytest tests/test_engine_path_resolution.py -v`
- [ ] Achieve 100% pass rate

**Time:** 2-3 hours

---

## Phase 4: Enhanced Coverage (Week 2)

### Task 4.1: Add Parametrized Hexagram Tests
**Modify:** `/home/user/pyChing/tests/test_hexagram_data.py`

Add parametrized tests for all 64 hexagrams:
- [ ] Content validation
- [ ] Image references
- [ ] HTML structure
- [ ] Translation integrity (sample)

**Time:** 3-4 hours

---

### Task 4.2: Add Error Handling Tests
**New File:** `/home/user/pyChing/tests/test_error_handling.py`

Coverage:
- Missing files
- Corrupted save files
- Invalid inputs
- Permission errors

**Lines:** ~80  
**Tests:** ~8-10

**Time:** 3-4 hours

---

### Task 4.3: Create CI/CD Configuration
**File:** `.github/workflows/tests.yml`

- [ ] Create GitHub Actions workflow
- [ ] Run tests on push/PR
- [ ] Generate coverage reports
- [ ] Set minimum coverage threshold (50%)

**Time:** 1-2 hours

---

## Phase 5: Documentation (1-2 days)

### Task 5.1: Create Test Documentation
- [ ] Document test structure
- [ ] Create fixture guide
- [ ] Add examples
- [ ] Document how to run tests

**Time:** 2-3 hours

---

### Task 5.2: Update README
- [ ] Add testing section
- [ ] Document how to run tests
- [ ] Document test coverage
- [ ] Add contribution guidelines for tests

**Time:** 1-2 hours

---

## Timeline Summary

```
Week 1:
  Days 1-2:   Phase 1 - Bug fixes (15 min)
  Days 2-3:   Phase 2 - Test setup (2-3 hours)
  Days 3-5:   Phase 3 - New tests (~10 hours)
  Day 5:      Documentation (2-3 hours)

Week 2:
  Days 1-4:   Phase 4 - Enhanced coverage (10-12 hours)
  Day 5:      Review and cleanup (2-3 hours)
```

**Total Effort:** ~25-30 hours of development

---

## Success Criteria

### Coverage Targets:
- [ ] All existing tests pass (42/42)
- [ ] New tests pass (20+)
- [ ] Total test coverage reaches 35-40%
- [ ] Critical bugs fixed (2)
- [ ] Code quality bugs fixed (1)

### Quality Metrics:
- [ ] No failing tests
- [ ] No warnings in pytest output
- [ ] All imports explicit (no more fragile wildcards)
- [ ] 100% syntax verification

### Documentation:
- [ ] TEST_COVERAGE_ANALYSIS.md created
- [ ] BUG_REPORT.md created
- [ ] ACTION_PLAN.md created (this file)
- [ ] Test documentation updated
- [ ] README updated with test info

---

## Priority Order

**IMMEDIATE (This Week):**
1. Fix bugs (#1, #2)
2. Install pytest
3. Verify existing tests pass
4. Create test_engine_paths.py
5. Create test_gui_constants.py

**NEXT WEEK:**
6. Create test_console_interface.py
7. Enhance hexagram tests
8. Add error handling tests
9. Set up CI/CD

**FUTURE:**
10. Performance tests
11. Platform-specific tests
12. Property-based testing

---

## Commands Reference

### Install dependencies:
```bash
pip install -r requirements-dev.txt
```

### Run all tests:
```bash
pytest tests/ -v
```

### Run specific test file:
```bash
pytest tests/test_oracle_coin_method.py -v
```

### Run with coverage:
```bash
pytest tests/ --cov=pyching --cov-report=html
```

### Verify syntax:
```bash
python -m py_compile pyching_interface_tkinter.py
```

### Check import safety:
```bash
python -c "from tkinter import TclError; print('OK')"
```

---

## Notes

- This plan assumes sequential development
- Tasks can be parallelized if multiple developers available
- Each phase should be git committed separately
- Run tests after each major change
- Document any blockers or issues discovered

---

## Questions to Address

1. Should GUI tests use mocking or headless Tk?
2. What's the target coverage percentage? (Currently 11.6%, aim for 40-50%?)
3. Are parametrized hexagram tests necessary? (All 64 or sample?)
4. Should console interface be refactored before testing?
5. Do we need property-based testing (hypothesis)?

---

See also:
- `/home/user/pyChing/TEST_COVERAGE_ANALYSIS.md` - Full analysis
- `/home/user/pyChing/COVERAGE_SUMMARY.txt` - Quick summary
- `/home/user/pyChing/BUG_REPORT.md` - Bug details
