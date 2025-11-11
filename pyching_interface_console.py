#!/usr/bin/env python3
##---------------------------------------------------------------------------##
##
## pyChing -- a Python program to cast and interpret I Ching hexagrams
##
## Copyright (C) 1999-2006 Stephen M. Gava
## Copyright (C) 2025 - Console interface implementation
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
##---------------------------------------------------------------------------##
"""
Console/terminal interface for pyChing
Provides a text-based I Ching oracle experience
"""

import sys
import os
import re
from html.parser import HTMLParser

# Import the pyChing oracle engine
import pyching_engine

# Import hexagram data modules
import pyching_int_data


class HTMLToText(HTMLParser):
    """Simple HTML to plain text converter for displaying hexagram interpretations"""
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        if tag == 'p':
            self.text_parts.append('\n')
        elif tag == 'br':
            self.text_parts.append('\n')
        elif tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.text_parts.append('\n')

    def handle_endtag(self, tag):
        if tag in ('p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.text_parts.append('\n')
        self.current_tag = None

    def handle_data(self, data):
        # Clean up whitespace but preserve intentional line breaks
        text = data.strip()
        if text:
            self.text_parts.append(text)
            self.text_parts.append(' ')

    def get_text(self):
        """Return the extracted plain text"""
        text = ''.join(self.text_parts)
        # Clean up multiple spaces and newlines
        text = re.sub(r' +', ' ', text)
        text = re.sub(r'\n\n+', '\n\n', text)
        return text.strip()


def html_to_text(html_string):
    """Convert HTML string to plain text"""
    parser = HTMLToText()
    parser.feed(html_string)
    return parser.get_text()


def print_banner():
    """Display the pyChing console banner"""
    pyching = pyching_engine.PychingAppDetails(createConfigDir=0)
    print("\n" + "="*70)
    print(f"  {pyching.title} - I Ching Oracle - Console Version")
    print(f"  Version {pyching.version}")
    print("="*70)
    print("\nWelcome to the I Ching oracle.")
    print("This ancient Chinese divination system uses the three-coin method")
    print("to generate hexagrams that provide wisdom and guidance.\n")


def get_question():
    """Prompt user for their question"""
    print("What question do you wish to ask the oracle?")
    print("(Maximum 70 characters, or press Ctrl+C to cancel)")
    print()
    while True:
        try:
            question = input("Question: ").strip()
            if len(question) == 0:
                print("Please enter a question.")
                continue
            if len(question) > 70:
                print(f"Question too long ({len(question)} characters). Please limit to 70.")
                continue
            return question
        except (EOFError, KeyboardInterrupt):
            print("\n\nReading cancelled.")
            return None


def cast_reading(hexes):
    """Cast all six lines of the reading"""
    print("\n" + "-"*70)
    print("Casting hexagram lines...")
    print("Press ENTER to cast each line (three coins will be tossed)")
    print("(Press Ctrl+C to cancel)")
    print("-"*70 + "\n")

    coin_faces = {2: 'Tails', 3: 'Heads'}
    line_names = {
        6: 'Old Yin (changing)',
        7: 'Yang',
        8: 'Yin',
        9: 'Old Yang (changing)'
    }

    try:
        for line_num in range(1, 7):
            input(f"Press ENTER to cast line {line_num} of 6...")

            # Cast the line using the oracle engine
            hexes.NewLine()

            # Get the coin values and line value
            coins = hexes.currentOracleValues
            line_value = hexes.hex1.lineValues[line_num - 1]

            # Display the coin toss results
            print(f"  Coins: {coin_faces[coins[0]]}, {coin_faces[coins[1]]}, {coin_faces[coins[2]]}")
            print(f"  Sum: {sum(coins)} = {line_names[line_value]}")
            print()
        return True
    except (EOFError, KeyboardInterrupt):
        print("\n\nReading cancelled.")
        return False


def display_reading(hexes):
    """Display the complete reading in ASCII art"""
    print("\n" + "="*70)
    print("YOUR READING")
    print("="*70)

    # Use the engine's built-in ASCII art formatter
    reading_text = hexes.ReadingAsText()
    print(reading_text)
    print("="*70 + "\n")


def display_interpretation(hexes):
    """Display the hexagram interpretation(s)"""
    print("\n" + "="*70)
    print("INTERPRETATION")
    print("="*70 + "\n")

    # Display Hexagram 1 interpretation
    print(f"\nHEXAGRAM {hexes.hex1.number}: {hexes.hex1.name}")
    print("-" * 70)

    try:
        # Get the HTML data for hexagram 1
        hex1_func = getattr(pyching_int_data, f'in{hexes.hex1.number}data')
        hex1_html = hex1_func()
        hex1_text = html_to_text(hex1_html)

        # Wrap text to 70 columns
        print(wrap_text(hex1_text, 70))
    except Exception as e:
        print(f"Unable to load interpretation for hexagram {hexes.hex1.number}")
        print(f"Error: {e}")

    # Display Hexagram 2 interpretation if there are moving lines
    if hexes.hex2.number:
        print(f"\n\nTRANSFORMATION TO HEXAGRAM {hexes.hex2.number}: {hexes.hex2.name}")
        print("-" * 70)

        try:
            hex2_func = getattr(pyching_int_data, f'in{hexes.hex2.number}data')
            hex2_html = hex2_func()
            hex2_text = html_to_text(hex2_html)

            print(wrap_text(hex2_text, 70))
        except Exception as e:
            print(f"Unable to load interpretation for hexagram {hexes.hex2.number}")
            print(f"Error: {e}")

    print("\n" + "="*70 + "\n")


def wrap_text(text, width):
    """Simple text wrapper for console display"""
    words = text.split()
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        word_length = len(word)
        if current_length + word_length + len(current_line) <= width:
            current_line.append(word)
            current_length += word_length
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_length = word_length

    if current_line:
        lines.append(' '.join(current_line))

    return '\n'.join(lines)


def save_reading(hexes):
    """Offer to save the reading to a file"""
    print("\nWould you like to save this reading?")

    while True:
        try:
            response = input("Save? (y/n): ").strip().lower()
            if response in ('y', 'yes', 'n', 'no', ''):
                break
            print("Please enter 'y' for yes or 'n' for no.")
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled.")
            return

    if response in ('y', 'yes'):
        pyching = pyching_engine.PychingAppDetails()
        default_name = "reading"

        print(f"\nReadings are saved to: {pyching.savePath}")

        try:
            filename = input(f"Filename (default: {default_name}): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled.")
            return

        if not filename:
            filename = default_name

        if not filename.endswith(pyching.saveFileExt):
            filename += pyching.saveFileExt

        filepath = os.path.join(pyching.savePath, filename)

        try:
            hexes.Save(filepath)
            print(f"\nReading saved to: {filepath}")
        except Exception as e:
            print(f"\nError saving reading: {e}")


def main_menu():
    """Display main menu and handle user choices"""
    while True:
        try:
            print("\n" + "="*70)
            print("MAIN MENU")
            print("="*70)
            print("\n1. New Reading")
            print("2. Load Saved Reading")
            print("3. Quit")
            print()

            choice = input("Choose an option (1-3): ").strip()

            if choice == '1':
                new_reading()
            elif choice == '2':
                load_reading()
            elif choice in ('3', 'q', 'quit', 'exit'):
                print("\nMay the wisdom of the I Ching guide your path.")
                print("Farewell.\n")
                sys.exit(0)
            elif choice == '':
                continue
            else:
                print("\nInvalid choice. Please enter 1, 2, or 3.")
        except (EOFError, KeyboardInterrupt):
            print("\n\nMay the wisdom of the I Ching guide your path.")
            print("Farewell.\n")
            sys.exit(0)


def new_reading():
    """Perform a new oracle reading"""
    # Get the question
    question = get_question()
    if question is None:
        return  # User cancelled

    # Create new hexagrams object with coin oracle
    hexes = pyching_engine.Hexagrams('coin')
    hexes.question = question

    # Cast all six lines
    if not cast_reading(hexes):
        return  # User cancelled

    # Display the reading
    display_reading(hexes)

    # Display the interpretation
    display_interpretation(hexes)

    # Offer to save
    save_reading(hexes)


def load_reading():
    """Load and display a saved reading"""
    pyching = pyching_engine.PychingAppDetails()

    print(f"\nReadings are stored in: {pyching.savePath}")

    # List available save files
    try:
        files = [f for f in os.listdir(pyching.savePath)
                if f.endswith(pyching.saveFileExt)]

        if not files:
            print("No saved readings found.")
            return

        print("\nAvailable readings:")
        for i, filename in enumerate(files, 1):
            print(f"  {i}. {filename}")

        print()
        try:
            choice = input("Enter number to load (or press ENTER to cancel): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled.")
            return

        if not choice:
            return

        try:
            file_index = int(choice) - 1
            if 0 <= file_index < len(files):
                filepath = os.path.join(pyching.savePath, files[file_index])

                # Load the reading
                hexes = pyching_engine.Hexagrams()
                hexes.Load(filepath)

                # Display it
                display_reading(hexes)
                display_interpretation(hexes)
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    except FileNotFoundError:
        print(f"Directory not found: {pyching.savePath}")
    except Exception as e:
        print(f"Error loading readings: {e}")


def main():
    """Main entry point for console interface"""
    print_banner()
    main_menu()


# Only run when executed directly or when explicitly called
if __name__ == '__main__':
    main()

# When imported by pyching.py, it will call main() explicitly
# So we don't auto-run it here
