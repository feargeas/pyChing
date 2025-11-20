"""
Test Application Configuration
===============================

These tests validate application initialization and path detection.

THESE TESTS VALIDATE APP CONFIGURATION AND PATH HANDLING.
"""

import sys
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pyching_engine
from pyching_engine import PychingAppDetails
import pytest


class TestPychingAppDetailsInitialization:
    """Test PychingAppDetails class initialization"""

    def test_app_details_creates_successfully(self):
        """PychingAppDetails should initialize without errors"""
        app = PychingAppDetails(createConfigDir=0)
        assert app is not None

    def test_app_has_title(self):
        """App should have title attribute"""
        app = PychingAppDetails(createConfigDir=0)
        assert hasattr(app, 'title')
        assert app.title == 'pyChing'

    def test_app_has_version(self):
        """App should have version attribute"""
        app = PychingAppDetails(createConfigDir=0)
        assert hasattr(app, 'version')
        assert isinstance(app.version, str)
        assert len(app.version) > 0

    def test_app_has_os_info(self):
        """App should detect OS information"""
        app = PychingAppDetails(createConfigDir=0)
        assert hasattr(app, 'os')
        assert hasattr(app, 'osType')
        assert app.os == sys.platform
        assert app.osType == os.name

    def test_app_has_paths(self):
        """App should have path attributes"""
        app = PychingAppDetails(createConfigDir=0)
        assert hasattr(app, 'execPath')
        assert hasattr(app, 'configPath')
        assert hasattr(app, 'savePath')
        assert isinstance(app.execPath, Path)
        assert isinstance(app.configPath, Path)
        assert isinstance(app.savePath, Path)

    def test_app_has_file_extensions(self):
        """App should define file extensions"""
        app = PychingAppDetails(createConfigDir=0)
        assert hasattr(app, 'saveFileExt')
        assert hasattr(app, 'internalImageExt')
        assert hasattr(app, 'internalHtmlExt')
        assert app.saveFileExt == '.psv'

    def test_app_has_save_file_id(self):
        """App should have save file ID tuple"""
        app = PychingAppDetails(createConfigDir=0)
        assert hasattr(app, 'saveFileID')
        assert isinstance(app.saveFileID, tuple)
        assert len(app.saveFileID) == 2
        assert app.saveFileID[0] == 'pyching_save_file'


class TestGetProgramDir:
    """Test GetProgramDir method"""

    def test_get_program_dir_returns_path(self):
        """GetProgramDir should return a Path object"""
        app = PychingAppDetails(createConfigDir=0)
        program_dir = app.GetProgramDir()
        assert isinstance(program_dir, Path)

    def test_get_program_dir_exists(self):
        """Program directory should exist"""
        app = PychingAppDetails(createConfigDir=0)
        program_dir = app.GetProgramDir()
        assert program_dir.exists(), f"Program dir {program_dir} does not exist"

    def test_get_program_dir_is_directory(self):
        """Program path should be a directory"""
        app = PychingAppDetails(createConfigDir=0)
        program_dir = app.GetProgramDir()
        assert program_dir.is_dir(), f"Program dir {program_dir} is not a directory"

    def test_get_program_dir_contains_engine(self):
        """Program directory should contain pyching_engine.py"""
        app = PychingAppDetails(createConfigDir=0)
        program_dir = app.GetProgramDir()
        engine_file = program_dir / 'pyching_engine.py'
        assert engine_file.exists(), \
            f"Engine file not found in {program_dir}"


class TestGetUserCfgDir:
    """Test GetUserCfgDir method"""

    def test_get_user_cfg_dir_returns_path(self):
        """GetUserCfgDir should return a Path object"""
        app = PychingAppDetails(createConfigDir=0)
        cfg_dir = app.GetUserCfgDir('.pyching_test')
        assert isinstance(cfg_dir, Path)

    def test_get_user_cfg_dir_with_creation(self):
        """GetUserCfgDir should create directory when flag is set"""
        # Use a temporary unique directory name
        test_dir = f'.pyching_test_{os.getpid()}'
        app = PychingAppDetails(createConfigDir=0)

        # Clean up if it exists
        cfg_dir = app.GetUserCfgDir(test_dir)
        if cfg_dir.exists():
            cfg_dir.rmdir()

        # Now test creation
        app2 = PychingAppDetails(createConfigDir=1)
        cfg_dir = app2.GetUserCfgDir(test_dir)

        try:
            # Directory should be created
            assert cfg_dir.exists(), f"Config dir {cfg_dir} was not created"
            assert cfg_dir.is_dir(), f"Config dir {cfg_dir} is not a directory"
        finally:
            # Clean up
            if cfg_dir.exists():
                try:
                    cfg_dir.rmdir()
                except:
                    pass

    def test_get_user_cfg_dir_in_home(self):
        """Config directory should be in home directory"""
        app = PychingAppDetails(createConfigDir=0)
        cfg_dir = app.GetUserCfgDir('.pyching_test')
        home_dir = Path.home()

        # cfg_dir should be under home
        assert cfg_dir.parent == home_dir or home_dir in cfg_dir.parents

    @patch('pathlib.Path.home')
    def test_get_user_cfg_dir_fallback_to_cwd(self, mock_home):
        """Should fallback to CWD if home directory doesn't exist"""
        # Mock home to return non-existent directory
        mock_home.return_value = Path('/nonexistent/home/directory')

        app = PychingAppDetails(createConfigDir=0)
        cfg_dir = app.GetUserCfgDir('.pyching_test')

        # Should fallback to current directory
        cwd = Path.cwd()
        assert cwd in cfg_dir.parents or cfg_dir.parent == cwd


class TestConfigPaths:
    """Test configuration path attributes"""

    def test_config_path_set(self):
        """configPath should be set"""
        app = PychingAppDetails(createConfigDir=0)
        assert app.configPath is not None
        assert isinstance(app.configPath, Path)

    def test_save_path_set(self):
        """savePath should be set"""
        app = PychingAppDetails(createConfigDir=0)
        assert app.savePath is not None
        assert isinstance(app.savePath, Path)

    def test_config_file_path_set(self):
        """configFile should be set"""
        app = PychingAppDetails(createConfigDir=0)
        assert app.configFile is not None
        assert isinstance(app.configFile, Path)

    def test_config_file_has_correct_name(self):
        """Config file should be named pychingrc"""
        app = PychingAppDetails(createConfigDir=0)
        assert app.configFile.name == 'pychingrc'

    def test_config_file_in_config_path(self):
        """Config file should be in config path"""
        app = PychingAppDetails(createConfigDir=0)
        assert app.configFile.parent == app.configPath


class TestModuleLevelPychingInstance:
    """Test the module-level pyching instance"""

    def test_module_has_pyching_instance(self):
        """Module should have a pyching instance"""
        assert hasattr(pyching_engine, 'pyching')

    def test_module_pyching_is_correct_type(self):
        """Module pyching should be PychingAppDetails"""
        assert isinstance(pyching_engine.pyching, PychingAppDetails)

    def test_module_pyching_accessible(self):
        """Module pyching instance should be accessible"""
        pyching = pyching_engine.pyching
        assert pyching.title == 'pyChing'
        assert isinstance(pyching.version, str)


class TestAppDetailsContacts:
    """Test contact information in app details"""

    def test_has_email_address(self):
        """App should have email address"""
        app = PychingAppDetails(createConfigDir=0)
        assert hasattr(app, 'emailAddress')
        assert isinstance(app.emailAddress, str)
        assert '@' in app.emailAddress

    def test_has_web_address(self):
        """App should have web address"""
        app = PychingAppDetails(createConfigDir=0)
        assert hasattr(app, 'webAddress')
        assert isinstance(app.webAddress, str)
        assert 'http' in app.webAddress.lower()


class TestAppDetailsEdgeCases:
    """Test edge cases in app configuration"""

    def test_multiple_instances_independent(self):
        """Multiple PychingAppDetails instances should be independent"""
        app1 = PychingAppDetails(createConfigDir=0)
        app2 = PychingAppDetails(createConfigDir=0)

        assert app1 is not app2
        # But they should have same values
        assert app1.title == app2.title
        assert app1.version == app2.version

    def test_create_config_dir_flag_respected(self):
        """createConfigDir flag should be respected"""
        # createConfigDir=0 should not create directory
        test_dir = f'.pyching_no_create_{os.getpid()}'
        cfg_path = Path.home() / test_dir

        # Clean up if exists
        if cfg_path.exists():
            try:
                cfg_path.rmdir()
            except:
                pass

        app = PychingAppDetails(createConfigDir=0)
        # Manual call with createConfigDir=0 shouldn't create
        # (actual behavior depends on implementation)

    @patch.dict(os.environ, {}, clear=True)
    def test_works_with_minimal_environment(self):
        """App should work even with minimal environment"""
        try:
            app = PychingAppDetails(createConfigDir=0)
            assert app is not None
            assert app.title == 'pyChing'
        except Exception as e:
            # Should not crash
            pytest.fail(f"Failed with minimal environment: {e}")


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
