"""
Enhanced GUI windows for pyChing

Provides sophisticated windows for:
- Hexagram information display (with Chinese characters, SVG, changing lines)
- Text file editing (for earth.txt and notes)
"""

import io
import json
from pathlib import Path
from tkinter import *
from tkinter import font as tkFont
from tkinter import messagebox as tkMessageBox
from tkinter.scrolledtext import ScrolledText
from typing import Optional, List
try:
    from cairosvg import svg2png
    from PIL import Image, ImageTk
    HAS_SVG_SUPPORT = True
except ImportError:
    HAS_SVG_SUPPORT = False


def load_hexagram_metadata(hexagram_number: int) -> dict:
    """Load hexagram metadata including Chinese characters."""
    data_path = Path(__file__).parent / 'data' / 'hexagrams.json'
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for hex_data in data['hexagrams']:
        if hex_data['number'] == hexagram_number:
            return hex_data

    return {}


class TextEditorWindow(Toplevel):
    """
    Window for editing text files (e.g., earth.txt).

    Features:
    - Load and save text files
    - Scrollable text area
    - Save button
    """

    def __init__(self, parent, title: str, file_path: Path, width: int = 700, height: int = 500):
        """
        Initialize text editor window.

        Args:
            parent: Parent window
            title: Window title
            file_path: Path to file to edit
            width: Window width in pixels
            height: Window height in pixels
        """
        super().__init__(parent)
        self.title(title)
        self.file_path = file_path
        self.is_modified = False  # Track if text has been modified

        # Set window size and make it prominent
        self.geometry(f"{width}x{height}")
        self.minsize(500, 400)  # Ensure buttons are always visible

        # Create main frame
        main_frame = Frame(self)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Label at top
        Label(main_frame, text=f"Editing: {file_path.name}",
              font=('TkDefaultFont', 10, 'bold')).pack(anchor='w', pady=(0, 5))

        # Scrolled text widget
        self.text_widget = ScrolledText(main_frame, wrap=WORD,
                                        font=('TkFixedFont', 10))
        self.text_widget.pack(fill=BOTH, expand=True, pady=(0, 10))

        # Load existing content
        self._load_content()

        # Bind text modification event
        self.text_widget.bind('<<Modified>>', self._on_text_modified)

        # Button frame
        button_frame = Frame(main_frame, bg='lightgray', relief=RAISED, borderwidth=2)
        button_frame.pack(fill=X, pady=(10, 0))

        # Inner frame for buttons
        inner_frame = Frame(button_frame, bg='lightgray')
        inner_frame.pack(fill=X, padx=5, pady=5)

        # Save button (starts unhighlighted)
        self.save_button = Button(inner_frame, text='Save', command=self._save_content,
                                  width=12, relief=RAISED)
        self.save_button.pack(side=LEFT, padx=(0, 5))

        # Store original button colors for restoration after save
        self.original_bg = self.save_button.cget('bg')
        self.original_fg = self.save_button.cget('fg')

        # Close button
        Button(inner_frame, text='Close', command=self.destroy,
               width=12, relief=RAISED).pack(side=LEFT)

        # Info label (changes based on modification state)
        self.info_label = Label(inner_frame, text="",
                               font=('TkDefaultFont', 10), bg='lightgray')
        self.info_label.pack(side=RIGHT, padx=10)

    def _load_content(self):
        """Load file content into text widget."""
        if self.file_path.exists():
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_widget.insert('1.0', content)
            except Exception as e:
                tkMessageBox.showerror("Load Error",
                                      f"Could not load file:\n\n{str(e)}")
        else:
            # File doesn't exist, show help text
            help_text = "# Earth Method Seed\n\n"
            help_text += "This text serves as the 'soil' into which your question (the seed) is planted.\n"
            help_text += "It determines the deterministic randomness for Earth method castings.\n\n"
            help_text += "You can write anything here - a date, a phrase, or leave it as is.\n"
            help_text += "The same seed + question will always produce the same hexagram.\n"
            self.text_widget.insert('1.0', help_text)

        # Reset modified flag after loading
        self.text_widget.edit_modified(False)
        self.is_modified = False

    def _on_text_modified(self, event=None):
        """Called when text is modified."""
        if self.text_widget.edit_modified():
            if not self.is_modified:
                self.is_modified = True
                self._highlight_save_button()
            # Reset the modified flag (required for Tkinter)
            self.text_widget.edit_modified(False)

    def _highlight_save_button(self):
        """Make save button prominent when text is modified."""
        self.save_button.config(bg='#4CAF50', fg='white',
                               font=('TkDefaultFont', 10, 'bold'),
                               borderwidth=2)
        self.info_label.config(text="Remember to click Save!",
                              font=('TkDefaultFont', 10, 'bold'),
                              fg='#D32F2F')

    def _unhighlight_save_button(self):
        """Return save button to normal state after saving."""
        self.save_button.config(bg=self.original_bg, fg=self.original_fg,
                               font=('TkDefaultFont', 10),
                               borderwidth=1)
        self.info_label.config(text="Saved", fg='#4CAF50',
                              font=('TkDefaultFont', 10))

    def _save_content(self):
        """Save text widget content to file."""
        try:
            # Ensure parent directory exists
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            # Get content and save
            content = self.text_widget.get('1.0', 'end-1c')
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # Reset modified state and unhighlight button
            self.is_modified = False
            self._unhighlight_save_button()

        except Exception as e:
            tkMessageBox.showerror("Save Error",
                                  f"Could not save file:\n\n{str(e)}")


class HexagramInfoWindow(Toplevel):
    """
    Sophisticated window for displaying hexagram information.

    Features:
    - Chinese character (top left)
    - SVG hexagram diagram (top right)
    - Number and bilingual name (center top)
    - Judgment and Image texts
    - Changing line interpretations
    """

    def __init__(self, parent, hexagram, changing_lines: Optional[List[int]] = None,
                 width: int = 700, height: int = 600, colors: Any = None):
        """
        Initialize hexagram info window.

        Args:
            parent: Parent window
            hexagram: Hexagram dataclass instance
            changing_lines: List of changing line positions (1-6)
            width: Window width
            height: Window height
            colors: Theme colors object
        """
        super().__init__(parent)
        self.hexagram = hexagram
        self.changing_lines = changing_lines or []
        self.colors = colors

        # Apply theme colors to window
        if colors:
            self.configure(bg=colors.bgControls)

        # Load metadata for Chinese characters
        self.metadata = load_hexagram_metadata(hexagram.number)

        # Set window title
        self.title(f"Hexagram {hexagram.number}: {hexagram.english_name}")
        self.geometry(f"{width}x{height}")

        # Create UI
        self._create_header()
        self._create_content()

    def _create_header(self):
        """Create header with Chinese char, name, and SVG."""
        bg_color = self.colors.bgControls if self.colors else 'white'
        fg_color = self.colors.fgControls if self.colors else 'black'

        header_frame = Frame(self, bg=bg_color, height=100)
        header_frame.pack(fill=X, padx=10, pady=10)
        header_frame.pack_propagate(False)

        # Left: Chinese character
        chinese_char = self.metadata.get('chinese', '?')
        Label(header_frame, text=chinese_char,
              font=('Arial', 48), bg=bg_color, fg=fg_color).pack(side=LEFT, padx=10)

        # Center: Number and bilingual name
        center_frame = Frame(header_frame, bg=bg_color)
        center_frame.pack(side=LEFT, expand=True, fill=BOTH, padx=20)

        # Line 1: Hexagram number and Wade-Giles romanization on same line
        line1_frame = Frame(center_frame, bg=bg_color)
        line1_frame.pack(anchor='w')

        Label(line1_frame, text=f"{self.hexagram.number}.",
              font=('Arial', 24, 'bold'), bg=bg_color, fg=fg_color).pack(side=LEFT)

        wade_giles = self.metadata.get('wade_giles', self.hexagram.name)
        Label(line1_frame, text=f"  {wade_giles}",
              font=('Arial', 20), bg=bg_color, fg=fg_color).pack(side=LEFT)

        # Line 2: English name below
        Label(center_frame, text=self.hexagram.english_name,
              font=('Arial', 16), bg=bg_color, fg=fg_color).pack(anchor='w', pady=(5, 0))

        # Right: SVG hexagram (if available)
        self._add_svg_diagram(header_frame)

    def _add_svg_diagram(self, parent_frame):
        """Add SVG hexagram diagram to header."""
        bg_color = self.colors.bgControls if self.colors else 'white'
        fg_color = self.colors.fgControls if self.colors else 'black'
        svg_path = Path(__file__).parent / 'data' / 'svg' / f"hexagram_{self.hexagram.number:02d}.svg"

        if not svg_path.exists():
            # Fallback: show unicode hexagram symbol
            unicode_char = self.metadata.get('unicode', '?')
            Label(parent_frame, text=unicode_char,
                  font=('Arial', 48), bg=bg_color, fg=fg_color).pack(side=RIGHT, padx=10)
            return

        # Try to load and display SVG
        if HAS_SVG_SUPPORT:
            try:
                # Convert SVG to PNG in memory
                png_data = svg2png(url=str(svg_path), output_width=80, output_height=100)
                image = Image.open(io.BytesIO(png_data))
                photo = ImageTk.PhotoImage(image)

                label = Label(parent_frame, image=photo, bg=bg_color)
                label.image = photo  # Keep reference
                label.pack(side=RIGHT, padx=10)
                return
            except Exception:
                pass

        # Fallback: show unicode symbol
        unicode_char = self.metadata.get('unicode', '?')
        Label(parent_frame, text=unicode_char,
              font=('Arial', 48), bg=bg_color, fg=fg_color).pack(side=RIGHT, padx=10)

    def _create_content(self):
        """Create scrollable content area with judgment, image, and lines."""
        bg_color = self.colors.bgReading if self.colors else 'white'
        fg_color = self.colors.fgControls if self.colors else 'black'

        # Scrollable text area
        text_frame = Frame(self, bg=bg_color)
        text_frame.pack(fill=BOTH, expand=True, padx=10, pady=(0, 10))

        self.text_widget = ScrolledText(text_frame, wrap=WORD,
                                        font=('TkDefaultFont', 11),
                                        padx=15, pady=15,
                                        bg=bg_color, fg=fg_color)
        self.text_widget.pack(fill=BOTH, expand=True)

        # Configure tags for formatting
        self.text_widget.tag_config('heading', font=('Arial', 12, 'bold'),
                                    foreground='#333', spacing1=10, spacing3=5)
        self.text_widget.tag_config('body', font=('TkDefaultFont', 11),
                                   spacing1=5)
        self.text_widget.tag_config('line_heading', font=('Arial', 11, 'bold'),
                                   foreground='#006600', spacing1=8, spacing3=3)
        self.text_widget.tag_config('changing_line', font=('Arial', 11, 'bold'),
                                   foreground='#CC0000', spacing1=8, spacing3=3)

        # Add content
        self._add_judgment()
        self._add_image()
        self._add_changing_lines()

        # Make read-only
        self.text_widget.config(state=DISABLED)

        # Close button
        Button(self, text='Close', command=self.destroy,
               width=10).pack(pady=(0, 10))

    def _add_judgment(self):
        """Add judgment text."""
        self.text_widget.insert(END, "The Judgment\n", 'heading')
        self.text_widget.insert(END, f"{self.hexagram.judgment}\n\n", 'body')

    def _add_image(self):
        """Add image text."""
        self.text_widget.insert(END, "The Image\n", 'heading')
        self.text_widget.insert(END, f"{self.hexagram.image}\n\n", 'body')

    def _add_changing_lines(self):
        """Add changing line interpretations."""
        if not self.changing_lines:
            return

        self.text_widget.insert(END, "Changing Lines\n", 'heading')

        # Get line texts from hexagram data
        line_texts = self.hexagram.line_texts

        # Position name mapping
        position_map = {
            'bottom': 'bottom',
            'second': 'second',
            'third': 'third',
            'fourth': 'fourth',
            'fifth': 'fifth',
            'topmost': 'topmost'
        }

        # Type name mapping (nine/six)
        type_map = {
            'nine': 'nine',
            'six': 'six'
        }

        for line_pos in sorted(self.changing_lines):
            line_key = str(line_pos)
            if line_key in line_texts:
                line_data = line_texts[line_key]
                position_name = line_data.get('position', f'line {line_pos}')
                line_type = line_data.get('type', 'nine').lower()
                line_text = line_data.get('text', '[No text available]')

                # Format: "the bottom line, as nine" instead of "Bottom (Nine)"
                position_lower = position_map.get(position_name.lower(), position_name.lower())
                type_lower = type_map.get(line_type, line_type)
                heading = f"The {position_lower} line, as {type_lower}\n"

                self.text_widget.insert(END, heading, 'changing_line')

                # Text
                self.text_widget.insert(END, f"{line_text}\n\n", 'body')
