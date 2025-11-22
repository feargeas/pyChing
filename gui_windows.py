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

    def __init__(self, parent, title: str, file_path: Path, width: int = 600, height: int = 400):
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

        # Set window size
        self.geometry(f"{width}x{height}")

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

        # Button frame
        button_frame = Frame(main_frame)
        button_frame.pack(fill=X)

        # Save button
        Button(button_frame, text='Save', command=self._save_content,
               width=10).pack(side=LEFT, padx=(0, 5))

        # Close button
        Button(button_frame, text='Close', command=self.destroy,
               width=10).pack(side=LEFT)

        # Info label
        Label(button_frame, text="(Changes saved automatically when you click Save)",
              font=('TkDefaultFont', 9), fg='gray').pack(side=RIGHT)

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

    def _save_content(self):
        """Save text widget content to file."""
        try:
            # Ensure parent directory exists
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            # Get content and save
            content = self.text_widget.get('1.0', 'end-1c')
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            tkMessageBox.showinfo("Saved", f"File saved successfully:\n{self.file_path}")
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
                 width: int = 700, height: int = 600):
        """
        Initialize hexagram info window.

        Args:
            parent: Parent window
            hexagram: Hexagram dataclass instance
            changing_lines: List of changing line positions (1-6)
            width: Window width
            height: Window height
        """
        super().__init__(parent)
        self.hexagram = hexagram
        self.changing_lines = changing_lines or []

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
        header_frame = Frame(self, bg='white', height=100)
        header_frame.pack(fill=X, padx=10, pady=10)
        header_frame.pack_propagate(False)

        # Left: Chinese character
        chinese_char = self.metadata.get('chinese', '?')
        Label(header_frame, text=chinese_char,
              font=('Arial', 48), bg='white').pack(side=LEFT, padx=10)

        # Center: Number and bilingual name
        center_frame = Frame(header_frame, bg='white')
        center_frame.pack(side=LEFT, expand=True, fill=BOTH, padx=20)

        # Hexagram number
        Label(center_frame, text=f"{self.hexagram.number}.",
              font=('Arial', 24, 'bold'), bg='white').pack(anchor='w')

        # Wade-Giles romanization
        wade_giles = self.metadata.get('wade_giles', self.hexagram.name)
        Label(center_frame, text=wade_giles,
              font=('Arial', 18), bg='white', fg='#666').pack(anchor='w')

        # English name
        Label(center_frame, text=self.hexagram.english_name,
              font=('Arial', 16), bg='white').pack(anchor='w')

        # Right: SVG hexagram (if available)
        self._add_svg_diagram(header_frame)

    def _add_svg_diagram(self, parent_frame):
        """Add SVG hexagram diagram to header."""
        svg_path = Path(__file__).parent / 'data' / 'svg' / f"hexagram_{self.hexagram.number:02d}.svg"

        if not svg_path.exists():
            # Fallback: show unicode hexagram symbol
            unicode_char = self.metadata.get('unicode', '?')
            Label(parent_frame, text=unicode_char,
                  font=('Arial', 48), bg='white').pack(side=RIGHT, padx=10)
            return

        # Try to load and display SVG
        if HAS_SVG_SUPPORT:
            try:
                # Convert SVG to PNG in memory
                png_data = svg2png(url=str(svg_path), output_width=80, output_height=100)
                image = Image.open(io.BytesIO(png_data))
                photo = ImageTk.PhotoImage(image)

                label = Label(parent_frame, image=photo, bg='white')
                label.image = photo  # Keep reference
                label.pack(side=RIGHT, padx=10)
                return
            except Exception:
                pass

        # Fallback: show unicode symbol
        unicode_char = self.metadata.get('unicode', '?')
        Label(parent_frame, text=unicode_char,
              font=('Arial', 48), bg='white').pack(side=RIGHT, padx=10)

    def _create_content(self):
        """Create scrollable content area with judgment, image, and lines."""
        # Scrollable text area
        text_frame = Frame(self)
        text_frame.pack(fill=BOTH, expand=True, padx=10, pady=(0, 10))

        self.text_widget = ScrolledText(text_frame, wrap=WORD,
                                        font=('TkDefaultFont', 11),
                                        padx=15, pady=15)
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
        self.text_widget.insert(END,
                              f"The following lines are changing (moving): {', '.join(map(str, self.changing_lines))}\n\n",
                              'body')

        # Get line texts from hexagram data
        line_texts = self.hexagram.line_texts

        for line_pos in sorted(self.changing_lines):
            line_key = str(line_pos)
            if line_key in line_texts:
                line_data = line_texts[line_key]
                position_name = line_data.get('position', f'Line {line_pos}')
                line_type = line_data.get('type', '').capitalize()
                line_text = line_data.get('text', '[No text available]')

                # Heading
                heading = f"{position_name.capitalize()} ({line_type})\n"
                self.text_widget.insert(END, heading, 'changing_line')

                # Text
                self.text_widget.insert(END, f"{line_text}\n\n", 'body')
