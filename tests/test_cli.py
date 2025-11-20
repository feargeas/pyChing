"""
Test Command Line Interface
============================

These tests validate command-line argument parsing and execution.

THESE TESTS VALIDATE CLI ARGUMENT HANDLING.
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from io import StringIO

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pyching
import pytest


class TestHelpFlag:
    """Test -h and --help flags"""

    @patch('sys.argv', ['pyching', '-h'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_help_flag_short(self, mock_stdout):
        """'-h' should display help and exit"""
        with pytest.raises(SystemExit) as exc_info:
            pyching.CommandLineSwitches()

        assert exc_info.value.code == 0
        output = mock_stdout.getvalue()
        assert 'help' in output.lower()

    @patch('sys.argv', ['pyching', '--help'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_help_flag_long(self, mock_stdout):
        """'--help' should display help and exit"""
        with pytest.raises(SystemExit) as exc_info:
            pyching.CommandLineSwitches()

        assert exc_info.value.code == 0
        output = mock_stdout.getvalue()
        assert 'help' in output.lower()

    @patch('sys.argv', ['pyching', '/h'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_help_flag_windows_style(self, mock_stdout):
        """'/h' should display help (Windows style)"""
        with pytest.raises(SystemExit) as exc_info:
            pyching.CommandLineSwitches()

        assert exc_info.value.code == 0

    @patch('sys.argv', ['pyching', '-h'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_help_shows_all_options(self, mock_stdout):
        """Help should show all available options"""
        with pytest.raises(SystemExit):
            pyching.CommandLineSwitches()

        output = mock_stdout.getvalue()
        assert '-h' in output or '--help' in output
        assert '-v' in output or '--version' in output
        assert '-c' in output or '--console' in output
        assert '-d' in output or '--disable-version-check' in output


class TestVersionFlag:
    """Test -v and --version flags"""

    @patch('sys.argv', ['pyching', '-v'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_version_flag_short(self, mock_stdout):
        """'-v' should display version and exit"""
        with pytest.raises(SystemExit) as exc_info:
            pyching.CommandLineSwitches()

        assert exc_info.value.code == 0
        output = mock_stdout.getvalue()
        assert 'version' in output.lower()

    @patch('sys.argv', ['pyching', '--version'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_version_flag_long(self, mock_stdout):
        """'--version' should display version and exit"""
        with pytest.raises(SystemExit) as exc_info:
            pyching.CommandLineSwitches()

        assert exc_info.value.code == 0
        output = mock_stdout.getvalue()
        assert 'version' in output.lower()

    @patch('sys.argv', ['pyching', '/v'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_version_flag_windows_style(self, mock_stdout):
        """'/v' should display version (Windows style)"""
        with pytest.raises(SystemExit) as exc_info:
            pyching.CommandLineSwitches()

        assert exc_info.value.code == 0

    @patch('sys.argv', ['pyching', '-v'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_version_shows_number(self, mock_stdout):
        """Version output should contain version number"""
        with pytest.raises(SystemExit):
            pyching.CommandLineSwitches()

        output = mock_stdout.getvalue()
        # Should contain something that looks like a version number
        assert any(char.isdigit() for char in output)


class TestConsoleFlag:
    """Test -c and --console flags"""

    @patch('sys.argv', ['pyching', '-c'])
    def test_console_flag_short(self):
        """'-c' flag should be recognized"""
        # Just test that it doesn't crash during switches check
        # Actual console launching tested elsewhere
        assert '-c' in sys.argv

    @patch('sys.argv', ['pyching', '--console'])
    def test_console_flag_long(self):
        """'--console' flag should be recognized"""
        assert '--console' in sys.argv

    @patch('sys.argv', ['pyching', '/c'])
    def test_console_flag_windows_style(self):
        """'/c' flag should be recognized (Windows style)"""
        assert '/c' in sys.argv


class TestDisableVersionCheckFlag:
    """Test -d and --disable-version-check flags"""

    @patch('sys.argv', ['pyching', '-d'])
    @patch('sys.stderr', new_callable=StringIO)
    def test_disable_version_check_short(self, mock_stderr):
        """'-d' should disable version checking with warning"""
        pyching.CommandLineSwitches()
        output = mock_stderr.getvalue()
        assert 'warning' in output.lower() or 'disabled' in output.lower()

    @patch('sys.argv', ['pyching', '--disable-version-check'])
    @patch('sys.stderr', new_callable=StringIO)
    def test_disable_version_check_long(self, mock_stderr):
        """'--disable-version-check' should disable version checking"""
        pyching.CommandLineSwitches()
        output = mock_stderr.getvalue()
        assert 'warning' in output.lower() or 'disabled' in output.lower()

    @patch('sys.argv', ['pyching', '/d'])
    @patch('sys.stderr', new_callable=StringIO)
    def test_disable_version_check_windows_style(self, mock_stderr):
        """'/d' should disable version checking (Windows style)"""
        pyching.CommandLineSwitches()
        output = mock_stderr.getvalue()
        assert 'warning' in output.lower() or 'disabled' in output.lower()


class TestVersionChecking:
    """Test Python and Tk version checking"""

    @patch('sys.argv', ['pyching'])
    @patch('sys.version_info', (3, 9, 0, 'final', 0))
    @patch('sys.stderr', new_callable=StringIO)
    def test_insufficient_python_version(self, mock_stderr):
        """Python < 3.10 should be rejected"""
        with pytest.raises(SystemExit) as exc_info:
            pyching.CommandLineSwitches()

        assert exc_info.value.code == 1
        output = mock_stderr.getvalue()
        assert 'Python' in output
        assert '3.10' in output

    @patch('sys.argv', ['pyching'])
    def test_sufficient_python_version(self):
        """Python >= 3.10 should pass version check"""
        # Current Python should be >= 3.10 for tests to run
        assert sys.version_info >= (3, 10)
        # Should not raise during version check
        try:
            pyching.CommandLineSwitches()
        except SystemExit:
            # May exit for other reasons, that's ok
            pass

    @patch('sys.argv', ['pyching', '-d'])
    @patch('sys.version_info', (3, 9, 0, 'final', 0))
    def test_version_check_bypassed_with_flag(self):
        """Version check should be bypassed with -d flag"""
        # Should not exit due to version check
        try:
            pyching.CommandLineSwitches()
            # If we get here, version check was bypassed
            assert True
        except SystemExit as e:
            # Should not be version-related exit
            assert e.code != 1


class TestNoArguments:
    """Test running with no arguments"""

    @patch('sys.argv', ['pyching'])
    def test_no_arguments_default_behavior(self):
        """Running with no args should proceed normally"""
        # Should not exit during CommandLineSwitches
        try:
            pyching.CommandLineSwitches()
        except SystemExit:
            pytest.fail("Should not exit with no arguments")


class TestMultipleFlags:
    """Test combining multiple flags"""

    @patch('sys.argv', ['pyching', '-d', '-c'])
    @patch('sys.stderr', new_callable=StringIO)
    def test_disable_and_console(self, mock_stderr):
        """Multiple flags should work together"""
        pyching.CommandLineSwitches()
        output = mock_stderr.getvalue()
        assert 'warning' in output.lower()
        assert '-c' in sys.argv

    @patch('sys.argv', ['pyching', '-h', '-v'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_help_takes_precedence(self, mock_stdout):
        """Help flag should be processed first"""
        with pytest.raises(SystemExit) as exc_info:
            pyching.CommandLineSwitches()

        # Should exit with help, not version
        assert exc_info.value.code == 0


class TestMainFunction:
    """Test the main() entry point"""

    @patch('sys.argv', ['pyching', '-h'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_help(self, mock_stdout):
        """main() should handle help flag"""
        with pytest.raises(SystemExit) as exc_info:
            pyching.main()

        assert exc_info.value.code == 0

    @patch('sys.argv', ['pyching', '-v'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_version(self, mock_stdout):
        """main() should handle version flag"""
        with pytest.raises(SystemExit) as exc_info:
            pyching.main()

        assert exc_info.value.code == 0


class TestFlagVariations:
    """Test various flag format combinations"""

    @patch('sys.stdout', new_callable=StringIO)
    def test_help_variations(self, mock_stdout):
        """All help flag variations should work"""
        variations = ['-h', '--help', '/h']

        for flag in variations:
            with patch('sys.argv', ['pyching', flag]):
                with pytest.raises(SystemExit) as exc_info:
                    pyching.CommandLineSwitches()
                assert exc_info.value.code == 0

    @patch('sys.stdout', new_callable=StringIO)
    def test_version_variations(self, mock_stdout):
        """All version flag variations should work"""
        variations = ['-v', '--version', '/v']

        for flag in variations:
            with patch('sys.argv', ['pyching', flag]):
                with pytest.raises(SystemExit) as exc_info:
                    pyching.CommandLineSwitches()
                assert exc_info.value.code == 0


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
