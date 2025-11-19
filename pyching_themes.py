"""
pyChing Theme System

Provides theme presets (colors + line drawing styles) for the GUI.
Themes control both color palettes and visual aesthetics (beveled vs flat lines).

Author: pyChing modernization project
License: GPL v2+
"""

from typing import Dict, Type


class Theme:
    """
    Base theme class - defines all visual properties

    All themes inherit from this and override specific colors/styles.
    This base theme preserves the original pyChing aesthetic.
    """

    def __init__(self):
        # === BACKGROUND COLORS ===
        self.bgReading = "#323c4a"          # Main reading area background

        # === FOREGROUND COLORS ===
        self.fgLabelHexTitles = "#FFFFFF"   # Hexagram title text (white)
        self.fgLabelPlaces = "#FFA07A"      # Place names text (light salmon)
        self.fgLabelLines = "#FFFFFF"       # Line labels text (white)
        self.fgLabelHint = "#000000"        # Line hint text (black)
        self.fgMessageQuestion = "#FFFFFF"  # Question text (white)

        # === LINE HINT COLORS ===
        self.bgLabelHint = "#DAA520"        # Line hint background (goldenrod)

        # === HEXAGRAM LINE COLORS ===
        # These are used for drawing the actual hexagram lines
        self.colorLineBody = "#DAA520"      # Main line color (goldenrod)
        self.colorLineHighlight = "#EEE8AA"  # 3D highlight color (pale goldenrod)
        self.colorLineShadow = "#B8860B"    # 3D shadow color (dark goldenrod)

        # === LINE DRAWING STYLE ===
        self.line_style = 'beveled'         # Options: 'beveled', 'flat', 'unicode'
        self.line_width = 2                 # Line thickness for flat style
        self.line_rounded_corners = False   # Rounded corners for flat style

        # === THEME METADATA ===
        self.name = "Default (Classic)"
        self.description = "Original pyChing look with 3D beveled lines"
        self.author = "Stephen M. Gava (1999-2006)"


class SystemTheme(Theme):
    """
    System theme - follows OS default colors

    Uses system colors when possible, falls back to simple flat style.
    Good for users who want the app to match their OS theme.
    """

    def __init__(self):
        super().__init__()

        # Use neutral gray palette that matches most OS themes
        # (System color names like "SystemButtonText" aren't universally supported)
        self.bgReading = "#e0e0e0"          # Light gray background
        self.bgLabelHint = "#f5f5f5"        # Very light gray

        self.fgLabelHexTitles = "#202020"   # Very dark gray
        self.fgLabelPlaces = "#404040"      # Dark gray
        self.fgLabelLines = "#303030"       # Very dark gray
        self.fgLabelHint = "#000000"        # Black
        self.fgMessageQuestion = "#202020"  # Very dark gray

        self.colorLineBody = "#404040"      # Dark gray lines
        self.colorLineHighlight = "#606060" # Medium gray
        self.colorLineShadow = "#202020"    # Very dark gray

        # Use flat style for modern OS look
        self.line_style = 'flat'
        self.line_width = 2

        self.name = "System Default"
        self.description = "Matches your operating system theme"
        self.author = "pyChing team"


class SolarizedDarkTheme(Theme):
    """
    Solarized Dark - precision colors designed by Ethan Schoonover

    Scientifically designed color scheme with optimal contrast
    and reduced brightness for long viewing sessions.
    """

    def __init__(self):
        super().__init__()

        # Solarized Dark base colors
        base03 = "#002b36"  # darkest background
        base02 = "#073642"  # background highlights
        base01 = "#586e75"  # comments / secondary content
        base00 = "#657b83"  # body text / default code
        base0 = "#839496"   # primary content
        base1 = "#93a1a1"   # optional emphasized content

        # Solarized accent colors
        yellow = "#b58900"
        orange = "#cb4b16"
        red = "#dc322f"
        magenta = "#d33682"
        violet = "#6c71c4"
        blue = "#268bd2"
        cyan = "#2aa198"
        green = "#859900"

        # Apply Solarized palette
        self.bgReading = base03             # Dark background
        self.fgLabelHexTitles = blue        # Blue titles
        self.fgLabelPlaces = green          # Green place names
        self.fgLabelLines = yellow          # Yellow line labels
        self.fgLabelHint = base03           # Dark text on yellow bg
        self.fgMessageQuestion = cyan       # Cyan question text

        self.bgLabelHint = yellow           # Yellow hint background

        # Lines use orange/red/yellow palette
        self.colorLineBody = orange         # Orange lines
        self.colorLineHighlight = yellow    # Yellow highlights
        self.colorLineShadow = red          # Red shadows (for beveled)

        # Use flat style for clean Solarized look
        self.line_style = 'flat'
        self.line_width = 3
        self.line_rounded_corners = False

        self.name = "Solarized Dark"
        self.description = "Precision colors for reduced eyestrain"
        self.author = "Ethan Schoonover (adapted)"


class SolarizedLightTheme(Theme):
    """
    Solarized Light - bright variant of Solarized

    Same precision colors as Solarized Dark but with light background.
    Excellent for daytime use and bright environments.
    """

    def __init__(self):
        super().__init__()

        # Solarized Light base colors (inverted from dark)
        base3 = "#fdf6e3"   # lightest background
        base2 = "#eee8d5"   # background highlights
        base1 = "#93a1a1"   # comments / secondary content
        base0 = "#839496"   # body text
        base00 = "#657b83"  # primary content
        base01 = "#586e75"  # optional emphasized content

        # Solarized accent colors (same as dark)
        yellow = "#b58900"
        orange = "#cb4b16"
        red = "#dc322f"
        magenta = "#d33682"
        violet = "#6c71c4"
        blue = "#268bd2"
        cyan = "#2aa198"
        green = "#859900"

        # Apply light palette
        self.bgReading = base3              # Light background
        self.fgLabelHexTitles = blue        # Blue titles
        self.fgLabelPlaces = green          # Green place names
        self.fgLabelLines = orange          # Orange line labels
        self.fgLabelHint = base3            # Light text on dark bg
        self.fgMessageQuestion = violet     # Violet question text

        self.bgLabelHint = base01           # Dark hint background

        # Lines use similar palette but adjusted for light bg
        self.colorLineBody = orange         # Orange lines
        self.colorLineHighlight = red       # Red highlights
        self.colorLineShadow = base01       # Dark shadows

        self.line_style = 'flat'
        self.line_width = 3
        self.line_rounded_corners = False

        self.name = "Solarized Light"
        self.description = "Precision colors for bright environments"
        self.author = "Ethan Schoonover (adapted)"


class TokyoNightTheme(Theme):
    """
    Tokyo Night - modern dark theme with vibrant colors

    Inspired by Tokyo's night skyline. Clean, modern aesthetic
    with vibrant accent colors on a dark background.
    """

    def __init__(self):
        super().__init__()

        # Tokyo Night color palette
        bg = "#1a1b26"          # Deep blue-black background
        bg_dark = "#16161e"     # Darker variant
        bg_highlight = "#292e42"  # Highlight background

        fg = "#c0caf5"          # Foreground text
        fg_dark = "#a9b1d6"     # Darker foreground

        # Accent colors
        blue = "#7aa2f7"        # Bright blue
        cyan = "#7dcfff"        # Sky blue
        purple = "#bb9af7"      # Soft purple
        magenta = "#c678dd"     # Magenta
        red = "#f7768e"         # Soft red
        orange = "#ff9e64"      # Orange
        yellow = "#e0af68"      # Yellow
        green = "#9ece6a"       # Green
        teal = "#1abc9c"        # Teal

        # Apply Tokyo Night palette
        self.bgReading = bg                 # Dark background
        self.fgLabelHexTitles = blue        # Blue titles
        self.fgLabelPlaces = green          # Green place names
        self.fgLabelLines = purple          # Purple line labels
        self.fgLabelHint = bg               # Dark on light
        self.fgMessageQuestion = cyan       # Cyan question

        self.bgLabelHint = yellow           # Yellow hint bg

        # Vibrant line colors
        self.colorLineBody = red            # Red/pink lines
        self.colorLineHighlight = orange    # Orange highlights
        self.colorLineShadow = purple       # Purple shadows

        # Modern flat style with rounded corners
        self.line_style = 'flat'
        self.line_width = 3
        self.line_rounded_corners = True    # Rounded for modern look

        self.name = "Tokyo Night"
        self.description = "Modern dark theme with vibrant colors"
        self.author = "Folke Lemaitre (adapted)"


class TokyoNightStormTheme(Theme):
    """
    Tokyo Night Storm - softer variant of Tokyo Night

    Less intense than standard Tokyo Night, with a slightly lighter
    background for reduced contrast. Easier on the eyes for long sessions.
    """

    def __init__(self):
        super().__init__()

        # Tokyo Night Storm palette (lighter bg)
        bg = "#24283b"          # Lighter blue-black
        bg_dark = "#1f2335"     # Darker variant

        fg = "#c0caf5"          # Foreground text

        # Same accent colors as Tokyo Night
        blue = "#7aa2f7"
        cyan = "#7dcfff"
        purple = "#bb9af7"
        red = "#f7768e"
        orange = "#ff9e64"
        yellow = "#e0af68"
        green = "#9ece6a"

        # Apply Storm palette
        self.bgReading = bg
        self.fgLabelHexTitles = blue
        self.fgLabelPlaces = green
        self.fgLabelLines = cyan
        self.fgLabelHint = bg
        self.fgMessageQuestion = purple

        self.bgLabelHint = yellow

        self.colorLineBody = green          # Green lines (softer)
        self.colorLineHighlight = cyan      # Cyan highlights
        self.colorLineShadow = blue         # Blue shadows

        self.line_style = 'flat'
        self.line_width = 3
        self.line_rounded_corners = True

        self.name = "Tokyo Night Storm"
        self.description = "Softer Tokyo Night with reduced contrast"
        self.author = "Folke Lemaitre (adapted)"


class NordTheme(Theme):
    """
    Nord - arctic, north-bluish color palette

    Inspired by the arctic ice and snow. Cool, clean aesthetic
    with blues and cool grays.
    """

    def __init__(self):
        super().__init__()

        # Nord Polar Night (dark backgrounds)
        nord0 = "#2e3440"   # Darkest
        nord1 = "#3b4252"   # Dark
        nord2 = "#434c5e"   # Medium dark
        nord3 = "#4c566a"   # Lightest dark

        # Nord Snow Storm (light foregrounds)
        nord4 = "#d8dee9"   # Medium light
        nord5 = "#e5e9f0"   # Light
        nord6 = "#eceff4"   # Lightest

        # Nord Frost (blues)
        nord7 = "#8fbcbb"   # Teal
        nord8 = "#88c0d0"   # Cyan
        nord9 = "#81a1c1"   # Blue
        nord10 = "#5e81ac"  # Dark blue

        # Nord Aurora (accent colors)
        nord11 = "#bf616a"  # Red
        nord12 = "#d08770"  # Orange
        nord13 = "#ebcb8b"  # Yellow
        nord14 = "#a3be8c"  # Green
        nord15 = "#b48ead"  # Purple

        # Apply Nord palette
        self.bgReading = nord0              # Dark background
        self.fgLabelHexTitles = nord8       # Cyan titles
        self.fgLabelPlaces = nord14         # Green place names
        self.fgLabelLines = nord13          # Yellow line labels
        self.fgLabelHint = nord0            # Dark on light
        self.fgMessageQuestion = nord9      # Blue question

        self.bgLabelHint = nord13           # Yellow hint

        # Arctic line colors
        self.colorLineBody = nord8          # Cyan lines
        self.colorLineHighlight = nord7     # Teal highlights
        self.colorLineShadow = nord10       # Dark blue shadows

        self.line_style = 'flat'
        self.line_width = 2
        self.line_rounded_corners = False

        self.name = "Nord"
        self.description = "Arctic-inspired cool color palette"
        self.author = "Arctic Ice Studio (adapted)"


class DraculaTheme(Theme):
    """
    Dracula - dark theme with pastel colors

    Popular dark theme with carefully chosen pastel accent colors.
    Comfortable for long coding sessions.
    """

    def __init__(self):
        super().__init__()

        # Dracula color palette
        bg = "#282a36"          # Background
        fg = "#f8f8f2"          # Foreground
        selection = "#44475a"   # Selection
        comment = "#6272a4"     # Comments

        # Dracula accent colors
        cyan = "#8be9fd"        # Bright cyan
        green = "#50fa7b"       # Bright green
        orange = "#ffb86c"      # Orange
        pink = "#ff79c6"        # Pink
        purple = "#bd93f9"      # Purple
        red = "#ff5555"         # Red
        yellow = "#f1fa8c"      # Yellow

        # Apply Dracula palette
        self.bgReading = bg
        self.fgLabelHexTitles = purple      # Purple titles
        self.fgLabelPlaces = green          # Green place names
        self.fgLabelLines = orange          # Orange labels
        self.fgLabelHint = bg               # Dark on light
        self.fgMessageQuestion = cyan       # Cyan question

        self.bgLabelHint = yellow           # Yellow hint

        self.colorLineBody = pink           # Pink lines
        self.colorLineHighlight = purple    # Purple highlights
        self.colorLineShadow = red          # Red shadows

        self.line_style = 'flat'
        self.line_width = 3
        self.line_rounded_corners = True

        self.name = "Dracula"
        self.description = "Dark theme with pastel accent colors"
        self.author = "Zeno Rocha (adapted)"


class GruvboxDarkTheme(Theme):
    """
    Gruvbox Dark - retro groove colors

    Designed with warm colors and good contrast. Retro aesthetic
    without being garish. Excellent for readability.
    """

    def __init__(self):
        super().__init__()

        # Gruvbox Dark backgrounds
        bg0_h = "#1d2021"   # Hard background
        bg0 = "#282828"     # Default background
        bg1 = "#3c3836"     # Lighter background
        bg2 = "#504945"     # Selection

        # Gruvbox Dark foregrounds
        fg0 = "#fbf1c7"     # Lightest
        fg1 = "#ebdbb2"     # Default
        fg2 = "#d5c4a1"     # Darker

        # Gruvbox accent colors
        red = "#fb4934"     # Bright red
        green = "#b8bb26"   # Bright green
        yellow = "#fabd2f"  # Bright yellow
        blue = "#83a598"    # Bright blue
        purple = "#d3869b"  # Bright purple
        aqua = "#8ec07c"    # Bright aqua
        orange = "#fe8019"  # Bright orange

        # Apply Gruvbox palette
        self.bgReading = bg0                # Dark background
        self.fgLabelHexTitles = blue        # Blue titles
        self.fgLabelPlaces = green          # Green place names
        self.fgLabelLines = yellow          # Yellow labels
        self.fgLabelHint = bg0              # Dark on light
        self.fgMessageQuestion = aqua       # Aqua question

        self.bgLabelHint = yellow           # Yellow hint

        self.colorLineBody = orange         # Orange lines
        self.colorLineHighlight = yellow    # Yellow highlights
        self.colorLineShadow = red          # Red shadows

        self.line_style = 'flat'
        self.line_width = 3
        self.line_rounded_corners = False

        self.name = "Gruvbox Dark"
        self.description = "Retro warm colors with excellent contrast"
        self.author = "Pavel Pertsev (adapted)"


# === THEME REGISTRY ===

THEMES: Dict[str, Type[Theme]] = {
    'default': Theme,
    'system': SystemTheme,
    'solarized-dark': SolarizedDarkTheme,
    'solarized-light': SolarizedLightTheme,
    'tokyo-night': TokyoNightTheme,
    'tokyo-night-storm': TokyoNightStormTheme,
    'nord': NordTheme,
    'dracula': DraculaTheme,
    'gruvbox-dark': GruvboxDarkTheme,
}


def get_theme(theme_name: str) -> Theme:
    """
    Get a theme instance by name

    Args:
        theme_name: Theme identifier (e.g., 'tokyo-night', 'solarized-dark')

    Returns:
        Theme instance

    If theme_name is not found, returns the default theme.
    """
    theme_class = THEMES.get(theme_name, Theme)
    return theme_class()


def list_themes() -> list:
    """
    Get list of all available themes

    Returns:
        List of (theme_id, theme_name, theme_description) tuples
    """
    themes_list = []
    for theme_id, theme_class in THEMES.items():
        theme = theme_class()
        themes_list.append((theme_id, theme.name, theme.description))
    return themes_list


if __name__ == '__main__':
    # Test theme creation
    print("=== pyChing Theme System Test ===\n")

    for theme_id, theme_name, description in list_themes():
        theme = get_theme(theme_id)
        print(f"{theme_name}")
        print(f"  ID: {theme_id}")
        print(f"  Description: {description}")
        print(f"  Line Style: {theme.line_style}")
        print(f"  Main BG: {theme.bgReading}")
        print(f"  Line Color: {theme.colorLineBody}")
        print()
