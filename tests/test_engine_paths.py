"""
Test path handling in pyching_engine module

Tests the Path concatenation fixes and path resolution logic introduced
in the Python 3 migration and bug fixes.
"""
import pytest
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pyching_engine


class TestPychingAppDetails:
    """Test PychingAppDetails path handling"""

    def test_app_details_creation(self):
        """Test that PychingAppDetails can be instantiated"""
        app = pyching_engine.PychingAppDetails()
        assert app is not None
        assert app.title == 'pyChing'
        assert app.version == '1.2.2'

    def test_exec_path_is_path_object(self):
        """Test that execPath is a Path object, not a string"""
        app = pyching_engine.PychingAppDetails()
        assert isinstance(app.execPath, Path)

    def test_config_path_is_path_object(self):
        """Test that configPath is a Path object"""
        app = pyching_engine.PychingAppDetails()
        assert isinstance(app.configPath, Path)

    def test_config_file_is_path_object(self):
        """Test that configFile is a Path object"""
        app = pyching_engine.PychingAppDetails()
        assert isinstance(app.configFile, Path)

    def test_path_concatenation_with_division_operator(self):
        """Test that Path objects can be concatenated with / operator"""
        app = pyching_engine.PychingAppDetails()

        # This is the critical fix - ensure / operator works
        test_path = app.execPath / 'test_file.txt'
        assert isinstance(test_path, Path)
        assert str(test_path).endswith('test_file.txt')

    def test_copying_license_path_construction(self):
        """Test the COPYING file path construction (Bug fix verification)"""
        app = pyching_engine.PychingAppDetails()

        # This was the bug: execPath+'COPYING' failed after Path migration
        # Should now work: execPath / 'COPYING'
        copying_path = app.execPath / 'COPYING'
        assert isinstance(copying_path, Path)
        assert str(copying_path).endswith('COPYING')

    def test_credits_license_path_construction(self):
        """Test the CREDITS file path construction (Bug fix verification)"""
        app = pyching_engine.PychingAppDetails()

        # This was the bug: execPath+'CREDITS' failed after Path migration
        # Should now work: execPath / 'CREDITS'
        credits_path = app.execPath / 'CREDITS'
        assert isinstance(credits_path, Path)
        assert str(credits_path).endswith('CREDITS')

    def test_icon_path_construction(self):
        """Test the icon.xbm file path construction"""
        app = pyching_engine.PychingAppDetails()

        icon_path = app.execPath / 'icon.xbm'
        assert isinstance(icon_path, Path)
        assert str(icon_path).endswith('icon.xbm')

    def test_config_file_path_construction(self):
        """Test config file path (pychingrc) construction"""
        app = pyching_engine.PychingAppDetails()

        # configFile = configPath / 'pychingrc'
        assert isinstance(app.configFile, Path)
        assert app.configFile.name == 'pychingrc'
        assert app.configFile.parent == app.configPath

    def test_path_in_fstring_interpolation(self):
        """Test that Path objects work correctly in f-strings"""
        app = pyching_engine.PychingAppDetails()

        # This is used in the icon bitmap loading
        icon_path_str = f'{app.execPath / "icon.xbm"}'
        assert isinstance(icon_path_str, str)
        assert 'icon.xbm' in icon_path_str

    def test_config_directory_created(self):
        """Test that config directory is created if it doesn't exist"""
        app = pyching_engine.PychingAppDetails()

        # Config directory should exist after initialization
        # (created in GetUserCfgDir if needed)
        assert app.configPath.exists() or app.configPath == Path.cwd() / '.pyching'


class TestPathResolution:
    """Test path resolution edge cases"""

    def test_program_dir_resolution(self):
        """Test GetProgramDir returns valid Path"""
        app = pyching_engine.PychingAppDetails()
        program_dir = app.GetProgramDir()

        assert isinstance(program_dir, Path)
        assert program_dir.exists()

    def test_user_cfg_dir_resolution(self):
        """Test GetUserCfgDir returns valid Path"""
        app = pyching_engine.PychingAppDetails()

        # Get the .pyching directory
        cfg_dir = app.GetUserCfgDir('.pyching_test')

        assert isinstance(cfg_dir, Path)
        # Directory should be created
        assert cfg_dir.exists()
        assert cfg_dir.name == '.pyching_test'

        # Clean up test directory
        try:
            cfg_dir.rmdir()
        except OSError:
            pass  # Directory not empty or other error


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
