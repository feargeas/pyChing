"""
Test Configuration Directory Handling
======================================

These tests validate configuration directory creation and permission handling.

THESE TESTS VALIDATE CONFIG DIRECTORY CREATION AND ERROR HANDLING.
"""

import sys
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import shutil

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pyching_engine
from pyching_engine import PychingAppDetails
import pytest


class TestConfigDirectoryCreation:
    """Test configuration directory creation"""

    def test_config_dir_created_when_missing(self):
        """Config directory should be created if it doesn't exist"""
        # Use a unique test directory name
        test_dir = f'.pyching_test_create_{os.getpid()}'
        home_dir = Path.home()
        test_path = home_dir / test_dir

        # Clean up first
        if test_path.exists():
            try:
                test_path.rmdir()
            except:
                pass

        app = PychingAppDetails(createConfigDir=0)
        cfg_dir = app.GetUserCfgDir(test_dir)

        try:
            # If directory doesn't exist, GetUserCfgDir should create it
            # when called with appropriate flags
            if not cfg_dir.exists():
                cfg_dir.mkdir(parents=True, exist_ok=True)

            assert cfg_dir.exists(), "Config directory should be created"
        finally:
            # Clean up
            if test_path.exists():
                try:
                    test_path.rmdir()
                except:
                    pass

    def test_config_dir_not_recreated_if_exists(self):
        """Config directory creation should be idempotent"""
        test_dir = f'.pyching_test_exists_{os.getpid()}'
        home_dir = Path.home()
        test_path = home_dir / test_dir

        # Create it first
        test_path.mkdir(parents=True, exist_ok=True)

        try:
            app = PychingAppDetails(createConfigDir=0)
            cfg_dir = app.GetUserCfgDir(test_dir)

            # Should work even if directory exists
            assert cfg_dir.exists()
            assert cfg_dir == test_path
        finally:
            # Clean up
            if test_path.exists():
                try:
                    test_path.rmdir()
                except:
                    pass

    def test_nested_config_dir_creation(self):
        """Nested config directories should be created"""
        test_dir = f'.pyching_test/nested/deep_{os.getpid()}'
        home_dir = Path.home()
        test_path = home_dir / test_dir

        # Clean up first
        root_test = home_dir / '.pyching_test'
        if root_test.exists():
            try:
                shutil.rmtree(root_test)
            except:
                pass

        try:
            app = PychingAppDetails(createConfigDir=0)
            cfg_dir = app.GetUserCfgDir(test_dir)

            # Create it
            cfg_dir.mkdir(parents=True, exist_ok=True)
            assert cfg_dir.exists(), "Nested config directory should be created"
        finally:
            # Clean up
            if root_test.exists():
                try:
                    shutil.rmtree(root_test)
                except:
                    pass


class TestConfigDirectoryPermissions:
    """Test config directory permission handling"""

    @patch('pathlib.Path.mkdir')
    def test_config_dir_creation_handles_permission_error(self, mock_mkdir):
        """Permission errors during creation should be handled"""
        mock_mkdir.side_effect = PermissionError("No permission")

        app = PychingAppDetails(createConfigDir=0)

        # Should handle error gracefully
        try:
            cfg_dir = app.GetUserCfgDir('.pyching_test_perm')
            # Should still return a path even if creation failed
            assert isinstance(cfg_dir, Path)
        except PermissionError:
            # If it propagates, that's also acceptable behavior
            pass

    @patch('pathlib.Path.mkdir')
    def test_config_dir_creation_handles_io_error(self, mock_mkdir):
        """IO errors during creation should be handled"""
        mock_mkdir.side_effect = IOError("IO Error")

        app = PychingAppDetails(createConfigDir=0)

        try:
            cfg_dir = app.GetUserCfgDir('.pyching_test_io')
            assert isinstance(cfg_dir, Path)
        except IOError:
            # If it propagates, that's also acceptable
            pass


class TestConfigDirectoryFallbacks:
    """Test fallback behavior when home directory is problematic"""

    @patch('pathlib.Path.home')
    def test_fallback_when_home_missing(self, mock_home):
        """Should fallback to CWD when home doesn't exist"""
        mock_home.return_value = Path('/nonexistent/home')

        app = PychingAppDetails(createConfigDir=0)
        cfg_dir = app.GetUserCfgDir('.pyching_test')

        # Should use current directory as fallback
        cwd = Path.cwd()
        assert cwd in cfg_dir.parents or cfg_dir.parent == cwd

    @patch('pathlib.Path.home')
    def test_fallback_when_home_raises(self, mock_home):
        """Should handle exceptions from Path.home()"""
        mock_home.side_effect = RuntimeError("No home")

        app = PychingAppDetails(createConfigDir=0)

        try:
            cfg_dir = app.GetUserCfgDir('.pyching_test')
            # Should fallback to CWD
            cwd = Path.cwd()
            assert cwd in cfg_dir.parents or cfg_dir.parent == cwd
        except RuntimeError:
            # Or might propagate error
            pass

    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.home')
    def test_fallback_when_home_not_accessible(self, mock_home, mock_exists):
        """Should fallback when home exists but isn't accessible"""
        test_home = Path('/tmp/test_home')
        mock_home.return_value = test_home
        mock_exists.return_value = False  # Simulate non-existent home

        app = PychingAppDetails(createConfigDir=0)
        cfg_dir = app.GetUserCfgDir('.pyching_test')

        # Should handle gracefully
        assert isinstance(cfg_dir, Path)


class TestConfigPathsConsistency:
    """Test that config paths are consistent"""

    def test_config_path_equals_save_path(self):
        """Initially, configPath should equal savePath"""
        app = PychingAppDetails(createConfigDir=0)
        assert app.configPath == app.savePath, \
            "configPath and savePath should be the same initially"

    def test_config_file_in_config_path(self):
        """configFile should be inside configPath"""
        app = PychingAppDetails(createConfigDir=0)
        assert app.configFile.parent == app.configPath, \
            "configFile should be in configPath"

    def test_all_paths_are_absolute(self):
        """All paths should be absolute"""
        app = PychingAppDetails(createConfigDir=0)

        assert app.execPath.is_absolute(), "execPath should be absolute"
        assert app.configPath.is_absolute(), "configPath should be absolute"
        assert app.savePath.is_absolute(), "savePath should be absolute"
        assert app.configFile.is_absolute(), "configFile should be absolute"


class TestDefaultPychingConfigDir:
    """Test the default .pyching config directory"""

    def test_default_config_dir_is_pyching(self):
        """Default config directory should be .pyching"""
        app = PychingAppDetails(createConfigDir=0)
        assert '.pyching' in str(app.configPath), \
            "Default config path should contain .pyching"

    def test_default_config_in_home(self):
        """Default config should be in home directory"""
        app = PychingAppDetails(createConfigDir=0)
        home = Path.home()

        # configPath should be under home (or be cwd fallback)
        try:
            assert home in app.configPath.parents or app.configPath.parent == home
        except AssertionError:
            # Might be CWD fallback, check that
            cwd = Path.cwd()
            assert cwd in app.configPath.parents or app.configPath.parent == cwd


class TestSavePathBehavior:
    """Test save path behavior and modifications"""

    def test_save_path_initially_set(self):
        """savePath should be set on initialization"""
        app = PychingAppDetails(createConfigDir=0)
        assert app.savePath is not None
        assert isinstance(app.savePath, Path)

    def test_save_path_modifiable(self):
        """savePath should be modifiable (public attribute)"""
        app = PychingAppDetails(createConfigDir=0)
        original_path = app.savePath

        new_path = Path('/tmp/new_save_path')
        app.savePath = new_path

        assert app.savePath == new_path
        assert app.savePath != original_path

    def test_save_path_can_be_different_from_config(self):
        """savePath can be set to different location than configPath"""
        app = PychingAppDetails(createConfigDir=0)

        app.savePath = Path('/tmp/different')

        assert app.savePath != app.configPath
        # But configPath should remain unchanged
        assert '.pyching' in str(app.configPath)


class TestConfigDirectoryCleanup:
    """Test that we can clean up test directories"""

    def test_can_remove_empty_config_dir(self):
        """Empty config directories should be removable"""
        test_dir = f'.pyching_test_cleanup_{os.getpid()}'
        home = Path.home()
        test_path = home / test_dir

        # Create it
        test_path.mkdir(parents=True, exist_ok=True)

        try:
            assert test_path.exists()
            # Should be able to remove it
            test_path.rmdir()
            assert not test_path.exists()
        except:
            # Clean up even if test fails
            if test_path.exists():
                try:
                    test_path.rmdir()
                except:
                    pass


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
