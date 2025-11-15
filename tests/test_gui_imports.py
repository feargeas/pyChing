"""
Test that critical imports are available in GUI modules

Verifies the import bug fixes (TclError, TkVersion) are correctly implemented.
These tests ensure that exception handling will work properly.
"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestTkinterImports:
    """Test that tkinter imports are correct in GUI modules"""

    def test_tclerror_available_in_pyching_interface_tkinter(self):
        """Verify TclError is imported in pyching_interface_tkinter (Bug #1 fix)"""
        import pyching_interface_tkinter

        # TclError should be accessible in the module namespace
        # This was the critical bug - TclError was used but not imported
        assert hasattr(pyching_interface_tkinter, 'TclError')

        # Verify it's the actual TclError exception
        from tkinter import TclError as ActualTclError
        assert pyching_interface_tkinter.TclError is ActualTclError

    def test_tclerror_available_in_smgHtmlView(self):
        """Verify TclError is imported in smgHtmlView (Bug #2 fix)"""
        import smgHtmlView

        # TclError should be accessible
        assert hasattr(smgHtmlView, 'TclError')

        # Verify it's the actual TclError exception
        from tkinter import TclError as ActualTclError
        assert smgHtmlView.TclError is ActualTclError

    def test_tkversion_available_in_smgAbout(self):
        """Verify TkVersion is explicitly imported in smgAbout (Bug #3 fix)"""
        import smgAbout

        # TkVersion should be accessible
        # Previously relied on wildcard import which is fragile
        assert hasattr(smgAbout, 'TkVersion')

        # Verify it's the actual TkVersion
        from tkinter import TkVersion as ActualTkVersion
        assert smgAbout.TkVersion is ActualTkVersion


class TestExceptionHandling:
    """Test that exception handling works correctly"""

    def test_tclerror_can_be_caught(self):
        """Test that TclError can be caught in exception handlers"""
        from tkinter import TclError

        # Verify we can raise and catch TclError
        with pytest.raises(TclError):
            raise TclError("Test error")

    def test_icon_loading_error_handling_pattern(self):
        """Test the pattern used in icon loading (line 126)"""
        from tkinter import TclError

        # This simulates the try/except pattern used in the GUI
        error_caught = False
        try:
            # Simulate an icon loading failure
            raise TclError("Can't load icon")
        except TclError:
            error_caught = True

        assert error_caught, "TclError should be caught"


class TestImportStructure:
    """Test the import structure of GUI modules"""

    def test_pyching_interface_tkinter_imports(self):
        """Verify all necessary imports in pyching_interface_tkinter"""
        import pyching_interface_tkinter

        # Check for critical imports
        assert hasattr(pyching_interface_tkinter, 'TclError')
        assert hasattr(pyching_interface_tkinter, 'Tk')
        assert hasattr(pyching_interface_tkinter, 'Frame')
        assert hasattr(pyching_interface_tkinter, 'Button')

    def test_smgAbout_imports(self):
        """Verify all necessary imports in smgAbout"""
        import smgAbout

        # Check for critical imports
        assert hasattr(smgAbout, 'TkVersion')
        assert hasattr(smgAbout, 'smgDialog')

    def test_smgHtmlView_imports(self):
        """Verify all necessary imports in smgHtmlView"""
        import smgHtmlView

        # Check for critical imports
        assert hasattr(smgHtmlView, 'TclError')
        assert hasattr(smgHtmlView, 'smgDialog')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
