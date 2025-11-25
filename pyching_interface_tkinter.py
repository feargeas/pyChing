##---------------------------------------------------------------------------##
##
## pyChing -- a Python program to cast and interpret I Ching hexagrams
##
## Copyright (C) 1999-2006 Stephen M. Gava
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be of some
## interest to somebody, but WITHOUT ANY WARRANTY; without even the 
## implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
## See the GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING or COPYING.txt. If not, 
##  write to the Free Software Foundation, Inc.,
## 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
## The license can also be found at the GNU/FSF website: http://www.gnu.org
##
## Stephen M. Gava
## <elguavas@users.sourceforge.net>
## http://pyching.sourgeforge.net
##
##---------------------------------------------------------------------------##
"""
tkinter interface module for pyching
"""

#python library imports
import sys
import os
import time
import copy
import argparse
import json
from pathlib import Path
from typing import Optional, Any

#tkinter imports
from tkinter import *
from tkinter import TclError
from tkinter import font as tkFont
import tkinter.filedialog as tkFileDialog
import tkinter.messagebox as tkMessageBox
import tkinter.colorchooser as tkColorChooser
import tkinter.simpledialog as tkSimpleDialog

#pyChing source specific imports
import pyching_cimages
import pyching_themes
from pyching_coin_animation import CoinAnimator

# Modern pyChing imports
from pyching import HexagramEngine, Element, Reading, Hexagram
from pyching.data import HexagramResolver

# Enhanced GUI windows
from gui_windows import HexagramInfoWindow, TextEditorWindow

#smg library module imports
from smgDialog import smgDialog
from smgHtmlView import smgHtmlView
from smgAbout import smgAbout

# Global verbose and debug flags for debugging output
VERBOSE = False
DEBUG = False

def vprint(*args, **kwargs):
    """Print only if verbose mode is enabled (-v)"""
    if VERBOSE:
        print("[pyChing]", *args, **kwargs)

def dprint(*args, **kwargs):
    """Print only if debug mode is enabled (very verbose -vv)"""
    if DEBUG:
        print("[pyChing DEBUG]", *args, **kwargs)

class WidgetColors:
    """
    colours for widgets in the reading display area

    Now supports theme loading. Can load a theme preset and optionally
    override individual colors.
    """
    def __init__(self, theme_name: str = 'default') -> None:
        """
        Initialize colors from a theme.

        Args:
            theme_name: Name of the theme to load (e.g., 'default', 'solarized-dark')
        """
        dprint(f"WidgetColors.__init__(theme_name='{theme_name}')")
        # Store theme name for config persistence
        self.theme_name = theme_name

        # Load the theme
        theme = pyching_themes.get_theme(theme_name)
        dprint(f"  Loaded theme class: {theme.__class__.__name__}")
        dprint(f"  Theme description: {theme.description}")
        dprint(f"  Theme line_style: {theme.line_style}")

        # Copy all color attributes from theme
        self.bgReading = theme.bgReading
        self.bgLabelHint = theme.bgLabelHint
        self.fgLabelHint = theme.fgLabelHint
        self.fgLabelPlaces = theme.fgLabelPlaces
        self.fgLabelHexTitles = theme.fgLabelHexTitles
        self.fgLabelLines = theme.fgLabelLines
        self.fgMessageQuestion = theme.fgMessageQuestion
        self.colorLineBody = theme.colorLineBody
        self.colorLineHighlight = theme.colorLineHighlight
        self.colorLineShadow = theme.colorLineShadow
        dprint(f"  Colors: bg={self.bgReading}, lineBody={self.colorLineBody}")

        # Store the theme object for HexLine to access line_style settings
        self.theme = theme

class WidgetFonts:
    """
    Modern font system for widgets in the main window

    Uses tkinter.font.Font objects for better cross-platform compatibility
    and easier customization. Fonts automatically adapt to the platform
    while maintaining consistent relative sizing.

    Supports font size scaling from 50% to 200% of base size.
    """
    def __init__(self, scale: float = 1.0) -> None:
        """
        Initialize fonts with optional scaling factor.

        Args:
            scale: Font size multiplier (0.5 to 2.0). Default 1.0 = 100%
        """
        dprint(f"WidgetFonts.__init__(scale={scale})")
        # Store scale for later adjustment
        self.scale = max(0.5, min(2.0, scale))  # Clamp between 50% and 200%
        dprint(f"  Clamped scale to: {self.scale} ({int(self.scale*100)}%)")

        # Define font families with fallbacks
        # Tkinter will use the first available font from the list
        self.sans_serif = ('Helvetica', 'Arial', 'DejaVu Sans', 'sans-serif')
        dprint(f"  Font family fallbacks: {self.sans_serif}")

        # Base font sizes (before scaling)
        self._base_sizes = {
            'small': 10,   # Menu, button, label
            'large': 12,   # Hexagram titles
        }

        # Create modern Font objects with scaled sizes
        # These work consistently across all platforms
        self._create_fonts()

    def _create_fonts(self) -> None:
        """Create or recreate all fonts with current scale"""
        small_size = int(self._base_sizes['small'] * self.scale)
        large_size = int(self._base_sizes['large'] * self.scale)
        dprint(f"  Creating fonts: small={small_size}pt, large={large_size}pt")

        # Menu and button fonts - small size, regular weight
        self.menu = tkFont.Font(family=self.sans_serif, size=small_size, weight='normal')
        self.button = tkFont.Font(family=self.sans_serif, size=small_size, weight='normal')

        # Regular label font - small size, regular weight
        self.label = tkFont.Font(family=self.sans_serif, size=small_size, weight='normal')

        # Hexagram title font - large size, bold
        self.labelHexTitles = tkFont.Font(family=self.sans_serif, size=large_size, weight='bold')

        # Line hint font - small size, regular weight
        self.labelLineHint = tkFont.Font(family=self.sans_serif, size=small_size, weight='normal')
        dprint(f"  Created 5 font objects")

    def set_scale(self, scale: float) -> None:
        """
        Adjust font sizes by setting a new scale factor.

        Args:
            scale: New scale factor (0.5 to 2.0)
        """
        old_scale = self.scale
        self.scale = max(0.5, min(2.0, scale))
        dprint(f"WidgetFonts.set_scale({scale:.2f}) - old={old_scale:.2f}, new={self.scale:.2f}")

        if old_scale != self.scale:
            # Recalculate sizes
            small_size = int(self._base_sizes['small'] * self.scale)
            large_size = int(self._base_sizes['large'] * self.scale)
            dprint(f"  Updating fonts: small={small_size}pt, large={large_size}pt")

            # Update existing Font objects
            self.menu.configure(size=small_size)
            self.button.configure(size=small_size)
            self.label.configure(size=small_size)
            self.labelHexTitles.configure(size=large_size)
            self.labelLineHint.configure(size=small_size)
            dprint(f"  All 5 font objects reconfigured")
        else:
            dprint(f"  No change needed (same scale)")

class WindowMain:
    """
    main application window
    """
    def __init__(self, master: Any) -> None:
        vprint("Initializing WindowMain...")
        self.master = master
        # Enable window resizing
        self.master.resizable(height=True, width=True)
        vprint("Window configured: resizable=True")

        #self.master.colormapwindows([self.master])#debug, does this solve the 256 color problem??
        self.images = pyching_cimages.CoinImages()
        vprint("Loaded coin images")

        try:
            self.master.iconbitmap(bitmap=f'@{pyching.execPath / "icon.xbm"}')
            vprint("Loaded application icon")
        except TclError:
            #sys.stderr.write("can't load icon bitmap")
            vprint("Could not load icon bitmap (not critical)")
            pass #just ignore this
        self.master.title(pyching.title + '  ' + pyching.version)

        #application-wide event bindings
        self.master.bind('<F1>',self.HelpBinding) #help key #bind_all
        self.master.bind('<Alt-c>',self.CastButtonBinding) #cast button
        self.master.bind('<Alt-v>',self.ViewHex1InfoButtonBinding) #view hex 1 info button
        self.master.bind('<Alt-i>',self.ViewHex2InfoButtonBinding) #view hex 2 info button
        vprint("Registered keyboard bindings: F1, Alt-c, Alt-v, Alt-i")

        #application-wide protocol bindings
        self.master.protocol("WM_DELETE_WINDOW", self.Quit)

        #configuration attributes
        self.showPlaces = BooleanVar()
        self.showPlaces.set(True)
        self.showLineHints = BooleanVar()
        self.showLineHints.set(True)
        self.castAll = BooleanVar()
        self.castAll.set(True)
        self.showCoinAnimation = BooleanVar()
        self.showCoinAnimation.set(True)
        vprint("Default settings: showPlaces=True, showLineHints=True, castAll=True, showCoinAnimation=True")

        #instantiate default colour and font values
        self.colors = WidgetColors()
        self.fonts = WidgetFonts()
        vprint(f"Initialized colors: theme='{self.colors.theme_name}'")
        vprint(f"Initialized fonts: scale={self.fonts.scale} (100% = {int(self.fonts.scale * 100)}%)")

        #load configuration file (if any)
        self.LoadSettings()

        self.MakeMenus(self.master)

        self.MakeStatusBar(self.master)

        #main frame
        frameMainBevel = Frame(self.master, borderwidth=2, relief='sunken', highlightthickness=0)
        frameMainBevel.pack(expand=True, fill='both', padx=4)#used as a bevel for the main frame
        self.frameMain = Frame(frameMainBevel, bg=self.colors.bgReading)#highlightthickness=4,borderwidth=4,relief='sunken')#,borderwidth=1,relief='solid'
        self.frameMain.pack(expand=True, fill='both')
        
        self.MakeCastDisplay(self.frameMain)

        self.MakeQuestionDisplay(self.frameMain)

        self.MakeHexDisplay(self.frameMain)

        # Create coin animator with hex line drawing capability
        # (must be after MakeHexDisplay since it needs self.hexLines)
        self.coin_animator = CoinAnimator(
            self.labelsCoins,
            self.images,
            self.master,
            hex_lines=self.hexLines,
            place_labels=self.labelsHexPlaces,
            show_places_var=self.showPlaces,
            colors=self.colors
        )
        vprint("Created coin animator with progressive line drawing")

        # Set dynamic minimum size based on natural content size
        # This ensures the window is never larger than needed initially
        # while preventing users from shrinking it below usable size
        # Info buttons are grid()'ed during this calculation for accurate sizing
        self.master.update_idletasks()  # Force layout calculation
        natural_width = self.master.winfo_reqwidth()
        natural_height = self.master.winfo_reqheight()
        self.master.minsize(natural_width, natural_height)
        vprint(f"Set dynamic minsize: {natural_width}x{natural_height} (includes all elements)")
        dprint(f"  Window will start at natural size and can be resized larger")
        dprint(f"  Minimum prevents shrinking below usable dimensions")
        dprint(f"  Info buttons included in calculation")

        # Hide info buttons initially (no reading yet)
        # Frame stays grid()'ed during sizing, but removed now for clean initial appearance
        self.frameInfoButtons.grid_remove()
        dprint(f"  Info buttons hidden initially (will appear on first reading)")

        self.hexes = None #so we can test if a reading has been performed yet
    
    def Quit(self):
        #print 'bye now'#debug
        vprint("User quit - closing application...")
        self.master.quit()
        
    def __AddMenu(self,parent,title):
        if title == 'Help': menuName = 'help'#name option to right justify help menu under X
        else: menuName = None
        _menu = Menu(parent,name=menuName,tearoff=0,font=self.fonts.menu)#create the menu
        if parent == self.master:#this is the menubar itself
            parent.configure(menu=_menu)#make _menu the menubar
            _menu.configure(borderwidth=0)
        else: #this is a dropdown from the menubar  
            parent.add_cascade(label=title,underline=0,menu=_menu)#add the menu to the menubar
        return _menu

    def MakeMenus(self, parent):
        dprint("Creating application menus...")
        self.menuMain = self.__AddMenu(parent,'')#create the menubar
        self.menuMainFile = self.__AddMenu(self.menuMain,'File')#create the file menu
        dprint("  Created File menu")
        self.menuMainSettings = self.__AddMenu(self.menuMain,'Settings')#create the settings menu
        dprint("  Created Settings menu")
        self.menuMainHelp = self.__AddMenu(self.menuMain,'Help')#create the help menu
        dprint("  Created Help menu")

        def AddMenuItems(menu, items):
            dprint(f"  Adding {len(items)} items to menu")
            for item in items:
                if item[0] == 's':#add a separator
                    menu.add_separator()
                    dprint(f"    - separator")
                elif item[0] == 'c':#add a command
                    menu.add_command(label=item[1],underline=item[2],command=item[3])
                    dprint(f"    - command: {item[1]}")
                elif item[0] == 'k':#add a checkbutton
                    menu.add_checkbutton(label=item[1],underline=item[2],command=item[3],variable=item[4])
                    dprint(f"    - checkbutton: {item[1]}")
                elif item[0] == 'r':#add a radiobutton
                    menu.add_radiobutton(label=item[1],underline=item[2],command=item[3],variable=item[4],value=item[5])
                    dprint(f"    - radiobutton: {item[1]} (value={item[5]})")
                #elif item[0] == 'm':#add a submenu
                # pass #not implemented 
        
        AddMenuItems(self.menuMainFile,(('c','Load Reading...',0,self.LoadReading),
                                                    ('c','Save Reading...',0,self.SaveReading),('s',),
                                                    ('c','Save Reading As Text...',16,self.SaveReadingAsText),('s',),
                                                    ('c','Compare Sources...',0,self.CompareSourcesDialog),('s',),
                                                    ('c','Exit',1,self.Quit)) )
        AddMenuItems(self.menuMainSettings,(('k','Show Places',5,self.__ToggleLabelsPlaces,self.showPlaces),
            ('k','Show Line Hints',10,None,self.showLineHints),
            ('k','Show Coin Animation',10,None,self.showCoinAnimation),('s',),
            ('r','Cast Each Line Separately',10,None,self.castAll,False),
            ('r','Cast Entire Hexagram Automatically',12,None,self.castAll,True),('s',),
            ('c','Select Theme...',7,self.SelectTheme),
            ('c','Adjust Font Size...',7,self.AdjustFontSize),
            ('c','Configure Colors...',10,self.SetColors),('s',),
            ('c','Save Settings',0,self.SaveSettings)) )
        AddMenuItems(self.menuMainHelp,(
            ('c','Using '+pyching.title,0,self.ShowHelpUsingPyching),
            ('c','Introduction to the I Ching',0,self.ShowHelpIChingIntro),
            ('c','Browse Hexagram Information',0,self.ShowHelpHexInfo),
            ('s',),
            ('c','About '+pyching.title+'...',0,self.ShowAbout)) )
        #self.ShowText(title='Help - Using '+pyching.title,textFile='help.txt')),
        self.menuMainFile.entryconfigure(1, state='disabled')#disable save item by default
        self.menuMainFile.entryconfigure(3, state='disabled')#disable save as text item by default
        
    def HelpBinding(self,event):
        #main window binding for the F1 key
        #try:
        self.ShowHelpUsingPyching()
        #except KeyError:
        # pass #this error is raised while pressing F1 over a tk file dialog, ignore it

    def CastButtonBinding(self,event):
        #binding for the Meta-c hotkey on buttonCast
        if self.buttonCast.cget('state') == 'normal': #if the button isn't disabled
            self.buttonCast.invoke()
    
    def ViewHex1InfoButtonBinding(self, event):
        #binding for the Meta-v hotkey on buttonViewHex1Info
        if self.buttonViewHex1Info.cget('state') == 'normal': #if the button isn't disabled
            self.buttonViewHex1Info.invoke()

    def ViewHex2InfoButtonBinding(self, event):
        #binding for the Meta-i hotkey on buttonViewHex1Info
        if self.buttonViewHex2Info.cget('state') == 'normal': #if the button isn't disabled
            self.buttonViewHex2Info.invoke()

    def ShowHelpUsingPyching(self):
        self.ShowHtml(title=pyching.title + ' - Help',
                htmlSource='pyching_hlhtx_data.hlHelpData()',
                index='pyching_hlhtx_data.hlHelpData()')
        
    def ShowHelpIChingIntro(self):
        self.ShowHtml(title=pyching.title + ' - Help',
                htmlSource='pyching_hlhtx_data.hlIntroData()',
                index='pyching_hlhtx_data.hlHelpData()')
            
    def ShowHelpHexInfo(self):
        """Browse hexagram information using modern interface."""
        # Prompt user for hexagram number
        hexNum = tkSimpleDialog.askinteger(
            'Browse Hexagram Information',
            'Enter hexagram number (1-64):',
            parent=self.master,
            initialvalue=1,
            minvalue=1,
            maxvalue=64
        )

        if hexNum:
            # Load the hexagram using the from_number class method
            hexagram = Hexagram.from_number(hexNum)

            # Display using modern HexagramInfoWindow (no changing lines for browsing)
            HexagramInfoWindow(self.master, hexagram, changing_lines=[])
            
    def ShowText(self,title=None,textFile=None):
        #dialogTxt = DialogShowHtml(self.master,title=title,htmlFile=textFile,
        #    plainText=1)
        dialogTxt = smgHtmlView(self.master,title=title,htmlSource=textFile,
                plainText=1)

    def ShowHtml(self,title=None,htmlSource=None,index=None,hexBrowser=0):
        #dialoghtml = DialogShowHtml(self.master,title=title,htmlFile=textFile,
        #    indexFile=indexFile)
        dialoghtml = smgHtmlView(self.master,title=title,
                htmlSource=htmlSource,
                internalLink=None,index=index,hexBrowser=hexBrowser)
        
    def ShowAbout(self):
        #dialogAbout = DialogAbout(self.master,currentColors=self.colors)
        aboutPicData="""R0lGODlhMgAyAKEAAAICBP4CBAIC/P///yH+Dk1hZGUgd2l0aCBHSU1QACH5BAEKAAMALAAA
AAAyADIAAAL+nI+ZwO0Ko1SOhYvvmzw2YWUi1nTmwAgqMLYic0rp6tYkEC+AStt+AMvNeKyf
L2ga9oxHXEe5ZNqQnh0v2nIwqZQrcXot/pwQqxdUM3+NZAR0nT2Lm90zNqO+pxd2+CiPJtUG
GAbmx3bw5jX31yB1Y0C4+EjpJDlJuRXZh5k5hsIp58l2acc42hhqeoqqUcoZ0nqjGuooq0i7
GJuJmyvHOvbqGwacJjxcKHiMfDgFyuxbjLcJnStNQl1New0UuUzcG2icyDxXKj2IfHqJzhf9
B7un8/4Sn9VGbg3fB4zvRq+hVpYJ4cC9WudvnjZRLxJS+KaKEReCEPk1zIGiIkMfVxgTaVwy
EWNBU5A6lhkJgkUJkxRxVXDIssrLkCYKAAA7"""
        dialogAbout = smgAbout(self.master,title='About '+pyching.title, 
                appTitle=pyching.title,
                version='Version: '+pyching.version,
                copyright='Copyright (c) 1999-2003 Stephen M. Gava',
                licence='Released under the GNU General Public Licence',
                email='email:  '+pyching.emailAddress,
                www='web:  '+pyching.webAddress,
                pictureData=aboutPicData,
                licenceFile=pyching.execPath / 'COPYING',
                creditsFile=pyching.execPath / 'CREDITS',
                fontAppTitle=self.fonts.labelHexTitles,  
                fontText=self.fonts.label,
                fg=self.colors.fgLabelHexTitles,
                bg=self.colors.bgReading )

    def SelectTheme(self):
        """Show theme selection dialog and apply the selected theme"""
        vprint("Opening theme selection dialog...")
        dialogSelectTheme = DialogSelectTheme(self.master,
                                              current_theme=getattr(self.colors, 'theme', None))
        if dialogSelectTheme.result:  # user selected a theme
            # Apply the new theme
            theme_name = dialogSelectTheme.result
            vprint(f"User selected theme: '{theme_name}'")
            self.colors = WidgetColors(theme_name)
            vprint(f"Applied theme '{theme_name}' (line_style={self.colors.theme.line_style})")
            self.RepaintColors(self.colors)
            vprint("Theme applied and GUI repainted")
        else:
            vprint("Theme selection cancelled")

    def AdjustFontSize(self):
        """Show font size adjustment dialog"""
        old_scale = self.fonts.scale
        vprint(f"Opening font size dialog (current scale={old_scale:.2f} = {int(old_scale*100)}%)...")
        dialogFontSize = DialogAdjustFontSize(self.master,
                                              current_scale=self.fonts.scale)
        if dialogFontSize.result is not None:  # user selected a new size
            # Apply the new font scale
            new_scale = dialogFontSize.result
            vprint(f"User selected font scale: {new_scale:.2f} ({int(new_scale*100)}%)")
            self.fonts.set_scale(new_scale)
            vprint(f"Font sizes updated: small={int(10*new_scale)}pt, large={int(12*new_scale)}pt")
            # Fonts are Font objects, so changes propagate automatically to all widgets

            # Recalculate minimum size to accommodate new font sizes
            # If info buttons are hidden, temporarily show them for accurate size calculation
            frame_was_hidden = False
            try:
                self.frameInfoButtons.grid_info()
                dprint("  Info buttons frame is visible")
            except:
                # Frame is not grid()'ed, temporarily show it for sizing
                frame_was_hidden = True
                dprint("  Info buttons hidden, temporarily showing for size calculation")
                self.frameInfoButtons.grid(column=1, row=0, columnspan=3, sticky='nw', pady=5)
                # Set sample text with maximum expected length for accurate sizing
                sample_text = 'View information on:  64. Before Completion'
                self.buttonViewHex1Info.configure(text=sample_text)

            self.master.update_idletasks()  # Force layout recalculation
            natural_width = self.master.winfo_reqwidth()
            natural_height = self.master.winfo_reqheight()
            self.master.minsize(natural_width, natural_height)
            vprint(f"Updated minsize to {natural_width}x{natural_height} (adjusted for font scale)")
            dprint(f"  Window minimum size dynamically adjusted for new font size")

            # Hide frame again if it was hidden
            if frame_was_hidden:
                self.frameInfoButtons.grid_remove()
                self.buttonViewHex1Info.configure(text='')
                dprint("  Info buttons re-hidden after size calculation")
        else:
            vprint("Font size adjustment cancelled")

    def SetColors(self):
        dialogSetColors = DialogSetColors(self.master,currentColors=copy.copy(self.colors))
        if dialogSetColors.result: #user didn't cancel
            self.RepaintColors(dialogSetColors.result)    

    def SaveSettings(self) -> None:
        """Save settings to JSON config file"""
        vprint("Saving settings...")
        dprint(f"SaveSettings() called")
        try:
            # Failsafe if user deleted ~/.pyching while program running
            if not pyching.configPath.exists():
                pyching.configPath.mkdir(parents=True, exist_ok=True)
                vprint(f"Created config directory: {pyching.configPath}")
                dprint(f"  Created directory: {pyching.configPath}")
        except (RuntimeError, OSError) as e:
            dprint(f"  Failed to create config directory: {e}")
            pass  # If we can't create config dir, write will handle the error

        # Gather settings
        castAllValue = self.castAll.get()
        showPlacesValue = self.showPlaces.get()
        showLineHintsValue = self.showLineHints.get()
        showCoinAnimationValue = self.showCoinAnimation.get()
        theme_name = getattr(self.colors, 'theme_name', 'default')
        font_scale = self.fonts.scale

        vprint(f"  castAll={castAllValue}, showPlaces={showPlacesValue}, showLineHints={showLineHintsValue}, showCoinAnimation={showCoinAnimationValue}")
        vprint(f"  theme='{theme_name}', font_scale={font_scale:.2f} ({int(font_scale*100)}%)")

        # Create JSON config structure
        config = {
            'version': pyching.version,
            'appearance': {
                'theme': theme_name,
                'font_scale': font_scale
            },
            'display': {
                'cast_all': castAllValue,
                'show_places': showPlacesValue,
                'show_line_hints': showLineHintsValue,
                'show_coin_animation': showCoinAnimationValue
            }
        }
        dprint(f"  Config structure: {config}")

        # Write JSON file
        try:
            with open(pyching.configFile, 'w') as f:
                json.dump(config, f, indent=2)
            vprint(f"Settings saved to: {pyching.configFile}")
            dprint(f"  JSON written successfully")
            self.labelStatus.configure(text='saved settings')
        except (IOError, OSError) as e:
            vprint(f"ERROR: Unable to write config file: {pyching.configFile}")
            dprint(f"  Error: {e}")
            tkMessageBox.showerror(title='File Error',
                            message=f'Unable to write configuration file:\n{pyching.configFile}')

    def LoadSettings(self) -> None:
        """Load settings from JSON config file"""
        if pyching.configFile.exists():
            vprint(f"Loading settings from: {pyching.configFile}")
            dprint(f"LoadSettings() - config file exists")
            try:
                with open(pyching.configFile, 'r') as f:
                    config = json.load(f)
                dprint(f"  JSON loaded successfully: {config}")

                # Extract settings with defaults
                theme_name = config.get('appearance', {}).get('theme', 'default')
                font_scale = config.get('appearance', {}).get('font_scale', 1.0)
                castAllValue = config.get('display', {}).get('cast_all', True)
                showPlacesValue = config.get('display', {}).get('show_places', True)
                showLineHintsValue = config.get('display', {}).get('show_line_hints', True)
                showCoinAnimationValue = config.get('display', {}).get('show_coin_animation', True)

                vprint(f"  Loaded theme='{theme_name}', font_scale={font_scale:.2f} ({int(font_scale*100)}%)")
                dprint(f"  Display settings: cast_all={castAllValue}, show_places={showPlacesValue}, show_line_hints={showLineHintsValue}, show_coin_animation={showCoinAnimationValue}")

                # Apply theme and fonts
                self.colors = WidgetColors(theme_name)
                self.fonts = WidgetFonts(font_scale)

                # Apply display settings
                self.castAll.set(castAllValue)
                self.showPlaces.set(showPlacesValue)
                self.showLineHints.set(showLineHintsValue)
                self.showCoinAnimation.set(showCoinAnimationValue)

                vprint(f"  Settings loaded: castAll={castAllValue}, showPlaces={showPlacesValue}, showLineHints={showLineHintsValue}, showCoinAnimation={showCoinAnimationValue}")

            except (IOError, OSError) as e:
                vprint(f"ERROR: Unable to read configuration file: {pyching.configFile}")
                dprint(f"  IOError: {e}")
                sys.stderr.write(f'\n error (IOError): unable to read configuration file {pyching.configFile}\n')
                # Use defaults on error
                self.castAll.set(True)
                self.showPlaces.set(True)
                self.showLineHints.set(True)
                self.showCoinAnimation.set(True)
            except json.JSONDecodeError as e:
                vprint(f"ERROR: Invalid JSON in configuration file: {pyching.configFile}")
                dprint(f"  JSONDecodeError: {e}")
                sys.stderr.write(f'\n error (JSONDecodeError): invalid JSON in configuration file {pyching.configFile}\n')
                # Use defaults on error
                self.castAll.set(True)
                self.showPlaces.set(True)
                self.showLineHints.set(True)
                self.showCoinAnimation.set(True)
            except Exception as e:
                vprint(f"ERROR: Unexpected error loading configuration: {e}")
                dprint(f"  Exception: {e}")
                sys.stderr.write(f'\n error: unexpected error loading configuration file {pyching.configFile}\n')
                # Use defaults on error
                self.castAll.set(True)
                self.showPlaces.set(True)
                self.showLineHints.set(True)
                self.showCoinAnimation.set(True)
        else:
            vprint(f"No config file found at: {pyching.configFile}, using defaults")
            dprint("  Using default settings")
        
    def __HideLabel(self,label):
        label.configure(fg=label.cget('bg'))#fg=bg to hide label  
        
    def __ToggleLabelsPlaces(self):
        if self.hexes: #if there's been a reading yet
            for label in self.labelsHexPlaces:
                if label.cget('fg') == self.colors.fgLabelPlaces:
                    self.__HideLabel(label)
                else:
                    label.configure(fg=self.colors.fgLabelPlaces)
    
    def ClearReading(self): 
        self.HideInfoButtons()#get rid of any info buttons  
        for coin in self.labelsCoins:#clear coins display
            coin.configure(image=self.images.coinFrames[16])
        #blank both hexagram displays
        for i in range(2):
            for line in self.hexLines[i]:
                line.Draw(linetype=None)
        for label in self.labelsHexPlaces:
            self.__HideLabel(label)
        for key in self.labelsNoMovingLines.keys():
            self.labelsNoMovingLines[key].lower()#hide the 'no moving lines' labels
        self.__HideLabel(self.labelBecomes)     
        self.labelH1Title.configure(text='')
        self.labelH2Title.configure(text='')
        self.messageQuestion.configure(text='')
        #wiped stuff still appears on win32?? - try below
        self.master.update()
    
    def CastHexes(self):
        vprint("Cast button pressed - starting new reading...")
        self.labelLineHint.show = 0 #disable line hints
        #get the question
        questionDialog = DialogGetQuestion(self.master)
        self.master.update()#makes sure the main app window gets redrawn properly (seems only to be a problem on win32)
        if questionDialog.result: #the user didn't cancel
            # Use modern HexagramEngine
            engine = HexagramEngine()

            # Get selected method and source
            method = Element(self.methodVar.get())
            source = self.sourceVar.get()

            # For Earth method: use earth.txt content as seed (the "soil")
            if method == Element.EARTH:
                earth_file = pyching.configPath / 'earth.txt'
                if earth_file.exists():
                    try:
                        with open(earth_file, 'r', encoding='utf-8') as f:
                            seed = f.read().strip()
                    except Exception:
                        seed = questionDialog.result  # Fallback to question
                else:
                    # Create default earth.txt if it doesn't exist
                    try:
                        if not pyching.configPath.exists():
                            pyching.configPath.mkdir(parents=True, exist_ok=True)
                        seed = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        with open(earth_file, 'w', encoding='utf-8') as f:
                            f.write(seed)
                    except Exception:
                        seed = questionDialog.result  # Fallback to question
            else:
                seed = None

            # Check method availability
            available, error = engine.check_method_available(method)
            if not available:
                tkMessageBox.showwarning(
                    "Method Unavailable",
                    f"The {method.value} method is unavailable:\n\n{error}\n\n"
                    "Suggestion: Use Fire method for high-quality randomness.\n\n"
                    "Please select another method."
                )
                self.labelLineHint.show = 1
                return

            try:
                # Cast reading using modern engine
                vprint(f"Question entered: '{questionDialog.result}'")
                vprint(f"Casting with method={method.value}, source={source}")

                self.reading = engine.cast_reading(
                    method=method,
                    question=questionDialog.result,
                    source=source,
                    seed=seed
                )

                # Display the reading (modern engine casts all at once)
                self.ClearReading()
                for coin in self.labelsCoins:  # initialise coins display
                    coin.configure(image=self.images.coinFrames[0])
                self.ShowQuestion()

                # Animate coin flips if enabled
                if self.showCoinAnimation.get():
                    vprint(f"Running coin animation for all 6 lines (method: {method.value})...")
                    self.coin_animator.animate_full_reading(self.reading, method=method.value)
                    vprint("Animation complete")

                self.DisplayReading()

            except Exception as e:
                tkMessageBox.showerror("Casting Error", f"Error casting reading:\n\n{e}")
                self.labelLineHint.show = 1
        else: #the user cancelled
            self.labelLineHint.show = 1 #re-enable line hints
        
    def CastNextLine(self):
        self.buttonCast.configure(state='disabled')
        self.CastLine()
        self.buttonCast.configure(state='normal')
        if self.hexes.hex1.lineValues[5] == 0:#if hex1 is'nt fully built yet
            self.buttonCast.configure(text='Cast Line '+str(self.hexes.currentLine+1)+' of 6')
            self.labelStatus.configure(text='Waiting to cast line '+str(self.hexes.currentLine+1)+ ' of 6 ...')
        else:#hex1 is fully built now
            for menuItem in range(3,5):#re-enable cast-type changing
                self.menuMainSettings.entryconfigure(menuItem, state='normal')
            self.buttonCast.configure(text='Create 2nd Hexagram',command=self.BuildHex2)
            self.labelStatus.configure(text='Waiting to create 2nd hexagram ...')
            
    def CastAllLines(self,loadingSaveFile=0):
        self.buttonCast.configure(state='disabled')
        if loadingSaveFile: 
            self.hexes.currentLine = 0
            self.ShowQuestion()
        for line in self.hexLines[0]:#build and display hexagram 1
            if loadingSaveFile: #increment the current line
                self.hexes.currentLine = self.hexes.currentLine + 1
            self.CastLine(loadingFromFile=loadingSaveFile)
            self.master.update_idletasks()
            if not loadingSaveFile: time.sleep(1)#pause to let user see the thrown coins
        self.BuildHex2()#show second hexagram
        self.buttonCast.configure(state='normal')
        #self.master.update_idletasks()

    def CastLine(self,loadingFromFile=0):
        if not loadingFromFile:
            self.hexes.NewLine()
            self.labelStatus.configure(text='Casting Line '+str(self.hexes.currentLine)+' of 6 ...')
            #for spins in range(3):
            for spins in range(2):
                    for frameNum in range(14):
                        for coin in self.labelsCoins:
                            coin.configure(image=self.images.coinFrames[frameNum])
                            self.master.update_idletasks()
                        #time.sleep(0.06)
                        #time.sleep(0.04)
                        time.sleep(0.02)

            for i in range(3):
                self.labelsCoins[i].configure(image=self.images.coinFrames[self.hexes.currentOracleValues[i]+12])
                self.master.update_idletasks()

        #self.hexes.hex1.lineValues[self.hexes.currentLine-1] = 8#debug!!
        if self.showPlaces.get():#if places should be shown
            self.labelsHexPlaces[self.hexes.currentLine-1].configure(fg=self.colors.fgLabelPlaces)#show the place name
            #self.__ShowLabel(self.labelsHexPlaces[self.hexes.currentLine-1])#show the place name
        self.hexLines[0][self.hexes.currentLine-1].Draw(self.hexes.hex1.lineValues[self.hexes.currentLine-1])     
        #if loadingFromFile: self.hexLines[0][self.hexes.currentLine-1].update()
        #self.master.update_idletasks()
    
    def DisplayReading(self):
        """Display a reading using the modern Reading dataclass."""
        if not hasattr(self, 'reading') or not self.reading:
            return

        vprint(f"Displaying reading: {self.reading.primary.number} -> {self.reading.relating.number if self.reading.relating else 'no change'}")

        # Display hexagram 1 title
        self.labelH1Title.configure(
            text=f"{self.reading.primary.number}.  {self.reading.primary.english_name}"
        )

        # Display hexagram 1 lines
        for i, line_value in enumerate(self.reading.primary.lines):
            if self.showPlaces.get():
                self.labelsHexPlaces[i].configure(fg=self.colors.fgLabelPlaces)
            self.hexLines[0][i].Draw(line_value)

        # Display hexagram 2 if there are moving lines
        if self.reading.relating:
            self.labelBecomes.configure(fg=self.colors.fgLabelLines)
            self.labelH2Title.configure(
                text=f"{self.reading.relating.number}.  {self.reading.relating.english_name}"
            )

            # Display hex2 lines (already transformed in relating hexagram)
            for i, line_value in enumerate(self.reading.relating.lines):
                self.hexLines[1][i].Draw(line_value)
        else:
            # Show "no moving lines" message
            for i in self.labelsNoMovingLines:
                self.labelsNoMovingLines[i].tkraise()

        # Finalize display
        self.labelStatus.configure(text='')
        self.labelLineHint.show = 1  # enable line hints

        for coin in self.labelsCoins:  # blank coins display
            coin.configure(image=self.images.coinFrames[16])

        self.buttonCast.configure(text='Cast New Hexagram', command=self.CastHexes)
        self.ShowInfoButtons()  # show the info buttons

        self.menuMainFile.entryconfigure(1, state='normal')  # enable save menuitem
        self.menuMainFile.entryconfigure(3, state='normal')  # enable save as text menuitem

    def BuildHex2(self):
        """Legacy method - redirects to DisplayReading()"""
        self.DisplayReading()

    def MakeCastDisplay(self, parent):
        self.frameCast = Frame(parent, bg=self.colors.bgReading)
        self.frameCast.pack(anchor='nw', side='top')

        # Modern controls frame
        self.frameControls = Frame(self.frameCast, bg=self.colors.bgReading)
        self.frameControls.grid(column=0, row=0, columnspan=5, sticky='nw', padx=20, pady=10)

        # Method selection
        Label(self.frameControls, text='Method:', bg=self.colors.bgReading,
              fg=self.colors.fgLabelLines, font=self.fonts.label).grid(row=0, column=0, sticky='w', padx=5)
        self.methodVar = StringVar(value='wood')
        self.methodMenu = OptionMenu(self.frameControls, self.methodVar,
                                      'wood', 'metal', 'fire', 'earth', 'water',
                                      command=self.OnMethodChange)
        self.methodMenu.config(width=8, font=self.fonts.button)
        self.methodMenu.grid(row=0, column=1, sticky='w', padx=5)

        # Source selection
        Label(self.frameControls, text='Source:', bg=self.colors.bgReading,
              fg=self.colors.fgLabelLines, font=self.fonts.label).grid(row=0, column=2, sticky='w', padx=5)
        self.sourceVar = StringVar(value='canonical')
        self.sourceMenu = OptionMenu(self.frameControls, self.sourceVar,
                                      'canonical', 'wilhelm_baynes', 'legge_simplified')
        self.sourceMenu.config(width=12, font=self.fonts.button)
        self.sourceMenu.grid(row=0, column=3, sticky='w', padx=5)

        # Manual input button
        self.buttonManual = Button(self.frameControls, text='Manual Input',
                                   width=12, bg=None, fg=None, font=self.fonts.button,
                                   highlightthickness=0, takefocus=False,
                                   command=self.ManualInput)
        self.buttonManual.grid(row=0, column=4, sticky='w', padx=10)

        # "View earth text" button (initially hidden, shows when Earth method selected)
        self.buttonViewEarthText = Button(self.frameControls, text='View earth text',
                                          width=15, bg=None, fg=None, font=self.fonts.button,
                                          highlightthickness=0, takefocus=False,
                                          command=self.ViewEarthText)
        # Initially hidden - will be grid()'ed when Earth method is selected

        # Cast button
        self.buttonCast = Button(self.frameCast, text='Cast New Hexagram', underline=0,
                        width=20, bg=None, fg=None, font=self.fonts.button, highlightthickness=0,
                        takefocus=False, command=self.CastHexes)
        self.buttonCast.grid(column=0, row=1, sticky='nw', padx=20, pady=10)

        self.labelsCoins = []
        for i in range(3):
            self.labelsCoins.append(Label(self.frameCast,image=self.images.coinFrames[16],
                            bg=self.colors.bgReading) )
            self.labelsCoins[i].grid(column=i+1,row=1,padx=10,pady=10)

        # Note: coin animator will be created after hex display is set up
        # (needs access to hexLines which are created in MakeHexDisplay)

        # Info button frame and buttons
        # These are always grid()'ed to be included in layout calculations,
        # but disabled/invisible when not in use
        self.frameInfoButtons = Frame(self.frameCast, bg=self.colors.bgReading)
        self.buttonViewHex1Info = Button(self.frameInfoButtons, text='', underline=0,
                        bg=None, fg=None, font=self.fonts.button, highlightthickness=0,
                        takefocus=False, state='disabled', command=self.ViewHex1Info)
        self.buttonViewHex2Info = Button(self.frameInfoButtons, text='', underline=1,
                        bg=None, fg=None, font=self.fonts.button, highlightthickness=0,
                        takefocus=False, state='disabled', command=self.ViewHex2Info)

        # Grid them immediately so they're always part of layout (ensures correct minsize)
        self.buttonViewHex1Info.grid(column=0, row=0, pady=15)
        self.frameInfoButtons.grid(column=0, row=2, columnspan=4, sticky='nw', pady=10, padx=20)
                
    def ShowInfoButtons(self):
        """Show and enable info buttons by setting text, state, and making frame visible"""
        if not hasattr(self, 'reading') or not self.reading:
            return

        textStub = 'View information on:  '

        # Ensure frame is visible (in case it was hidden)
        self.frameInfoButtons.grid(column=0, row=2, columnspan=4, sticky='nw', pady=10, padx=20)

        # Always update hex1 button (always visible when there's a reading)
        self.buttonViewHex1Info.configure(
            text=f"{textStub}{self.reading.primary.number}. {self.reading.primary.english_name}",
            state='normal')

        # Hex2 button only shown if there are moving lines
        if self.reading.relating:
            self.buttonViewHex2Info.configure(
                text=f"{textStub}{self.reading.relating.number}. {self.reading.relating.english_name}",
                state='normal')
            # Adjust hex1 button padding when both buttons are visible
            self.buttonViewHex1Info.grid(column=0, row=0, pady=5)
            self.buttonViewHex2Info.grid(column=0, row=1)
        else:
            # Hide hex2 button when there are no moving lines
            self.buttonViewHex2Info.configure(text='', state='disabled')
            self.buttonViewHex2Info.grid_remove()  # Remove from layout but keep grid position
            # More padding when only hex1 button is visible
            self.buttonViewHex1Info.grid(column=0, row=0, pady=15)

    def HideInfoButtons(self):
        """Hide info buttons by removing frame from view (buttons stay grid()'ed inside frame)"""
        # Clear text and disable buttons
        self.buttonViewHex1Info.configure(text='', state='disabled')
        self.buttonViewHex2Info.configure(text='', state='disabled')
        self.buttonViewHex2Info.grid_remove()  # Remove hex2 from layout when hidden

        # Hide the entire frame so no empty button widgets are visible
        # Buttons stay grid()'ed inside frame for proper sizing calculations
        self.frameInfoButtons.grid_remove()

    def OnMethodChange(self, *args):
        """Show/hide 'View earth text' button when Earth method is selected."""
        method = self.methodVar.get()
        if method == 'earth':
            # Show the "View earth text" button
            self.buttonViewEarthText.grid(row=1, column=0, columnspan=5, sticky='w', padx=20, pady=5)
        else:
            # Hide the button
            self.buttonViewEarthText.grid_forget()

    def ManualInput(self):
        """Allow manual input of hexagram number and moving lines."""
        dialogManual = DialogManualInput(self.master)
        if dialogManual.result:  # User didn't cancel
            hex_number, moving_lines = dialogManual.result
            self.CastManualHexagram(hex_number, moving_lines)

    def CastManualHexagram(self, hex_number: int, moving_lines: list[int]):
        """Create reading from manually entered hexagram."""
        self.ClearReading()

        # Get the hexagram data
        source = self.sourceVar.get()

        # Convert hexagram number to line values (initially all stable)
        # Get base hexagram to know the binary pattern
        base_hex = Hexagram.from_number(hex_number, source=source)

        line_values = []
        for i, bit in enumerate(reversed(base_hex.binary)):
            if bit == '1':
                # Yang line - check if it's moving
                if (i + 1) in moving_lines:
                    line_values.append(9)  # Old yang (moving)
                else:
                    line_values.append(7)  # Young yang (stable)
            else:
                # Yin line - check if it's moving
                if (i + 1) in moving_lines:
                    line_values.append(6)  # Old yin (moving)
                else:
                    line_values.append(8)  # Young yin (stable)

        # Create primary hexagram with line values
        hex_data = Hexagram.from_number(hex_number, source=source)
        hex_data.lines = line_values

        # Calculate relating hexagram if there are moving lines
        relating_hex = None
        if moving_lines:
            # Transform moving lines to get relating hexagram
            # 6 (old yin) → 7 (yang), 9 (old yang) → 8 (yin), stable lines unchanged
            transformed_lines = []
            for line_val in line_values:
                if line_val == 6:  # old yin becomes yang
                    transformed_lines.append(7)
                elif line_val == 9:  # old yang becomes yin
                    transformed_lines.append(8)
                else:  # stable lines unchanged
                    transformed_lines.append(line_val)
            relating_hex = Hexagram.from_lines(transformed_lines, source=source)

        # Create reading
        self.reading = Reading(
            primary=hex_data,
            relating=relating_hex,
            question='[Manually entered hexagram]',
            method='manual',
            source_id=source,
            changing_lines=moving_lines,
            oracle_values=[]
        )

        # Display the hexagram
        self.ShowQuestion()
        self.DisplayReading()

    def DisplayManualReading(self):
        """Legacy method - redirects to DisplayReading()"""
        self.DisplayReading()

    def ViewEarthText(self):
        """Open earth.txt in an editable window."""
        earth_file = pyching.configPath / 'earth.txt'
        window = TextEditorWindow(self.master, "Earth Method Seed - Edit Text", earth_file)

    def ViewHex1Info(self):
        """View hexagram 1 information with Chinese character, SVG, and changing lines."""
        if not hasattr(self, 'reading') or not self.reading:
            return

        # Open sophisticated info window with changing lines
        window = HexagramInfoWindow(self.master, self.reading.primary,
                                    changing_lines=self.reading.changing_lines)

    def ViewHex2Info(self):
        """View hexagram 2 (relating) information."""
        if not hasattr(self, 'reading') or not self.reading or not self.reading.relating:
            return

        # For hex2, no changing lines (they've already transformed)
        window = HexagramInfoWindow(self.master, self.reading.relating,
                                    changing_lines=[])

    def MakeHexDisplay(self, parent):
        self.frameHexes = Frame(parent, bg=self.colors.bgReading)
        self.frameHexes.pack(anchor='nw', side='top', padx=20)
                        
        self.frameSpacerC4R1 = Frame(self.frameHexes,height=8,bg=self.colors.bgReading)
        self.frameSpacerC4R1.grid(column=4,row=1)
        
        self.labelsHexPlaces = []
        labelsTexts = ('topmost','fifth','fourth','third','second','bottom')
        for labelNum in range(6):
            self.labelsHexPlaces.append(Label(self.frameHexes, text=labelsTexts[labelNum],
                            bg=self.colors.bgReading, fg=self.colors.bgReading, font=self.fonts.label) )#fg=bg because label starts off hidden
            self.__HideLabel(self.labelsHexPlaces[labelNum])
            self.labelsHexPlaces[labelNum].grid(column=0, row=labelNum+2, sticky='e')
        self.labelsHexPlaces.reverse()#puts the labels in order of appearance

        self.labelH1Title = Label(self.frameHexes,text='',bg=self.colors.bgReading,
                        fg=self.colors.fgLabelHexTitles,font=self.fonts.labelHexTitles)
        self.labelH1Title.grid(column=1,row=0)
        
        self.labelH2Title = Label(self.frameHexes,text='',bg=self.colors.bgReading,
                        fg=self.colors.fgLabelHexTitles,font=self.fonts.labelHexTitles)
        self.labelH2Title.grid(column=3,row=0)

        self.labelBecomes = Label(self.frameHexes,text='becomes',bg=self.colors.bgReading,
                        fg=self.colors.bgReading,font=self.fonts.label)#fg=bg because label starts off hidden
        #self.__HideLabel(self.labelBecomes)
        self.labelBecomes.grid(column=2,row=4)
        
        #lineTexts = ('no','moving','lines')#lineTexts[key-3]
        self.labelsNoMovingLines = {3:'no',4:'moving',5:'lines'}
        for key in self.labelsNoMovingLines.keys():
            self.labelsNoMovingLines[key] = Label(self.frameHexes,
                        text=self.labelsNoMovingLines[key],bg=self.colors.bgReading,
                        fg=self.colors.fgLabelLines,font=self.fonts.label)
            self.labelsNoMovingLines[key].grid(row=key,column=3)
            
        self.hexLines = ([],[])
        
        for hexNum in range(2):
            for lineNum in range(6):
                self.hexLines[hexNum].append(HexLine(self.frameHexes,
                                bindingEnter=self.ShowLineDetails,bindingLeave=self.ClearLineDetails,
                                currentColors=self.colors, theme=self.colors.theme))
                if hexNum == 0: colNum = 1 
                else: colNum = 3 #set the corect grid column
                self.hexLines[hexNum][lineNum].grid(column=colNum,row=lineNum+2,padx=20,pady=1)
            self.hexLines[hexNum].reverse()#puts the labels in hex filling order
        
        self.frameSpacerC4R7 = Frame(self.frameHexes,width=20,bg=self.colors.bgReading)
        self.frameSpacerC4R7.grid(column=4,row=8)

        self.labelLineHint = Label(self.master, text=None, bg=self.colors.bgLabelHint,
                                            fg=self.colors.fgLabelHint, font=self.fonts.labelLineHint,
                                            borderwidth=1, relief='solid', padx=6)
        self.labelLineHint.place_forget() 
        #add an attribute to the hint label to indicate if it can currently be
        #shown or not (eg. hints should not be shown during hex building). 
        #this is independent of the user preference held in self.showLineHints .
        self.labelLineHint.show = 0 
    
    def ShowLineDetails(self,event):
        if  self.labelLineHint.show and event.widget.hint: #if hints can be shown and there is a hint for the line
            self.labelStatus.configure(text=event.widget.hint)#show line details on the status line
            if self.showLineHints.get():#if the user wants to see line details hints, show them
                self.labelLineHint.configure(text=event.widget.hint)
                self.labelLineHint.place(relx=0.1,rely=1.0,x=2,y=2,in_=event.widget)
                #self.labelLineHint.tkraise()
                self.labelLineHint.update()
                
    def ClearLineDetails(self,event):
        if event.widget.hint: #if there's a hint for the line
            self.labelStatus.configure(text='')
            if self.showLineHints.get():
                self.labelLineHint.configure(text=None)
                self.labelLineHint.place_forget() 

    def MakeQuestionDisplay(self, parent):
        #print self.frameMain.winfo_width()#cget('width')#.winfo_width()#cget(key)
        self.frameQuestion = Frame(parent, bg=self.colors.bgReading, borderwidth=2)
        self.frameQuestion.pack(anchor='sw', side='bottom', expand=True, fill='x', padx=10, pady=5)
        self.messageQuestion = Message(self.frameQuestion, width=20, text=None, justify='left',
                                                 bg=self.colors.bgReading, fg=self.colors.fgMessageQuestion,
                                                 font=self.fonts.label)
        self.messageQuestion.pack(anchor='w')

    def ShowQuestion(self):
        if hasattr(self, 'reading') and self.reading:
            self.messageQuestion.configure(width=self.frameQuestion.winfo_width(),
                                         text=self.reading.question)
    def HideQuestion(self):
        #self.frameQuestion.configure(relief=FLAT)
        self.messageQuestion.configure(width=20,text=None)

    def MakeStatusBar(self, parent):
        self.frameStatusBar = Frame(parent, borderwidth=2, relief='sunken', highlightthickness=2)
        self.frameStatusBar.pack(anchor='sw', side='bottom', fill='x', padx=2)#,expand=True
        self.labelStatus = Label(self.frameStatusBar,
                        text=pyching.title + '  ' + pyching.version,font=self.fonts.label)
        self.labelStatus.pack()

        #button for debug/testing purposes only
        #self.buttonDebug = Button(self.frameStatusBar,text='DEBUG',command=self.DEBUG)
        #self.buttonDebug.pack(anchor=E)
 
    def DEBUG(self):
        #run any routines in test or debug from here
        print('begin debug\n')
        #
        print(sys.path)
        #
        print('\nend debug')
        
    def RepaintColors(self,newColors):
        dprint(f"RepaintColors() called")
        dprint(f"  Old theme: {getattr(self.colors, 'theme_name', 'unknown')}")
        dprint(f"  New theme: {getattr(newColors, 'theme_name', 'unknown')}")
        dprint(f"  Updating {12 + 6*2} widget backgrounds...")
        oldColors=self.colors #save them for comparison below
        self.colors=newColors
        #these are always repainted
        self.frameMain.configure(bg=self.colors.bgReading)
        self.frameCast.configure(bg=self.colors.bgReading)
        for i in range(3):
            self.labelsCoins[i].configure(bg=self.colors.bgReading)
        self.frameHexes.configure(bg=self.colors.bgReading)
        self.frameInfoButtons.configure(bg=self.colors.bgReading)
        self.frameSpacerC4R1.configure(bg=self.colors.bgReading)
        self.frameSpacerC4R7.configure(bg=self.colors.bgReading)
        self.frameQuestion.configure(bg=self.colors.bgReading)
        self.labelLineHint.configure(bg=self.colors.bgLabelHint,fg=self.colors.fgLabelHint)
        self.messageQuestion.configure(bg=self.colors.bgReading,fg=self.colors.fgMessageQuestion)
        self.labelH1Title.configure(bg=self.colors.bgReading,fg=self.colors.fgLabelHexTitles)
        self.labelH2Title.configure(bg=self.colors.bgReading,fg=self.colors.fgLabelHexTitles)
        for key in self.labelsNoMovingLines.keys():
            self.labelsNoMovingLines[key].configure(bg=self.colors.bgReading,fg=self.colors.fgLabelLines)
        #the backgrounds of these are always repainted
        for hexNum in range(2):
            for lineNum in range(6):
                self.hexLines[hexNum][lineNum].configure(bg=self.colors.bgReading)
                self.hexLines[hexNum][lineNum].colors = self.colors #so they will draw correctly next time
        #self.frameMain.update()
        #the backgrounds of these are always repainted, and fg=bg to hide them as
        #fg will be repainted in the correct color below if required
        for labelNum in range(6):
            self.labelsHexPlaces[labelNum].configure(bg=self.colors.bgReading,fg=self.colors.bgReading)
        self.labelBecomes.configure(bg=self.colors.bgReading,fg=self.colors.bgReading)
        #the foreground of these are only repainted here if a reading has been performed
        #otherwise they will paint in the new colors next time they are shown
        if hasattr(self, 'reading') and self.reading:  # a reading has been performed
            if self.showPlaces.get():  # if places should be shown
                for labelNum in range(6):
                    self.labelsHexPlaces[labelNum].configure(fg=self.colors.fgLabelPlaces)
            if self.reading.relating:  # if there is a second hexagram
                self.labelBecomes.configure(fg=self.colors.fgLabelLines)
            #only redraw all lines now if their fg colors have changed
            if (oldColors.colorLineBody != self.colors.colorLineBody) or \
                            (oldColors.colorLineHighlight != self.colors.colorLineHighlight) or \
                            (oldColors.colorLineShadow != self.colors.colorLineShadow):
                for hexNum in range(2):
                    for lineNum in range(6):
                        self.hexLines[hexNum][lineNum].Draw(self.hexLines[hexNum][lineNum].value)
            elif oldColors.bgReading != self.colors.bgReading: #but if only the bg color has changed
                for hexNum in range(2): #repaint any 9 lines, to give the correct color in their inner circle
                    for lineNum in range(6):
                        if self.hexLines[hexNum][lineNum].value == 9:
                            self.hexLines[hexNum][lineNum].Draw(self.hexLines[hexNum][lineNum].value)
                
    def SaveReading(self):
        fileName = tkFileDialog.asksaveasfilename(parent=self.master,
                        title='Save Reading', defaultextension='.json',
                        filetypes=[('JSON reading files', '*.json'),
                                   ('All files', '*.*')],
                        initialdir=pyching.savePath)
        if not fileName:
            return  # user cancelled

        if not hasattr(self, 'reading') or not self.reading:
            tkMessageBox.showwarning(title='No Reading',
                                    message='No reading to save. Please cast a hexagram first.')
            return

        try:
            # Save using modern Reading JSON format
            self.reading.save(fileName)
            self.labelStatus.configure(text='saved reading: '+fileName)
        except IOError:
            tkMessageBox.showerror(title='File Error',
                            message='Unable to write save file:\n'+fileName)
        except Exception as e:
            tkMessageBox.showerror(title='Save Error',
                            message=f'Error saving reading:\n\n{str(e)}')
            
    def LoadReading(self):
        self.labelLineHint.show = 0  # disable line hints
        fileName = tkFileDialog.askopenfilename(parent=self.master,
                        title='Load Saved Reading', defaultextension='.json',
                        filetypes=[('JSON reading files', '*.json'),
                                   ('All files', '*.*')],
                        initialdir=pyching.savePath)
        if not fileName:
            self.labelLineHint.show = 1  # re-enable line hints
            return  # user cancelled

        try:
            # Load modern JSON Reading format
            self.reading = Reading.load(fileName)

            # Update UI to reflect loaded settings
            self.methodVar.set(self.reading.method)
            self.sourceVar.set(self.reading.source_id)

            # Display the reading
            self.ClearReading()
            self.ShowQuestion()
            self.DisplayReading()
            self.labelStatus.configure(text='loaded reading: '+fileName)

        except Exception as e:
            tkMessageBox.showerror(title='Load Error',
                                  message=f'Error loading reading file:\n\n{str(e)}')

        self.labelLineHint.show = 1  # re-enable line hints

    def SaveReadingAsText(self):
        fileName = tkFileDialog.asksaveasfilename(parent=self.master,
                        title='Save Reading As Text',defaultextension='.txt',
                        filetypes=[('text files','*.txt')],
                        initialdir=pyching.savePath)
        if not fileName:
            return  # user cancelled

        if not hasattr(self, 'reading') or not self.reading:
            tkMessageBox.showwarning(title='No Reading',
                                    message='No reading to save. Please cast a hexagram first.')
            return

        # Format reading as text
        textData = f"pyChing I Ching Reading\n"
        textData += "=" * 60 + "\n\n"
        textData += f"Question: {self.reading.question}\n"
        textData += f"Date: {self.reading.timestamp}\n"
        textData += f"Method: {self.reading.method}\n"
        textData += f"Source: {self.reading.source_id}\n\n"
        textData += f"Hexagram {self.reading.primary.number}: {self.reading.primary.english_name}\n"
        textData += "-" * 60 + "\n"
        textData += f"Line values: {self.reading.primary.lines}\n"
        if self.reading.relating:
            textData += f"\nChanging to Hexagram {self.reading.relating.number}: {self.reading.relating.english_name}\n"
            textData += f"Moving lines: {self.reading.changing_lines}\n"
        else:
            textData += "\nNo moving lines\n"
        textData += "\n" + "=" * 60 + "\n"

        try:
            with open(fileName, 'w') as textFile:
                textFile.write(textData)
        except IOError:
            tkMessageBox.showerror(title='File Error',
                            message='Unable to write text file:\n'+fileName)

    def CompareSourcesDialog(self):
        """Show source comparison dialog."""
        if not hasattr(self, 'reading') or not self.reading:
            tkMessageBox.showinfo(title='No Reading',
                                 message='Please cast a hexagram first before comparing sources.')
            return

        # Create a simple comparison window
        dialogCompare = DialogCompareSources(self.master, str(self.reading.primary.number))
        # The dialog will display itself

class HexLine(Canvas):
    """
    creates a hexagram line object
    """
    def __init__(self, parent: Any, bindingEnter: Optional[Any] = None,
                 bindingLeave: Optional[Any] = None, currentColors: Optional[WidgetColors] = None,
                 theme: Optional[Any] = None) -> None:
        self.value=None
        self.hint=None
        if currentColors: self.colors = currentColors
        else: self.colors = WidgetColors()

        # Store theme for line style rendering
        self.theme = theme if theme else None

        Canvas.__init__(self, parent, height=25, width=145, bg=self.colors.bgReading,
                        takefocus=False, highlightthickness=0)
        #self.tag_bind('all','<Enter>',bindingEnter)#when the mouse enters the drawing
        self.bind('<Enter>',bindingEnter)#when the mouse enters the canvas
        self.bind('<Leave>',bindingLeave)#when the mouse leaves the canvas

    def Draw(self,linetype=None):
        """Draw the hexagram line using the appropriate style"""
        #draw the required linetype and set the relevant value and hint
        hints = {6: 'line value = 6 (moving yin)',7: 'line value = 7 (yang)',
                        8: 'line value = 8 (yin)',9: 'line value = 9 (moving yang)'}
        self.configure(bg=self.colors.bgReading)
        self.update()

        if linetype in [6, 7, 8, 9]:
            self.value = linetype
            self.hint = hints[linetype]

            # Dispatch to appropriate drawing style based on theme
            if self.theme and hasattr(self.theme, 'line_style'):
                if self.theme.line_style == 'flat':
                    self.DrawFlat(linetype)
                elif self.theme.line_style == 'beveled':
                    self.DrawBeveled(linetype)
                else:
                    # Default to beveled for unknown styles
                    self.DrawBeveled(linetype)
            else:
                # No theme specified, use beveled (classic)
                self.DrawBeveled(linetype)
        else:  # blank the canvas (clear any existing drawing)
            self.value=None
            self.hint=None
            self.delete('all')

    def DrawBeveled(self, linetype):
        """Draw line with classic 3D beveled style"""
        if linetype == 6:  # Moving yin (broken with X)
            self.DrawBevelRectangle(origin=(1,6),height=13,width=60)
            self.DrawBevelRectangle(origin=(84,6),height=13,width=60)
            self.DrawBevelX(origin=(62,2),height=20,width=20)
        elif linetype == 7:  # Yang (solid)
            self.DrawBevelRectangle(origin=(2,6),height=13,width=141)
        elif linetype == 8:  # Yin (broken)
            self.DrawBevelRectangle(origin=(2,6),height=13,width=60)
            self.DrawBevelRectangle(origin=(83,6),height=13,width=60)
        elif linetype == 9:  # Moving yang (broken with O)
            self.DrawBevelRectangle(origin=(2,6),height=13,width=60)
            self.DrawBevelRectangle(origin=(83,6),height=13,width=60)
            self.DrawBevelO(origin=(62,2),height=20,width=20)

    def DrawFlat(self, linetype):
        """Draw line with modern flat style"""
        # Get line width from theme, default to 3
        line_width = 3
        if self.theme and hasattr(self.theme, 'line_width'):
            line_width = self.theme.line_width

        # Check if rounded corners requested
        rounded = False
        if self.theme and hasattr(self.theme, 'line_rounded_corners'):
            rounded = self.theme.line_rounded_corners

        color = self.colors.colorLineBody

        if linetype == 7:  # Yang (solid line)
            if rounded:
                self.DrawFlatRectangleRounded(origin=(2,8), height=9, width=141, color=color)
            else:
                self.create_rectangle(2, 8, 143, 17,
                    fill=color, outline=color, width=0, tags='BODY')

        elif linetype == 8:  # Yin (broken line)
            if rounded:
                self.DrawFlatRectangleRounded(origin=(2,8), height=9, width=60, color=color)
                self.DrawFlatRectangleRounded(origin=(83,8), height=9, width=60, color=color)
            else:
                self.create_rectangle(2, 8, 62, 17,
                    fill=color, outline=color, width=0, tags='BODY')
                self.create_rectangle(83, 8, 143, 17,
                    fill=color, outline=color, width=0, tags='BODY')

        elif linetype == 6:  # Moving yin (broken with X)
            if rounded:
                self.DrawFlatRectangleRounded(origin=(2,8), height=9, width=60, color=color)
                self.DrawFlatRectangleRounded(origin=(83,8), height=9, width=60, color=color)
            else:
                self.create_rectangle(2, 8, 62, 17,
                    fill=color, outline=color, width=0, tags='BODY')
                self.create_rectangle(83, 8, 143, 17,
                    fill=color, outline=color, width=0, tags='BODY')
            # Draw X marker
            self.DrawFlatX(origin=(67,7), size=11, color=color, width=line_width)

        elif linetype == 9:  # Moving yang (broken with O)
            if rounded:
                self.DrawFlatRectangleRounded(origin=(2,8), height=9, width=60, color=color)
                self.DrawFlatRectangleRounded(origin=(83,8), height=9, width=60, color=color)
            else:
                self.create_rectangle(2, 8, 62, 17,
                    fill=color, outline=color, width=0, tags='BODY')
                self.create_rectangle(83, 8, 143, 17,
                    fill=color, outline=color, width=0, tags='BODY')
            # Draw O marker
            self.DrawFlatO(origin=(67,7), size=11, color=color, width=line_width)

    def DrawFlatRectangleRounded(self, origin, height, width, color):
        """Draw a flat rectangle with rounded corners"""
        x, y = origin
        radius = min(4, height // 2)  # Corner radius

        # Create rounded rectangle using polygon
        self.create_polygon(
            x + radius, y,
            x + width - radius, y,
            x + width, y + radius,
            x + width, y + height - radius,
            x + width - radius, y + height,
            x + radius, y + height,
            x, y + height - radius,
            x, y + radius,
            fill=color, outline=color, smooth=True, tags='BODY')

    def DrawFlatX(self, origin, size, color, width=2):
        """Draw a simple X marker for moving yin"""
        x, y = origin
        # Draw X with two diagonal lines
        self.create_line(x, y, x + size, y + size,
            fill=color, width=width, tags='MARKER')
        self.create_line(x + size, y, x, y + size,
            fill=color, width=width, tags='MARKER')

    def DrawFlatO(self, origin, size, color, width=2):
        """Draw a simple O marker for moving yang"""
        x, y = origin
        # Draw circle outline
        self.create_oval(x, y, x + size, y + size,
            outline=color, width=width, tags='MARKER')
    
    def DrawBevelRectangle(self,origin=(0,0),height=13,width=0,bevel=2):

        color=self.colors.colorLineBody
        highlightcolor=self.colors.colorLineHighlight,
        shadowcolor=self.colors.colorLineShadow
                
        #fill with fg colour
        self.create_rectangle( ((origin[0],origin[1]),
                        (origin[0]+width-1,origin[1]+height-1)),width=0,
                        outline=color,fill=color,tags='BODY')

        #draw bevels
        for i in range(bevel):
            #draw highlight bevel
            if pyching.osType == 'nt': #allow for differences in tk canvas on win32
                self.create_line( ((origin[0]+i,origin[1]+height-i-1),
                                (origin[0]+i,origin[1]+i),
                                (origin[0]+width-i,origin[1]+i)),width=1,fill=highlightcolor,tags='HIGHLIGHT')
            else: #just draw without above modifications
                self.create_line( ((origin[0]+i,origin[1]+height-i),
                                (origin[0]+i,origin[1]+i),
                                (origin[0]+width-i,origin[1]+i)),width=1,fill=highlightcolor,tags='HIGHLIGHT')
            
            #draw shadow bevel
            if pyching.osType == 'nt': #allow for differences in tk canvas on win32
                self.create_line(  ( (origin[0]+i+1,origin[1]+((height-i)-1)),
                                                            (origin[0]+(width-i),origin[1]+((height-i)-1)) ),
                                                            width=1,fill=shadowcolor,tags='SHADOW')
                self.create_line(  ( (origin[0]+(width-i)-1,origin[1]+((height-i)-1)),
                                                            (origin[0]+(width-i)-1,origin[1]+i) ),
                                                            width=1,fill=shadowcolor,tags='SHADOW')
            else: #just draw without above modifications
                self.create_line(  ( (origin[0]+i+1,origin[1]+((height-i)-1)),
                                                            (origin[0]+(width-i),origin[1]+((height-i)-1)) ),
                                                            width=1,fill=shadowcolor,tags='SHADOW')
                self.create_line(  ( (origin[0]+(width-i)-1,origin[1]+((height-i)-1)),
                                                            (origin[0]+(width-i)-1,origin[1]+i+1) ),
                                                            width=1,fill=shadowcolor,tags='SHADOW')

    def DrawBevelX(self,origin=(0,0),height=0,width=0,thickness=4):

        color=self.colors.colorLineBody
        highlightcolor=self.colors.colorLineHighlight,
        shadowcolor=self.colors.colorLineShadow
                
        #filled cross with shadowcolor outline
        centre = ( origin[0]+width/2 , origin[1]+height/2 )
        iCO = thickness/2+2 #insideCornerOffset
        self.create_polygon(( ( origin[0]+thickness , origin[1] ),
                                                        ( centre[0] , centre[1]-iCO ),
                                                        ( origin[0]+width-thickness , origin[1] ),
                                                        ( origin[0]+width , origin[1]+thickness ),
                                                        ( centre[0]+iCO , centre[1] ),
                                                        ( origin[0]+width , origin[1]+height-thickness ),
                                                        ( origin[0]+width-thickness , origin[1]+height ),
                                                        ( centre[0] , centre[1]+iCO ),
                                                        ( origin[0]+thickness , origin[1]+height ),
                                                        ( origin[0] , origin[1]+height-thickness ),
                                                        ( centre[0]-iCO , centre[1] ),
                                                        ( origin[0] , origin[1]+thickness ) ),
                                                        outline=shadowcolor,width=1,fill=color,tags='BODY')     
        #pad the shadow to bevel width
        self.create_line( ( ( origin[0] +2, origin[1]+thickness +1),
                                                    ( centre[0]-iCO +1, centre[1] ) ),
                                                    width=1,fill=shadowcolor,tags='SHADOW')
        self.create_line( ( ( centre[0]+iCO , centre[1] -1),
                                                    ( origin[0]+width -1, origin[1]+thickness) ),
                                                    width=1,fill=shadowcolor,tags='SHADOW')
        self.create_line( ( ( origin[0] +2, origin[1]+height-thickness +1),
                                                    ( origin[0]+thickness , origin[1]+height -1),
                                                    ( centre[0] , centre[1]+iCO -1),
                                                    ( origin[0]+width-thickness , origin[1]+height -1),
                                                    ( origin[0]+width -1, origin[1]+height-thickness) ),
                                                    width=1,fill=shadowcolor,tags='SHADOW')
        #add the highlight
        self.create_line( ( ( origin[0] , origin[1]+height-thickness ),
                                                    ( centre[0]-iCO +1  , centre[1] -1 ) ),
                                                    width=1,fill=highlightcolor,tags='HIGHLIGHT')
        self.create_line( ( ( origin[0] +1, origin[1]+height-thickness ),
                                                    ( centre[0]-iCO +1  +1, centre[1] -1 ) ),
                                                    width=1,fill=highlightcolor,tags='HIGHLIGHT')
        self.create_line( ( ( centre[0]+iCO , centre[1] ),
                                                    ( origin[0]+width +1 , origin[1]+height-thickness +1 ) ),
                                                    width=1,fill=highlightcolor,tags='HIGHLIGHT')
        self.create_line( ( ( centre[0]+iCO -1, centre[1] ),
                                                    ( origin[0]+width, origin[1]+height-thickness +1) ),
                                                    width=1,fill=highlightcolor,tags='HIGHLIGHT')
        self.create_line( ( ( origin[0] , origin[1]+thickness ),
                                                    ( origin[0]+thickness , origin[1] ),
                                                    ( centre[0] , centre[1]-iCO ),
                                                    ( origin[0]+width-thickness , origin[1] ),
                                                    ( origin[0]+width +1 , origin[1]+thickness +1 ) ),
                                                    width=1,fill=highlightcolor,tags='HIGHLIGHT')
        self.create_line( ( ( origin[0] +1 , origin[1]+thickness ),
                                                    ( origin[0]+thickness , origin[1] +1),
                                                    ( centre[0] , centre[1]-iCO +1),
                                                    ( origin[0]+width-thickness , origin[1] +1),
                                                    ( origin[0]+width , origin[1]+thickness +1 ) ),
                                                    width=1,fill=highlightcolor,tags='HIGHLIGHT')

    def DrawBevelO(self,origin=(0,0),height=0,width=0,thickness=4):
        color=self.colors.colorLineBody
        highlightcolor=self.colors.colorLineHighlight,
        shadowcolor=self.colors.colorLineShadow
                
        #draw filled O with shadowcolor border
        self.create_oval( ( ( origin[0] , origin[1] ), 
                                                    ( origin[0]+width , origin[1]+height ) ), 
                                                    outline=shadowcolor,width=1,fill=shadowcolor)
        self.create_oval( ( ( origin[0]+1 , origin[1]+1 ), 
                                                    ( origin[0]+width-1 , origin[1]+height-1 ) ), 
                                                    outline=shadowcolor,width=1,fill=color,tags='BODY')#,fill=color
        #draw central O with shadowcolor border
        self.create_oval( ( ( origin[0]+thickness+1 , origin[1]+thickness+1 ), 
                                                    ( origin[0]+width-thickness-1 , origin[1]+height-thickness-1) ), 
                                                    outline=shadowcolor,width=1,fill=shadowcolor)
        self.create_oval( ( ( origin[0]+thickness+2 , origin[1]+thickness+2 ), 
                                                    ( origin[0]+width-thickness-2 , origin[1]+height-thickness-2) ), 
                                                    outline=shadowcolor,width=1,fill=self.cget('bg'),tags='SHADOW')#,fill='DarkGray'
        #add highlights
        #top
        self.create_arc(  ( ( origin[0] , origin[1] ), 
                                                    ( origin[0]+width , origin[1]+height ) ),
                                                    start=40,extent=180,
                                                    style='arc',width=1,outline=highlightcolor,tags='HIGHLIGHT')#'red' 
        self.create_arc(  ( ( origin[0]+1 , origin[1]+1 ), 
                                                    ( origin[0]+width-1 , origin[1]+height-1 ) ),
                                                    start=35,extent=180,
                                                    style='arc',width=1,outline=highlightcolor,tags='HIGHLIGHT')#'black' highlightcolor

        #lower inside
        self.create_arc(  ( ( origin[0]+thickness+1 , origin[1]+thickness+1 ), 
                                                    ( origin[0]+width-thickness-1 , origin[1]+height-thickness-1) ),
                                                    start=220,extent=180,
                                                    style='arc',width=1,outline=highlightcolor,tags='HIGHLIGHT')#'red'
        self.create_arc(  ( ( origin[0]+thickness+2 , origin[1]+thickness+2 ), 
                                                    ( origin[0]+width-thickness-2 , origin[1]+height-thickness-2) ),
                                                    start=215,extent=180,
                                                    style='arc',width=1,outline=highlightcolor,tags='HIGHLIGHT')#'black'
        #patch the highlight drawing to compensate for 
        #differences(!) in behaviour of tk canvas on win32
        if pyching.osType == 'nt':
            self.create_line( ( (origin[0]+1 , origin[1]+13),
                                                        (origin[0]+1 , origin[1]+6), 
                                                        (origin[0]+6 , origin[1]+1),
                                                        (origin[0]+8 , origin[1]+1),
                                                        (origin[0]+14 , origin[1]+1),
                                                        (origin[0]+16 , origin[1]+3) ),
                                                        width=1,fill=highlightcolor,tags='HIGHLIGHT')
            self.create_line( ( (origin[0]+7 , origin[1]+13),
                                                        (origin[0]+8 , origin[1]+14), 
                                                        (origin[0]+12 , origin[1]+14),
                                                        (origin[0]+15 , origin[1]+11) ),
                                                        width=1,fill=highlightcolor,tags='HIGHLIGHT')

class DialogSelectTheme(smgDialog):
    """
    Display a theme selection dialog
    """
    def __init__(self, parent: Any, current_theme: Optional[Any] = None) -> None:
        # Determine current theme name
        if current_theme and hasattr(current_theme, 'name'):
            # Search THEMES for matching theme class
            for theme_name, theme_class in pyching_themes.THEMES.items():
                if isinstance(current_theme, theme_class):
                    self.current_theme_name = theme_name
                    break
            else:
                self.current_theme_name = 'default'
        else:
            self.current_theme_name = 'default'

        self.selected_theme = StringVar()
        self.selected_theme.set(self.current_theme_name)

        smgDialog.__init__(self, parent, title='Select Theme',
                    buttons=[{'name':'buttonOk','title':'Ok','binding':'Ok','underline':None,'hotKey':'<Return>'},
                                {'name':'buttonCancel','title':'Cancel','binding':'Cancel','underline':None,'hotKey':'<Escape>'}],
                    buttonsDef=0, buttonsWidth=0, buttonsPad=5,
                    resizeable=0, transient=1, wait=1)

    def Body(self, master):
        """Create the theme selection UI"""
        master.configure(borderwidth=2, relief='sunken', highlightthickness=4)

        # Title
        label_title = Label(master, text='Select a theme for pyChing:',
                           font=('Helvetica', 11, 'bold'))
        label_title.grid(row=0, column=0, columnspan=2, sticky='w', padx=10, pady=(10, 5))

        # Create radio buttons for each theme
        row = 1
        for theme_name, theme_class in pyching_themes.THEMES.items():
            theme = theme_class()

            # Radio button
            rb = Radiobutton(master, text=theme.name,
                            variable=self.selected_theme, value=theme_name)
            rb.grid(row=row, column=0, sticky='w', padx=20, pady=2)

            # Description
            label_desc = Label(master, text=theme.description,
                              font=('Helvetica', 9), foreground='#666666')
            label_desc.grid(row=row, column=1, sticky='w', padx=5, pady=2)

            row += 1

    def Ok(self, event=None):
        """Handle OK button - return selected theme name"""
        self.result = self.selected_theme.get()
        self.Cancel()


class DialogAdjustFontSize(smgDialog):
    """
    Display a font size adjustment dialog with slider
    """
    def __init__(self, parent: Any, current_scale: float = 1.0) -> None:
        self.current_scale = current_scale
        self.scale_var = DoubleVar()
        self.scale_var.set(current_scale)

        smgDialog.__init__(self, parent, title='Adjust Font Size',
                    buttons=[{'name':'buttonOk','title':'Ok','binding':'Ok','underline':None,'hotKey':'<Return>'},
                                {'name':'buttonCancel','title':'Cancel','binding':'Cancel','underline':None,'hotKey':'<Escape>'}],
                    buttonsDef=0, buttonsWidth=0, buttonsPad=5,
                    resizeable=0, transient=1, wait=1)

    def Body(self, master):
        """Create the font size adjustment UI"""
        master.configure(borderwidth=2, relief='sunken', highlightthickness=4)

        # Title
        label_title = Label(master, text='Adjust Font Size:',
                           font=('Helvetica', 11, 'bold'))
        label_title.grid(row=0, column=0, columnspan=3, sticky='w', padx=10, pady=(10, 5))

        # Instructions
        label_inst = Label(master, text='Move the slider to adjust all font sizes proportionally.',
                          font=('Helvetica', 9))
        label_inst.grid(row=1, column=0, columnspan=3, sticky='w', padx=10, pady=5)

        # Current size display
        self.label_current = Label(master, text=f'{int(self.current_scale * 100)}%',
                                   font=('Helvetica', 14, 'bold'))
        self.label_current.grid(row=2, column=0, columnspan=3, pady=(5, 10))

        # Scale slider
        self.slider = Scale(master, from_=50, to=200, orient='horizontal',
                           variable=self.scale_var, command=self.on_scale_change,
                           length=300, showvalue=False, resolution=10)
        self.slider.grid(row=3, column=0, columnspan=3, padx=20, pady=10)

        # Size labels
        label_small = Label(master, text='50%', font=('Helvetica', 8))
        label_small.grid(row=4, column=0, sticky='w', padx=20)

        label_normal = Label(master, text='100% (Normal)', font=('Helvetica', 9, 'bold'))
        label_normal.grid(row=4, column=1)

        label_large = Label(master, text='200%', font=('Helvetica', 8))
        label_large.grid(row=4, column=2, sticky='e', padx=20)

        # Preset buttons
        frame_presets = Frame(master)
        frame_presets.grid(row=5, column=0, columnspan=3, pady=(10, 10))

        Button(frame_presets, text='Small (80%)', command=lambda: self.set_preset(0.8)).pack(side='left', padx=5)
        Button(frame_presets, text='Normal (100%)', command=lambda: self.set_preset(1.0)).pack(side='left', padx=5)
        Button(frame_presets, text='Large (120%)', command=lambda: self.set_preset(1.2)).pack(side='left', padx=5)
        Button(frame_presets, text='Extra Large (150%)', command=lambda: self.set_preset(1.5)).pack(side='left', padx=5)

    def on_scale_change(self, value):
        """Update the percentage label when slider moves"""
        scale = float(value) / 100
        self.label_current.configure(text=f'{int(float(value))}%')

    def set_preset(self, scale):
        """Set a preset font size"""
        self.scale_var.set(scale * 100)
        self.label_current.configure(text=f'{int(scale * 100)}%')

    def Ok(self, event=None):
        """Handle OK button - return selected scale"""
        self.result = self.scale_var.get() / 100  # Convert percentage to scale
        self.Cancel()


class DialogSetColors(smgDialog):
    """
    display a colour configuration dialog
    """
    def __init__(self, parent: Any, currentColors: Optional[WidgetColors] = None) -> None:
        if currentColors: self.colors=currentColors
        else: self.colors=WidgetColors()
        self.fonts=WidgetFonts()
        smgDialog.__init__(self, parent, title='Configure Colors',
                    buttons=[{'name':'buttonOk','title':'Ok','binding':'Ok','underline':None,'hotKey':'<Return>'},
                                {'name':'buttonCancel','title':'Cancel','binding':'Cancel','underline':None,'hotKey':'<Escape>'}],
                    buttonsDef=-1, buttonsWidth=0, buttonsPad=5,
                    resizeable=0, transient=1, wait=1)#buttonsPos='bottom',

    def Body(self, master):
        master.configure(borderwidth=2, relief='sunken', highlightthickness=4)

        self.frameDemo = Frame(master, bg=self.colors.bgReading, borderwidth=2, relief='flat')
        self.frameDemo.grid(row=1,column=0,padx=0,pady=10)
        self.frameDemo.bind('<ButtonPress-1>',self.SetColorExampleDetails)

        self.labelTitleDemo = Label(self.frameDemo,text='Hexagram Title',
                        font=self.fonts.labelHexTitles,borderwidth=0,
                        fg=self.colors.fgLabelHexTitles,bg=self.colors.bgReading)
        self.labelTitleDemo.grid(row=0,column=0,pady=5)
        self.labelTitleDemo.bind('<ButtonPress-1>',self.SetColorExampleDetails)
        
        self.lineDemos = []
        for i in range(4):
            self.lineDemos.append(HexLine(self.frameDemo,currentColors=self.colors, theme=self.colors.theme))
            #self.lineDemos[i].colors = self.colors
            self.lineDemos[i].Draw(linetype=i +6)  
            self.lineDemos[i].grid(row=i+1,column=0,padx=10)  
            self.lineDemos[i].bind('<ButtonPress-1>',self.SetColorExampleDetails)
            #self.tag_bind('BODY','<ButtonPress-1>',self.SetColorExampleDetails)
            #self.tag_bind('HIGHLIGHT','<ButtonPress-1>',self.SetColorExampleDetails)
            #self.tag_bind('SHADOW','<ButtonPress-1>',self.SetColorExampleDetails)
        
        self.labelQuestionDemo = Label(self.frameDemo,text='Reading Question',
                        font=self.fonts.label,borderwidth=0,
                        fg=self.colors.fgMessageQuestion,bg=self.colors.bgReading)
        self.labelQuestionDemo.grid(row=5,column=0,pady=5)
        self.labelQuestionDemo.bind('<ButtonPress-1>',self.SetColorExampleDetails)

        self.labelPlaceDemo = Label(self.frameDemo,text='place name',
                        font=self.fonts.label,borderwidth=0,
                        fg=self.colors.fgLabelPlaces,bg=self.colors.bgReading)
        self.labelPlaceDemo.grid(row=1,column=1,padx=5)
        self.labelPlaceDemo.bind('<ButtonPress-1>',self.SetColorExampleDetails)

        self.labelBecomesDemo = Label(self.frameDemo,text='becomes',
                        font=self.fonts.label,borderwidth=0,
                        fg=self.colors.fgLabelLines,bg=self.colors.bgReading)
        self.labelBecomesDemo.grid(row=2,column=1,padx=5)
        self.labelBecomesDemo.bind('<ButtonPress-1>',self.SetColorExampleDetails)

        self.labelNoMovingDemo = Label(self.frameDemo,text='no moving lines',
                        font=self.fonts.label,borderwidth=0,
                        fg=self.colors.fgLabelLines,bg=self.colors.bgReading)
        self.labelNoMovingDemo.grid(row=3,column=1,padx=5)
        self.labelNoMovingDemo.bind('<ButtonPress-1>',self.SetColorExampleDetails)

        self.frameHintBgDemo = Label(self.frameDemo, text='line hint',
                        font=self.fonts.labelLineHint, relief='solid', borderwidth=1,
                        bg=self.colors.bgLabelHint)
        self.frameHintBgDemo.grid(row=4, column=1, sticky='nsew', padx=5)#padx=5
        self.frameHintBgDemo.bind('<ButtonPress-1>',self.SetColorExampleDetails)

        self.labelHintDemo = Label(self.frameHintBgDemo,text='line hint',
                        font=self.fonts.labelLineHint,borderwidth=0,
                        fg=self.colors.fgLabelHint,bg=self.colors.bgLabelHint)
        self.labelHintDemo.grid(row=0,column=0)
        self.labelHintDemo.bind('<ButtonPress-1>',self.SetColorExampleDetails)
        
        self.SetColorButtonDetails()

        self.colorExampleDetails = { 'name': self.colorButtonDetails[0][0],
                                                    'color': self.colorButtonDetails[0][1] }

        self.frameColorSelect = Frame(master, bg=self.colorExampleDetails['color'],
                        relief='solid', borderwidth=1)
        self.frameColorSelect.grid(row=0, column=0, padx=10, pady=10, ipadx=10, ipady=10)

        self.buttonGetColor = Button(self.frameColorSelect, text='Set Color of:',
                        underline=0, highlightthickness=0, font=self.fonts.button,
                        takefocus=False, command=self.GetColor)
        self.buttonGetColor.grid(row=0,column=0,padx=2)

        self.menubuttonOptions = Menubutton(self.frameColorSelect, width=32,
                        text=self.colorButtonDetails[0][0], font=self.fonts.menu, indicatoron=True,
                        underline=self.colorButtonDetails[0][0].find('e'),
                        relief='raised', highlightthickness=0)
        self.menubuttonOptions.grid(row=0, column=1, padx=2, sticky='ns')#sticky='ns' makes the menubutton the same height as buttonGetColor
        self.menuOptions = Menu(self.menubuttonOptions,tearoff=0,font=self.fonts.menu)
        self.menubuttonOptions.configure(menu=self.menuOptions)
        for item in self.colorButtonDetails: #build the menu
            self.menuOptions.add_command(label=item[0],command=self.SetColorExample)
        #self.menuOptions.bind('<<MenuSelect>>',self.SetColorExampleDetails)

        self.buttonDefaults = Button(master,
                        text='Reset All Colors To '+pyching.title+' Defaults',
                        underline=0, highlightthickness=0, font=self.fonts.button,
                        takefocus=False, command=self.SetDefaultColors)
        self.buttonDefaults.grid(row=2, column=0, padx=10, pady=10, sticky='we')

        #return self.menubuttonOptions #control for initial focus

        #hot key bindings for this dialog
        self.bind('<Alt-s>',self.SetColorButtonBinding) #set color button
        self.bind('<Alt-e>',self.ScreenElementButtonBinding) #screen element selection button
        self.bind('<Alt-r>',self.ResetColorsButtonBinding) #reset default colors button

    def SetColorButtonBinding(self,event):
        self.buttonGetColor.invoke()

    def ScreenElementButtonBinding(self,event):
        #self.menubuttonOptions.invoke()
        #print self.menubuttonOptions.winfo_rootx(),self.menubuttonOptions.winfo_rooty(),\
        #   self.menubuttonOptions.winfo_height() #debug
        self.menuOptions.post(self.menubuttonOptions.winfo_rootx(),
                self.menubuttonOptions.winfo_rooty()+self.menubuttonOptions.winfo_height())
        #self.menuOptions.tk_mbPost()

    def ResetColorsButtonBinding(self,event):
        self.buttonDefaults.invoke()

    def SetColorButtonDetails(self):
        self.colorButtonDetails=( 
                ('Reading Background',self.colors.bgReading),
                ('Hexagram Titles',self.colors.fgLabelHexTitles),
                ('Reading Question',self.colors.fgMessageQuestion),
                ('Place Names',self.colors.fgLabelPlaces),
                ("'becomes' & 'no moving lines'",self.colors.fgLabelLines),
                ('Line Hint Background',self.colors.bgLabelHint),
                ('Line Hint Text',self.colors.fgLabelHint),
                ('Hexagram Line Body',self.colors.colorLineBody),
                ('Hexagram Line Highlight',self.colors.colorLineHighlight),
                ('Hexagram Line Shadow',self.colors.colorLineShadow) )

    def SetColorExampleDetails(self,event):
        if event.widget == self.frameDemo:
            self.colorExampleDetails['name']=self.colorButtonDetails[0][0]
            self.colorExampleDetails['color']=self.colorButtonDetails[0][1]
        elif event.widget == self.labelTitleDemo:
            self.colorExampleDetails['name']=self.colorButtonDetails[1][0]
            self.colorExampleDetails['color']=self.colorButtonDetails[1][1]
        elif event.widget == self.labelQuestionDemo:
            self.colorExampleDetails['name']=self.colorButtonDetails[2][0]
            self.colorExampleDetails['color']=self.colorButtonDetails[2][1]
        elif event.widget == self.labelPlaceDemo:
            self.colorExampleDetails['name']=self.colorButtonDetails[3][0]
            self.colorExampleDetails['color']=self.colorButtonDetails[3][1]
        elif event.widget == self.labelBecomesDemo:
            self.colorExampleDetails['name']=self.colorButtonDetails[4][0]
            self.colorExampleDetails['color']=self.colorButtonDetails[4][1]
        elif event.widget == self.labelNoMovingDemo:
            self.colorExampleDetails['name']=self.colorButtonDetails[4][0]
            self.colorExampleDetails['color']=self.colorButtonDetails[4][1]
        elif event.widget == self.frameHintBgDemo:
            self.colorExampleDetails['name']=self.colorButtonDetails[5][0]
            self.colorExampleDetails['color']=self.colorButtonDetails[5][1]
        elif event.widget == self.labelHintDemo:
            self.colorExampleDetails['name']=self.colorButtonDetails[6][0]
            self.colorExampleDetails['color']=self.colorButtonDetails[6][1]
        elif event.widget in self.lineDemos:
            tags = event.widget.itemcget('current','tags').split()
            #print tags
            if 'SHADOW' in tags:
                self.colorExampleDetails['name']=self.colorButtonDetails[9][0]
                self.colorExampleDetails['color']=self.colorButtonDetails[9][1]
            elif 'HIGHLIGHT' in tags:
                self.colorExampleDetails['name']=self.colorButtonDetails[8][0]
                self.colorExampleDetails['color']=self.colorButtonDetails[8][1]
            elif 'BODY' in tags:
                self.colorExampleDetails['name']=self.colorButtonDetails[7][0]
                self.colorExampleDetails['color']=self.colorButtonDetails[7][1]
            else: #background clicked
                self.colorExampleDetails['name']=self.colorButtonDetails[0][0]
                self.colorExampleDetails['color']=self.colorButtonDetails[0][1]

        self.SetColorExample()
    
    def SetColorExample(self):
        #print 'active menuitem is:',self.menuOptions.index('active') #debug
        if self.menuOptions.index('active') != None: #if this routine was called by self.menuOptions
            self.colorExampleDetails['name']=self.colorButtonDetails[self.menuOptions.index('active')][0]
            self.colorExampleDetails['color']=self.colorButtonDetails[self.menuOptions.index('active')][1]
        
        self.menubuttonOptions.configure(text=self.colorExampleDetails['name'],
                underline=self.colorExampleDetails['name'].find('e'))
        self.frameColorSelect.configure(bg=self.colorExampleDetails['color'])
        
    def GetColor(self):
        rgbTuplet, colorString = tkColorChooser.askcolor(parent=self,
                        title='Pick a new colour for: '+self.colorExampleDetails['name'],
                        initialcolor=self.colorExampleDetails['color'])#._root()
        if colorString: #user didn't cancel
            self.frameDemo.update() #redraw after dialog
            #print 'GetColor colorString =',colorString
            self.colorExampleDetails['color']=colorString
            self.frameColorSelect.configure(bg=colorString)
            self.UpdateColors()
            self.RepaintColors()
            #self.frameDemo.update() #redraw new colors
    
    def UpdateColors(self):
        if self.colorExampleDetails['name'] == self.colorButtonDetails[0][0]: 
            self.colors.bgReading = self.colorExampleDetails['color']
        elif self.colorExampleDetails['name'] == self.colorButtonDetails[1][0]: 
            self.colors.fgLabelHexTitles = self.colorExampleDetails['color']
        elif self.colorExampleDetails['name'] == self.colorButtonDetails[2][0]: 
            self.colors.fgMessageQuestion = self.colorExampleDetails['color']
        elif self.colorExampleDetails['name'] == self.colorButtonDetails[3][0]: 
            self.colors.fgLabelPlaces = self.colorExampleDetails['color']
        elif self.colorExampleDetails['name'] == self.colorButtonDetails[4][0]: 
            self.colors.fgLabelLines = self.colorExampleDetails['color']
        elif self.colorExampleDetails['name'] == self.colorButtonDetails[5][0]: 
            self.colors.bgLabelHint = self.colorExampleDetails['color']
        elif self.colorExampleDetails['name'] == self.colorButtonDetails[6][0]: 
            self.colors.fgLabelHint = self.colorExampleDetails['color']
        elif self.colorExampleDetails['name'] == self.colorButtonDetails[7][0]:
            self.colors.colorLineBody = self.colorExampleDetails['color']
        elif self.colorExampleDetails['name'] == self.colorButtonDetails[8][0]:
            self.colors.colorLineHighlight = self.colorExampleDetails['color']
        elif self.colorExampleDetails['name'] == self.colorButtonDetails[9][0]:
            self.colors.colorLineShadow = self.colorExampleDetails['color']
    
    def RepaintColors(self):
        #print 'ConfigureWidgetCustomColors frameDemo bg was =',self.frameDemo.cget('bg') 
        self.frameDemo.configure(bg=self.colors.bgReading)
        #print 'ConfigureWidgetCustomColors frameDemo bg is =',self.frameDemo.cget('bg') 
        self.labelTitleDemo.configure(fg=self.colors.fgLabelHexTitles,bg=self.colors.bgReading)
        self.labelQuestionDemo.configure(fg=self.colors.fgMessageQuestion,bg=self.colors.bgReading)
        self.labelPlaceDemo.configure(fg=self.colors.fgLabelPlaces,bg=self.colors.bgReading)
        self.labelBecomesDemo.configure(fg=self.colors.fgLabelLines,bg=self.colors.bgReading)
        self.labelNoMovingDemo.configure(fg=self.colors.fgLabelLines,bg=self.colors.bgReading)
        self.frameHintBgDemo.configure(bg=self.colors.bgLabelHint)
        self.labelHintDemo.configure(fg=self.colors.fgLabelHint,bg=self.colors.bgLabelHint)
        self.frameDemo.update()
        for item in self.lineDemos: 
            #item.configure(bg=self.colors.bgReading)
            item.colors = self.colors
            item.Draw(linetype=item.value)  

        self.SetColorButtonDetails()

    def SetDefaultColors(self):
        self.colors=WidgetColors()
        self.RepaintColors()
        self.colorExampleDetails['name']=self.colorButtonDetails[0][0]
        self.colorExampleDetails['color']=self.colorButtonDetails[0][1]
        self.SetColorExample()

    def Apply(self):
        self.result = self.colors

class DialogGetQuestion(smgDialog):
    """
    gets the question for a reading
    """
    def __init__(self, parent: Any) -> None:
        smgDialog.__init__(self, parent, title='Enter Question',
                    buttons=[{'name':'buttonOk','title':'Ok','binding':'Ok','underline':None,'hotKey':'<Return>'},
                                {'name':'buttonCancel','title':'Cancel','binding':'Cancel','underline':None,'hotKey':'<Escape>'}],
                    buttonsDef=-1, buttonsWidth=0, buttonsPad=5,
                    resizeable=0, transient=1, wait=1) # buttonsPos='bottom',

    def Body(self, master):
        labelPrompt = Label(master, text='Enter a question to ask the I Ching (maximum 70 characters):',
                        ).grid(column=0, row=0, sticky='w', padx=5, pady=5)
        self.questionText = StringVar()
        self.questionText.set('Tell me about my current circumstances.')
        self.entryQuestion = Entry(master, textvariable=self.questionText, width=70)
        self.entryQuestion.grid(column=0, row=1, sticky='w', padx=5)
        return self.entryQuestion
    
    def Apply(self):
        self.result = self.questionText.get()
         
    def Validate(self):
        if len(self.questionText.get()) > 70:#question too long
            tkMessageBox.showerror(title='Question Too Long',
                                                message='The question you have entered is longer than 70 characters.')
            return 0
        elif len(self.questionText.get().strip()) == 0:#null question
            tkMessageBox.showerror(title='No Question Entered',
                                                message='You have entered a blank question.')
            return 0
        else:
            return 1

class DialogManualInput(smgDialog):
    """
    Allows manual input of hexagram number and moving lines.
    """
    def __init__(self, parent: Any) -> None:
        smgDialog.__init__(self,parent,title='Manual Hexagram Input',
                    buttons=[{'name':'buttonOk','title':'Ok','binding':'Ok','underline':None,'hotKey':'<Return>'},
                                {'name':'buttonCancel','title':'Cancel','binding':'Cancel','underline':None,'hotKey':'<Escape>'}],
                    buttonsDef=-1,buttonsWidth=0,buttonsPad=5,
                    resizeable=0, transient=1, wait=1)

    def Body(self,master):
        # Hexagram number input
        Label(master,text='Enter hexagram number (1-64):').grid(column=0,row=0,sticky=W,padx=5,pady=5)
        self.hexNumberVar = StringVar()
        self.hexNumberVar.set('1')
        self.entryHexNumber = Entry(master,textvariable=self.hexNumberVar,width=10)
        self.entryHexNumber.grid(column=1,row=0,sticky=W,padx=5,pady=5)

        # Moving lines input
        Label(master,text='Enter moving lines (optional):').grid(column=0,row=1,sticky=W,padx=5,pady=5)
        Label(master,text='(comma-separated, e.g., 1,3,6)',
              font=('TkDefaultFont',9)).grid(column=0,row=2,columnspan=2,sticky=W,padx=5)
        self.movingLinesVar = StringVar()
        self.entryMovingLines = Entry(master,textvariable=self.movingLinesVar,width=30)
        self.entryMovingLines.grid(column=1,row=1,sticky=W,padx=5,pady=5)

        # Help text
        helpText = ("Enter the hexagram number from a physical I Ching reading\n"
                   "(coins, yarrow stalks, etc.) and optionally specify which\n"
                   "lines are moving (changing lines).\n\n"
                   "Line positions: 1=bottom, 2=second, 3=third,\n"
                   "                4=fourth, 5=fifth, 6=top")
        Label(master,text=helpText,justify=LEFT,
              font=('TkDefaultFont',9)).grid(column=0,row=3,columnspan=2,sticky=W,padx=5,pady=10)

        return self.entryHexNumber

    def Apply(self):
        hex_number = int(self.hexNumberVar.get())
        moving_lines_str = self.movingLinesVar.get().strip()

        if moving_lines_str:
            try:
                moving_lines = [int(x.strip()) for x in moving_lines_str.split(',')]
            except ValueError:
                moving_lines = []
        else:
            moving_lines = []

        self.result = (hex_number, moving_lines)

    def Validate(self):
        # Validate hexagram number
        try:
            hex_num = int(self.hexNumberVar.get())
            if hex_num < 1 or hex_num > 64:
                tkMessageBox.showerror(title='Invalid Hexagram Number',
                                      message='Hexagram number must be between 1 and 64.')
                return 0
        except ValueError:
            tkMessageBox.showerror(title='Invalid Input',
                                  message='Hexagram number must be a number.')
            return 0

        # Validate moving lines
        moving_lines_str = self.movingLinesVar.get().strip()
        if moving_lines_str:
            try:
                moving_lines = [int(x.strip()) for x in moving_lines_str.split(',')]
                for line in moving_lines:
                    if line < 1 or line > 6:
                        tkMessageBox.showerror(title='Invalid Line Number',
                                              message='Line numbers must be between 1 and 6.')
                        return 0
            except ValueError:
                tkMessageBox.showerror(title='Invalid Input',
                                      message='Moving lines must be comma-separated numbers (e.g., 1,3,6).')
                return 0

        return 1

class DialogCompareSources(Toplevel):
    """
    Simple dialog to compare hexagram interpretations from different sources.
    """
    def __init__(self, parent: Any, hex_number: str) -> None:
        Toplevel.__init__(self, parent)
        self.title(f'Source Comparison - Hexagram {hex_number}')
        self.transient(parent)

        # Get hexagram from different sources
        hex_num = int(hex_number)
        sources = ['canonical', 'wilhelm_baynes', 'legge_simplified']
        available_sources = []

        # Check which sources are available
        for source_id in sources:
            try:
                hex_data = Hexagram.from_number(hex_num, source=source_id)
                # Check if it's not just a placeholder
                if not hex_data.metadata.get('manual_extraction_required', False):
                    available_sources.append((source_id, hex_data))
            except:
                pass

        if not available_sources:
            Label(self, text='No alternative sources available yet.',
                  padx=20, pady=20).pack()
            Button(self, text='Close', command=self.destroy).pack(pady=10)
            return

        # Create scrollable frame
        canvas = Canvas(self)
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Display each source
        for source_id, hex_data in available_sources:
            frame = Frame(scrollable_frame, relief=RIDGE, borderwidth=2, padx=10, pady=10)
            frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

            # Source title
            source_name = hex_data.metadata.get('translator', source_id)
            year = hex_data.metadata.get('year', '')
            title = f"{source_id.upper()}\n{source_name} ({year})"
            Label(frame, text=title, font=('TkDefaultFont', 10, 'bold')).pack(anchor=W)

            # Hexagram name
            Label(frame, text=f"\nHexagram {hex_data.number}: {hex_data.english_name}",
                  font=('TkDefaultFont', 9, 'bold')).pack(anchor=W)

            # Judgment
            Label(frame, text="\nJUDGMENT:", font=('TkDefaultFont', 9, 'bold')).pack(anchor=W)
            judgment_text = Text(frame, height=5, width=80, wrap=WORD)
            judgment_text.insert('1.0', hex_data.judgment)
            judgment_text.config(state=DISABLED)
            judgment_text.pack(fill=BOTH, expand=True, pady=5)

            # Image
            Label(frame, text="IMAGE:", font=('TkDefaultFont', 9, 'bold')).pack(anchor=W)
            image_text = Text(frame, height=3, width=80, wrap=WORD)
            image_text.insert('1.0', hex_data.image)
            image_text.config(state=DISABLED)
            image_text.pack(fill=BOTH, expand=True, pady=5)

        canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        # Close button at bottom
        Button(self, text='Close', command=self.destroy, width=10).pack(pady=10)

        # Set window size
        self.geometry('900x600')

# Application details (replacing old pyching_engine.PychingAppDetails)
class AppDetails:
    """Simple application details class"""
    def __init__(self):
        self.title = 'pyChing'
        self.version = '2.0.0-devnew'
        self.execPath = Path(__file__).parent
        self.osType = os.name  # 'posix' or 'nt'

        # Config paths
        home = Path.home()
        if self.osType == 'nt':  # Windows
            self.configPath = home / 'AppData' / 'Local' / 'pyChing'
        else:  # Unix/Linux/Mac
            self.configPath = home / '.pyching'

        self.configFile = self.configPath / 'config.json'
        self.savePath = self.configPath / 'readings'

        # Create save path if it doesn't exist
        if not self.savePath.exists():
            self.savePath.mkdir(parents=True, exist_ok=True)

        # Contact info
        self.emailAddress = 'feargeas@gmail.com'
        self.webAddress = 'https://github.com/feargeas/pyChing'

        # Legacy attributes (may not be needed)
        self.saveFileExt = '.json'
        self.saveFileID = ('pyChing', '2.0')

# Create an instance of the app details for use throughout this module
pyching = AppDetails()

# Main execution
if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='pyChing - I Ching Oracle GUI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pyching_interface_tkinter.py          # Run normally (quiet)
  python pyching_interface_tkinter.py -v       # Run with verbose output
  python pyching_interface_tkinter.py -vv      # Run with very verbose/debug output
  python pyching_interface_tkinter.py --verbose # Run with verbose output
""")
    parser.add_argument('-v', '--verbose',
                       action='count',
                       default=0,
                       help='Increase verbosity (-v for verbose, -vv for debug)')

    args = parser.parse_args()

    # Set global verbose and debug flags based on count
    VERBOSE = args.verbose >= 1
    DEBUG = args.verbose >= 2

    if DEBUG:
        print("[pyChing DEBUG] Debug mode enabled (very verbose)")
        print("[pyChing DEBUG] Starting pyChing I Ching Oracle...")
    elif VERBOSE:
        print("[pyChing] Verbose mode enabled")
        print("[pyChing] Starting pyChing I Ching Oracle...")

    vprint(f"Application path: {pyching.execPath}")
    vprint(f"Config path: {pyching.configPath}")
    vprint(f"Config file: {pyching.configFile}")
    vprint(f"OS type: {pyching.osType}")

    windowRoot = Tk()
    vprint("Creating main window...")
    windowMain = WindowMain(windowRoot)
    vprint("Entering main event loop...")
    windowRoot.mainloop()
    vprint("Application exited")
