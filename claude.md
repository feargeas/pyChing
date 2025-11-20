# Claude Development Notes

## Environment Information

### Operating System
This project is developed on **Gentoo Linux**.

### Package Management
⚠️ **IMPORTANT**: This system uses Gentoo, so `pip install...` commands are **bad and wrong**.

Instead of using pip, packages should be installed through Gentoo's package manager:

```bash
# WRONG - Do not use pip
pip install pytest

# CORRECT - Use emerge
emerge --ask dev-python/pytest
```

### Python Dependencies
When suggesting installation of Python packages, always use:
- `emerge --ask <package-name>` for system-wide packages
- For development dependencies, check `/etc/portage/package.use` and other Portage configurations

### Testing
The project uses pytest for testing. To run tests:

```bash
# After installing pytest via emerge
pytest tests/ -v
```

For coverage reports:
```bash
# Install coverage tool via emerge first
emerge --ask dev-python/pytest-cov

# Then run coverage
pytest tests/ --cov=. --cov-report=html
```

## Project Structure

### Core Application Files
- `pyching.py` - Original entry point
- `pyching_cli.py` - Modern CLI implementation with argument parsing
- `pyching_engine.py` - Core I Ching oracle engine
- `pyching_interface_console.py` - Console/terminal interface
- `pyching_interface_tkinter.py` - GUI interface with modern features
- `pyching_themes.py` - GUI theming and styling support

### Data Files
- `pyching_int_data.py` - Hexagram interpretation data
- `pyching_idimage_data.py` - Ideogram image data
- `pyching_hlhtx_data.py` - Hexagram line text data
- `pyching_cimages.py` - Coin/divination images

### GUI Components
- `smgAbout.py` - About dialog
- `smgDialog.py` - Custom dialog widgets
- `smgHtmlView.py` - HTML content viewer
- `smgAnimate.py` - Animation support

### Package Structure
- `pyching/` - Modern package directory with submodules
  - Core engine components
  - Casting methods (Air, Earth, Fire, Metal, Wood)
  - Data loaders and resolvers
- `data/` - Data management modules
  - `hexagram_lookup.py`
  - `hexagram_svg.py`
  - `examples.py`
- `tools/` - Utility scripts
  - `convert_legacy_data.py`
  - `extract_wilhelm.py`
  - `test_data_loading.py`
  - `validate_data.py`
- `examples/` - Usage examples and demos

### Test Suite
- `tests/` - Main test directory (comprehensive test coverage)
  - `test_casting_methods.py`
  - `test_core_engine.py`
  - `test_core_hexagram.py`
  - `test_core_reading.py`
  - `test_data_loader.py`
  - `test_data_resolver.py`
  - `test_engine_paths.py`
  - `test_gui_imports.py`
  - `test_hexagram_data.py`
  - `test_oracle_coin_method.py`
  - `test_python3_compatibility.py`
  - `test_reading_persistence.py`

- Root-level test files (GUI/sizing tests):
  - `test_adaptive_sizing.py`
  - `test_config_compatibility.py`
  - `test_dynamic_sizing.py`
  - `test_fonts.py`
  - `test_json_config.py`
  - `test_sizing_simple.py`
  - `test_themes_integration.py`
  - `test_themes_only.py`
  - `test_verbose_mode.py`
  - `test_visual_perfection.py`
  - `test_window_sizing.py`

### Utility Scripts
- `check_sizing.py` - GUI sizing verification
- `verify_sizing_fix.py` - Sizing fix validation

## Notes for Claude

- Always respect Gentoo's package management philosophy
- Do not suggest `pip install` commands
- The user prefers emerge for all system package management
- This is a Python 3.10+ project
- Tests must pass before committing changes
- The project has both legacy (root-level) and modern (pyching/ package) code structures
- GUI components use tkinter with custom theming support
